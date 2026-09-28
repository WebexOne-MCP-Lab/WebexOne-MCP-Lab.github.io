# Lab 1 - Provision Webex MCP in Control Hub

!!! note "Time: 10-30 min"
    Enable the official Webex Meetings and Messaging MCP servers, apply governance controls, then generate the tokens that let VS Code connect to them.

## Section 1 - Enable the Agentic Apps

Sign in to Control Hub with your lab account:

| <!-- -->         | <!-- -->         |
| ---------------- | ---------------- |
| `URL`            | [https://admin.webex.com](https://admin.webex.com){:target="_blank"} |
| `Email`          | <copy><w class="WbxUser">See Lab Credentials</w></copy> |
| `Password`       | <copy><w class="WbxPW">See Lab Credentials</w></copy> |

!!! blank "Your credentials"
    All values for this lab live on the [Lab Credentials](reference/credentials.md) page.

### Enable the Webex Meeting app

1. Sign in to [admin.webex.com](https://admin.webex.com/){:target="_blank"} with the lab administrator account.
2. Open **Apps → Agentic Apps → Webex**.
3. Locate the **Webex Meeting** agentic app.
4. Open the app's **General** settings, select **Allowed for all users**, and click **Save** at the bottom right of the page.
5. Select the **Tools** tab.
6. Enable **all** Webex Meeting tools by toggling **Allow tool** on for each one, then click **Save**.

### Enable the Webex Messaging app

7. Go back to **Apps → Agentic Apps → Webex** and open the **Webex Messaging** agentic app.
8. Open **General** settings, select **Allowed for all users**, and click **Save**.
9. Select the **Tools** tab and enable only the following tools, then click **Save**:

    - Create Webex Message
    - Get Webex Messages
    - Create Webex Space
    - Get Webex Space
    - Add Webex Membership
    - Get Webex Membership
    - Search Webex Spaces
    - Create Webex Thread Reply
    - Get Webex Thread

10. **(Optional)** Click **Review** on any enabled tool to inspect its input schema, output schema, and annotations. This helps you understand what data the agent will send and receive when it invokes the tool later in the lab.

### Tool policy summary

| App | Policy |
| ---------------- | ---------------- |
| `Webex Meeting` | All 8 tools enabled |
| `Webex Messaging` | 9 of 26 tools enabled (see list above) |

!!! curious "Why not all Messaging tools?"
    The Messaging server has 26 tools. We enable only what the lab exercises use. Webhooks, file operations, and delete/update actions are not needed and stay disabled.

    This is the single strongest control you have: a tool that is not enabled here **cannot** be invoked, no matter what a prompt or skill file asks for.

## Section 2 - Configure VS Code and generate MCP tokens

In the lab workspace, sign in to GitHub Copilot Chat with the GitHub account assigned by the lab team. Set the chat **Session Target** to **Local**, select **Agent** mode, and choose the model designated for this lab. The Local target is required here because VS Code's secure `${input:...}` token prompts are not forwarded to the separate Copilot Agent Host.

### Add the MCP configuration

1. In VS Code, open the supplied lab workspace. Create or open `.vscode/mcp.json` at its root and add this configuration. Keep the `inputs` entries: VS Code will ask for the tokens when each server starts and store them securely.

    ```json
    {
      "inputs": [
        {
          "type": "promptString",
          "id": "webex-meeting-token",
          "description": "Webex Meeting Agentic App token",
          "password": true
        },
        {
          "type": "promptString",
          "id": "webex-messaging-token",
          "description": "Webex Messaging Agentic App token",
          "password": true
        }
      ],
      "servers": {
        "webex-meeting": {
          "type": "http",
          "url": "https://mcp.webexapis.com/mcp/webex-meeting",
          "headers": {
            "Authorization": "Bearer ${input:webex-meeting-token}"
          }
        },
        "webex-messaging": {
          "type": "http",
          "url": "https://mcp.webexapis.com/mcp/webex-messaging",
          "headers": {
            "Authorization": "Bearer ${input:webex-messaging-token}"
          }
        }
      }
    }
    ```

### Generate the tokens

2. Open [developer.webex.com](https://developer.webex.com/){:target="_blank"} and sign in with your lab credentials.
3. Click your **avatar** (top right) → **Webex Agentic App token**.
4. Under **Generate token**, click **Generate now**.
5. Select the **Webex Meeting** MCP server, give the token a name (for example `Lab Meeting Token`), and click **Create token**.
6. Copy the token; you will enter it in VS Code's hidden input prompt for `webex-meeting-token`.
7. Generate a second token for the **Webex Messaging** MCP server (for example `Lab Messaging Token`).
8. Copy the token for VS Code's hidden `webex-messaging-token` prompt.
9. Save `.vscode/mcp.json`. Open the Command Palette (`Ctrl+Shift+P`) and run **MCP: List Servers**. Start both Webex servers if needed. Enter each token when prompted, without the `Bearer` prefix.
10. Confirm both servers are running and their tools appear under **Configure Tools** in Copilot Chat. Select **Agent** mode and keep tool approvals enabled for the exercises.

!!! important "Treat these tokens as secrets"
    These tokens grant the agent access to Webex on your behalf. Never paste them into a chat prompt, a skill file, a screenshot, or a committed file. Enter them only in VS Code's hidden token prompts.

!!! curious "Why a URL and not a command?"
    These servers use `type: "http"` and a `url` because Cisco hosts them remotely; the transport is **Streamable HTTP**. In [Lab 4](lab4_quality.md) you will add a server addressed by `command` instead, which runs locally over **stdio**. See [MCP Transports](reference/mcp-transports.md) for why each is used.

## Checkpoint

You are ready for Lab 2 when:

- [x] Both official servers are allowed for your lab account
- [x] All Webex Meeting tools are enabled
- [x] The 9 required Webex Messaging tools are enabled
- [x] You have MCP tokens generated for both the Meeting and Messaging servers
- [x] Both servers are running in VS Code and their tools are enabled in Copilot Chat
- [x] You can explain which organization policy controls the tools exposed to the client

## Troubleshooting

| Problem | Solution |
| ---------------- | ---------------- |
| Agentic Apps is missing | Verify your administrator role and organization assignment |
| App is visible but tools are absent | Check capability-level tool settings and refresh the client |
| Authorization fails | Confirm you are in the allowed population and reauthorize |
| A tool disappeared after an update | Review schema changes and reauthorize the server/tool baseline |
| Server fails to start in VS Code | Run **MCP: List Servers** → **Show Output**; check the token entered in the hidden prompt and confirm the workspace is trusted |
