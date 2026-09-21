# Skill File Overview

## What are skill files?

Skill files are modular instruction sets that customize the agent's behavior for specific workflows. They control **how** the agent presents, formats, and organizes its output - without changing the safety-critical control logic.

You built two of them yourself in [Lab 3](../lab3_follow_up.md) and [Lab 4](../lab4_quality.md).

## Two-layer design

| Layer | Who controls it | What it does |
| ---------------- | ---------------- | ---------------- |
| `Controlled agent prompt` | Lab team / platform | Defines the agent's role, safety rules, approval gates, and tool contracts |
| `Skill files` | You, the customer | Customize formatting, terminology, thresholds, and workflow-specific guidance |

!!! important
    The controlled prompt always takes precedence. If a skill conflicts with a safety rule, the agent follows the controlled prompt and reports the conflict.

## Skill bundle structure

```text
skills/
├── README.md
├── controlled-agent-prompt.md
├── meeting-follow-up/
│   ├── SKILL.md
│   └── references/
├── approval-gate/
│   ├── SKILL.md
│   └── references/
├── multilingual-output/
│   ├── SKILL.md
│   └── references/
├── attendance-report/
│   ├── SKILL.md
│   └── references/
├── meeting-quality/
│   ├── SKILL.md
│   └── references/
└── incident-mode/
    ├── SKILL.md
    └── references/
```

Each skill has a `SKILL.md` (the main instruction file) and a `references/` directory with supporting details.

## What each skill controls

| Skill file | Loaded for | Customizable examples |
| ---------------- | ---------------- | ---------------- |
| `meeting-follow-up/SKILL.md` | Transcript-to-follow-up workflow | Summary format, decision categories, action-item labels, space naming |
| `approval-gate/SKILL.md` | Before any write action | Approver role, approval wording, preview fields, expiration period |
| `multilingual-output/SKILL.md` | Translation and publication | Supported languages, terminology glossary, bilingual layout, confidence labels |
| `attendance-report/SKILL.md` | Attendance and participation output | Report columns, neutral labels, CSV/Markdown format, recipient restrictions |
| `meeting-quality/SKILL.md` | Quality analysis | Thresholds, evidence format, troubleshooting checklist, severity mapping |
| `incident-mode/SKILL.md` | Quality incident workflow | Incident-space naming, responder roles, update format, closure template |

## What you can and cannot change

=== "You can customize"

    > Section names and ordering
    >
    > Action-item labels and categories
    >
    > Space naming conventions
    >
    > Report columns and output format
    >
    > Severity labels and thresholds
    >
    > Troubleshooting checklists
    >
    > Supported languages and terminology glossaries

=== "You cannot change"

    > Approval gates - they cannot be bypassed or removed
    >
    > OAuth scopes or Control Hub policy
    >
    > Tool authentication or endpoint contracts
    >
    > Privacy rules and data restrictions
    >
    > Evidence requirements
    >
    > The requirement to separate observations from hypotheses

## How skills are loaded

The agent loads skills based on the workflow context:

```text
IF workflow = follow_up:
  load meeting-follow-up/SKILL.md
  load approval-gate/SKILL.md
  load multilingual-output/SKILL.md when translation is requested
  load attendance-report/SKILL.md when a report is requested

IF workflow = quality:
  load meeting-quality/SKILL.md
  load approval-gate/SKILL.md
  load incident-mode/SKILL.md when Incident Mode is requested
```

!!! curious "You saw this in action"
    The [capstone](../lab5_capstone.md) required the agent to make these loading decisions on its own, from a single business request.
