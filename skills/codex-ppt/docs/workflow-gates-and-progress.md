# Workflow Gates And Progress

Read this before creating downstream artifacts, advancing between phases, or reporting progress.

## Mandatory Phase Gates

This workflow has explicit approval gates. Do not advance to a later phase until the previous phase has been approved by the user, unless the user explicitly asks to skip that confirmation.

Phase order:

1. Source reading and asset extraction
2. Outline confirmation
3. Visual style confirmation
4. Image backend confirmation
5. One sample slide approval
6. Full slide generation (dispatch waves)
7. Per-wave user review of generated full-res slide images
8. QA, speaker notes finalization, and PPT assembly

Hard rules:

- Before outline approval, do not create final `deck_spec.json`, `speech.md`, prompt job files, slide images, or `.pptx` files.
- If you need an internal planning artifact before approval, name it with `.draft.` such as `deck_spec.draft.json` or `speech.draft.md`, and clearly report that it is not final.
- Downstream artifacts (`deck_spec.json`, `prompts/`, `slide_jobs.json`, `speech.md`, final slide images, and `.pptx`) should be created only after the relevant gates have been approved.
- If the deck uses required source images, stop at outline confirmation and ask the user to verify the slide-to-image mapping before style selection or image generation.
- Do not treat sample approval as full-deck image approval.
- Do not dispatch the next generation wave until every slide in the current wave is user-reviewed via `record_user_review.py`.
- Do not assemble when any non-sample `recorded` slide lacks a valid `user_review` (matching image sha). `assemble_ppt.py` does not enforce this — the agent must.
- Skipping the per-slide user-review gate requires an **explicit** user waiver for this deck. If waived, record it in run state (do not invent a silent skip), for example:

```bash
~/.codex-ppt-skill/.venv/bin/python -c "from slide_run_state import deck_dir_from_target, set_run_status; set_run_status(deck_dir_from_target('{base_dir}/{deck_name}'), 'user_review_waived', 'user explicitly waived per-slide review for this deck')"
```

  Prefer running that from `{skill_root}/scripts` (or with that directory on `PYTHONPATH`) so `slide_run_state` imports resolve. Also state the waiver in the chat report.

## Visible Progress Plan

For non-trivial decks, keep a user-visible checklist with one active step:

1. Prepare source, outline, style, and backend decisions.
2. Generate and approve one sample slide.
3. Prepare slide jobs and slide state.
4. Dispatch slide subagents (one wave at a time).
5. Record generated slide results for the wave.
6. User-review each newly recorded full-res slide in the wave.
7. QA, repair, notes, and PPT assembly.

Completion evidence:

- `Prepare source, outline, style, and backend decisions`: `outline.md` is approved and image backend is confirmed.
- `Generate and approve one sample slide`: one final `origin_image/slide_XX.png` is approved as the style reference.
- `Prepare slide jobs and slide state`: `prompts/slide_XX.json`, `slide_jobs.json`, and `slide_run_state.json` exist.
- `Dispatch slide subagents (one wave at a time)`: `slide_job_status.py` shows dispatchable slides and each spawned worker is recorded by `record_slide_dispatch.py`.
- `Record generated slide results for the wave`: each worker output is recorded by `record_slide_result.py`, which copies the selected image into `origin_image/slide_XX.png` and records backend provenance.
- `User-review each newly recorded full-res slide in the wave`: every slide in the wave has a valid `user_review` recorded by `record_user_review.py --approve` before the next wave starts. Track the current wave's slide ids in prose (do not rely on `slide_job_status.py` for review state).
- `QA, repair, notes, and PPT assembly`: every expected final image exists, every non-sample slide has valid `user_review`, QA is complete, `speech.md` is final, and `{deck_name}.pptx` exists.

Do not mark a step complete just because the chat says it is complete; use real files or script-recorded state.
