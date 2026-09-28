# Overview

## What you will build

In this lab you will configure a Webex organization, connect an AI client to the official Webex MCP servers, and build two practical workflows.

!!! webex "1 - Meeting follow-up assistant"
    - Find a completed meeting and retrieve its transcript or summary.
    - Extract decisions and action items with supporting evidence.
    - Request human approval before creating spaces or posting messages.
    - Create a follow-up Webex space with a structured recap.
    - Optionally translate the output and generate an attendance report.

!!! webex "2 - Meeting quality troubleshooting assistant"
    - Find a target meeting through the official Meetings MCP server.
    - Call a **custom MCP server** that wraps the Webex Meeting Qualities REST API.
    - Identify affected participants and degradation windows.
    - Generate an incident summary and recommended checks.
    - Enter **Incident Mode** - a dedicated coordination space created only after approval.

You will package both workflows into reusable skill files, then coordinate them from a single business request in the capstone.

## Learning Objectives

By the end of this lab, you will be able to:

- Explain the difference between an MCP server, an MCP client, a tool, and a REST API.
- Enable and govern official Webex Agentic Apps in Control Hub.
- Connect an AI client to Webex Meetings and Messaging MCP servers.
- Discover tools and inspect their required inputs and outputs.
- Use meeting and messaging tools safely with least privilege and human approval.
- Extend an agent with a custom MCP server backed by a Webex REST API.
- Customize agent skill files to match your organization's workflow.
- Coordinate multiple skills, MCP tools, and a REST API from one business request.

## Disclaimer

Although the lab design and configuration examples could be used as a reference, for design related questions for your production enrionments please contact your representative at Cisco, or a Cisco partner.

The Webex MCP servers, tool names, OAuth scopes, and client behavior shown in this guide reflect the versions validated for this event. Revalidate against the current Webex documentation before applying anything here to your own organization.

## Lab Access

Your pod is a self-contained Cisco dCloud Windows desktop with Webex App, a browser, and Visual Studio Code with GitHub Copilot Chat preconfigured. You do not need to install software; you will generate Webex tokens during the lab.

From your workstation, open an RDP (Remote Desktop) session to the host named **wkst1** using the values provided by your proctor.

<div class="grid" markdown>

<form id="info">
<label for="info">Enter the values provided by your proctor</label><br>

  <label for="PodIP">Workstation IP:</label>
  <input type="text" id="PodIP" name="PodIP"><br>

  <label for="PodUser">Windows Username:</label>
  <input type="text" id="PodUser" name="PodUser"><br>

  <label for="PodPW">Windows Password:</label>
  <input type="text" id="PodPW" name="PodPW"><br>

  <label for="WbxUser">Webex Lab User:</label>
  <input type="text" id="WbxUser" name="WbxUser"><br>

  <label for="WbxPW">Webex Password:</label>
  <input type="text" id="WbxPW" name="WbxPW"><br>

  <label for="Pod">Pod ID:</label>
  <input type="text" id="Pod" name="Pod"><br>
  <br>
  <button onclick="setValues()">Update Lab Guide</button>
</form>

> Workstation IP: <copy><w class="PodIP">Provided by proctor</w></copy>
>
> Windows Username: <copy><w class="PodUser">Provided by proctor</w></copy>
>
> Windows Password: <copy><w class="PodPW">Provided by proctor</w></copy>
>
> Webex Lab User: <copy><w class="WbxUser">Provided by proctor</w></copy>
>
> Webex Password: <copy><w class="WbxPW">Provided by proctor</w></copy>
>
> Pod ID: <copy><w class="Pod">Provided by proctor</w></copy>

</div>

!!! important
    The values you enter above are stored only in your own browser session and are used to personalize the instructions throughout this guide. They are never sent anywhere.

## Getting Started

### What you need

- [x] A Webex account in the lab organization (provided by the lab team)
- [x] Access to the assigned Webex Control Hub organization
- [x] A dCloud workstation with VS Code, GitHub Copilot Chat, and the lab workspace preloaded
- [x] The GitHub account assigned for Copilot access
- [x] The approved AI client configuration (supplied by the lab team)
- [x] Permission to authorize the Webex Agentic Apps requested in the lab

### What you should know

Basic familiarity with Webex meetings and spaces, JSON data structures, and HTTP APIs (request/response concepts).

No prior MCP experience is required - the lab will teach you.

### Your first five minutes

1. Open the dCloud desktop and sign in with your Windows credentials.
2. Open the browser and sign in to Webex with your assigned lab identity.
3. Open Webex App and confirm the seeded meetings and spaces are visible.
4. Open the preloaded lab workspace in VS Code and sign in to GitHub Copilot Chat with the account assigned for the lab.
5. Open Copilot Chat, set **Session Target: Local**, select **Agent** mode and the lab's designated model. You will connect the Webex MCP servers in Lab 1.

## Lab Rules

!!! danger "Protect your credentials"
    Do not paste tokens into chat prompts, screenshots, or Webex messages. Enter the official server tokens only in VS Code's hidden input prompts; keep the quality server token only in its local `.env` file.

!!! warning "Use only the lab environment"
    Work only with the lab organization and seeded data provided. Do not connect to your production Webex organization.

1. **Review before approving.** Keep Copilot Chat on manual tool approvals, review the tool name and inputs, and approve only the actions you intend.
2. **Don't trust output blindly.** AI-generated summaries and recommendations may be incomplete or incorrect. Verify before acting on them.

## Lab Flow and Timing

| Time | Module | What you do |
| ---: | ---------------- | ---------------- |
| 0-10 min | Orientation | Understand the architecture and lab rules |
| 10-30 min | [Lab 1](lab1_control_hub.md) | Enable Agentic Apps, configure tools, generate MCP tokens |
| 30-55 min | [Lab 2](lab2_connect_discover.md) | Discover, predict, invoke, reject, and approve MCP tools |
| 55-95 min | [Lab 3](lab3_follow_up.md) | Build and refine the meeting follow-up assistant |
| 95-135 min | [Lab 4](lab4_quality.md) | Build and test the meeting quality assistant |
| 135-145 min | [Lab 5](lab5_capstone.md) | Coordinate both skills in a cross-workflow capstone |
| 145-150 min | [Wrap-up](skills/customization-exercise.md) | Customize skills, export your bundle, clean up |

!!! note
    This lab is designed as crawl, walk, run. Complete the core path first. Each lab marks its advanced exercises so that you can go deeper if you finish early.
