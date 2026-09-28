# Lab 5 - Cross-Workflow Capstone

!!! note "Time: 135-145 min"
    Use a single business request to make the agent select and coordinate the correct skills, MCP tools, and the quality server.

## Start with no conversation context

Open a **new local Copilot Chat session** in VS Code with **Agent** mode selected. Do not tell the agent which tools to use.

!!! blank "Capstone prompt"
    <copy>Help me close out my most recent relevant meeting. First, list my recent meetings and let me choose one. Create a reviewed follow-up with decisions and evidence-supported action items. If meeting-quality data is available and shows a meaningful issue, also prepare an incident summary. Show me every draft before posting anything. Ask for approval before each side effect. Tell me which skill and data source you use at each stage.</copy>

## Observe the agent's plan

Before approving any tool call, confirm the agent:

1. Discovers a meeting using the Meetings MCP server.
2. Uses the `meeting-follow-up` skill for transcript analysis and recap generation.
3. Uses the `meeting-quality` skill and the quality MCP server only when quality analysis is requested and data is available.
4. Separates metadata from the official MCP servers from telemetry the quality server fetched over REST.
5. Shows drafts before creating spaces, messages, memberships, or meetings.
6. Requests approval for each side effect.

!!! curious "This is the real test"
    Everything up to now told the agent what to do. Here it must decide for itself which skills apply, in what order, and where the data comes from. That is the difference between a scripted demo and a workflow you could actually hand to a colleague.

## Introduce a change

After reviewing the first draft, change one requirement:

!!! blank "Steer the workflow"
    <copy>Revise the follow-up for an executive audience. Keep it under 200 words, retain the evidence-supported action items, and do not change the incident findings.</copy>

Confirm the agent updates presentation without changing source facts or bypassing approval.

## Complete and verify

Approve the final actions, then verify the results in the Webex desktop app:

- The follow-up space contains the approved recap.
- Any incident space contains evidence, hypotheses, recommended checks, and data gaps.
- No unsupported claim was posted.
- The agent did not expose tokens or credentials.

## Capstone checkpoint

- [x] The agent selected the appropriate skills and tools from a high-level request
- [x] MCP and quality-server data sources were clearly attributed
- [x] A mid-workflow requirement change was handled correctly
- [x] Every side effect required review and approval
- [x] The final Webex content matched the approved drafts
