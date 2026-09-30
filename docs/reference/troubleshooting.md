# Troubleshooting Matrix

!!! important
    If a fix here does not resolve your issue within a couple of minutes, raise your hand. A roaming proctor can unblock you faster than you can debug it alone.

| Symptom | Likely cause | Mitigation |
|---|---|---|
| MCP server is not visible | Control Hub policy, wrong org, or stale client session | Verify organization, Agentic App policy, and reconnect |
| Tool call requests unexpected authorization | Tool requires an additional OAuth scope | Review the tool schema and approve only the required scope |
| Transcript not found | Processing delay, missing transcript, wrong meeting, or insufficient access | Confirm meeting ID, wait for processing, verify permissions |
| Agent sees only the user's meetings | MCP authorization is user-scoped | Use an approved admin/service integration for broader operational use |
| Quality data is empty | Data availability delay, unsupported meeting, wrong ID, or missing scope | Confirm the endpoint contract, wait for data, show a data-gap message |
| Quality API returns 403 | Caller lacks authorization for meeting-quality data | Use the approved integration and least-privilege reporting scope |
| Quality API returns 429 | Rate limit | Back off, cache read results, reduce parallel calls |
| Scheduled meeting time is wrong | Relative or timezone-ambiguous transcript language | Require explicit timezone, date, time, duration, and invitees |
| Duplicate space or message | Agent retry or repeated prompt | Use idempotency keys or search-before-create where supported |
| Webex Markdown looks wrong | Unsupported Markdown or line-break encoding | Use supported Markdown only and verify by reading the message back |
| File upload fails | Size/type restriction, scanning delay, or private URL | Use approved file types, keep files small, and handle retry |
| Agent posts without approval | Approval state is not enforced in the workflow | Make approval a mandatory state transition |
| Agent repeatedly compacts or loses the task | Context window is crowded by conversation history, tool schemas, or files | Start a new Agent chat for a new task, or use `/compact` and then type `continue` for the current task; preserve important facts in your next prompt |
| Copilot reports "model provider reported a failed response" without details | The model request failed; this message alone does not identify whether the cause was a rate limit or another provider issue | Note the Client Request Id, wait briefly, and retry a read once in a fresh Local Agent chat. If a Webex write may already have run, check Webex before retrying. Ask a proctor if it recurs |
| OpenAI `rate_limit_exceeded` (429) | Organization or project token/request burst | Wait at least the returned `Retry-After`, then retry once. If a write tool may already have succeeded, inspect Webex before repeating it; ask a proctor if the limit recurs |
| Direct paste from your local Chrome tab into the RDP desktop does not work | Browser clipboard permission, focus, or Guacamole clipboard synchronization | Use the Guacamole clipboard panel (`Ctrl+Alt+Shift`; on a Mac, `Ctrl+Option+Shift`) to paste text into the remote clipboard, then paste into the Windows app. Ask a proctor if it still fails |
| Attendance report overclaims engagement | Attendance data treated as participation | Label only source-supported facts; omit unsupported claims |
