# Lab 5 - Cross-Workflow Capstone

!!! note "Time: 105-115 min"
    Use a single business request to make the agent select and coordinate the correct skills, MCP tools, and the quality server.

## Start with no conversation context

Open a **new local Copilot Chat session** in VS Code with **Agent** mode selected. Do not tell the agent which tools to use.

!!! blank "Capstone prompt"
    <copy>Help me close out "Wayfinder Mission - New Images Review" from September 29 to October 7, 2026. Find the meeting by its exact title across UTC date windows and all meeting states. Use its transcript to draft a follow-up with evidence-supported decisions and actions, and its meeting-quality data to prepare an incident update for the observed media issue. Follow my workspace skill customizations and propose a name for the follow-up space. Use the existing incident space from Lab 4 if you find it; do not create a duplicate. Show every draft and exact recipient before a write. Ask for approval before each side effect. Tell me which skill instruction shaped each draft and which MCP tool or quality API supplied its evidence.</copy>

## Observe the agent's plan

Before approving any tool call, confirm the agent:

1. Discovers a meeting using the Meetings MCP server.
2. Uses the `meeting-follow-up` skill for transcript analysis and recap generation.
3. Uses the `meeting-quality` skill and the quality MCP server only when quality analysis is requested and data is available.
4. Separates metadata from the official MCP servers from telemetry the quality server fetched over REST.
5. Shows drafts before creating or reusing spaces, posting messages, adding members, or scheduling meetings.
6. Requests approval for each side effect.

After the drafts appear, compare them with your saved skill edits. Look for the Lab 3 follow-up space name and the Lab 4 explanation of why each troubleshooting check would help. The agent saying it used a skill is not enough: the behavior you added should be visible in its proposal or draft. If either change is missing, ask the agent to read the edited skill file and revise its response before approving a write.

!!! curious "This is the real test"
    Everything up to now told the agent what to do. Here it must decide for itself which skills apply, in what order, and where the data comes from. That is the difference between a scripted demo and a workflow you could actually hand to a colleague.

## Introduce a change

After reviewing the first draft, change one requirement:

!!! blank "Steer the workflow"
    <copy>Revise the follow-up for an executive audience. Keep it under 200 words, retain the evidence-supported action items, and do not change the incident findings.</copy>

Confirm the agent updates presentation without changing source facts or bypassing approval.

## Complete and verify if time allows

If time remains, approve the final actions and verify the results in Webex App. Otherwise, stop after reviewing the drafts and proposed tool calls; do not rush a write approval. If the quality API enforces its five-minute per-meeting limit after Lab 4, let that window pass before one fresh call; do not loop retries or pretend an old summary is fresh telemetry:

- The follow-up space contains the approved recap.
- The existing incident space contains the approved update, or a newly approved incident space contains evidence, hypotheses, recommended checks, and data gaps.
- No unsupported claim was posted.
- The agent did not expose tokens or credentials.

## Capstone checkpoint

- [x] The agent selected the appropriate skills and tools from a high-level request
- [x] Your follow-up space-naming rule and troubleshooting rule were visible in the proposal and drafts
- [x] MCP and quality-server data sources were clearly attributed
- [x] A mid-workflow requirement change was handled correctly
- [x] Every side effect required review and approval
- [x] If you posted content, it matched the approved drafts
