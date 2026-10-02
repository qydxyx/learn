# Description Optimization

The `description` field in SKILL.md frontmatter is the primary mechanism determining whether an agent invokes a skill. Optimize it after the skill's core workflow is solid.

## Step 1: Generate Trigger Eval Queries

Create 16-20 eval queries — mix of should-trigger (8-10) and should-not-trigger (8-10).

```json
[
  {"query": "realistic user prompt here", "should_trigger": true},
  {"query": "near-miss prompt here", "should_trigger": false}
]
```

### Query quality rules

Queries must be realistic — what a real user would actually type:
- Include file paths, personal context, column names, company names
- Mix lengths: short casual to detailed backstory
- Include abbreviations, typos, casual speech
- Focus on edge cases, not clear-cut matches

**Bad:** `"Format this data"`, `"Create a chart"`
**Good:** `"ok so my boss sent me this xlsx (in downloads, 'Q4 sales final FINAL v2.xlsx') and wants a profit margin column. Revenue in C, costs in D i think"`

### Should-trigger queries (8-10)

Coverage over repetition:
- Different phrasings of same intent (formal + casual)
- Cases where user doesn't explicitly name the skill but clearly needs it
- Uncommon use cases
- Cases where this skill competes with another but should win

### Should-not-trigger queries (8-10)

Near-misses are most valuable:
- Queries sharing keywords but needing something different
- Ambiguous phrasing where naive keyword match would trigger but shouldn't
- Adjacent domains
- "Write a fibonacci function" is TOO easy as a negative — make them tricky

## Step 2: Review with User

Present the eval set. Let user edit, add, remove. This step matters — bad queries → bad description.

## Step 3: Test Triggering

### Pi

```bash
pi --no-skills --skill /path/to/skill
```

Test each query. Note which triggered the skill and which didn't. Compare against expected.

### Antigravity CLI / Grok Build

Start a session with only the target skill loaded. Test each query manually. Note trigger/miss behavior.

## Step 4: Iterate on Description

Based on trigger test results:

1. If undertriggering: add more trigger phrases, make description pushier
2. If overtriggering: add negative constraints ("NOT for X")
3. Test again
4. Repeat until trigger accuracy is satisfactory

### Tips

- All "when to use" info goes in description, not body
- Include both what the skill does AND specific trigger contexts
- Combat undertriggering by being pushy: "Make sure to use this skill whenever the user mentions X, Y, or Z, even if they don't explicitly ask for it"
- For Grok Build, also populate `when-to-use` array in frontmatter for extra trigger signal
