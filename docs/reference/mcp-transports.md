# MCP Transports: stdio vs. Streamable HTTP

By the end of this lab you have three MCP servers connected — and they do **not** all talk to Kiro the same way. Two use Streamable HTTP, one uses stdio. This page explains the difference and why each was chosen.

## What you configured

Look back at your `.kiro/settings/mcp.json`. The two official Webex servers are addressed by **URL**:

```json
"webex-meeting": {
  "url": "https://mcp.webexapis.com/mcp/webex-meeting",
  "headers": { "Authorization": "Bearer <token>" }
}
```

The custom quality server is addressed by **command**:

```json
"webex-meeting-qualities": {
  "command": "uv",
  "args": ["run", "--directory", "/path/to/quality-tool", "server.py"]
}
```

That difference — `url` vs. `command` — is the transport.

## How each one works

=== "stdio"

    > Kiro **launches the server as a child process** on your machine.
    >
    > Messages travel as JSON-RPC over the process's standard input and standard output. There is no network, no port, and no URL.
    >
    > When you close Kiro, the server process exits with it.

=== "Streamable HTTP"

    > The server is **already running somewhere else**, reachable at an HTTPS endpoint.
    >
    > Kiro sends JSON-RPC requests as HTTP POSTs. The server can stream responses back over the same connection when a result arrives incrementally.
    >
    > The server's lifecycle is completely independent of your editor.

## Side-by-side

| | stdio | Streamable HTTP |
| ---------------- | ---------------- | ---------------- |
| **Addressed by** | `command` + `args` | `url` |
| **Where it runs** | Your machine, as a subprocess | A server, anywhere |
| **Who starts it** | The MCP client (Kiro) | Operated independently |
| **Network exposure** | None | Requires a reachable HTTPS endpoint |
| **Authentication** | Inherits your local user; no auth layer needed | Must authenticate every caller (here, a bearer token) |
| **Secrets live in** | A local file the server reads (`.env`) | Request headers, plus server-side config |
| **Serves** | Exactly one user | Many users concurrently |
| **Setup cost** | Install dependencies, done | Hosting, TLS, auth, monitoring, scaling |
| **Good for** | Local tools, developer utilities, prototypes | Shared services, centrally governed capabilities |

## Why stdio for the quality server

The quality server is a small script wrapping one REST endpoint. stdio was the right fit here for four reasons:

1. **The credential never crosses a network.** `WEBEX_DEVELOPER_TOKEN` is read from `quality-tool/.env` by a process running on your own machine. There is no endpoint for anyone else to call, so there is nothing to authenticate and no token to transmit.
2. **No infrastructure.** `uv run server.py` is the entire deployment. No host, no TLS certificate, no reverse proxy, no uptime concern.
3. **Lifecycle is free.** Kiro starts the server when you open the workspace and stops it when you quit. Nothing is left running.
4. **It is single-user by nature.** Your token, your meetings, your pod. There is no case where a second person should call *your* instance.

!!! curious "The tradeoff you accepted"
    Every attendee runs their own copy. There is no central place to update the code, revoke access, or audit usage. For a lab — and for a personal developer tool — that is fine. For a capability your whole org depends on, it is not.

## Why Streamable HTTP for the Webex servers

The official servers are the mirror image:

1. **Cisco runs them, not you.** You could not launch them as a subprocess even if you wanted to; the code is not yours.
2. **They serve an entire organization.** One deployment, thousands of callers, each needing separate identity and authorization.
3. **Control Hub governs them centrally.** Tool-level policy applies to every user at once. That only works if there is one shared server enforcing it.
4. **Access must be revocable.** Your bearer token can be invalidated centrally without touching your machine.

## Choosing for your own servers

| If your server... | Use |
| ---------------- | ---------------- |
| Runs a local tool, script, or file operation | `stdio` |
| Holds a credential that belongs to one person | `stdio` |
| Is a prototype you are iterating on | `stdio` |
| Must be shared across a team or org | `Streamable HTTP` |
| Needs central policy, audit, or revocation | `Streamable HTTP` |
| Wraps a service that is already centrally hosted | `Streamable HTTP` |

!!! important "Moving from stdio to HTTP is not just a config change"
    If you promoted this lab's quality server to Streamable HTTP for your organization, the token isolation argument above **inverts**. The server would then hold a credential on behalf of many callers, so you would need to authenticate each caller, authorize which meetings they may query, and audit every request — none of which stdio required. Plan for that work before you make the switch.

!!! note "A note on SSE"
    Older MCP material refers to an "HTTP + SSE" transport. It has been superseded by Streamable HTTP, which folds streaming into a single endpoint. Prefer Streamable HTTP for new remote servers. See the [MCP specification](https://modelcontextprotocol.io/docs/2026-07-28/getting-started/intro){:target="_blank"}.
