---
name: approval-gate
description: Require explicit human review immediately before Webex side effects such as creating spaces, adding members, posting messages, uploading files, scheduling meetings, or creating webhooks. Use whenever an agent is about to change Webex state or publish meeting data.
---

# Approval Gate

Prevent unreviewed external side effects. Before each write action, present a preview and wait for explicit approval.

Offer: `Approve`, `Edit`, `Approve selected`, or `Reject`. Do not execute until the user explicitly approves the exact action. An approval expires if the target, recipients, content, or schedule changes. Never interpret general instructions such as "handle it" as approval.

For the full list of required preview fields, see [references/preview-fields.md](references/preview-fields.md).

## Customization

Customers may change wording, approver role, preview layout, and expiration period. They may not remove the approval requirement.
