# Eval Workflow (Pi with Subagents)

This is the full evaluation framework. Only usable in Pi, which has subagent support.

For Antigravity CLI and Grok Build, use the lightweight manual testing described in the main SKILL.md.

## Setup

Put results in `<skill-name>-workspace/` as sibling to the skill directory. Organize by iteration (`iteration-1/`, `iteration-2/`) and within that, each test case gets a directory (`eval-0/`, `eval-1/`).

## Step 1: Create Test Cases

Write 2-3 realistic test prompts. Save to `evals/evals.json`:

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": [],
      "expectations": [
        "The output includes X",
        "The skill used script Y"
      ]
    }
  ]
}
```

## Step 2: Spawn Runs

For each test case, spawn two pi subagents in the same turn:

**With-skill run:**
```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
```

**Baseline run (no skill):**
Same prompt, no skill path. Save to `without_skill/outputs/`.

Write `eval_metadata.json` for each test case:
```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

## Step 3: Draft Assertions While Runs Execute

Don't wait idle. Draft quantitative assertions for each test case:
- Make assertions objectively verifiable
- Give them descriptive names
- For programmatically checkable assertions, write a script

Update `eval_metadata.json` and `evals/evals.json` with assertions.

## Step 4: Capture Timing

When each subagent completes, save `total_tokens` and `duration_ms` from the notification to `timing.json`:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

## Step 5: Grade

Grade each run's assertions against outputs. Save to `grading.json` in each run directory.

The `expectations` array must use fields `text`, `passed`, and `evidence`.

```json
{
  "expectations": [
    {
      "text": "The output includes X",
      "passed": true,
      "evidence": "Found in output file: ..."
    }
  ],
  "summary": {
    "passed": 2,
    "failed": 1,
    "total": 3,
    "pass_rate": 0.67
  }
}
```

## Step 6: Present Results

Show results to the user:
- Per test case: prompt, output, grading
- Aggregate: pass rates, timing, token usage
- Ask for feedback inline

## Step 7: Iterate

Based on feedback:
1. Improve the skill
2. Rerun all test cases into `iteration-<N+1>/`
3. Compare with previous iteration
4. Repeat until user is happy or feedback is all empty

## Grading Guidelines

**PASS when:**
- Clear evidence the expectation is true
- Evidence reflects genuine substance, not surface compliance

**FAIL when:**
- No evidence found
- Evidence contradicts expectation
- Evidence is superficial (right filename but wrong content)

**When uncertain:** burden of proof is on the expectation to pass.

## Full Schema Reference

See `references/schemas.md` for complete JSON schemas for all data files.
