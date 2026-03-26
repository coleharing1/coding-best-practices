You are planning implementation for [FEATURE_NAME] in [PROJECT_NAME].

Context:
- Stack: [STACK]
- Constraints: [CONSTRAINTS]
- Existing architecture notes: [NOTES]
- Risk tier target: [TIER]

Output requirements:
1. A short technical spec (interfaces/contracts/data flow).
2. A phased implementation plan with discrete, sequential steps.
3. Risk analysis per phase (what can break, why, and mitigation).
4. Acceptance criteria per phase (testable, binary pass/fail).
5. A `tasks.json` list with dependency links.

Rules:
- Do not write code yet.
- Call out unknowns explicitly.
- Prefer minimal-change integration with existing patterns.
- Highlight any phase that should require Gemini/Claude dual review.
