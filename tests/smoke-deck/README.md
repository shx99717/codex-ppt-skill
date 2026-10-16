# codex-ppt smoke deck

The three-content-slide coffee fixture checks multilingual pixels, backend provenance, layouts, notes, and plain/Medavis assembly. Every successful live run produces three final content images; repairs can produce additional candidates. Saved historical runs are unchanged.

## Managed v2 and historical compatibility

New runs use the adaptive managed workflow. A topic or prepared source first becomes a whole-deck content/visual/talk draft. Review exact copy, relationships, assets, recurring identities, numbering, natural notes, output profile/title, representative strategy and review policy before expensive generation. Do not require three-to-five bullets or postpone notes until images exist.

Consolidated review (the former low-interruption intent of FAST) continues routine batches after first-batch agent QA, then asks the user to accept actual current images together. Strict review (GATED) asks for each batch. Neither policy pre-approves unseen samples/images or manufactures approval evidence. Output choices belong in planning, not a new last-minute question.

Historical pre-v2 image folders remain usable with explicit `--legacy-unmanaged` on assembly/state CLIs. That flag cannot bypass managed records. Existing `verify_deck.py` physical BASELINE/TARGET assertions are preserved for historical comparison; they are supplemental checks, not proof of managed approval or visual quality.

## Start a live test

Use [portable prompt](RUN_PROMPT.md), or a pinned host/backend prompt:

- [Codex image_gen](RUN_PROMPT_codex.md)
- [Cursor GenerateImage, 16:9 / 4:3](RUN_PROMPT_cursor.md)
- [Cursor codex-gpt-image](RUN_PROMPT_cursor_codex-gpt-image.md)
- [Claude Code codex-gpt-image, consolidated](RUN_PROMPT_claude.md)
- [Claude Code codex-gpt-image, strict](RUN_PROMPT_claude_interactive.md)

Live tests require separate generation authorization and real user reviews. They are not part of offline implementation verification. Test the intended skill root explicitly. Do not overwrite an installed skill, commit or push as a side effect of a smoke test; installation synchronization is a separate user choice.

## Preflight and outputs

```bash
python tests/smoke-deck/verify_deck.py --preflight
python tests/smoke-deck/verify_deck.py tests/smoke-deck/runs/<run-id>/coffee-extraction \
  --host codex --skill-root skills/codex-ppt
```

Use a fresh run directory under ignored `runs/`. The fixture uses three slides: Chinese, English, then mixed CJK/Latin. Keep the pinned clean professional style; to test discovery separately, omit that style pin and record that the run is no longer baseline-comparable.

Use 16:9 or 4:3 only. Prefer the callable native tool: Codex image_gen may use prompt-only ratio control; Cursor GenerateImage passes a supported aspect_ratio value. Inspect actual inputs, attach every snapshot, measure original pixels, and record the current attempt receipt. No fixed native model identity or invented size argument. API uses its explicit configured model and documented capabilities.

An unrequested CLI fallback fails host-pinned runs. Deliberately selected CLI tests use `--allow-cli-fallback`; managed execution uses `run_slide_job.py` with an explicitly approved operation policy, not nested-job replay through text-only batch generation.

Plain has N slides; Medavis has landing + N content + ending (N+2) and content-note offset. Recommend both with a proposed landing title in the combined plan when testing branding. Never silently create an unapproved output profile.

## Quality and verification

Inspect the first batch before later production, record per-slide and ordered-deck QA, and obtain actual current-image user approval according to policy. One isolated rendering defect gets one automatic targeted repair; further attempts need authorization. Pause common first-batch failures. Repairs preserve exact approved labels and immutable style references.

The legacy verifier exit code reflects BASELINE assertions; TARGET is supplemental progress information. Report both and explain any limitation. Managed readiness additionally comes from the scripts' scoped fingerprints, actual decisions, current-image review, source/sample/job integrity and sequence QA. Passing a physical file check cannot approve a deck.

Offline regression command:

```bash
python -B -m unittest discover -s skills/codex-ppt/scripts/tests -p 'test_*.py'
```

The implementation's separate synthetic two-content-slide smoke uses Pillow test fixtures, MOCK/TEST decision evidence and managed plain/Medavis assembly. It exercises contract/state/notes mapping only; it is never a live model deck or real human approval. Source-asset fidelity, lettering quality and timed speech still need real inspection in a later authorized pilot.

For failures, reproduce the actual layer, add meaningful regression RED before a script fix, verify GREEN, and report changes. Preserve prior run evidence and existing local edits.
