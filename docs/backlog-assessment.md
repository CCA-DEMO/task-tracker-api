# Agentic Backlog Assessment

The `backlog-assessment` GitHub Agentic Workflow reviews open Task Tracker issues
in the [CCA-DEMO product backlog](https://github.com/orgs/CCA-DEMO/projects/1).
It evaluates issue clarity, acceptance criteria, scope, directional impact, and
suitability for Copilot coding agent, then posts a structured advisory comment.

## Components

| Component | Repository | Location |
|---|---|---|
| Backlog-assessor custom agent | `CCA-DEMO/.github-private` | `agents/backlog-assessor.agent.md` |
| Agentic workflow source | `CCA-DEMO/task-tracker-api` | `.github/workflows/backlog-assessment.md` |
| Compiled Actions workflow | `CCA-DEMO/task-tracker-api` | `.github/workflows/backlog-assessment.lock.yml` |

The workflow imports the organization-level `backlog-assessor` instructions from
`.github-private`. Compilation resolves `main` to a commit and caches the prompt
under `.github/aw/imports/`, so runs are reproducible.

The Copilot CLI used by `gh aw` discovers repository-local agents but does not
currently discover organization agents from `.github-private` through
`engine.agent`. The import reuses the same organization-owned instructions
without relying on runtime agent discovery.

## Authentication

The default Actions `GITHUB_TOKEN` cannot read organization Projects. Create a
fine-grained PAT with:

- resource owner `CCA-DEMO`
- access to `task-tracker-api`
- repository `Contents: Read` and `Issues: Read`
- organization `Projects: Read`

Store it as a repository secret:

```bash
gh aw secrets set GH_AW_READ_PROJECT_TOKEN --value "<token>"
```

Copilot inference requires a separate user-owned fine-grained PAT with the
account permission `Copilot Requests: Read`. The token owner must have an active
Copilot license. Store it as:

```bash
gh aw secrets set COPILOT_GITHUB_TOKEN --value "<token>"
```

Do not add `copilot-requests: write` to this workflow unless centralized Copilot
billing is enabled for the organization. That permission takes precedence over
and causes `COPILOT_GITHUB_TOKEN` to be ignored.

## Candidate tracking

Comments created by the workflow automatically include:

```html
<!-- gh-aw-workflow-id: backlog-assessment -->
```

An issue is new to the workflow when it is an open `task-tracker-api` issue in
Project 1 and none of its comments contains that marker. This makes scheduled
runs idempotent without a separate database or memory branch.

Each run processes at most three issues, oldest first. The workflow does not edit
issues, modify project fields, assign work, or dispatch a coding agent.

## Compile and run

Recompile after changing the workflow source:

```bash
gh aw compile .github/workflows/backlog-assessment.md
```

Commit both the Markdown source and generated lock workflow. After the custom
agent and workflow are merged and the secret is configured, trigger a run with:

```bash
gh aw run backlog-assessment
```
