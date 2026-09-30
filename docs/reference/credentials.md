# Lab Accounts and Tokens

## Find your lab sign-in details

On the **wkst1** dCloud desktop, open **Session_Info.txt**. The file lists the credentials for this pod's Control Hub administrator and Webex App user. Use the account named for each step; the two sign-ins may be different. The Expo session ID identifies your pod if you need a proctor's help.

Keep this guide open in Chrome on your own computer, alongside the dCloud RDP tab. Do not enter passwords into this website or copy them into Copilot Chat.

| Where | Which account or token |
| --- | --- |
| Control Hub in Lab 1 | Control Hub account from `Session_Info.txt` |
| Webex App and developer.webex.com | Webex account from `Session_Info.txt` |
| Official Meetings and Messaging MCP servers | Separate Agentic App tokens generated in Lab 1 |
| Custom quality MCP server | Personal access token generated in Lab 4 |

## Tokens are different from passwords

The two Agentic App tokens authorize the official Webex MCP servers. The personal access token authorizes the local quality server to call the Webex Meeting Qualities REST API. Enter tokens only in the **hidden VS Code prompts** when starting the corresponding server. Do not paste them into Copilot Chat, **Session_Info.txt**, skill files, screenshots, or Webex messages. Do not assume the pod's files or clipboard are wiped when you disconnect.

If a token expires or a server fails to start, return to the token step in [Lab 1](../lab1_control_hub.md) or [Lab 4](../lab4_quality.md), then start that server again.
