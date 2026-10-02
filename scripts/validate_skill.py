#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Validate an Agent Skill directory for cross-agent compatibility (Pi, Antigravity, Grok Build)."""

import sys
import re
import yaml
from pathlib import Path

NAME_RE = re.compile(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$')
MAX_NAME_LEN = 64
MAX_BODY_LINES = 500

def validate(skill_dir: Path, require_readme: bool = False) -> list[str]:
    errors = []
    warnings = []
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        return ["SKILL.md not found"], []

    text = skill_md.read_text(encoding="utf-8")

    # Parse frontmatter
    if not text.startswith("---"):
        errors.append("Missing YAML frontmatter (must start with ---)")
        return errors, warnings

    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append("Malformed frontmatter (missing closing ---)")
        return errors, warnings

    try:
        fm = yaml.safe_load(parts[1])
    except yaml.YAMLError as e:
        errors.append(f"Invalid YAML in frontmatter: {e}")
        return errors, warnings

    if not isinstance(fm, dict):
        errors.append("Frontmatter must be a YAML mapping")
        return errors, warnings

    # Required fields
    name = fm.get("name")
    desc = fm.get("description")

    if not name:
        errors.append("Missing required frontmatter field: name")
    elif not isinstance(name, str):
        errors.append("name must be a string")
    else:
        if len(name) > MAX_NAME_LEN:
            errors.append(f"name exceeds {MAX_NAME_LEN} chars: {len(name)}")
        if not NAME_RE.match(name):
            errors.append(f"name '{name}' invalid: use lowercase letters, digits, hyphens; no leading/trailing/consecutive hyphens")
        if name != skill_dir.name:
            errors.append(f"name '{name}' does not match directory name '{skill_dir.name}'")

    if not desc:
        errors.append("Missing required frontmatter field: description")
    elif not isinstance(desc, str):
        errors.append("description must be a string")
    elif len(desc) < 20:
        warnings.append("description is very short — include trigger phrases for better auto-invocation")

    # Body length
    body = parts[2]
    body_lines = body.strip().split("\n")
    if len(body_lines) > MAX_BODY_LINES:
        warnings.append(f"SKILL.md body is {len(body_lines)} lines (recommended <{MAX_BODY_LINES}). Consider splitting into references/")

    # Scripts executable
    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        for script in scripts_dir.iterdir():
            if script.is_file() and script.suffix in ('.py', '.sh', '.bash'):
                import os
                if not os.access(script, os.X_OK):
                    warnings.append(f"Script not executable: {script.name} (run: chmod +x {script})")

    # README check
    if require_readme:
        readme = skill_dir / "README.md"
        if not readme.exists():
            errors.append("--require-readme: README.md not found")
        else:
            readme_text = readme.read_text(encoding="utf-8").lower()
            if "install" not in readme_text:
                warnings.append("README.md has no Installation section")

    # Cross-agent path check
    for ref_file in (skill_dir / "references").glob("*.md") if (skill_dir / "references").is_dir() else []:
        content = ref_file.read_text(encoding="utf-8")
        if re.search(r'(?:/Users/|/home/|C:\\)', content):
            warnings.append(f"Absolute path found in {ref_file.name} — use relative paths for portability")

    return errors, warnings


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate Agent Skill for Pi/Antigravity/Grok")
    parser.add_argument("skill_dir", type=Path, help="Path to skill directory")
    parser.add_argument("--require-readme", action="store_true", help="Require README.md with install section")
    args = parser.parse_args()

    if not args.skill_dir.is_dir():
        print(f"Error: {args.skill_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    errors, warnings = validate(args.skill_dir, args.require_readme)

    for w in warnings:
        print(f"⚠ {w}")
    for e in errors:
        print(f"✗ {e}")

    if not errors:
        print(f"✓ {args.skill_dir.name} is valid")
        sys.exit(0)
    else:
        print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
        sys.exit(1)


if __name__ == "__main__":
    main()
