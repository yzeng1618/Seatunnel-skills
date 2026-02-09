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

from pathlib import Path
from typing import Dict, List, Tuple

from skill_metadata import FrontmatterError, iter_skill_dirs, normalize_newlines, parse_frontmatter

AUTO_GENERATED_START = "<!-- AUTO-GENERATED:START -->"
AUTO_GENERATED_END = "<!-- AUTO-GENERATED:END -->"


class IndexError(ValueError):
    """Raised for skills index generation/check failures."""


def collect_skill_index_entries(
    skills_root: Path, allow_legacy_no_frontmatter: bool = False
) -> Tuple[List[Dict[str, str]], List[str]]:
    entries: List[Dict[str, str]] = []
    warnings: List[str] = []

    for skill_dir in iter_skill_dirs(skills_root):
        if (skill_dir / "DISABLED").exists():
            continue

        skill_md = skill_dir / "SKILL.md"
        try:
            content = skill_md.read_text(encoding="utf-8")
        except OSError as exc:
            raise IndexError("Failed to read %s: %s" % (skill_md, exc))

        try:
            frontmatter, _ = parse_frontmatter(content)
        except FrontmatterError as exc:
            raise IndexError("Failed to parse %s: %s" % (skill_md, exc))

        if frontmatter is None:
            if allow_legacy_no_frontmatter:
                warnings.append(
                    "[WARN] %s: missing front-matter; skipped in generated index "
                    "(legacy compatibility mode)." % skill_dir.as_posix()
                )
                continue
            raise IndexError(
                "%s: missing front-matter; run migration or use --allow-legacy-no-frontmatter."
                % skill_dir.as_posix()
            )

        name = str(frontmatter.get("name", "")).strip()
        description = str(frontmatter.get("description", "")).strip()
        if not name or not description:
            raise IndexError(
                "%s: front-matter fields 'name' and 'description' are required for index generation."
                % skill_dir.as_posix()
            )

        entries.append(
            {
                "name": name,
                "description": description,
                "entry": "./%s/SKILL.md" % name,
            }
        )

    entries.sort(key=lambda item: item["name"])
    return entries, warnings


def render_auto_generated_block(entries: List[Dict[str, str]]) -> str:
    lines = [
        AUTO_GENERATED_START,
        "| Name | Description | Entry |",
        "| --- | --- | --- |",
    ]
    for entry in entries:
        lines.append(
            "| `%s` | %s | [`SKILL.md`](%s) |"
            % (
                _escape_markdown(entry["name"]),
                _escape_markdown(entry["description"]),
                entry["entry"],
            )
        )
    lines.append(AUTO_GENERATED_END)
    return "\n".join(lines)


def replace_auto_generated_block(readme_content: str, generated_block: str) -> str:
    text = normalize_newlines(readme_content)
    start_idx = text.find(AUTO_GENERATED_START)
    end_idx = text.find(AUTO_GENERATED_END)

    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        raise IndexError(
            "Missing or invalid auto-generated block markers in skills/README.md. "
            "Expected markers: '%s' and '%s'." % (AUTO_GENERATED_START, AUTO_GENERATED_END)
        )

    end_idx += len(AUTO_GENERATED_END)
    return text[:start_idx] + generated_block + text[end_idx:]


def extract_auto_generated_block(readme_content: str) -> str:
    text = normalize_newlines(readme_content)
    start_idx = text.find(AUTO_GENERATED_START)
    end_idx = text.find(AUTO_GENERATED_END)
    if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
        raise IndexError(
            "Missing or invalid auto-generated block markers in skills/README.md."
        )
    end_idx += len(AUTO_GENERATED_END)
    return text[start_idx:end_idx]


def _escape_markdown(value: str) -> str:
    return value.replace("|", "\\|")
