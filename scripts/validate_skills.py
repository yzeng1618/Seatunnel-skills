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

from __future__ import print_function

import re
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024

ALLOWED_PROPERTIES = {"name", "description"}


def _parse_frontmatter(content):
    if not content.startswith("---"):
        raise ValueError("No YAML frontmatter found (file must start with '---').")

    lines = content.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError("Invalid frontmatter start.")

    end_index = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_index = idx
            break

    if end_index is None:
        raise ValueError("Frontmatter end marker '---' not found.")

    frontmatter_lines = lines[1:end_index]
    frontmatter = {}
    for raw_line in frontmatter_lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith(("-", "[")):
            raise ValueError("Frontmatter must be a mapping (no lists supported).")
        if line.endswith(":"):
            raise ValueError("Frontmatter value cannot be empty mapping.")
        if ":" not in line:
            raise ValueError("Invalid frontmatter line: %r" % raw_line)
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        frontmatter[key] = value

    return frontmatter


def _validate_name(name):
    if not name:
        raise ValueError("Missing 'name' in frontmatter.")
    if not re.match(r"^[a-z0-9-]+$", name):
        raise ValueError(
            "Name '%s' should be hyphen-case (lowercase letters, digits, hyphens only)."
            % name
        )
    if name.startswith("-") or name.endswith("-") or "--" in name:
        raise ValueError(
            "Name '%s' cannot start/end with hyphen or contain consecutive hyphens."
            % name
        )
    if len(name) > MAX_SKILL_NAME_LENGTH:
        raise ValueError(
            "Name is too long (%d). Maximum is %d."
            % (len(name), MAX_SKILL_NAME_LENGTH)
        )


def _validate_description(description):
    if description is None or description == "":
        raise ValueError("Missing 'description' in frontmatter.")
    if "<" in description or ">" in description:
        raise ValueError("Description cannot contain angle brackets (< or >).")
    if len(description) > MAX_DESCRIPTION_LENGTH:
        raise ValueError(
            "Description is too long (%d). Maximum is %d."
            % (len(description), MAX_DESCRIPTION_LENGTH)
        )


def validate_skill_dir(skill_dir):
    skill_dir = Path(skill_dir)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        raise ValueError("SKILL.md not found.")

    content = skill_md.read_text(encoding="utf-8")
    frontmatter = _parse_frontmatter(content)

    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        raise ValueError(
            "Unexpected key(s) in SKILL.md frontmatter: %s. Allowed: %s."
            % (", ".join(sorted(unexpected)), ", ".join(sorted(ALLOWED_PROPERTIES)))
        )

    _validate_name(frontmatter.get("name", "").strip())
    _validate_description(frontmatter.get("description", "").strip())


def iter_skill_dirs(skills_root):
    if not skills_root.exists():
        return
    for child in sorted(skills_root.iterdir()):
        if not child.is_dir():
            continue
        if (child / "DISABLED").exists():
            continue
        if (child / "SKILL.md").exists():
            yield child


def main(argv):
    repo_root = Path(__file__).resolve().parents[1]
    skills_root = repo_root / "skills"

    targets = argv[1:] if len(argv) > 1 else [str(p) for p in iter_skill_dirs(skills_root)]
    if not targets:
        print("No skills found under %s" % skills_root)
        return 0

    failed = 0
    for target in targets:
        try:
            validate_skill_dir(target)
            print("[OK] %s" % target)
        except Exception as e:
            failed += 1
            print("[FAIL] %s: %s" % (target, e))

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
