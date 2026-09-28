# Skill File Overview

## What are skill files?

Skill files are modular instruction sets that customize the agent's behavior for specific workflows. They control **how** the agent presents, formats, and organizes its output - without changing the safety-critical control logic.

You built two of them yourself in [Lab 3](../lab3_follow_up.md) and [Lab 4](../lab4_quality.md).

## Two-layer design

| Layer | Who controls it | What it does |
| ---------------- | ---------------- | ---------------- |
| `Workspace instructions` | Lab team | Guides the agent's role, review steps, and tool use through `.github/copilot-instructions.md` |
| `Skill files` | You, the customer | Customize formatting, terminology, thresholds, and workflow-specific guidance under `.github/skills/` |

!!! important
    Workspace instructions and skills guide Copilot's behavior; neither is an enforcement boundary. Keep manual tool approvals enabled and rely on Control Hub to restrict available Webex tools. If a skill asks to skip review, decline the tool call and remove that instruction.

## Skill bundle structure

```text
lab-workspace/
├── .github/
│   ├── copilot-instructions.md
│   └── skills/
│       ├── meeting-follow-up/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── approval-gate/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── multilingual-output/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── attendance-report/
│       │   ├── SKILL.md
│       │   └── references/
│       ├── meeting-quality/
│       │   ├── SKILL.md
│       │   └── references/
│       └── incident-mode/
│           ├── SKILL.md
│           └── references/
```

Each skill has a `SKILL.md` (the main instruction file) and a `references/` directory with supporting details. The downloadable bundle stores the skill directories under `skills/`; copy them to `.github/skills/` in the lab workspace so VS Code discovers them.

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

=== "Lab rules you must preserve"

    > Approval steps - do not bypass or remove them
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

VS Code discovers skills under `.github/skills/` and Copilot loads them when the request matches their descriptions (or when you invoke them from chat). The intended routing is:

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
    The [capstone](../lab5_capstone.md) asks the agent to choose relevant skills from a single business request. Verify the skills actually loaded; model behavior can vary.
