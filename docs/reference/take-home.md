# Take-Home Bundle

## What you receive

At the end of the lab you take home a sanitized bundle containing:

| Deliverable | Description |
| ---------------- | ---------------- |
| `Skill files` | The `skills/` directory with all SKILL.md files and references - your customized versions |
| `Controlled prompt` | A read-only copy of `controlled-agent-prompt.md` for reference |
| `MCP client config template` | VS Code `.vscode/mcp.json` server entries for all three MCP servers, with token prompts instead of embedded secrets |
| **`Custom MCP server source`** | The complete `quality-tool/` project - `server.py`, `pyproject.toml`, and `.env.example`. Yours to run, modify, and extend |
| `Sample output schemas` | JSON structures for follow-up, quality, and attendance outputs |
| `Caveat sheet` | Authorization, quality-data availability, scheduling, privacy, and rate limits |
| `Cleanup checklist` | Steps for cleaning up your own test environment |
| `README` | Skill loading, allowed edits, versioning, and rollback |

!!! important "The quality server is working code, not just a contract"
    You take home the actual [FastMCP](https://gofastmcp.com/getting-started/welcome){:target="_blank"} server - a single readable `server.py` of roughly 180 lines. It is the reference pattern for wrapping *any* REST API as an MCP tool, not just meeting qualities.

## What you need to provide

The bundle is portable, but to use it in your environment you must supply:

- Your own Webex organization
- A Webex developer token for the quality server, plus authorization for the official MCP servers
- GitHub Copilot access (or another supported agent and model) in VS Code
- A host to run the custom Meeting Qualities MCP server (a laptop is fine to start)

## What is NOT included

!!! important
    Nothing from the lab environment leaves with you.

- Lab tokens or credentials
- Seeded meeting data, transcripts, or quality telemetry
- Organization IDs from the lab environment
- Screenshots containing tokens or personal data
- Internal lab team notes

## Getting started after the lab

1. **Set up your Webex org** - enable Agentic Apps in Control Hub.
2. **Run the quality MCP server** - `cd quality-tool && uv sync`, set `WEBEX_DEVELOPER_TOKEN` in `.env`, then `uv run server.py`.
3. **Configure VS Code** - put the MCP template in `.vscode/mcp.json`, start the servers, and enter your own tokens when prompted.
4. **Load the skills** - copy each skill directory from `skills/` into your workspace's `.github/skills/` directory; place the reviewed lab instructions in `.github/copilot-instructions.md`. Verify discovery in Copilot Chat before testing.
5. **Customize** - modify skill files to match your organization's terminology, thresholds, and workflow.
6. **Test** - run both workflows in a non-production environment first.

!!! important "Change management"
    Skills can be customized freely. The controlled prompt is safety-critical - store it in a controlled repository and review changes through your normal change-management process.

## Support

If you have questions after the lab, contact the lab team using the information provided during the event.
