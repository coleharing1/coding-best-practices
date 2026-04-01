# Portable Repo Skills

Store portable Codex/Gemini skill packs in `.agents/skills/`.

Use this folder when a workflow needs more than a prompt:

- scripts or command sequences
- structured input/output conventions
- repeated browser or service setup
- reusable review posture

Recommended structure:

```text
.agents/skills/
└── skill-name/
    ├── SKILL.md
    └── agents/
        └── openai.yaml
```

Keep skills narrow. A skill should own one reusable workflow, not the entire repo operating system.
