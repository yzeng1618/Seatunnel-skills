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

import argparse
import sys
from pathlib import Path

from skills_index_lib import (
    collect_skill_index_entries,
    render_auto_generated_block,
    replace_auto_generated_block,
)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate the skills index table in skills/README.md."
    )
    parser.add_argument(
        "--allow-legacy-no-frontmatter",
        action="store_true",
        help=(
            "Allow skills without SKILL.md front-matter and skip them with warnings. "
            "This is a temporary compatibility mode."
        ),
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check whether skills/README.md is up to date; do not modify files.",
    )
    return parser


def main(argv):
    parser = _build_parser()
    args = parser.parse_args(argv[1:])

    repo_root = Path(__file__).resolve().parents[1]
    skills_root = repo_root / "skills"
    readme_path = skills_root / "README.md"

    try:
        entries, warnings = collect_skill_index_entries(
            skills_root,
            allow_legacy_no_frontmatter=args.allow_legacy_no_frontmatter,
        )
        readme_content = readme_path.read_text(encoding="utf-8")
        generated_block = render_auto_generated_block(entries)
        updated_content = replace_auto_generated_block(readme_content, generated_block)
    except Exception as exc:  # noqa: BLE001 - keep plain, user-friendly script output
        print("[FAIL] %s" % exc)
        return 1

    for warning in warnings:
        print(warning)

    if readme_content.replace("\r\n", "\n") == updated_content:
        print("[OK] skills/README.md index is up to date")
        return 0

    if args.check:
        print(
            "[FAIL] skills/README.md index is outdated. "
            "Run: python scripts/generate_skills_index.py"
        )
        return 1

    readme_path.write_text(updated_content, encoding="utf-8")
    print("[OK] Updated skills/README.md auto-generated skills index")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
