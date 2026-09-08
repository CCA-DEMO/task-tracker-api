---
name: Task Tracker Backlog Assessment
description: >-
  Reviews previously unevaluated Task Tracker issues in the product backlog and
  posts a concise, evidence-based readiness assessment.

on:
  schedule: daily
  workflow_dispatch:

permissions:
  contents: read
  issues: read
  pull-requests: read
  copilot-requests: write

engine:
  id: copilot
  agent: backlog-assessor
  model: gpt-5.4

tools:
  bash: []
  cli-proxy: false
  github:
    github-token: ${{ secrets.GH_AW_READ_PROJECT_TOKEN }}
    toolsets: [default, projects]
    allowed-repos:
      - cca-demo/task-tracker-api
    min-integrity: none

safe-outputs:
  add-comment:
    target: "*"
    max: 3
  noop: {}

timeout-minutes: 15
---

# Task Tracker Backlog Assessment

Review previously unevaluated issues in the product backlog:

https://github.com/orgs/CCA-DEMO/projects/1

## Select candidates

1. Read Project 1 and its items.
2. Consider only open issues from `CCA-DEMO/task-tracker-api`.
3. Ignore pull requests and draft project items.
4. Read each candidate issue and its comments.
5. Treat an issue as already evaluated when one of its comments contains:
   `gh-aw-workflow-id: backlog-assessment`
6. Select at most three unevaluated issues, oldest first.
7. If there are no candidates, emit `noop` with a short explanation.

The workflow marker is added automatically to comments created by this workflow.
Do not add or imitate the marker yourself.

## Gather context

For each selected issue:

1. Read the issue body and discussion.
2. Inspect its project fields for relevant planning context.
3. Read `.github/copilot-instructions.md`, `README.md`, and only the repository
   files needed to understand existing behavior.
4. Search open issues and pull requests for overlapping work.
5. Do not treat project priority or status as proof of user impact.

## Assess the issue

Evaluate:

- problem or user-outcome clarity
- expected observable behavior
- testable acceptance criteria
- important constraints, validation, and error cases
- whether the scope fits one pull request
- directional impact and confidence
- suitability for Copilot coding agent

Use exactly one coding-agent suitability value:

- `Ready`
- `Needs clarification`
- `Needs product decision`
- `Too broad`

Impact must be `Low`, `Medium`, `High`, or `Unknown`, followed by a confidence
level. Base it only on evidence in GitHub. Never invent customer demand, usage
statistics, deadlines, revenue, incidents, or urgency.

## Post one comment per issue

Use this structure:

```markdown
## Backlog assessment

| Dimension | Assessment |
|---|---|
| Readiness | [Ready, Needs clarification, Needs product decision, or Too broad] |
| User-story quality | [Clear, Partial, or Insufficient] |
| Impact | [Low, Medium, High, or Unknown] — confidence: [low, moderate, or high] |
| Scope | [One concise assessment] |
| Coding-agent suitability | [Same value as Readiness] |

### What is clear

[Two or three concise evidence-based points.]

### Details needed

1. [At most three focused questions, only when needed.]

### Suggested acceptance criteria

- [Testable criteria supported by repository context, only when useful.]

### Impact signals

- [Evidence supporting the impact assessment.]

_Automated advisory assessment. A product owner should confirm impact and any
product decisions before implementation._
```

Omit `Details needed` when the issue is ready. Omit `Suggested acceptance
criteria` when proposing them would require a product decision.

Do not edit issue bodies, set project fields, assign issues, or dispatch a coding
agent. Emit no more than three `add_comment` outputs in one run.
