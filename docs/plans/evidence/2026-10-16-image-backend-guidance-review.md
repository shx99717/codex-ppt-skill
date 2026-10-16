# Image backend guidance review — 2026-10-16

## Original review (verbatim)

Changeset scope is coherent with the approved plan. Native capability guidance, truthful evidence labels, ratio retirement, historical preview attribution, remaining templates/logos and twelve styles are handled consistently.

- **D1 — Important — `skills/codex-ppt/docs/slide-generation-and-subagents.md:28`**
  The primary worker lifecycle example still invokes `record_slide_result.py` without `--submission-receipt`. Following it for any newly compiled managed job now fails before recording the result. Update the command with the receipt argument and show the preceding native receipt creation or adapter-produced receipt path.

- **D2 — Important — `skills/codex-ppt/scripts/tests/test_submission_evidence.py:35`**
  The “provider” fake intercepts `subprocess.run` before the real CLI/provider boundary. It proves forwarding staged filenames into a command, but never verifies OpenAI SDK file handles or AtlasCloud data URLs. No other test invokes those provider edit paths. A downstream omission/reordering of image bytes could pass every added test. Add local fake-SDK/fake-HTTP tests through real `image_gen.py edit`, checking all ordered source bytes and ensuring capability metadata stays outside provider payloads. This is an explicit handoff acceptance requirement.

- **D3 — Important — `skills/codex-ppt/scripts/tests/test_managed_execution.py:80` and `:105`**
  New broad `except AssertionError: continue` clauses turn any sample fixture failure into successful negative-test coverage. Unexpected receipt, dispatch or sample-approval regressions therefore satisfy these tests without demonstrating rejection of the intended invalid parameter. Assert the specific expected failure stage/message and absence of dispatch/provider execution; let unrelated fixture errors fail.

- **D4 — Minor — `README_en.md:7`, `:230`; corresponding Chinese/Korean documentation**
  Mechanical model-name replacement introduced malformed wording, including “configuring the configured image model” and “A the configured image model image generation skill.” Chinese has “配置 已配置的生图模型”; Korean installation has “설정된 이미지 모델 모델명.” Rewrite these sentences naturally. Also synchronize the fallback/subscription caution at `docs/en/installation.md:83`, which is absent from Chinese and Korean counterparts.

Verification performed: skill contract/link suite **3 passed**; submission evidence suite **4 passed**. Read-only review; no edits, installed-skill changes or external calls.

## Follow-up review

Scope remains coherent. Source fixes were reviewed read-only; only this report was written by the reviewer.

- **D1 closed.** The primary lifecycle command now supplies `--submission-receipt GENERATED.submission.json`, preceded by an explanation of native/bridge versus CLI receipt provenance.
- **D2 closed.** New `test_provider_input_boundary.py` executes real `image_gen.main()` edit paths through fake OpenAI SDK and AtlasCloud HTTP transports, captures file-handle/data-URL bytes for two distinct ordered images, and checks capability metadata exclusion. No real transport or paid call is used. Route and unsupported-setting checks also pass.
- **D3 closed.** The newly added catch branches now require the intended error text and absent job state; unrelated sample errors escape as test failures. The previously existing broad approval catch was not introduced by this changeset.
- **D4 partially closed at follow-up inspection.** README introductions and bridge descriptions are repaired. Remaining examples: `docs/ko/faq.md:35` uses the incorrect object particle `이미지 모델를` (use `이미지 모델을`); `docs/ko/installation.md:89` retains the mechanical phrase `서드파티 설정된 이미지 모델 프록시 API`; `docs/installation.md:89` and `:96` retain mechanically spaced model substitutions. The Korean installation fallback/subscription caution is still absent at inspection. The parent has been informed and is editing these sentences. These remain the original Minor D4 finding, not additional findings.

Follow-up verification actually run:

- Provider input boundary suite: **3 tests passed**, 0.157 seconds.
- Managed execution suite: **10 tests passed**, 17.018 seconds.
- Skill contract/link suite: **3 tests passed**, 0.007 seconds.
- `git diff --check`: exit 0.

No new findings or introduced regressions were identified in the reviewed fixes. D4 remains open only for the listed final language/parity corrections until their saved state is inspected. This is a focused follow-up, not a claim that the entire runtime suite or paid/native image generation was exercised.

## Final D4 closure

Re-inspected the saved Chinese installation/FAQ, Korean installation/FAQ, and affected README/English text. **D4 closed.** Chinese installation now uses natural third-party API wording and an accurate model-ID instruction. Korean FAQ uses `이미지 모델을`; Korean installation uses natural proxy wording and explicitly states the API fallback path and that a subscription does not guarantee a callable native tool. The identified malformed replacement strings are absent from the affected public documents. `git diff --check` again exited 0. No production files were edited by the reviewer.

All original findings **D1–D4 are closed**. No remaining findings from this focused guidance/tests review.
