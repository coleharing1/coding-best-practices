# Gemini CLI Hooks

Use hooks for behavior that should happen automatically rather than through an invoked command.

High-value hook candidates:

- notify when the agent is blocked on login or approval
- inject extra context for risky paths
- remind the agent about browser lanes
- run a lightweight check after edits

Start with one or two hooks only after the manual workflow is already reliable. Hooks should reinforce a working process, not compensate for an unclear one.
