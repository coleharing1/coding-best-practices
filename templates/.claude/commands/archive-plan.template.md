---
description: Archive completed plans from active to archive folder
---

## Archive Completed Plans

### Current Active Plans

!`ls -la plans/active/ 2>/dev/null | grep -v .gitkeep || echo "No active plans found"`

### Action

Move all plan files from `plans/active/` to `plans/archive/`:

1. Verify the Final plan exists and implementation is complete
2. Move all `Plan-XXX-*.md` files from `plans/active/` to `plans/archive/`
3. Confirm the move was successful

### Post-Archive

!`ls -la plans/archive/ 2>/dev/null | tail -10`

Report:
- Which plan set was archived (plan number and feature name)
- Confirm `plans/active/` is clean for the next feature
