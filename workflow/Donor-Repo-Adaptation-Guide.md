# Donor Repo Adaptation Guide

> Reusing a strong existing repo is often smarter than starting clean. The trick is to inherit deliberately.

## Goal

Extract leverage from a donor project without cloning its confusion.

## What To Reuse First

1. architecture patterns
2. planning and operating-system patterns
3. narrow modules
4. data-model ideas
5. UI sections only after you understand their data assumptions

## What Not To Reuse Blindly

- environment drift
- stale docs
- hidden auth assumptions
- tenant assumptions when the new repo is single-tenant
- direct copies of brittle code you do not yet understand

## Recommended Workflow

1. Audit the donor repo:
   - current routes
   - current data flow
   - core docs
   - known issues
2. Write a plan for the adaptation, not just the feature.
3. Port in narrow slices.
4. Verify behavior against the donor when that comparison matters.
5. Capture intentional divergence in `WORKLOG.md` or `knowledgebase/`.

## Good Questions To Ask

- What is the donor really good at?
- Which parts are donor-specific and should stay behind?
- What assumptions must be rewritten for the new repo?

## Recommendation

Donor repos are accelerants when you port their strengths, not their accidental complexity.
