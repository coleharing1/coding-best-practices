You are planning implementation for [FEATURE_NAME] in [PROJECT_NAME].

Context:
- Stack: [STACK]
- Constraints: [CONSTRAINTS]
- Existing architecture notes: [NOTES]
- Risk tier target: [TIER]

Output requirements:
1. A short technical spec (interfaces/contracts/data flow).
2. Working assumptions, owner tags, and blocking gates.
3. A phased implementation checklist with discrete, sequential steps.
4. Risk analysis and verification per phase.
5. A `tasks.json` list with dependency links and owner fields.

Rules:
- Do not write code yet.
- Call out unknowns explicitly.
- Prefer minimal-change integration with existing patterns.
- Highlight any phase that should require Gemini/Claude dual review.
- If a step needs login, 2FA, approval, or org selection, mark it explicitly instead of leaving it implied.
