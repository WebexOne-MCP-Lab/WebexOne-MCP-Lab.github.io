---
name: meeting-quality
description: Analyze Webex meeting-quality telemetry returned by a separate Meeting Qualities API tool, separating observations, hypotheses, recommendations, evidence, and data gaps. Use when troubleshooting degraded meeting media quality or generating a quality report.
---

# Meeting Quality

Analyze meeting-quality telemetry returned by the separate Meeting Qualities custom tool. Use the Webex Meetings MCP server to resolve the meeting ID; use the custom quality tool for media-quality telemetry.

Separate observations, hypotheses, recommendations, and data gaps. Cite the source field or timestamp for each observation. Require approval before creating an incident space or posting quality details.

For detailed analysis rules, see [references/analysis-rules.md](references/analysis-rules.md).
For default report sections, see [references/report-format.md](references/report-format.md).

## Customization

Customers may customize thresholds, severity labels, terminology, and troubleshooting checklists. They may not change the custom tool authentication or invent missing telemetry.

## Related skills

- [Approval gate](../approval-gate/SKILL.md)
- [Incident mode](../incident-mode/SKILL.md)
