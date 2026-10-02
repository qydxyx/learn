# JSON Schemas

Data schemas used by the eval workflow.

---

## evals.json

Eval definitions. Located at `evals/evals.json` within the skill directory.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's example prompt",
      "expected_output": "Description of expected result",
      "files": ["evals/files/sample1.pdf"],
      "expectations": [
        "The output includes X",
        "The skill used script Y"
      ]
    }
  ]
}
```

**Fields:**
- `skill_name`: matches frontmatter name
- `evals[].id`: unique integer
- `evals[].prompt`: task to execute
- `evals[].expected_output`: human-readable success description
- `evals[].files`: optional input file paths (relative to skill root)
- `evals[].expectations`: verifiable statements

---

## grading.json

Grading results per run. Located at `<run-dir>/grading.json`.

```json
{
  "expectations": [
    {
      "text": "The output includes the name 'John Smith'",
      "passed": true,
      "evidence": "Found in output Step 3: 'Extracted names: John Smith'"
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

**Fields:**
- `expectations[].text`: original expectation
- `expectations[].passed`: boolean
- `expectations[].evidence`: specific quote or description
- `summary`: aggregate pass/fail counts

---

## timing.json

Wall clock timing per run. Located at `<run-dir>/timing.json`.

Capture from subagent task notification — `total_tokens` and `duration_ms` are not persisted elsewhere.

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

---

## benchmark.json

Aggregate benchmark data. Located at workspace iteration directory.

```json
{
  "metadata": {
    "skill_name": "my-skill",
    "timestamp": "2025-01-15T10:30:00Z",
    "evals_run": [1, 2, 3],
    "runs_per_configuration": 3
  },
  "runs": [
    {
      "eval_id": 1,
      "eval_name": "descriptive-name",
      "configuration": "with_skill",
      "run_number": 1,
      "result": {
        "pass_rate": 0.85,
        "passed": 6,
        "failed": 1,
        "total": 7,
        "time_seconds": 42.5,
        "tokens": 3800
      }
    }
  ],
  "run_summary": {
    "with_skill": {
      "pass_rate": {"mean": 0.85, "stddev": 0.05},
      "time_seconds": {"mean": 45.0, "stddev": 12.0},
      "tokens": {"mean": 3800, "stddev": 400}
    },
    "without_skill": {
      "pass_rate": {"mean": 0.35, "stddev": 0.08},
      "time_seconds": {"mean": 32.0, "stddev": 8.0},
      "tokens": {"mean": 2100, "stddev": 300}
    },
    "delta": {
      "pass_rate": "+0.50",
      "time_seconds": "+13.0",
      "tokens": "+1700"
    }
  }
}
```

**Fields:**
- `configuration`: must be `"with_skill"` or `"without_skill"`
- `result`: nested object with `pass_rate`, `passed`, `total`, `time_seconds`, `tokens`
- `run_summary`: statistical aggregates per configuration with `mean` and `stddev`
