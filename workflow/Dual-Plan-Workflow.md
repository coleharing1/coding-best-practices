# Dual-Plan Workflow

> Claude and Codex plan independently. Claude then synthesizes the Final checklist that Codex implements.

---

## Why This Works

- Claude is better at architecture, risk framing, and missing edge cases.
- Codex is better at buildable sequencing, concrete file paths, and execution realism.
- The comparison step catches blind spots before code exists.

## Folder Structure

```text
plans/
├── MACRO-ROADMAP.md
├── active/
│   ├── Plan-001-CLAUDE.md
│   ├── Plan-001-Codex.md
│   └── Plan-001-Final.md
└── archive/
```

Only one active plan set at a time.

## Required Shape Of A Good Plan

Every plan should be:

- a checklist, not just narrative
- explicit about scope and constraints
- explicit about which macro-roadmap items it advances
- tagged with owners
- explicit about blockers and gates
- explicit about verification

Recommended owner tags:

- `[Cole]`
- `[Codex]`
- `[Claude]`
- `[Gemini]`
- `[Shared]`
- `[Gate]`

## Workflow

### Step 1: Write One Prompt

Give both tools the same feature prompt.

Include:

- desired user-facing behavior
- technical constraints
- what is out of scope
- known repo realities
- which macro-roadmap phase or IDs the work likely belongs to

### Step 2: Claude Writes Its Plan

Claude reads `plans/MACRO-ROADMAP.md` first, then writes `plans/active/Plan-XXX-CLAUDE.md`.

Best things for Claude to catch:

- architecture shape
- risk areas
- missing failure states
- human-only decisions or approvals

### Step 3: Codex Writes Its Plan

Codex reads `plans/MACRO-ROADMAP.md` first, then writes `plans/active/Plan-XXX-Codex.md`.

Best things for Codex to catch:

- execution order
- concrete file paths
- verification commands
- overbuilt phases

### Step 4: Claude Compares Both

Claude should identify:

1. agreements
2. important disagreements
3. good ideas unique to one plan
4. gaps in both plans

### Step 5: Claude Synthesizes The Final Plan

Claude writes `plans/active/Plan-XXX-Final.md`.

The Final plan should preserve:

- macro-roadmap alignment
- owner tags
- blocking gates
- verification criteria
- explicit human login/approval steps

### Step 6: You Review It

Use this as the decision point for:

- scope trimming
- reordering
- confirming human-only steps
- accepting or changing the gates

### Step 7: Codex Implements It

Codex builds from the Final checklist one phase at a time.

### Step 8: Archive It

After the feature is shipped and verified, move the full plan set to `plans/archive/`.

## Checklist Format

Use this shape:

```markdown
# Plan XXX -- [Feature Name] ([Source])

## Context
- Goal
- Scope
- Out of Scope
- Risk Tier
- Constraints

## Current Evidence
- [repo findings]

## Macro Roadmap Alignment
- [roadmap IDs and whether the roadmap itself needs a sync]

## Working Assumptions
- [assumption]

## Ownership Legend
- `[Cole]` ...
- `[Codex]` ...
- `[Claude]` ...
- `[Shared]` ...
- `[Gate]` ...

## Blocking Gates
| Gate | Must Be Complete Before | Required Outcome |

## Implementation Checklist
### Phase 1: [Name]
#### 1A. [Workstream]
- [ ] `[Owner]` [step]
- [ ] `[Owner]` [step]
#### Phase 1 Verification
- [ ] `[Owner] [Gate]` [binary result]
```

## Tips

- Treat `plans/MACRO-ROADMAP.md` as the whole-project roadmap, not the active implementation checklist.
- Do not let Codex read Claude's plan before writing its own.
- Do not hide login, 2FA, approval, or browser-consent work inside vague "manual setup" bullets.
- The Final plan should read like something you can execute directly, not something you still have to translate.
