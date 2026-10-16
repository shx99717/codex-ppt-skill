# Critical Review: Predictable Deck Generation Handoff

**Reviewed**: 2026-10-14 22:13 Asia/Shanghai  
**Branch**: feature/SQ5GEN-predictable-deck-generation  
**Task**: SQ5GEN-195  
**Target**: [self-contained implementation plan](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md)  
**Original result**: 0 Critical, 4 Important, 0 Minor findings confirmed.
**Resolution updated**: 2026-10-14 23:05 Asia/Shanghai. All four findings addressed in the revised handoff; focused reference checks passed. Runtime implementation/verification remains pending.

The user selected an agent critical review of the completed handoff. This review used think-mcp sequentialthinking and executable probes of the plan's reference Python and JSON examples. The approved workflow requirements remain valid. The findings concern inconsistencies in the concrete implementation contract; no feature implementation, live image generation, installation, commit, or push occurred.

The user subsequently accepted the recommendation to revise the plan. All four findings are now **addressed in the plan**, and the companion prompt and memory reflect the corrections. The findings below describe the original audited version; linked locations now point to the corrected replacement sections. This is not a claim that production code has been implemented or runtime defects fixed.

## Important-1: The prompt and visual fingerprint include different shared context

**Locations**: [common render projection](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:430), [projection invariant](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:553), [prompt builder](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:645).

The manifest includes only shared visuals referenced by the slide and its dependencies. The prompt builder serializes the entire shared-visual registry. Adding an unused shared element therefore changes the renderer's prompt without changing any slide's visual approval binding.

**Observed**: All visual bindings remained equal; the render prompt changed.

**Impact**: A supposedly unaffected slide can receive different generation instructions under its existing scoped approval. This defeats the intended alignment between approved production inputs and impact-aware revisions.

**Recommended correction**: Define one canonical render-context projection and use it in both fingerprinting and prompt compilation. Include only the shared elements and approved dependency context relevant to the slide. Audit every prompt-affecting field and input asset against that projection. Hashing the entire registry would bind the prompt, but would also invalidate unrelated slides unnecessarily.

**Regression criteria**:

- Adding or changing an unreferenced shared definition changes neither a slide's render context nor its visual binding.
- Changing a referenced element changes both the relevant context and its binding, including actual dependents.
- Prompt compilation and fingerprinting consume the same approved semantic context; unrelated note edits do not leak into image prompts.

## Important-2: Changed slide facts can retain stale talk approval

**Locations**: [semantic note projection](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:472), [note dependencies](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:497).

The note projection includes note text, title, intent, and slide role. It omits approved local factual content, critical values, claim-source evidence, source-asset hashes, and relevant visual meaning. Dependencies repeat that incomplete note projection.

A synthetic fixture initially contained an illustrative ten-minute wait in both visible copy and notes. Changing the visible value and its source claim to twenty minutes changed the visual binding, while the talk binding remained equal and the notes still said ten minutes.

**Observed**: Visual binding changed; talk binding did not; the old spoken fact remained.

**Impact**: Revision handling can treat an inconsistent talk as still approved. This conflicts with the user's requirement that notes explain the approved material and form a coherent presentation.

**Recommended correction**: Bind notes to the approved semantic claims, critical values, source evidence, and relevant relationships they explain, including dependencies. Make that dependency contract explicit. Keep pure appearance and layout changes outside the talk projection so they do not create unnecessary note reviews.

**Regression criteria**:

- A changed approved fact or referenced source byte invalidates the affected talk approval even if the note text was not edited.
- Relevant upstream semantic changes invalidate dependent notes.
- A layout-only or color-only revision leaves otherwise unchanged talk approval valid.
- A note-only voice or pacing revision does not invalidate image approval.
- Human/content QA still checks factual consistency, natural speech, pacing, and continuity. Hash equality cannot establish those qualities.

## Important-3: Output-policy approval has no fingerprint in the ledger example

**Locations**: [ledger schema](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:243), [policy consumer](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:528), [shared gate contract](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:562), [decision recorder contract](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:599).

The manifest computes a policy hash covering review policy, output profile, and landing title. The approval consumer requires a current policy binding, but the ledger example stores only policy value and event ID. It provides no approved policy hash or output snapshot to compare.

Changing plain output to Medavis with a new landing title changed the policy hash while all visual/talk bindings and the review-policy string remained unchanged.

**Observed**: The policy hash changed; slide bindings stayed equal; the example ledger contained only `event_id` and `value`.

**Impact**: The handoff gives the decision recorder and its consumer incompatible contracts for approving output changes. This is a schema gap; the runtime consumer has not been implemented, so this review does not claim a live approval bypass.

**Recommended correction**: Persist the policy/output fingerprint with the actual user decision and validate it during preparation and assembly. Specify how policy changes are approved for all/scoped decisions. Synchronize the schema, CLI behavior, example ledger, helper contract, and tests.

**Regression criteria**:

- Review-policy, output-profile, and landing-title changes each make prior policy approval stale.
- A genuine new policy decision records the current fingerprint without relabeling unrelated historical approvals.
- Preparation/assembly reject a mismatched current policy and continue after a valid recorded decision.

## Important-4: Installing a draft can change the meaning of relative asset paths

**Locations**: [asset normalization](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:393), [reviewed candidate and installation](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:595), [canonical missing-approval fixture](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:290).

The recorder accepts a draft spec, then installs a canonical spec inside the deck folder. The manifest resolves relative assets against the spec's parent. The plan does not specify rebasing or source-root preservation before that move.

The probe created an asset available relative to an input draft folder. Hashing succeeded there; using the same spec relative to the deck folder raised `Required asset missing`.

**Observed**: Draft-relative resolution succeeded; resolution after relocation failed.

**Impact**: Valid prepared inputs outside the deck can become unreadable after approval, or resolve to different bytes if the destination contains a file with the same relative name.

**Recommended correction**: Resolve paths using the original draft/source root and normalize or rebase them before the canonical approval fingerprint is recorded. Define snapshot paths and preserve original provenance for the intended drift checks. Ensure workers use the approved asset bytes.

Also fix Task 1's missing-approval regression: install a valid canonical spec inside the deck first, so the failure specifically proves absent approval rather than absent canonical input.

**Regression criteria**:

- A valid draft outside the deck with relative assets installs correctly and retains the approved asset identity.
- A different destination file with the same relative name cannot replace the approved source silently.
- Missing assets refuse approval before partially installing approved state.
- The missing-approval test exercises a valid canonical spec and verifies that no prompt outputs are created.

## Resolution and corrected reference evidence

- **Important-1 addressed**: `build_contexts` supplies the exact filtered semantic projection to both visual hashing and sorted prompt serialization. Managed callers may not append raw spec/dependency fields. Controls cover unused/used shared elements, dictionary order, and dependency-note edits.
- **Important-2 addressed**: The talk projection binds approved visible content, claims/evidence, source bytes, shared meanings, and semantic relationships through declared dependencies. Controls cover factual/source changes, pure appearance/composition changes, and note-only revisions. Style-only calibration images remain separate from source evidence.
- **Important-3 addressed**: Ledger examples now include the output snapshot/fingerprint and explicit decision scopes. The shared policy gate rejects stale hashes, mismatched values, missing/wrong events, agent actors, empty evidence, or decisions without policy scope. Recorder CLI distinguishes policy-only and scoped decisions; preparation/assembly tasks require the gate.
- **Important-4 addressed**: Draft normalization freezes original absolute source paths before the approval view and fingerprint. Event provenance retains declared spelling/root; snapshot/install rules and `--expected-plan-hash` prevent changed candidates from being silently approved. The missing-approval fixture now installs its canonical spec in the deck. Controls exercise outside drafts, required/shared assets, destination filename conflicts, source drift/missing files, and normalized Windows path identity.

The schema, kernel, prompt builder, recording/view contracts, Tasks 1–6, D9 pressure scenario, acceptance checklist, and companion prompt were updated together. [Appendix G](D:/git/codex-ppt-skill/docs/plans/2026-10-14-predictable-deck-generation-handoff.md:1255) contains the saved runnable verification.

The corrected reference probe exited **0** and reported:

```json
{
  "Important-1": "PASS: common filtered projection; unused/shared/order/note controls",
  "Important-2": "PASS: factual/source/dependency changes stale talk; appearance/layout controls",
  "Important-3": "PASS: explicit policy fingerprint/event; output changes stale approval",
  "Important-4": "PASS: draft normalization, provenance, relocation and name-conflict checks",
  "scope": "Reference-contract checks only; implementation and live-quality checks remain pending"
}
```

The first revised probe exposed a fixture assertion comparing Windows short and full path spellings. Diagnostic output confirmed both refer to the same resolved input root; comparing normalized identities corrected that assertion. No production files were changed to accommodate the fixture.

Final document checks passed: eight Python/four JSON blocks parsed, twenty local links resolved, nine tasks remained ordered, and embedded project rules matched the repository exactly. The 3,873-character original speaker source and its SHA remained unchanged. Only the six existing planning/memory/source documents are changed or untracked; staging is empty and branch HEAD/upstream/main remain unchanged. Tracked whitespace validation passed.

## Strengths and limits

The plan carries the approved adaptive-input workflow, exact visible copy, deck-wide narrative/visual coherence, natural presenter notes, early note review, representative sample calibration, scoped revisions, distinct agent QA and user image approval, legacy compatibility, and multilingual documentation work. Its complete speaker-note source is preserved unchanged.

These four probes identify concrete gaps that syntax and document-integrity checks did not detect. Prior Python/JSON parsing and source-preservation checks remain useful, but they do not establish readiness for execution. The probes use temporary hash-only asset bytes and the reference code embedded in the plan. They do not test production gate implementations, concurrency, paid image rendering, source-figure fidelity, or spoken-delivery quality. No existing-code test suite rerun was warranted by this documentation-only review.

## Next step

The handoff and prompt have been revised and focused reference checks pass. Use the corrected plan for the user-selected execution route. The executor must still demonstrate RED/GREEN against production scripts and actual agent behavior, including failed-mutation preservation and assembly checks; reference examples cannot establish those runtime guarantees.

The complete speaker-note source remains authoritative and unchanged. Plan revision does not authorize execution or new publication; earlier publication requests are complete.

## Historical pre-revision reproduction evidence

The original diagnostic completed with exit code 0 and demonstrated the four defects:

```json
{
  "Important-1": {
    "all_visual_bindings_unchanged": true,
    "render_prompt_changed": true
  },
  "Important-2": {
    "visual_binding_changed": true,
    "talk_binding_unchanged": true,
    "talk_still_says_ten_minutes": true
  },
  "Important-3": {
    "visual_and_talk_bindings_unchanged": true,
    "policy_hash_changed": true,
    "ledger_policy_fields": ["event_id", "value"],
    "ledger_has_policy_hash": false
  },
  "Important-4": {
    "draft_directory_resolves_relative_asset": true,
    "same_spec_after_move_to_deck_directory": "Required asset missing"
  }
}
```

The script below is retained as historical diagnostic evidence for the original plan. Its signatures and defect assertions apply to that pre-revision version and are not current verification. Run Appendix G in the revised handoff instead; it uses the corrected APIs and expectations. Both diagnostics read reference examples and temporary files, not production implementations.

```python
from pathlib import Path
import copy
import json
import re
import tempfile

root = Path.cwd()
path = root / 'docs/plans/2026-10-14-predictable-deck-generation-handoff.md'
text = path.read_text(encoding='utf-8')
blocks = re.findall(r'^```([^\n]*)\n(.*?)^```\s*$', text, re.M | re.S)
json_blocks = [json.loads(code) for kind, code in blocks if kind.strip() == 'json']
ns = {}
for kind, code in blocks:
    if kind.strip() == 'python' and any(key in code for key in ('class ContractError', 'def validate_spec', 'def approved_prompt_blocks')):
        exec(compile(code, '<plan-reference>', 'exec'), ns)
spec = json_blocks[0]
ledger_example = json_blocks[1]
with tempfile.TemporaryDirectory() as tmp:
    base = Path(tmp)
    original = ns['build_manifest'](spec, base)
    unused = copy.deepcopy(spec)
    unused['planning']['shared_visuals']['unused'] = {
        'meaning': 'An unrelated entity', 'appearance': 'Bright red triangle'
    }
    unused_manifest = ns['build_manifest'](unused, base)
    r1 = {
        'all_visual_bindings_unchanged': all(
            original['slides'][sid]['visual_hash'] == unused_manifest['slides'][sid]['visual_hash']
            for sid in original['slides']
        ),
        'render_prompt_changed': ns['approved_prompt_blocks'](spec, spec['slides'][0], []) !=
            ns['approved_prompt_blocks'](unused, unused['slides'][0], []),
    }
    facts = copy.deepcopy(spec)
    facts['slides'][1]['visible_copy']['labels'].append('10 minutes')
    facts['slides'][1]['speaker_notes']['text'] = 'The illustrative wait is ten minutes.\n\nLet me explain the implication.'
    facts['slides'][1]['claim_sources'] = [
        {'claim': 'Illustrative wait: 10 minutes', 'status': 'provided', 'source': 'Synthetic fixture version 1'}
    ]
    before = ns['build_manifest'](facts, base)
    revised_facts = copy.deepcopy(facts)
    revised_facts['slides'][1]['visible_copy']['labels'][-1] = '20 minutes'
    revised_facts['slides'][1]['claim_sources'][0] = {
        'claim': 'Illustrative wait: 20 minutes', 'status': 'provided', 'source': 'Synthetic fixture version 2'
    }
    after = ns['build_manifest'](revised_facts, base)
    r2 = {
        'visual_binding_changed': before['slides']['slide_02']['visual_hash'] != after['slides']['slide_02']['visual_hash'],
        'talk_binding_unchanged': before['slides']['slide_02']['notes_hash'] == after['slides']['slide_02']['notes_hash'],
        'talk_still_says_ten_minutes': 'ten minutes' in revised_facts['slides'][1]['speaker_notes']['text'],
    }
    output_change = copy.deepcopy(spec)
    output_change['planning']['brief']['output_profile'] = 'medavis'
    output_change['planning']['brief']['landing_title'] = 'A new branded title'
    output_manifest = ns['build_manifest'](output_change, base)
    r3 = {
        'visual_and_talk_bindings_unchanged': original['slides'] == output_manifest['slides'],
        'policy_hash_changed': original['policy_hash'] != output_manifest['policy_hash'],
        'ledger_policy_fields': sorted(ledger_example['policy']),
        'ledger_has_policy_hash': 'policy_hash' in ledger_example['policy'],
    }
    input_dir = base / 'input'
    deck_dir = base / 'deck'
    (input_dir / 'assets').mkdir(parents=True)
    deck_dir.mkdir()
    (input_dir / 'assets' / 'figure.png').write_bytes(b'synthetic asset bytes for hash-only test')
    with_asset = copy.deepcopy(spec)
    with_asset['slides'][1]['required_images'] = [
        {'path': 'assets/figure.png', 'role': 'strict source figure', 'fidelity': 'preserve labels and values'}
    ]
    ns['build_manifest'](with_asset, input_dir)
    try:
        ns['build_manifest'](with_asset, deck_dir)
    except ns['ContractError'] as exc:
        canonical_error = str(exc).split(':', 1)[0]
    else:
        canonical_error = None
    r4 = {
        'draft_directory_resolves_relative_asset': True,
        'same_spec_after_move_to_deck_directory': canonical_error,
    }
results = {'Important-1': r1, 'Important-2': r2, 'Important-3': r3, 'Important-4': r4}
assert all(r1.values()) and all(r2.values())
assert r3['visual_and_talk_bindings_unchanged'] and r3['policy_hash_changed'] and not r3['ledger_has_policy_hash']
assert r4['same_spec_after_move_to_deck_directory'] == 'Required asset missing'
print(json.dumps(results, indent=2, ensure_ascii=False))
print('These are reference-code and plan-schema probes; no feature implementation or live images were executed.')
```

