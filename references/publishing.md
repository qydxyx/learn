# Publishing Skills

## For Pi

Make the skill installable with `pi install` from npm, git, or local path.

### Install examples

```bash
pi install npm:<package>
pi install git:github.com/org/repo
pi install ./local/path
```

### Minimal package.json (for npm/git)

```json
{
  "name": "my-agent-skills",
  "keywords": ["pi-package"],
  "pi": { "skills": ["./skills"] }
}
```

Pi loads skills from either:
1. `package.json` `pi.skills` manifest
2. Conventional `skills/` directory

Pi does NOT use `.skill` archives. `pi update` updates non-pinned npm and git installs.

### Validation

```bash
# Basic validation
scripts/validate_skill.py /path/to/my-skill

# With README requirement (for publishing)
scripts/validate_skill.py --require-readme /path/to/my-skill
```

Use `pi config` to enable/disable/filter after installation.

## For Antigravity CLI

No package manager. Copy skill directory to:
- Project: `.agents/skills/<skill-name>/`
- Global: `~/.gemini/skills/<skill-name>/`

Share via git repos or zip archives.

## For Grok Build

No package manager. Copy skill directory to:
- Project: `.grok/skills/<skill-name>/`
- Global: `~/.grok/skills/<skill-name>/`

Share via git repos or zip archives. Users can also use `/skillify` in Grok Build to create skills from sessions.

## Cross-Agent Distribution

For max reach, structure your repo like:

```
my-skills-repo/
├── README.md
├── package.json          # For pi install
├── skills/
│   └── my-skill/
│       ├── SKILL.md
│       ├── scripts/
│       └── references/
└── install.sh            # Optional: copies to all agent dirs
```

Example `install.sh`:

```bash
#!/usr/bin/env bash
SKILL_DIR="skills/my-skill"

# Pi (if installed)
if command -v pi &>/dev/null; then
  pi install ./
else
  mkdir -p ~/.pi/agent/skills/
  cp -r "$SKILL_DIR" ~/.pi/agent/skills/
fi

# Antigravity
mkdir -p ~/.gemini/skills/
cp -r "$SKILL_DIR" ~/.gemini/skills/

# Grok Build
mkdir -p ~/.grok/skills/
cp -r "$SKILL_DIR" ~/.grok/skills/

echo "Installed to all agent skill directories."
```
