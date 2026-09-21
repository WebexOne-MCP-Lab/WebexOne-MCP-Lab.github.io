# Known Caveats

!!! important
    Read this page before applying anything from this lab to a production organization.

## MCP capability and authorization

- MCP exposes the tools selected by Control Hub policy — not every possible Webex API.
- Tool visibility and data access can remain user-scoped even when the user is an administrator.
- OAuth scopes may be requested during authorization or tool invocation.

**Mitigation:** Use seeded data owned by the participant account, preflight every tool, and ask the facilitator for help with access failures.

## Meeting-quality data

- Quality telemetry is **outside** the official Meetings MCP tool set used in this lab.
- Quality data may be delayed, unavailable for some meeting types, aggregated, or limited by authorization.
- The quality endpoint may change fields, scopes, or availability rules.

**Mitigation:** The lab provides a versioned quality tool. If the live API is unavailable, your facilitator will switch to a live demo walkthrough for that step rather than skipping the concept.

## Scheduling

- A meeting request in a transcript may not specify a usable date, time, timezone, duration, or attendee list.
- The Meetings MCP server can schedule a meeting but should not be treated as a full calendar-availability engine.

**Mitigation:** Require explicit scheduling data and approval; otherwise ask the participant to supply it.

## Human approval

- A prompt that says "ask for approval" is not sufficient if the model can continue calling tools.
- Approval must be represented as a real workflow state and checked immediately before each side effect.

**Mitigation:** Gate every write operation, show an exact preview, expire approvals, and record the decision.

## Translation and sensitive content

- Translation can change meaning, names, dates, or technical terms.
- Transcripts can contain sensitive data that should not be sent to an external model or posted to a broad space.

**Mitigation:** Redact first, preserve source text, show language and confidence, and require approval for every translated publication.

## Attendance and participation

- Attendance is not the same as attention, contribution, or comprehension.
- Participant data may be subject to privacy, retention, and regional requirements.

**Mitigation:** Use neutral labels, minimize fields, restrict report recipients, and include a retention/deletion policy.
