# Lab 4 - Build the Meeting Quality Assistant

!!! note "Time: 95-135 min"
    Connect a custom MCP server that wraps the Webex Meeting Qualities REST API, use it to troubleshoot a real meeting, then package the workflow into a reusable skill file.

!!! important "Architecture note"
    The official Webex Meetings MCP server provides meeting lifecycle and intelligence tools, but it does **not** expose media-quality telemetry. Quality data comes from a separate REST API.

    In this lab that API is wrapped by a **custom MCP server the lab provides** ([`quality-tool/server.py`]({{config.extra.quality_tool_url}}){:target="_blank"}). Your agent speaks MCP to it, and it speaks REST to Webex on your behalf. This is the pattern you will use whenever an agent needs data from a non-MCP source. See [MCP vs. REST API](reference/mcp-vs-rest.md).

---

## Phase 1 - Set up the quality MCP server

### 4.1 Generate a personal access token

The Meeting Qualities API requires the `analytics:read_all` scope and an org admin account. The simplest way to get a token with this scope is a personal access token.

1. Go to [developer.webex.com](https://developer.webex.com/){:target="_blank"} and sign in with your lab credentials.
2. Click your **avatar** → **My Personal Access Token**.
3. Copy the token. It is valid for 12 hours and includes all scopes for your account.

!!! important "Personal access tokens"
    Personal access tokens grant full access to your account. In production you would use a scoped OAuth integration instead. This is a lab shortcut. Never commit a token to version control.

### 4.2 Configure and start the server

4. In your lab workspace, open the `quality-tool/` folder.
5. Copy `.env.example` to `.env` and paste your token:

    ```text
    WEBEX_DEVELOPER_TOKEN=paste_your_token_here
    ```

6. Install dependencies and confirm the server runs:

    ```bash
    cd quality-tool
    uv sync
    uv run server.py
    ```

7. Add the server inside the `servers` object of your workspace's `.vscode/mcp.json`, alongside the two official servers. On the lab's Windows desktop, `${workspaceFolder}` resolves to the open workspace:

    ```json
    "webex-meeting-qualities": {
      "type": "stdio",
      "command": "uv",
      "args": ["run", "--directory", "${workspaceFolder}/quality-tool", "server.py"]
    }
    ```

8. Save the file, run **MCP: List Servers**, and start `webex-meeting-qualities`. Confirm it is running and `get_meeting_qualities` appears under **Configure Tools** in Copilot Chat.

!!! curious "Where does the token live?"
    Only in `quality-tool/.env`, on the machine running the server. The agent never sees it, the model never sees it, and it is never sent in a prompt. That isolation is the main reason to wrap a REST API in an MCP server rather than letting the agent call it directly.

!!! curious "Notice the different transport"
    Unlike the Webex servers, this one has no `url` - VS Code launches it as a local subprocess over **stdio**. The token stays in the local `.env` file and is not sent to an MCP endpoint. The server still sends it to the Webex Analytics API over HTTPS when it calls that API. See [MCP Transports](reference/mcp-transports.md).

### 4.3 Know the API's limits

The server inherits the constraints of the underlying API. These matter during the exercise:

| Constraint | Value |
| ---------------- | ---------------- |
| `Data availability` | Roughly 10 minutes after a meeting starts |
| `Retention` | 7 days |
| `Rate limit` | 1 request per 5 minutes per meeting instance ID |
| `Required scope` | `analytics:read_all` |
| `Required role` | Org admin, with Pro Pack licensing |

!!! important
    Because of the rate limit, do **not** let the agent retry a failed call in a loop. One call, then read the error.

---

## Phase 2 - Interactive quality troubleshooting

### 4.4 Find the target meeting

!!! blank "Prompt the agent"
    <copy>Find a meeting with "LAB-QUALITY" in the title. Show me the title, date, and participants.</copy>

- Confirm the agent found the correct seeded quality meeting.

### 4.5 Get quality data

!!! blank "Prompt the agent"
    <copy>Call get_meeting_qualities for that meeting. Show me the quality metrics for each participant, and tell me which tool returned the meeting info versus the quality data.</copy>

- The agent should resolve the meeting ID from the Meetings MCP server, then pass it to `get_meeting_qualities`.
- Confirm it returns per-participant quality data.

!!! curious "Read the data_gaps field"
    The server returns an explicit `data_gaps` list. Webex reports some metrics as empty arrays and others as `-1` placeholders meaning "not measured." The server flags both so the agent cannot mistake a missing measurement for a real value of zero.

### 4.6 Analyze the data

!!! blank "Prompt the agent"
    <copy>Analyze the quality data. Identify: which participants were affected by poor quality; when the degradation started and ended; which metrics were impacted (latency, jitter, packet loss); what direction (send/receive) and media type (audio/video/share). Separate your observations (what the data shows) from your hypotheses (what might have caused it). Include a confidence level for each conclusion. Note any data gaps.</copy>

- Does the output clearly separate facts from guesses?
- Are confidence levels reasonable?
- Does it acknowledge missing or incomplete data?

### 4.7 Generate recommended checks

!!! blank "Prompt the agent"
    <copy>Based on your analysis, generate a list of recommended troubleshooting checks. Consider: client network, Wi-Fi, VPN, firewall, bandwidth, and endpoint issues. Link each recommendation back to a specific data observation.</copy>

- Good recommendations are grounded in the data, not generic checklists.

### 4.8 Evidence classification challenge

Classify each statement as an **observation**, **hypothesis**, or **unsupported claim** before asking the agent:

1. "Participant A had 12% packet loss between 10:14 and 10:18."
2. "Participant A's Wi-Fi caused the packet loss."
3. "The meeting server was overloaded."
4. "Participant B's audio receive stream had higher jitter than their audio send stream."

!!! blank "Prompt the agent"
    <copy>Classify these four statements as observation, hypothesis, or unsupported claim. Cite the quality data fields that support each classification. If the data does not support a statement, say so clearly.</copy>

Compare the agent's answer with yours. Revise any conclusion that is presented with more certainty than the evidence supports.

### 4.9 Practice failure handling

Test the server with an invalid meeting ID:

!!! blank "Prompt the agent"
    <copy>Call get_meeting_qualities with meetingId INVALID-LAB-MEETING-ID. Do not retry repeatedly. Explain the response and tell me what I should verify next.</copy>

The agent should:

- Report the failure instead of inventing quality data.
- Distinguish authentication failures (`401`/`403`) from missing or invalid meeting data (`404`).
- Avoid repeated calls because the API is rate-limited.
- Recommend checking the meeting instance ID, token validity, admin role, Pro Pack licensing, and the data-availability window.

!!! curious "The server never raises"
    `get_meeting_qualities` always returns the same shape with an `error` string set, rather than throwing. That gives the agent something structured to reason about instead of a stack trace.

### 4.10 Review the incident summary

!!! blank "Prompt the agent"
    <copy>Draft a complete incident summary I can share with my network team. Include: meeting title and date; affected participants; timeline of degradation; key metrics with values; observations vs. hypotheses; recommended checks; data gaps; and which data came from MCP versus the quality server. Formatting rules for the Webex message: Do NOT use markdown tables, Webex does not render them properly. Use bullet lists and bold labels instead. Use headings to separate sections. Show me the draft - do not post it yet.</copy>

- Review the draft. Would you send this to your network team?
- Ask for edits if needed.

### 4.11 Create an Incident Mode space

!!! blank "Prompt the agent"
    <copy>The summary looks good. Create a Webex space called "INCIDENT — [meeting title] — [date]" and post the incident summary.</copy>

- The agent should ask for your approval before creating the space.
- Approve, then switch to Webex to confirm the space and message.

!!! important "Privacy"
    Do not expose full participant quality records to a broad space by default. Use aggregated findings and a restricted responder space unless your organization explicitly permits detailed sharing.

### 4.12 Post a follow-up update

!!! blank "Prompt the agent"
    <copy>Post a reply in the incident space: "Checking VPN split-tunnel configuration for affected participants. Will report back with findings."</copy>

- Confirm the reply appears as a thread reply in Webex, not a new top-level message.

---

## Phase 3 - Complete the skill

### 4.13 Build the skill file

!!! blank "Prompt the agent"
    <copy>Create a VS Code Agent Skill at `.github/skills/meeting-quality/SKILL.md` with YAML frontmatter (`name: meeting-quality` and a description of when to use it). Capture the troubleshooting workflow we just completed: find a meeting via the Meetings MCP server; call get_meeting_qualities; analyze metrics (separate observations from hypotheses); respect data_gaps and never treat an unmeasured value as zero; generate data-linked troubleshooting checks; draft an incident summary (no markdown tables, always attribute data sources); create an Incident Mode space (with approval); post updates as thread replies; and handle authentication, invalid meeting IDs, empty data, and rate limits without fabricating results. Require human approval before creating spaces or posting messages.</copy>

- Review the generated skill file. Does it capture everything?

### 4.14 Test the skill on a new meeting

Start a **new local Copilot Chat session** in VS Code so the agent has no prior context. Confirm the skill appears under **Configure Skills**.

!!! blank "Prompt the agent (new session)"
    <copy>Run the meeting-quality skill. List my recent meetings and let me pick which one to troubleshoot.</copy>

- Pick a different meeting if available.
- Walk through the approval steps as prompted.
- Confirm the incident space and summary are created successfully.

!!! webex "What this proves"
    You extended the agent with a capability MCP does not cover, kept the credential server-side, and packaged the full workflow into a reusable artifact. This is the same pattern for integrating any API into an agent workflow.

---

## Checkpoint

You are ready for Lab 5 when:

- [x] The custom quality MCP server is running in VS Code and its tool is enabled in Copilot Chat
- [x] The agent retrieved and analyzed quality data for a meeting
- [x] Observations were separated from hypotheses with confidence levels
- [x] Unsupported claims were identified and removed
- [x] The server handled an invalid request without the agent fabricating data
- [x] The agent clearly attributed metadata to MCP and telemetry to the quality server
- [x] An incident space was created only after your approval
- [x] The complete workflow was captured in a reusable skill file
- [x] The skill was tested in a fresh session
