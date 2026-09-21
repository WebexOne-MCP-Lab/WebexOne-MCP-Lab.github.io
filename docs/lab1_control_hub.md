# Lab 1 - Provision Webex MCP in Control Hub

!!! note "Time: 10-30 min"
    Enable the official Webex Meetings and Messaging MCP servers, apply governance controls, then generate the tokens that let Kiro connect to them.

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

## Section 2 - Configure Kiro and generate MCP tokens

To connect the AI client to the Webex MCP servers, first set up the MCP configuration in Kiro, then generate tokens and paste them in.

### Add the MCP configuration

1. In Kiro, open the MCP configuration file (`.kiro/settings/mcp.json`) and replace its contents with the following template:

    ```json
    {
      "mcpServers": {
        "webex-meeting": {
          "url": "https://mcp.webexapis.com/mcp/webex-meeting",
          "headers": {
            "Authorization": "Bearer <YOUR_MEETING_TOKEN>"
          }
        },
        "webex-messaging": {
          "url": "https://mcp.webexapis.com/mcp/webex-messaging",
          "headers": {
            "Authorization": "Bearer <YOUR_MESSAGING_TOKEN>"
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
6. Copy the token and paste it into the `webex-meeting` Authorization header in `mcp.json`.
7. Generate a second token for the **Webex Messaging** MCP server (for example `Lab Messaging Token`).
8. Copy the token and paste it into the `webex-messaging` Authorization header in `mcp.json`.
9. Save the file. Kiro will automatically connect to both MCP servers.
10. Open the Command Palette (`Cmd+Shift+P`) and search for **Kiro: Focus on MCP Servers View**. Select it to open the MCP Servers panel in the bottom left of Kiro. Confirm both servers show a green connected status.

!!! important "Treat these tokens as secrets"
    These tokens grant the agent access to Webex on your behalf. Never paste them into a chat prompt, a skill file, a screenshot, or a commit. They belong only in `mcp.json`.

!!! curious "Why a URL and not a command?"
    These servers are addressed by `url` because Cisco hosts them remotely - the transport is **Streamable HTTP**. In [Lab 4](lab4_quality.md) you will add a server addressed by `command` instead, which runs locally over **stdio**. See [MCP Transports](reference/mcp-transports.md) for why each is used.

## Checkpoint

You are ready for Lab 2 when:

- [x] Both official servers are allowed for your lab account
- [x] All Webex Meeting tools are enabled
- [x] The 9 required Webex Messaging tools are enabled
- [x] You have MCP tokens generated for both the Meeting and Messaging servers
- [x] Both servers show green connected status in Kiro's MCP Servers panel
- [x] You can explain which organization policy controls the tools exposed to the client

## Troubleshooting

| Problem | Solution |
| ---------------- | ---------------- |
| Agentic Apps is missing | Verify your administrator role and organization assignment |
| App is visible but tools are absent | Check capability-level tool settings and refresh the client |
| Authorization fails | Confirm you are in the allowed population and reauthorize |
| A tool disappeared after an update | Review schema changes and reauthorize the server/tool baseline |
| Server shows red/disconnected in Kiro | Re-check the token was pasted in full, with no trailing spaces, and that the file is saved |
