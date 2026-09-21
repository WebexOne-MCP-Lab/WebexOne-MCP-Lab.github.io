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
| LLM rate limit reached | Shared token or burst traffic | Use smaller prompts, stagger calls, use backup tokens |
| Attendance report overclaims engagement | Attendance data treated as participation | Label only source-supported facts; omit unsupported claims |
