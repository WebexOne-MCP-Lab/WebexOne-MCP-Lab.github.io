# Lab 2 - Connect the AI Client and Discover Tools

!!! note "Time: 30-55 min"
    Inspect the connected MCP tools, discover their capabilities, and test them hands-on.

## Section 1 - Verify your connection

1. Open the supplied lab workspace in Kiro.
2. Confirm both MCP servers show a green connected status in the **MCP Servers** panel (configured in Lab 1).

## Section 2 - Discover tools

3. Ask the agent to **list all available tools** without executing any write action.
4. Inspect the schemas for these key tools:

    - `webex-list-meetings`
    - `webex-list-transcripts`
    - `webex-get-meeting-summary`
    - `webex-create-space`
    - `webex-create-message`
    - `webex-create-meeting`

5. Ask the agent to explain which tools are **read-only** and which have **side effects**.

!!! blank "Try this prompt"
    <copy>Show me the Webex Meetings and Messaging tools currently available. Group them by read-only and write/side-effecting behavior. Do not invoke any write tool. For each tool, show the required inputs and explain what data it can access.</copy>

## Section 3 - Tool-selection challenge

Before running each request below, predict which MCP server and tool the agent should use. Then run the request and compare your prediction with the actual tool call Kiro displays.

| Request | Your predicted server/tool |
| ---------------- | ---------------- |
| Show my recent meetings | `____________________________` |
| Find spaces with "MCP" in the title | `____________________________` |
| Create a new Webex space | `____________________________` |

For each request, answer:

- Did the agent choose the tool you expected?
- What required inputs did the tool need?
- Was the operation read-only or side-effecting?
- Did Kiro request approval?

!!! curious "Why this matters"
    Agents choose tools based on their names, descriptions, and schemas. Understanding that decision helps you diagnose incorrect tool selection and design better prompts.

## Section 4 - Warm-up: test your tools

Now that you know what tools are available, try them out and watch the results in real time.

### Preparation

6. Open the **Webex** desktop application on your lab workstation and sign in with your lab credentials. Keep it visible alongside Kiro so you can watch changes happen in real time.

!!! important "Tool approval"
    When the agent tries to invoke a tool, Kiro will prompt you to approve the action before it executes. This is expected - review what the tool will do and click **Allow** to proceed. This is the human-in-the-loop safety model in action.

### Try these tasks

Ask the agent to do each of the following. Watch the results appear in the Webex desktop app as the agent executes each tool.

7. **Create a space** - Ask the agent to create a Webex space with a fun name (for example `MCP Launch Pad` or `My First MCP Space`).
8. **Post a message** - Ask the agent to post a message in the new space (for example "Hello from MCP! This message was sent by an AI agent."). Switch to Webex and confirm the message appears.
9. **Add a member** - Ask the agent to add a lab partner or a second lab account to the space. Watch the membership notification appear in Webex.
10. **List your meetings** - Ask the agent to list your recent meetings. Confirm it returns meeting data from the Meetings MCP server.

!!! webex "What you should see"
    By the end of the warm-up you should have a Webex space with a message in it, visible in the Webex desktop app. This confirms both MCP servers are working and the agent can read and write data on your behalf.

## Section 5 - Approval experiment

Compare how Kiro handles a read operation and a write operation:

1. Ask the agent to list your Webex spaces. Review the tool call and approval behavior.
2. Ask the agent to post a second message in your warm-up space.
3. When Kiro asks for approval, choose **Reject**.
4. Confirm no message appeared in Webex.
5. Revise the message, run the request again, review the exact tool inputs, and approve it.
6. Confirm only the approved message appears.

!!! blank "Try this prompt after rejecting the first message"
    <copy>Post this revised message in my MCP warm-up space: "I reviewed and approved this message before the agent posted it."</copy>

!!! important
    This demonstrates that tool availability does not equal permission to act. The human still controls side effects.

## Section 6 - Find the lab meeting

11. Invoke `webex-list-meetings` with a narrow topic filter such as `LAB-FOLLOWUP`.
12. Confirm the seeded lab meeting appears in the results.

!!! note
    The agent should resolve the meeting ID from the API. It should never guess an ID from a meeting title.

## Checkpoint

You are ready for Lab 3 when:

- [x] Both MCP servers are connected (green status in Kiro)
- [x] You can list and describe the available MCP tools
- [x] You created a Webex space and posted a message using the agent
- [x] You can see the space and message in the Webex desktop app
- [x] You predicted and verified which tools the agent selected
- [x] You rejected, revised, and approved a write operation
- [x] You confirmed the seeded follow-up meeting appears in the results
