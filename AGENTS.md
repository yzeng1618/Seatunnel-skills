# Seatunnel-skills Agent Guide

This `AGENTS.md` applies to the **yzeng1618/Seatunnel-skills** repository (skills/templates/scripts/docs), not the Apache SeaTunnel runtime codebase.

## Scope

- This repository stores reusable Skills, templates, references, validation scripts, and contribution docs.
- If you are changing files in `skills/`, `scripts/`, `.github/`, or repo docs, follow this guide.
- Do **not** treat `./mvnw ...` SeaTunnel build/test commands as required checks for this repository.

## Required Local Verification

After adding or modifying any skill, run:

```bash
python scripts/validate_skills.py
python scripts/generate_skills_index.py
python scripts/validate_skills.py --check-index
```

Optional transition mode for old skills without front-matter:

```bash
python scripts/validate_skills.py --allow-legacy-no-frontmatter
```

## Skill Directory Contract

Each skill must follow this structure:

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml                 # optional but recommended
  references/*.md                    # optional
  templates/*.md                     # optional
  examples/example_input.md          # required in this repo
  examples/example_output.md         # required in this repo
```

### `SKILL.md` front-matter (required)

`SKILL.md` must start with YAML front-matter and include at least:

- `name` (must equal `<skill-name>` directory)
- `description`
- `when_to_use`
- `inputs_required` (array)
- `templates` (array, can be empty)
- `references` (array, can be empty)
- `agents` (array, can be empty)
- `version` (optional)

All `templates`/`references`/`agents` entries must be **skill-relative file paths** that exist.

## `DISABLED` Mechanism

If a skill directory contains a file named `DISABLED`:

- `scripts/validate_skills.py` skips validating that skill.
- `scripts/generate_skills_index.py` excludes that skill from the generated index.

Use this only for temporary deactivation; keep reason/context in PR description.

## Auto-generated Skills Index

`skills/README.md` contains an auto-generated block between:

- `<!-- AUTO-GENERATED:START -->`
- `<!-- AUTO-GENERATED:END -->`

Do not hand-edit this block. Regenerate with:

```bash
python scripts/generate_skills_index.py
```

## SeaTunnel Upstream Reference

When you are working on the **Apache SeaTunnel main codebase** (not this skills repo), use:

- `docs/upstream/AGENTS_SEATUNNEL_CODEBASE.md`

That document keeps the original SeaTunnel-specific contribution/checklist guidance for reference.
