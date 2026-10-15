"""Independent synthetic deck inputs for managed-workflow tests.

This is test data, never a real user approval or backend capability claim.
"""

import json


_MANAGED_SPEC_JSON = r'''{
  "workflow_version": 2,
  "deck_name": "shared-account",
  "language": "English",
  "aspect_ratio": "16:9",
  "selected_image_backend": "scripts/image_gen.py",
  "goal": "Explain why a shared account helps",
  "deck_context": {
    "core_claim": "One account simplifies access",
    "canonical_terms": ["shared account"],
    "source_summary": "Illustrative, qualitative training example; no measured claims"
  },
  "style": {
    "name": "clean-professional",
    "visual_direction": "plain, readable diagrams",
    "color_palette": "navy and teal on white",
    "typography": "clear large headings"
  },
  "planning": {
    "brief": {
      "audience": "Technical colleagues",
      "purpose": "Explain the proposed access model",
      "notes_language": "English",
      "tone": "Conversational and precise",
      "output_profile": "none",
      "landing_title": null
    },
    "readiness": {"content": "partial", "visual": "missing"},
    "story": "Start with the access problem, then explain the shared-account model.",
    "shared_visuals": {
      "account": {"meaning": "One account", "appearance": "teal key icon"}
    },
    "delivery": {"voice": "natural-presenter", "speaker_names": []},
    "review_policy": "consolidated",
    "sample_strategy": {"required_slides": ["slide_02"]},
    "generation": {
      "backend_used": "scripts/image_gen.py",
      "tool_name": "scripts/image_gen.py",
      "mode": "generate",
      "reference_mode": "edit",
      "model": "gpt-image-2",
      "quality": "medium",
      "aspect_ratio": "16:9",
      "size": "2560x1440"
    },
    "unresolved": []
  },
  "slides": [
    {
      "number": 1,
      "title": "One account, fewer access steps",
      "role": "opening",
      "intent": "Introduce the proposed simplification",
      "key_points": ["Explain the qualitative access problem"],
      "visible_copy": {"title": "One account, fewer access steps", "body": [], "labels": []},
      "visual_plan": {
        "type": "illustration",
        "subject": "A shared account",
        "objects": ["account"],
        "relationships": [],
        "composition": "Title above a single account symbol"
      },
      "shared_visual_ids": ["account"],
      "depends_on": [],
      "claim_sources": [{"claim": "Qualitative illustrative proposal", "status": "proposed", "source": "Approved example"}],
      "required_images": [],
      "speaker_notes": {
        "text": "Hi everyone.\n\nLet me show you one way to make access simpler.\n\nFirst, we will look at the model.",
        "speaking_time_seconds": 20,
        "transition": "Introduce the model"
      }
    },
    {
      "number": 2,
      "title": "The shared-account model",
      "role": "explanation",
      "intent": "Show the model's relationships",
      "key_points": ["Explain the links without quantitative claims"],
      "visible_copy": {"title": "The shared-account model", "body": [], "labels": ["Shared account", "Provider"]},
      "visual_plan": {
        "type": "diagram",
        "subject": "Access relationships",
        "objects": ["account", "provider"],
        "relationships": [{"from": "account", "to": "provider", "label": "Access"}],
        "composition": "Account on the left, provider on the right"
      },
      "shared_visual_ids": ["account"],
      "depends_on": ["slide_01"],
      "claim_sources": [{"claim": "Illustrative relationship", "status": "proposed", "source": "Approved example"}],
      "required_images": [],
      "speaker_notes": {
        "text": "Now, here is the model.\n\nThe key is the same account we just introduced.\n\nThat is the proposal. What questions do you have?",
        "speaking_time_seconds": 30,
        "transition": "Close and invite questions"
      }
    }
  ]
}'''


def managed_spec():
    """Return a fresh complete managed input with no runtime approvals."""
    return json.loads(_MANAGED_SPEC_JSON)

# The helpers below exercise real bundled CLIs with explicitly synthetic decisions.
def run_cli(script, *args):
    import os
    from pathlib import Path
    import subprocess
    import sys
    return subprocess.run(
        [sys.executable, "-B", str(Path(__file__).resolve().parents[1] / script),
         *[str(a) for a in args]], capture_output=True, text=True, encoding="utf-8",
        env=dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1"),
    )


def write_spec(path, spec):
    import json
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")


def fixture_image(path, color="white"):
    from PIL import Image
    path.parent.mkdir(parents=True, exist_ok=True)
    Image.new("RGB", (1600, 900), color=color).save(path)


def approve_fixture(deck, spec=None):
    from pathlib import Path
    from planning_contract import build_manifest
    spec = managed_spec() if spec is None else spec
    draft = Path(deck) / "input.json"
    write_spec(draft, spec)
    result = run_cli("record_plan_approval.py", deck, "--spec", draft, "--approve",
                     "--scope", "all", "--expected-plan-hash",
                     build_manifest(spec, draft.parent)["plan_hash"],
                     "--evidence", "SYNTHETIC TEST whole-plan user decision")
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return spec


def approve_fixture_sample(deck, sid="slide_02"):
    path = deck / "candidate.png"
    fixture_image(path)
    result = run_cli("record_plan_approval.py", deck, "--approve-sample", sid,
                     "--image", path, "--backend-used", "scripts/image_gen.py",
                     "--evidence", "SYNTHETIC TEST sample user decision")
    if result.returncode:
        raise AssertionError(result.stdout + result.stderr)
    return path

def compile_fixture(deck, spec=None, capacity=1):
    spec=approve_fixture(deck,spec)
    approve_fixture_sample(deck)
    result=run_cli("prepare_slide_prompts.py","--spec",deck/"deck_spec.json","--out-dir",deck,
                   "--max-concurrent-slides",capacity)
    if result.returncode:
        raise AssertionError(result.stdout+result.stderr)
    return spec


def dispatch_fixture(deck,sid="slide_01",agent="fixture-agent"):
    return run_cli("record_slide_dispatch.py",deck,"--slide",sid,"--agent-id",agent)


def result_fixture(deck,sid="slide_01",agent="fixture-agent",color="white"):
    path=deck/f"{sid}-candidate.png"
    fixture_image(path,color)
    return run_cli("record_slide_result.py",deck,"--slide",sid,"--agent-id",agent,
                   "--backend-used","scripts/image_gen.py","--selected-source",path,
                   "--qa-note","SYNTHETIC TEST worker return")


def qa_fixture(deck,sid="slide_01",decision="--pass"):
    return run_cli("record_slide_qa.py",deck,"--slide",sid,decision,
                   "--evidence","SYNTHETIC TEST agent inspection")

def completed_fixture(deck,spec=None):
    spec=compile_fixture(deck,spec)
    for sid in ("slide_01",):
        r=dispatch_fixture(deck,sid)
        if r.returncode:
            raise AssertionError(r.stderr)
        r=result_fixture(deck,sid)
        if r.returncode:
            raise AssertionError(r.stderr)
    for sid in ("slide_01","slide_02"):
        r=qa_fixture(deck,sid)
        if r.returncode:
            raise AssertionError(r.stderr)
    r=run_cli("record_slide_qa.py",deck,"--deck-pass","--evidence","SYNTHETIC TEST full-sequence QA")
    if r.returncode:
        raise AssertionError(r.stderr)
    return spec




