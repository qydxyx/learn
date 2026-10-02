# learn

Cross-agent skill for creating, testing, and improving agent skills that work on **Pi**, **Antigravity CLI**, and **Grok Build**.

Use it when you want to turn a workflow into a skill, edit an existing one, run evals, or tune a description so it triggers more reliably. Trigger phrases include “learn this”, “turn this into a skill”, and “skillify”.

## What it does

1. Scope the skill
2. Draft `SKILL.md` plus scripts and references
3. Test in the target agent
4. Iterate from feedback
5. Optimize the description
6. Package for Pi, Antigravity, and/or Grok

The shared format is `SKILL.md` with `name` and `description`. The directory name must match `name`.

## Install

**Pi**

```bash
pi install git:github.com/qydxyx/learn
```

**Antigravity CLI**

```bash
cp -r learn .agents/skills/   # project
# or ~/.gemini/skills/        # global
```

**Grok Build**

```bash
cp -r learn .grok/skills/     # project
# or ~/.grok/skills/          # global
```

Pi and Antigravity both discover `.agents/skills/`. Reload with `/reload` (Pi) or `/skills` (Antigravity / Grok).

## Layout

```
learn/
├── SKILL.md
├── references/   # evals, description optimization, publishing, schemas
└── scripts/      # validate_skill.py
```

Validate before publishing:

```bash
scripts/validate_skill.py --require-readme .
```
