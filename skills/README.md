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

For GitHub Copilot Chat in VS Code, copy each skill directory into the lab workspace's `.github/skills/` directory (for example `.github/skills/meeting-follow-up/SKILL.md`). VS Code discovers these skills by their `name` and `description` frontmatter; verify them in **Configure Skills**. Keep `controlled-agent-prompt.md` separate from skill directories and have the lab team review its contents before placing them in workspace `.github/copilot-instructions.md`. Prompt instructions guide the agent; Control Hub policy and manual tool approvals provide the enforceable controls.

- Follow-up: load `meeting-follow-up/SKILL.md` and `approval-gate/SKILL.md`; add multilingual and attendance skills when requested.
- Quality: load `meeting-quality/SKILL.md` and `approval-gate/SKILL.md`; add incident mode when requested.

## Safe customization

Customers may change terminology, formatting, thresholds, checklists, and space naming. They must not change authorization, approval requirements, tool contracts, privacy rules, or evidence requirements. Keep the controlled prompt under repository review and version skill changes.

Never include lab tokens, seeded transcripts, participant data, organization IDs, or production secrets in this bundle.
