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
from typing import List, Tuple

from skill_metadata import (
    FrontmatterError,
    iter_skill_dirs,
    normalize_newlines,
    parse_frontmatter,
    validate_frontmatter,
    validate_skill_body,
)
from skills_index_lib import (
    collect_skill_index_entries,
    extract_auto_generated_block,
    render_auto_generated_block,
    replace_auto_generated_block,
)

OPENAI_REQUIRED_INTERFACE_KEYS = ("display_name", "short_description", "default_prompt")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate skill folders and SKILL.md metadata for this repository."
    )
    parser.add_argument(
        "targets",
        nargs="*",
        help="Optional skill directories (or SKILL.md files). Defaults to all skills/*.",
    )
    parser.add_argument(
        "--allow-legacy-no-frontmatter",
        action="store_true",
        help=(
            "Allow SKILL.md without front-matter and report warning instead of failure. "
            "This is a temporary compatibility mode and will be removed in a future version."
        ),
    )
    parser.add_argument(
        "--check-index",
        action="store_true",
        help="Check whether skills/README.md auto-generated block is up to date.",
    )
    parser.add_argument(
        "--fix-index",
        action="store_true",
        help="When used with --check-index, update the skills/README.md auto-generated block.",
    )
    return parser


def validate_skill_dir(
    skill_dir: Path, allow_legacy_no_frontmatter: bool = False
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    if (skill_dir / "DISABLED").exists():
        return ["SKIP::DISABLED"], warnings

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md not found.")
        return errors, warnings

    try:
        content = skill_md.read_text(encoding="utf-8")
    except OSError as exc:
        errors.append("Failed to read SKILL.md: %s" % exc)
        return errors, warnings

    try:
        frontmatter, frontmatter_end_index = parse_frontmatter(content)
    except FrontmatterError as exc:
        errors.append("Invalid SKILL.md front-matter: %s" % exc)
        return errors, warnings

    if frontmatter is None:
        message = (
            "Missing YAML front-matter in SKILL.md. "
            "Required fields: name, description, when_to_use, inputs_required, "
            "templates, references, agents (version optional)."
        )
        if allow_legacy_no_frontmatter:
            warnings.append(
                "%s Allowed in legacy compatibility mode; this mode will be removed later."
                % message
            )
            return errors, warnings
        errors.append(message)
        return errors, warnings

    if frontmatter_end_index is None:
        errors.append("Invalid SKILL.md: unable to locate front-matter end marker.")
        return errors, warnings

    errors.extend(validate_frontmatter(frontmatter, skill_dir.name))
    errors.extend(validate_skill_body(content, frontmatter_end_index))

    for field in ("templates", "references", "agents"):
        value = frontmatter.get(field)
        if not isinstance(value, list):
            continue
        for rel_path in value:
            errors.extend(_validate_referenced_file(skill_dir, field, rel_path))

    agent_files = frontmatter.get("agents")
    if isinstance(agent_files, list):
        for rel_path in agent_files:
            agent_path = skill_dir / rel_path
            if agent_path.exists() and agent_path.name == "openai.yaml":
                errors.extend(_validate_openai_yaml(agent_path, skill_dir.name))

    return errors, warnings


def _validate_referenced_file(skill_dir: Path, field: str, rel_path: str) -> List[str]:
    errors: List[str] = []

    path_value = Path(rel_path)
    if path_value.is_absolute():
        errors.append(
            "Front-matter field '%s' contains absolute path '%s'; use a skill-relative path."
            % (field, rel_path)
        )
        return errors

    skill_dir_resolved = skill_dir.resolve()
    target_path = (skill_dir / path_value).resolve()

    if not _is_relative_to(target_path, skill_dir_resolved):
        errors.append(
            "Front-matter field '%s' contains path traversal '%s'; path must stay under %s."
            % (field, rel_path, skill_dir.as_posix())
        )
        return errors

    if not target_path.exists():
        errors.append(
            "Front-matter field '%s' references missing file: %s"
            % (field, (skill_dir / path_value).as_posix())
        )
        return errors

    if target_path.is_dir():
        errors.append(
            "Front-matter field '%s' must reference a file, not directory: %s"
            % (field, (skill_dir / path_value).as_posix())
        )

    return errors


def _is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
        return True
    except ValueError:
        return False


def _parse_openai_interface(openai_yaml: Path) -> Tuple[dict, List[str]]:
    interface = {}
    warnings: List[str] = []

    lines = openai_yaml.read_text(encoding="utf-8").splitlines()
    in_interface = False

    for raw_line in lines:
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if not in_interface:
            if stripped == "interface:":
                in_interface = True
            continue

        if not raw_line.startswith((" ", "\t")):
            break
        if ":" not in stripped:
            continue

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1]
        interface[key] = value

    if not in_interface:
        warnings.append("Missing 'interface:' section in %s." % openai_yaml.as_posix())
    return interface, warnings


def _validate_openai_yaml(openai_yaml: Path, skill_name: str) -> List[str]:
    errors: List[str] = []

    try:
        interface, parse_warnings = _parse_openai_interface(openai_yaml)
    except OSError as exc:
        return ["Failed to read %s: %s" % (openai_yaml.as_posix(), exc)]

    for warning in parse_warnings:
        errors.append(warning)

    missing = [k for k in OPENAI_REQUIRED_INTERFACE_KEYS if not interface.get(k, "").strip()]
    if missing:
        errors.append(
            "%s is missing required interface key(s): %s"
            % (openai_yaml.as_posix(), ", ".join(missing))
        )

    expected_trigger = "$%s" % skill_name
    default_prompt = interface.get("default_prompt", "")
    if default_prompt and expected_trigger not in default_prompt:
        errors.append(
            "%s default_prompt must include '%s'."
            % (openai_yaml.as_posix(), expected_trigger)
        )

    return errors


def _resolve_targets(repo_root: Path, args) -> Tuple[List[Path], List[str]]:
    errors: List[str] = []
    skills_root = repo_root / "skills"

    if not args.targets:
        return list(iter_skill_dirs(skills_root)), errors

    targets: List[Path] = []
    for raw_target in args.targets:
        target = Path(raw_target)
        if not target.is_absolute():
            target = (Path.cwd() / target).resolve()

        if target.is_file() and target.name == "SKILL.md":
            targets.append(target.parent)
            continue

        if target.is_dir():
            targets.append(target)
            continue

        errors.append("Target not found or invalid skill path: %s" % raw_target)

    return targets, errors


def _check_or_fix_index(
    repo_root: Path, allow_legacy_no_frontmatter: bool, fix_index: bool
) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    skills_root = repo_root / "skills"
    readme_path = skills_root / "README.md"

    try:
        entries, index_warnings = collect_skill_index_entries(
            skills_root,
            allow_legacy_no_frontmatter=allow_legacy_no_frontmatter,
        )
        warnings.extend(index_warnings)

        readme_content = readme_path.read_text(encoding="utf-8")
        generated_block = render_auto_generated_block(entries)
        current_block = extract_auto_generated_block(readme_content)

        if normalize_newlines(current_block) == generated_block:
            return errors, warnings

        if fix_index:
            updated_content = replace_auto_generated_block(readme_content, generated_block)
            readme_path.write_text(updated_content, encoding="utf-8")
            warnings.append("[FIXED] skills/README.md auto-generated index block updated.")
            return errors, warnings

        errors.append(
            "skills/README.md auto-generated index block is outdated. "
            "Run: python scripts/generate_skills_index.py"
        )
    except Exception as exc:  # noqa: BLE001 - keep script output explicit and simple
        errors.append("Failed to check skills index: %s" % exc)

    return errors, warnings


def main(argv):
    parser = _build_parser()
    args = parser.parse_args(argv[1:])

    if args.fix_index and not args.check_index:
        parser.error("--fix-index requires --check-index")

    repo_root = Path(__file__).resolve().parents[1]

    target_dirs, target_errors = _resolve_targets(repo_root, args)
    failed = 0

    for error in target_errors:
        failed += 1
        print("[FAIL] %s" % error)

    if not target_dirs and not target_errors:
        print("No skills found to validate.")

    for skill_dir in sorted(set(target_dirs), key=lambda p: p.as_posix()):
        rel_skill_dir = _to_repo_relative(skill_dir, repo_root)
        errors, warnings = validate_skill_dir(
            skill_dir, allow_legacy_no_frontmatter=args.allow_legacy_no_frontmatter
        )

        if errors == ["SKIP::DISABLED"]:
            print("[SKIP] %s: DISABLED marker found" % rel_skill_dir)
            continue

        if errors:
            failed += 1
            print("[FAIL] %s" % rel_skill_dir)
            for item in errors:
                print("  - %s" % item)
            for warning in warnings:
                print("  - [WARN] %s" % warning)
            continue

        print("[OK] %s" % rel_skill_dir)
        for warning in warnings:
            print("  - [WARN] %s" % warning)

    if args.check_index:
        index_errors, index_warnings = _check_or_fix_index(
            repo_root,
            allow_legacy_no_frontmatter=args.allow_legacy_no_frontmatter,
            fix_index=args.fix_index,
        )
        for warning in index_warnings:
            print(warning)
        if index_errors:
            failed += 1
            for error in index_errors:
                print("[FAIL] %s" % error)
        else:
            print("[OK] skills/README.md auto-generated index check passed")

    return 1 if failed else 0


def _to_repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
