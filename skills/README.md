# Webex MCP Customer Skill Bundle

This bundle separates the controlled agent prompt from customer-editable workflow skills.

## Structure

```
skills/
├── controlled-agent-prompt.md          # platform-controlled; not a customer skill
├── meeting-follow-up/
│   ├── SKILL.md
│   └── references/
│       ├── workflow.md
│       └── output-format.md
├── approval-gate/
│   ├── SKILL.md
│   └── references/
│       └── preview-fields.md
├── multilingual-output/
│   ├── SKILL.md
│   └── references/
│       └── translation-rules.md
├── attendance-report/
│   ├── SKILL.md
│   └── references/
│       └── default-fields.md
├── meeting-quality/
│   ├── SKILL.md
│   └── references/
│       ├── analysis-rules.md
│       └── report-format.md
└── incident-mode/
    ├── SKILL.md
    └── references/
        └── workflow.md
```

Each skill directory contains a `SKILL.md` with Anthropic-compatible YAML frontmatter (`name` and `description`) and a `references/` subdirectory with supporting detail files. The main `SKILL.md` is intentionally concise and links to references using progressive disclosure — references are always one level deep.

## Loading model

The host client or agent framework must load skills by workflow context. The directory-based layout follows the Anthropic Agent Skills structure. The final lab implementation must map these directories to the selected VS Code/OpenCode instruction mechanism.

- Follow-up: load `meeting-follow-up/SKILL.md` and `approval-gate/SKILL.md`; add multilingual and attendance skills when requested.
- Quality: load `meeting-quality/SKILL.md` and `approval-gate/SKILL.md`; add incident mode when requested.

## Safe customization

Customers may change terminology, formatting, thresholds, checklists, and space naming. They must not change authorization, approval requirements, tool contracts, privacy rules, or evidence requirements. Keep the controlled prompt under repository review and version skill changes.

Never include lab tokens, seeded transcripts, participant data, organization IDs, or production secrets in this bundle.
