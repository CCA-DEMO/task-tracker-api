# UI Testing Agent

This repo extends the Copilot Coding Agent (CCA) demo with a **repo-centric
browser-testing agent**. Alongside the developer agent that pulls issues from the
[project board](https://github.com/orgs/CCA-DEMO/projects/1), a committed
`ui-tester` agent writes and runs Playwright browser tests against the web UI.

## Pieces

| Piece | Location | Purpose |
|-------|----------|---------|
| Web UI | `templates/index.html`, `/` route in `app.py` | The browser target under test |
| Agent definition | `.github/agents/ui-tester.md` | Repo-committed agent persona + conventions |
| E2E stack | `requirements-e2e.txt`, `tests/e2e/` | pytest-playwright specs + live-server fixture |
| CI | `.github/workflows/e2e.yml` | Runs headless E2E on push/PR |
| Cloud agent env | `.github/workflows/copilot-setup-steps.yml` | Preinstalls browsers for CCA |
| Board wiring | `.github/ISSUE_TEMPLATE/ui-test.yml` + `ui-test` label | Feeds UI-test work to CCA |

## Run the browser tests locally

```bash
pip install -r requirements-e2e.txt
playwright install chromium
pytest tests/e2e -v
```

The `tests/e2e/conftest.py` fixture boots the Flask app on a free port with a
temporary SQLite DB, so no separate server needs to be started.

## Give the agent a live browser (Playwright MCP)

The [Playwright MCP server](https://github.com/microsoft/playwright-mcp) lets an
agent actually drive a browser — navigate, snapshot the accessibility tree,
click, and generate/verify specs — instead of guessing selectors.

### Copilot CLI

Add the server to `~/.copilot/mcp-config.json`:

```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest", "--headless"]
    }
  }
}
```

Then invoke the agent with `copilot` and pick the `ui-tester` agent.

### Copilot coding agent (cloud)

In **Repository Settings → Copilot → Coding agent → MCP configuration**, paste:

```json
{
  "mcpServers": {
    "playwright": {
      "type": "local",
      "command": "npx",
      "args": ["-y", "@playwright/mcp@latest", "--headless"],
      "tools": ["*"]
    }
  }
}
```

Browsers are preinstalled for the cloud agent by
`.github/workflows/copilot-setup-steps.yml`.

## Wire it to the project board

1. Create the label (once):

   ```bash
   gh label create ui-test --color 1D76DB --description "Browser/E2E test work for the web UI"
   ```

2. Open an issue with the **UI Test Request** template (auto-labeled `ui-test`),
   add it to the [project board](https://github.com/orgs/CCA-DEMO/projects/1),
   and **assign it to Copilot**. CCA will pick it up and follow the conventions in
   `.github/agents/ui-tester.md` to add specs under `tests/e2e/`.
