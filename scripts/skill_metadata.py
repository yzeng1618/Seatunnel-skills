#!/usr/bin/env python
#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
MAX_SKILL_BODY_LINES = 500

REQUIRED_FRONTMATTER_FIELDS = (
    "name",
    "description",
    "when_to_use",
    "inputs_required",
    "templates",
    "references",
    "agents",
)
OPTIONAL_FRONTMATTER_FIELDS = ("version",)
ARRAY_FIELDS = ("inputs_required", "templates", "references", "agents")
STRING_FIELDS = ("name", "description", "when_to_use", "version")


class FrontmatterError(ValueError):
    """Raised when SKILL.md front-matter cannot be parsed."""


def iter_skill_dirs(skills_root: Path):
    if not skills_root.exists():
        return
    for child in sorted(skills_root.iterdir(), key=lambda p: p.name):
        if child.is_dir() and (child / "SKILL.md").exists():
            yield child


def normalize_newlines(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def parse_frontmatter(content: str) -> Tuple[Optional[Dict[str, object]], Optional[int]]:
    lines = normalize_newlines(content).split("\n")
    if not lines or lines[0].strip() != "---":
        return None, None

    end_index = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_index = idx
            break

    if end_index is None:
        raise FrontmatterError("Front-matter end marker '---' not found.")

    frontmatter = _parse_frontmatter_lines(lines[1:end_index])
    return frontmatter, end_index


def validate_frontmatter(frontmatter: Dict[str, object], skill_dir_name: str) -> List[str]:
    errors: List[str] = []

    missing = [field for field in REQUIRED_FRONTMATTER_FIELDS if field not in frontmatter]
    if missing:
        errors.append(
            "Missing required front-matter field(s): %s." % ", ".join(missing)
        )

    name = frontmatter.get("name")
    if isinstance(name, str):
        errors.extend(_validate_name(name, skill_dir_name))
    else:
        errors.append("Field 'name' must be a string.")

    description = frontmatter.get("description")
    if isinstance(description, str):
        errors.extend(_validate_description(description))
    else:
        errors.append("Field 'description' must be a string.")

    when_to_use = frontmatter.get("when_to_use")
    if isinstance(when_to_use, str):
        if not when_to_use.strip():
            errors.append("Field 'when_to_use' cannot be empty.")
    else:
        errors.append("Field 'when_to_use' must be a string.")

    for field in ARRAY_FIELDS:
        value = frontmatter.get(field)
        if not isinstance(value, list):
            errors.append("Field '%s' must be an array." % field)
            continue
        for idx, item in enumerate(value):
            if not isinstance(item, str) or not item.strip():
                errors.append(
                    "Field '%s' contains an invalid item at index %d (must be non-empty string)."
                    % (field, idx)
                )

    inputs_required = frontmatter.get("inputs_required")
    if isinstance(inputs_required, list) and not inputs_required:
        errors.append("Field 'inputs_required' must contain at least one item.")

    version = frontmatter.get("version")
    if version is not None and not isinstance(version, str):
        errors.append("Field 'version' must be a string when provided.")

    return errors


def validate_skill_body(content: str, frontmatter_end_index: int) -> List[str]:
    errors: List[str] = []
    lines = normalize_newlines(content).split("\n")
    body_lines = lines[frontmatter_end_index + 1 :]

    if len(body_lines) > MAX_SKILL_BODY_LINES:
        errors.append(
            "SKILL.md body is too long (%d lines). Maximum is %d."
            % (len(body_lines), MAX_SKILL_BODY_LINES)
        )
    if not any(line.strip() for line in body_lines):
        errors.append("SKILL.md body is empty.")
    return errors


def _parse_frontmatter_lines(lines: List[str]) -> Dict[str, object]:
    frontmatter: Dict[str, object] = {}
    current_list_key: Optional[str] = None

    for line_number, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- "):
            if current_list_key is None:
                raise FrontmatterError(
                    "Invalid list item at front-matter line %d: %r"
                    % (line_number, raw_line)
                )
            item = stripped[2:].strip()
            if not item:
                raise FrontmatterError(
                    "Empty list item at front-matter line %d." % line_number
                )
            frontmatter[current_list_key].append(_parse_scalar(item))
            continue

        current_list_key = None
        if ":" not in stripped:
            raise FrontmatterError(
                "Invalid front-matter line %d: %r" % (line_number, raw_line)
            )

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            raise FrontmatterError("Empty key at front-matter line %d." % line_number)

        if value == "":
            frontmatter[key] = []
            current_list_key = key
            continue

        if value.startswith("[") and value.endswith("]"):
            frontmatter[key] = _parse_inline_list(value)
        else:
            frontmatter[key] = _parse_scalar(value)

    return frontmatter


def _parse_inline_list(value: str) -> List[str]:
    inner = value[1:-1].strip()
    if not inner:
        return []

    parts = [part.strip() for part in inner.split(",")]
    items = []
    for part in parts:
        if not part:
            continue
        items.append(_parse_scalar(part))
    return items


def _parse_scalar(value: str) -> str:
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def _validate_name(name: str, skill_dir_name: str) -> List[str]:
    errors = []
    if not name:
        errors.append("Field 'name' cannot be empty.")
        return errors

    if name != skill_dir_name:
        errors.append(
            "Field 'name' (%s) must match skill directory name (%s)."
            % (name, skill_dir_name)
        )

    if not re.match(r"^[a-z0-9-]+$", name):
        errors.append(
            "Name '%s' should be hyphen-case (lowercase letters, digits, hyphens only)."
            % name
        )

    if name.startswith("-") or name.endswith("-") or "--" in name:
        errors.append(
            "Name '%s' cannot start/end with hyphen or contain consecutive hyphens." % name
        )

    if len(name) > MAX_SKILL_NAME_LENGTH:
        errors.append(
            "Name is too long (%d). Maximum is %d."
            % (len(name), MAX_SKILL_NAME_LENGTH)
        )

    return errors


def _validate_description(description: str) -> List[str]:
    errors = []
    if not description.strip():
        errors.append("Field 'description' cannot be empty.")
        return errors

    if "<" in description or ">" in description:
        errors.append("Description cannot contain angle brackets (< or >).")

    if len(description) > MAX_DESCRIPTION_LENGTH:
        errors.append(
            "Description is too long (%d). Maximum is %d."
            % (len(description), MAX_DESCRIPTION_LENGTH)
        )

    return errors
