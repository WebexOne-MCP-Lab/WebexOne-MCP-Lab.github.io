# Lab Credentials

Use this single account for all lab activities - Control Hub, developer.webex.com, token generation, and Webex meetings and spaces.

## Your account

<div class="grid" markdown>

<form id="info">
<label for="info">Enter the values provided by your proctor</label><br>

  <label for="WbxUser">Webex Email:</label>
  <input type="text" id="WbxUser" name="WbxUser"><br>

  <label for="WbxPW">Webex Password:</label>
  <input type="text" id="WbxPW" name="WbxPW"><br>

  <label for="Pod">Pod ID:</label>
  <input type="text" id="Pod" name="Pod"><br>
  <br>
  <button onclick="setValues()">Update Lab Guide</button>
</form>

> Webex Email: <copy><w class="WbxUser">Provided by proctor</w></copy>
>
> Webex Password: <copy><w class="WbxPW">Provided by proctor</w></copy>
>
> Pod ID: <copy><w class="Pod">Provided by proctor</w></copy>

</div>

!!! important "Lab use only"
    These credentials are valid only for the duration of this lab session. The account and all associated data will be deactivated after the event.

!!! note
    Values you enter above are stored only in your own browser session and are used to personalize the instructions throughout this guide. They are never sent anywhere.

## Where you will use these credentials

| Step | Where | What you do |
| ---------------- | ---------------- | ---------------- |
| `Lab 1` | [admin.webex.com](https://admin.webex.com/){:target="_blank"} | Sign in to configure Agentic Apps and tools |
| `Lab 1` | [developer.webex.com](https://developer.webex.com/){:target="_blank"} | Generate the two Agentic App tokens for Kiro |
| `Lab 2` | Kiro + Webex desktop app | Run tools and watch results appear |
| `Lab 3-5` | Webex | Access seeded meetings, spaces, and transcripts |
| `Lab 4` | [developer.webex.com](https://developer.webex.com/){:target="_blank"} | Generate a personal access token for the quality server |

## Tokens you will generate

You generate three tokens during this lab. They are **not** your login credentials - they authorize specific applications to act on your behalf.

| Token | Created in | Where it goes | Lifetime |
| ---------------- | ---------------- | ---------------- | ---------------- |
| `Webex Meeting Agentic App token` | Lab 1 | `.kiro/settings/mcp.json` | Lab session |
| `Webex Messaging Agentic App token` | Lab 1 | `.kiro/settings/mcp.json` | Lab session |
| `Personal access token` | Lab 4 | `quality-tool/.env` | 12 hours |

!!! danger "Protect every token"
    Do not paste tokens into prompts, source files, screenshots, Git repositories, or Webex messages. The personal access token in particular grants full access to your account.
