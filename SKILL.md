---
name: learn
description: Create new agent skills, modify and improve existing skills, and measure skill performance across Pi, Antigravity CLI, and Grok Build environments. Use when users want to create a skill from scratch, edit or optimize an existing skill, convert a workflow into a reusable skill, test a skill with evals, or optimize a skill's description for better triggering accuracy. Also use when the user says "learn this", "turn this into a skill", "make a skill for X", "skillify", or wants to package a skill for cross-agent use.
---

# Learn — Multi-Agent Skill Creator

A skill for creating, testing, and iteratively improving agent skills that work across **Pi**, **Antigravity CLI**, and **Grok Build**.

## Core Workflow

1. Decide what the skill should do
2. Draft the skill (SKILL.md + resources)
3. Test it in the target agent environment
4. Evaluate results with the user
5. Iterate until satisfied
6. Optimize description for triggering
7. Package for target agent(s)

Your job: figure out where the user is in this process and help them progress. Maybe they say "I want a skill for X" → help scope, draft, test. Maybe they have a draft → jump to test/iterate. If they say "just vibe with me" → skip the formal eval loop.

## Target Environments

This skill creates skills compatible with all three agent harnesses. The SKILL.md format is the shared standard — same file works everywhere with minor path differences.

| Feature | Pi | Antigravity CLI | Grok Build |
|---------|-----|----------------|------------|
| **Skill file** | `SKILL.md` | `SKILL.md` | `SKILL.md` |
| **Frontmatter** | `name`, `description` (required) | `name`, `description` (required) | `name`, `description` (required) |
| **Project scope** | `.pi/skills/` or `.agents/skills/` | `.agents/skills/` | `.grok/skills/` |
| **Global scope** | `~/.pi/agent/skills/` | `~/.gemini/skills/` | `~/.grok/skills/` |
| **Install** | `pi install git:...` / `pi install npm:...` | manual copy | manual copy |
| **Reload** | `/reload` | `/skills` | `/skills` |
| **Explicit invoke** | `/skill:name` | — | `/name` |
| **Subagents** | Yes (pi subagents) | No | No |
| **Optional frontmatter** | `disable-model-invocation`, `metadata`, `allowed-tools` | — | `when-to-use`, `paths`, `user-invocable`, `disable-model-invocation`, `allowed-tools` |

### Cross-compatibility rules

- Directory name MUST equal frontmatter `name`
- Name: 1–64 chars, lowercase letters/digits/hyphens, no leading/trailing/consecutive hyphens
- Keep frontmatter to `name` + `description` for max portability. Add agent-specific fields only when needed
- Use `.agents/skills/` for project-scoped skills discoverable by both Pi and Antigravity
- Scripts should use `#!/usr/bin/env python3` or `#!/usr/bin/env bash` for portability

## Creating a Skill

### 1) Capture Intent

If the current conversation already contains a workflow (user says "turn this into a skill"), extract from history first: tools used, step sequence, corrections made, input/output formats.

Questions to answer:
1. What should the skill enable the agent to do?
2. When should it trigger? (user phrases, contexts)
3. What's the expected output format?
4. Which agent(s) will use it? (Pi / Antigravity / Grok / all)
5. Should we set up test cases? (yes for verifiable outputs, optional for subjective ones)

### 2) Interview & Research

Ask about edge cases, input/output formats, example files, success criteria, dependencies. Use web search or MCP tools if helpful for research. Come prepared to reduce burden on the user.

### 3) Write the SKILL.md

#### Anatomy

```
skill-name/
├── SKILL.md          # Required: frontmatter + instructions
├── scripts/          # Optional: executable helpers
├── references/       # Optional: docs loaded on demand
└── assets/           # Optional: templates, data files
```

#### Progressive Disclosure

Three-level loading (all three agents support this pattern):
1. **Metadata** (name + description) — always in context (~100 words)
2. **SKILL.md body** — loaded when skill triggers (<500 lines ideal)
3. **Bundled resources** — loaded on demand (unlimited)

Key patterns:
- Keep SKILL.md under 500 lines. If approaching limit, split into references with clear pointers
- Reference files: tell the agent WHEN to read each one
- Large reference files (>300 lines): include a table of contents
- Domain variants: organize by reference file, agent reads only the relevant one

#### Writing the frontmatter

```yaml
---
name: my-skill
description: What it does + when to use it. Include trigger phrases.
---
```

Make descriptions **slightly pushy** to combat undertriggering. Instead of "Validates SQL migrations", write "Validates SQL migrations against schema guidelines. Use when writing new migrations, modifying table structures, reviewing database PRs, or when anyone mentions schema changes."

#### Writing the body

- Imperative phrasing for procedures, context framing for guidance
- Explain **why** things matter — modern LLMs respond better to reasoning than rigid MUSTs
- Include examples with input/output pairs
- For output format requirements, show the exact template

### 4) Test the Skill

Testing depends on which agent you're using:

#### Pi (full eval loop)

Pi has subagents. Run test prompts in parallel:

```bash
# Load only this skill
pi --no-skills --skill /path/to/my-skill

# Or invoke explicitly
/skill:my-skill
```

For each test case, you can spawn with-skill and baseline runs as subagents. See `references/eval-workflow.md` for the full eval framework.

After edits, use `/reload` to pick up changes.

#### Antigravity CLI

No subagents. Test manually:

1. Copy skill to `.agents/skills/my-skill/`
2. Start new session or run `/skills` to reload
3. Test each prompt sequentially
4. Compare output to expectations by eye

#### Grok Build

No subagents. Test manually:

1. Copy skill to `.grok/skills/my-skill/`
2. Start new session or run `/skills` to reload
3. Test each prompt sequentially
4. Or use `/my-skill` for explicit invocation

#### Lightweight testing (any agent)

For quick iteration without the full eval framework:
1. Write 2-3 realistic test prompts
2. Run them in the target agent
3. Eyeball the results
4. Tweak the skill
5. Reload and repeat

### 5) Evaluate & Iterate

After testing:

1. **Generalize from feedback.** Don't overfit to test examples. If a fix only helps one test case, it's probably wrong
2. **Keep the prompt lean.** Remove instructions that don't pull their weight
3. **Explain the why.** If you're writing ALWAYS/NEVER in caps, reframe as reasoning
4. **Look for repeated work.** If every test run writes the same helper script, bundle it in `scripts/`

### 6) Optimize Description

The description is the primary trigger mechanism. After the skill works well:

1. Generate 10-20 eval queries (mix of should-trigger and should-not-trigger)
2. Make should-not-trigger queries genuinely tricky near-misses, not obviously irrelevant
3. Test triggering in the target agent
4. Iterate on description wording

See `references/description-optimization.md` for detailed process.

### 7) Package & Install

#### For Pi

```bash
# From local path
pi install ./path/to/skill

# From git
pi install git:github.com/org/my-skill

# From npm
pi install npm:my-package
```

See `references/publishing.md` for npm/git packaging details.

#### For Antigravity CLI

```bash
# Project scope
cp -r my-skill .agents/skills/

# Global scope
cp -r my-skill ~/.gemini/skills/
```

#### For Grok Build

```bash
# Project scope
cp -r my-skill .grok/skills/

# Global scope
cp -r my-skill ~/.grok/skills/
```

#### Universal (works in Pi + Antigravity)

```bash
cp -r my-skill .agents/skills/
```

Both Pi and Antigravity discover `.agents/skills/`.

---

## Improving an Existing Skill

When updating rather than creating:

1. **Preserve the original name.** Don't rename to `-v2`
2. **Copy to writeable location if needed.** Installed paths may be read-only: `cp -r <installed-path> /tmp/skill-name/`, edit there
3. **Snapshot before changes.** `cp -r <skill> <workspace>/skill-snapshot/` as baseline
4. **Same iterate loop:** test → evaluate → improve → reload → repeat

---

## Reference Files

Read these on demand:

- `references/eval-workflow.md` — Full eval framework for Pi (subagent-based testing, grading, benchmarking)
- `references/description-optimization.md` — Trigger description optimization process
- `references/publishing.md` — Packaging skills for Pi (npm/git), with cross-agent notes
- `references/schemas.md` — JSON schemas for evals.json, grading.json, benchmark.json

---

## Quick Checklist

Before declaring a skill done:

- [ ] `name` frontmatter matches directory name
- [ ] `description` includes trigger phrases and "when to use" context
- [ ] SKILL.md under 500 lines
- [ ] Heavy docs moved to `references/`
- [ ] Scripts are executable (`chmod +x`)
- [ ] Tested in target agent environment
- [ ] Works with `/reload` (no stale state issues)
- [ ] No hardcoded absolute paths (use relative paths from skill dir)
