"""Generate text-only behavioral evidence. No runtime approval ledger or image jobs."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent
ENC = "utf-8"

# After the schema seam has been exercised, rebuild the compatible representation
# from the immutable original evidence rather than regenerating the rejected shape.
if (ROOT / "schema-red" / "D1.json").exists():
    import runpy
    runpy.run_path(str(ROOT / "validate_schema_application.py"), run_name="__main__")
    raise SystemExit(0)

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding=ENC)

def slide(n, title, body, visual, notes, *, status="proposed", labels=None,
          depends=None, transition="", before="", after="", note_status=None):
    return {
        "id": f"slide_{n:02d}", "internal_order": n, "language": "English",
        "purpose": after, "role": title,
        "audience_state": {"before": before, "after": after},
        "visible_copy": {"title": title, "body": body, "critical_labels": labels or [], "critical_values": []},
        "visual_plan": visual,
        "source_mapping": {"visible_copy": status, "visual_plan": "proposed", "speaker_notes": note_status or status,
                           "organization_measurements": "not supplied; none invented"},
        "required_images": [], "shared_visual_ids": ["individual_account", "provider_tile"],
        "depends_on": depends or [],
        "speaker_notes": {"text": notes, "speaking_time_seconds": None, "transition": transition},
    }

def visual(kind, subject, objects, relationships, composition):
    return {"type": kind, "subject": subject, "objects": objects,
            "relationships": relationships, "approximate_composition": composition}

GENERATION = {
    "selected_image_backend": "codex-gpt-image", "underlying_model": "gpt-image-2",
    "aspect_ratio": "16:9", "size": "2560x1440", "tool": "codex-gpt-image bridge",
    "input_method": "MOCK/TEST image-capable bridge; real schema and attached snapshots still require verification",
    "mode": "generate", "reference_mode": "image-conditioned input when a style sample is used",
    "capability_basis": "TEST fixture only. Native image_gen schema in this context has no explicit size parameter; no native size capability is invented. No probe or API call occurred.",
}

CLEAN_STYLE = {
    "name": "proposed clean technical diagrams",
    "palette": "white background; charcoal text; blue individual account; teal provider tiles; gray connectors",
    "typography": "plain sans-serif; clear title and body hierarchy; no decorative lettering",
    "visual_language": "simple outlined diagrams, consistent account/provider symbols; no logos or factual chart",
    "composition": "layout varies with slide role; use whitespace and readable text",
}

SUPPLIED_STYLE = {
    "name": "MOCK/TEST supplied approved clean technical visual reference",
    "status": "reused supplied fixture decision; no new style vote",
    "rules": ["Retain the approved reference palette, typography and clean diagram language.",
              "Use new compositions for the local content; do not copy reference text.",
              "Exact palette/font extraction cannot be verified without the actual reference image."],
    "reference": "MOCK/TEST clean-reference fixture; binary image not supplied in this text-only application",
}

def spec(case, audience, purpose, slides, readiness, style, sample, reused=None):
    return {
        "workflow_version": 2,
        "test_context": {"case": case, "kind": "text-only behavioral application",
                         "actual_user_approval_recorded": False,
                         "fixture_concretization": "16:9 plus codex-gpt-image/gpt-image-2 is a TEST capability fixture, not a measured live backend or an organization fact.",
                         "reused_fixture_decisions": reused or []},
        "deck": {"title": "Shared account proposal", "language": "English", "audience": audience,
                 "purpose": purpose, "delivery_intent": "internal live discussion with speaker notes",
                 "readiness": readiness, "story": [s["purpose"] for s in slides],
                 "canonical_terminology": {
                     "shared account": "one individual's account used across providers; never multiple people sharing a password",
                     "provider access": "permission to use an individual provider; distinct from signing in"},
                 "shared_visual_identities": {
                     "individual_account": "one personal account symbol; same meaning and appearance throughout",
                     "provider_tile": "repeated provider shape; distinct providers, no claim about real provider count"},
                 "style": style, "selected_image_backend": "codex-gpt-image", "aspect_ratio": "16:9",
                 "output_profile": "plain", "landing_title": None, "visible_numbering": "none",
                 "review_policy": "consolidated", "required_representative_samples": sample},
        "planning": {"generation": GENERATION.copy()}, "slides": slides,
    }

D1 = [
    slide(1, "Shared login: a proposal to examine",
          ["One personal account across services", "Expected benefit: less repeated access work", "Trade-offs need investigation"],
          visual("proposal overview", "one personal identity across services", ["individual account", "three illustrative service tiles"],
                 ["one account connects to multiple distinct services"], "account at left; three services stacked at right; restrained connecting lines"),
          "Hi everyone.\n\nI want to walk through a shared login proposal and the trade-offs it brings.\n\nThe idea we will examine is one personal account across services. We expect that could reduce some repeated access work, but we do not have measurements yet.\n\nLet me start with the access pattern we are using as a working assumption.",
          after="Know the proposal, the discussion purpose and the absence of measured benefit", transition="Move from the proposal to the current-pattern assumption"),
    slide(2, "Access today: a working assumption",
          ["Separate service accounts", "Repeated sign-in and account recovery", "Confirm this matches our environment"],
          visual("separate paths", "assumed current access pattern", ["one person", "three service-account pairs"],
                 ["each illustrative service has a separate account path"], "three separate horizontal paths; no shared identity hub"),
          "Imagine a colleague moving between three services. This is an illustration, not a report about a particular person.\n\nFor the discussion, I am assuming each service has its own account and access steps. That can mean choosing credentials again or dealing with recovery separately.\n\nWe need to confirm that pattern against our actual environment. With that assumption visible, we can look at what the proposal changes.",
          status="proposed working assumption, not supplied organization fact", depends=["slide_01"],
          before="Know this is an unmeasured proposal", after="Understand the illustrative current pattern and the need to confirm it",
          transition="Compare the separate paths with the proposed shared identity"),
    slide(3, "The proposed model",
          ["One personal identity", "Reusable sign-in session where supported", "Separate permissions for each service"],
          visual("identity and access diagram", "proposed identity/session model with separate permissions",
                 ["individual account hub", "three service tiles", "a gate inside each service boundary"],
                 ["account links to each service", "session reuse is conditional on service support", "permissions are checked at each service"],
                 "shared identity hub across top; three service boundaries below, each with its own small gate"),
          "Now, here is the model I propose we discuss. The account belongs to one person and can be recognised across services.\n\nWhere a service supports it, the sign-in session could be reused. That is a design condition to check, not something we have already proved.\n\nSigning in tells a service who the person is. Permissions still decide what that person can do in that service. Keeping those responsibilities clear gives us a basis for discussing the benefit.",
          depends=["slide_01", "slide_02"], before="Understand the current-pattern assumption",
          after="Distinguish personal identity, conditional session reuse and service permissions", transition="Explain the possible benefit mechanism without numerical claims"),
    slide(4, "Where time could be saved",
          ["Fewer account credentials to manage", "Reuse sign-in where supported", "No time-saving measurements yet"],
          visual("qualitative journey comparison", "possible reduction in repeated access steps",
                 ["current-pattern lane", "proposed lane", "same three illustrative services"],
                 ["current-pattern lane repeats separate account steps", "proposed lane reuses the personal account; session reuse remains conditional"],
                 "two horizontal lanes; illustrate account/sign-in actions with icons; no times, percentages, bar lengths or invented metric"),
          "So, where might the time saving come from?\n\nFirst, a person could have fewer account credentials to keep track of. Second, where session reuse works, they may avoid some repeated sign-in steps as they move between services.\n\nThose are the mechanisms we expect to help. We cannot say how much time they save yet, and the benefit will depend on how people actually move between services.\n\nNow let us look at the questions that come with sharing the sign-in path.",
          depends=["slide_02", "slide_03"], before="Understand the proposed model and its conditions",
          after="Understand qualitative expected benefit without interpreting it as measured outcome", transition="Move from possible benefit to trade-offs"),
    slide(5, "Trade-offs to investigate",
          ["Shared sign-in dependency", "Account recovery and revocation", "Provider permissions and ownership"],
          visual("three investigation lenses", "questions raised by a shared identity path",
                 ["common identity hub", "recovery loop", "provider permission gates"],
                 ["services depend on a shared identity path", "account lifecycle affects the shared identity", "provider permissions still have distinct owners"],
                 "three equally weighted panels; show dependency, recovery and permission concepts; no severity ranking"),
          "A shared sign-in path gives us a common dependency to design carefully. What should happen if that path is unavailable?\n\nWe also need a clear account lifecycle. Who helps with recovery, and how should access be removed when it is no longer appropriate?\n\nThen there is ownership: who manages the personal account, and who grants access inside each provider? These are investigation questions. I am not presenting settled implementation decisions.\n\nThat leaves us with a useful set of questions for the engineering discussion.",
          depends=["slide_03", "slide_04"], before="Know the expected benefit is unmeasured",
          after="Recognise common dependency, account lifecycle and permissions as unresolved trade-offs", transition="Turn unresolved trade-offs into discussion questions"),
    slide(6, "Questions for investigation",
          ["Which assumptions need evidence?", "Which trade-offs need a design spike?", "How would we evaluate a trial?"],
          visual("discussion map", "questions that connect the proposal to possible investigation",
                 ["current-pattern assumption card", "trade-off cards", "three discussion question cards"],
                 ["current assumptions inform evidence questions", "trade-offs inform a possible design spike", "a trial would need agreed evaluation criteria"],
                 "inputs on the left; three question cards on the right; an open discussion area, no assigned people or dates"),
          "So, we have a proposal, a possible benefit mechanism and a set of trade-offs.\n\nI would like us to check which assumptions need evidence and which design questions deserve a small investigation. If we later choose a trial, we should agree how to evaluate it before claiming a saving.\n\nWhat have we missed, and where would you start?",
          depends=["slide_02", "slide_04", "slide_05"], before="Understand proposal and trade-offs",
          after="Be ready to discuss evidence and design questions without an implied rollout commitment", transition="Invite the room to discuss")
]

FIXED_NOTES = [
    "Hi everyone.\n\nLet me start with the access problem.",
    "Now, here is the proposal.\n\nThe same account connects these providers.",
    "So, those are the two decisions.\n\nWhat questions do you have?",
]

D2 = [
    slide(1, "Access today", ["Separate accounts"],
          visual("separate access paths", "separate accounts across providers", ["three provider tiles", "one account icon for each provider"],
                 ["each account icon connects only to its own provider"], "three separated parallel paths; fixed title and body above; no extra labels"),
          FIXED_NOTES[0], status="provided fixed copy and notes", after="See separate account/provider paths", transition="The supplied next note introduces the proposal"),
    slide(2, "A shared account", ["One account across providers"],
          visual("shared hub", "one account connecting multiple providers", ["one individual account icon", "the same three provider tiles"],
                 ["one account connects to every illustrative provider"], "account at left, providers at right; fixed title and body above; no extra labels"),
          FIXED_NOTES[1], status="provided fixed copy and notes", depends=["slide_01"], before="See the separated paths",
          after="See the contrast: one account connects the provider set", transition="The supplied next note opens ownership and rollout discussion"),
    slide(3, "What we need to decide", ["Ownership and rollout"],
          visual("two decision concepts", "ownership and rollout questions", ["account with ownership/hand symbol", "small provider set expanding to larger illustrative set"],
                 ["ownership symbol refers to the shared account", "rollout symbol shows staged expansion without dates or quantities"],
                 "two balanced pictorial areas; only the supplied title/body are rendered as text; no implied implementation answer"),
          FIXED_NOTES[2], status="provided fixed copy and notes", depends=["slide_02"], before="Understand the shared-account proposal",
          after="See ownership and rollout as discussion topics", transition="Preserve the supplied invitation for questions")
]

D3 = [
    slide(1, "One account across providers", ["A proposed way to move between providers"],
          visual("journey overview", "one person's account across two illustrative providers", ["person/account symbol", "two provider tiles"],
                 ["the same account links to both providers"], "a short left-to-right journey in the existing clean reference style"),
          "Hi everyone.\n\nLet me show you the access journey we are proposing. Imagine a colleague who needs to open two different providers. This is a simple illustration.\n\nThe idea is that the colleague uses their own account for both. Let us follow that journey one step at a time.",
          after="Understand the deck explains a proposed personal-account journey", transition="Start at the personal account"),
    slide(2, "Start with your account", ["Use your own account", "Sign in before opening a provider"],
          visual("journey start", "a person signs in using their personal account", ["same person/account symbol", "sign-in doorway", "first provider tile"],
                 ["person uses the account before entering the provider path"], "large account symbol on left; sign-in doorway in middle; first provider at right"),
          "First, our colleague starts with their own account.\n\nSigning in lets the service recognise who is arriving. In this proposed journey, that is the account the colleague will use as they move between providers.\n\nNow they can choose the first provider.",
          depends=["slide_01"], before="Know this is one person's account", after="Understand where sign-in sits in the journey", transition="Move into the first provider"),
    slide(3, "Open a provider", ["Choose the provider", "Your access is checked there"],
          visual("provider entry", "recognised person opens a provider and access is checked", ["same account symbol", "highlighted first provider", "entry gate"],
                 ["account connects to selected provider", "gate belongs to that provider"], "first provider highlighted; second provider quieter in background; simple gate at entry"),
          "Now the colleague chooses the provider they need.\n\nThe proposal keeps a separate access check there. Having an account answers who the person is; the provider still needs to decide whether the person may use it.\n\nThat matters when the colleague moves to another provider.",
          depends=["slide_01", "slide_02"], before="Know the account recognises a person", after="Understand that provider permission is a separate check", transition="Switch providers without implying automatic permission"),
    slide(4, "Switch to another provider", ["Use the same account", "Access can differ by provider"],
          visual("provider switch", "the same account reaches a second provider with its own permission check", ["same account", "first provider", "highlighted second provider", "one gate per provider"],
                 ["identity remains the same", "provider permissions are distinct"], "journey advances right; account appearance stays constant; second provider highlighted"),
          "So, the colleague moves to the second provider using the same account.\n\nThat does not mean the two providers give the colleague the same access. Each provider can have its own permissions.\n\nWe also have not settled every sign-in detail. Using the same account alone does not tell us whether another sign-in step will appear. What stays clear is the personal account and the separate provider access.",
          depends=["slide_02", "slide_03"], before="Know access is checked at a provider", after="Understand account reuse without assuming automatic access or proven session reuse", transition="Recap what the access journey changes"),
    slide(5, "What this changes", ["One account to recognise", "Provider access still matters", "Support details need investigation"],
          visual("journey recap", "account continuity and distinct provider access", ["same account", "both providers with entry gates", "support question symbol"],
                 ["account is reused across both provider paths", "each gate remains distinct", "support handling remains an open question"],
                 "compact journey across top; account and access concepts beneath; open support question at right"),
          "That is the access journey in the proposal: the person carries one account across providers, and provider access remains a separate question.\n\nFor operations, the support path will matter too. We still need to work out how account questions and provider access questions reach the right help.\n\nIs the journey clear, and where would someone need more guidance?",
          depends=["slide_01", "slide_03", "slide_04"], before="Understand the complete proposed journey",
          after="Be able to explain the proposed journey and identify support questions without a technical decision request", transition="Invite understanding questions")
]

MIXED = json.loads(json.dumps(D2[:2]))
MIXED.append(slide(3, "Next steps to investigate",
                   ["Who owns the account?", "How is provider access granted?", "What should a pilot test?"],
                   visual("investigation map", "open questions about the shared account", ["shared account", "provider access gates", "small illustrative pilot path"],
                          ["ownership question points to the account", "access question points to provider entry", "pilot question tests the proposed journey"],
                          "three question areas below the existing shared-account motif; keep the already approved look"),
                   "So, we have seen the separate-account pattern and the proposed shared account.\n\nI suggest we leave this discussion with three things to investigate: who owns the account, how provider access is granted, and what a small pilot would need to test.\n\nThose are proposed next steps. We can use the discussion to choose where to start and what information we need.\n\nWhat would you put first?",
                   status="proposed expansion of the supplied phrase 'decide next steps'", depends=["slide_01", "slide_02"],
                   before="Have seen the fixed current and proposed diagrams", after="Be ready to choose investigation priorities", transition="Invite prioritisation"))

SCENARIOS = {
    "D1": spec("D1", "engineering colleagues", "Help colleagues understand the proposal and its trade-offs.", D1,
               {"content": "topic and lack of measurements provided; complete story/copy/talk proposed", "visual": "unresolved; clean technical system proposed"}, CLEAN_STYLE,
               [{"id": "slide_03", "reason": "tests the shared identity, conditional session relation and per-service permission boundary; more representative than a cover"}]),
    "D2": spec("D2", "internal technical audience", "Internal technical discussion; decide what to investigate next", D2,
               {"content": "all three supplied titles, bodies and note paragraphs fixed", "visual": "clean diagrams requested; objects, connections and layout proposed"}, CLEAN_STYLE,
               [{"id": "slide_02", "reason": "tests the shared-account hub, provider identities and exact fixed copy"}]),
    "D3": spec("D3", "nontechnical operations colleagues", "Understand the access journey", D3,
               {"content": "topic ready; audience/purpose clarified once; all copy and talk proposed", "visual": "supplied approved clean technical reference; compatible backend/ratio fixture reused"}, SUPPLIED_STYLE,
               [{"id": "clean_reference_fixture", "action": "reuse approved compatible sample style-only", "suitability": "clean diagram style, simple account/provider symbols and short labels fit the proposed operations journey; compatible ratio/backend supplied by the mock fixture", "accepts_new_content_pages": False}],
               ["approved clean technical reference", "compatible existing backend and ratio"]),
    "mixed": spec("mixed", "internal technical audience", "Internal technical discussion; decide what to investigate next", MIXED,
                  {"content": "slides 1–2 fixed; slide 3 is only an intention and needs copy/talk expansion", "visual": "shared look already approved; local compositions for all three slides proposed"}, SUPPLIED_STYLE,
                  [{"id": "slide_02", "reason": "calibrate the proposed hub composition in the already approved look; no new style-selection interview"}],
                  ["approved shared look", "fixed slide 1–2 copy and notes"]),
}

TRANSCRIPTS = {
    "D1": """# D1 actual text-only interaction path

Every user turn below is SCRIPTED MOCK/TEST. These are not real approvals.

## Input and readiness response

USER INPUT: “Make a presentation for our engineering colleagues, in English. We want to explain a shared login proposal. We think it will save users time, but we have no measurements yet. Give me intelligent recommendations; I don't want a long interview.”

ASSISTANT: “I have the audience, language, topic and evidence limit. I will keep the benefit qualitative and make the proposal and its trade-offs concrete. What should colleagues leave with? I recommend understanding the proposal and its trade-offs so the discussion can surface the right engineering questions.”

MOCK/TEST USER: “Help colleagues understand the proposal and its trade-offs.”

ASSISTANT RECOMMENDATION: “I recommend a six-part story: the proposal, an explicitly assumed current access pattern, the proposed account/session/permission model, the possible saving mechanism, trade-offs, and investigation questions. I would interpret ‘shared login’ as one personal account across services. Session reuse is conditional on service support; permissions stay with each service. We have no measurements, so there will be no time-saving number or chart. The current separate-account pattern is a working assumption to confirm. Shall I draft with those substantive assumptions visible?”

MOCK/TEST USER: “Yes, use that interpretation and those clearly labelled assumptions. Keep the benefit qualitative.”

## Consequential presentation defaults

ASSISTANT: “I recommend 16:9 for this internal screen presentation. Shall we use that ratio?”

MOCK/TEST USER: “Yes, 16:9.”

ASSISTANT: “For the TEST capability fixture, codex-gpt-image is available: gpt-image-2 through Codex OAuth, 2560×1440, with image-reference input support. Native image_gen has no explicit size parameter in the provided schema, so I cannot offer it as a verified ratio-capable option. No real probe or cost verification has occurred. Shall the mock run lock codex-gpt-image?”

MOCK/TEST USER: “Yes, lock that mock backend.”

ASSISTANT: “I recommend a clean diagram style: white background, charcoal sans-serif text, a blue account symbol and teal provider tiles, varied layouts with whitespace. An alternative is a warm explanatory look with an off-white background, dark text, rounded diagrams and a coral accent. The clean style makes identity and permission boundaries easier to compare. I also recommend a plain deck with no visible page numbers and consolidated image review after the first production-batch check. Shall I use those recommendations?”

MOCK/TEST USER: “Yes, use the clean style, plain output, no page numbers, and consolidated review.”

## Produced combined plan and talk

ASSISTANT: “Here is the whole draft, including exact visible wording, diagram objects and connections, and every speaker note. Slide 2's current pattern is an assumption; session reuse is conditional; the saving has no measurements. The representative sample would be slide 3 because it tests account identity, session reuse and separate permissions. The opening note starts ‘Hi everyone’ and sets the evidence limit; the full talk is available now. Please name any exceptions to the copy, model, visual meaning or presenter voice. If there are none, approve the complete draft plan and talk.”

The material shown is preserved verbatim in outline.draft.md, speech.draft.md and deck_spec.draft.json. No further note-calibration interview was needed for this short, natural internal explanation.

MOCK/TEST USER: “For this test, approve the complete draft plan and talk with no exceptions.”

ASSISTANT ACTION: Wrote draft evidence only. Did not record a real approval, compile managed jobs, generate a sample, or request an image acceptance without an image. The next real action waits for actual plan/talk evidence and a verified backend, then compiles the explicit slide_03 sample. A sample-image approval must be based on the actual rendered sample.
""",
    "D2": """# D2 actual text-only interaction path

Every user acceptance below is SCRIPTED MOCK/TEST, not a real approval.

## Supplied fixed material

Audience/purpose: “Internal technical discussion; decide what to investigate next.” English. The user asks for clean diagrams and fixes the copy and notes.

Slide 1 title: “Access today”. Body: “Separate accounts”. Notes exactly: “Hi everyone.\\n\\nLet me start with the access problem.”

Slide 2 title: “A shared account”. Body: “One account across providers”. Notes exactly: “Now, here is the proposal.\\n\\nThe same account connects these providers.”

Slide 3 title: “What we need to decide”. Body: “Ownership and rollout”. Notes exactly: “So, those are the two decisions.\\n\\nWhat questions do you have?”

The \\n markers above describe literal note newlines. The JSON strings and speech.draft.md contain the actual newlines.

ASSISTANT: “Your three titles, body lines and note paragraphs are already ready. I will retain them exactly. The remaining work is visual: separate account/provider pairs on slide 1, one shared account connected to the same providers on slide 2, and ownership plus staged-rollout concepts on slide 3. The three provider tiles are illustrative, not a claimed provider count. I recommend simple white-background diagrams, blue account symbols and teal provider tiles, using only your supplied words as visible text. Does that visual meaning fit?”

MOCK/TEST USER: “Yes, use those visual connections and keep every supplied word and note unchanged.”

ASSISTANT: “I recommend 16:9. Shall we use it?”

MOCK/TEST USER: “Yes.”

ASSISTANT: “The only available backend in the MOCK/TEST fixture is codex-gpt-image, gpt-image-2 via Codex OAuth at 2560×1440, with reference-image inputs. Native image_gen lacks an explicit size parameter here; no live probe or generation occurred. Shall I lock this fixture backend?”

MOCK/TEST USER: “Yes, for this test.”

ASSISTANT: “I recommend plain output, no visible numbering and consolidated review. Slide 2 is the representative sample because it tests the shared account and provider relationships. Please review the whole visual plan by exception alongside the exact supplied copy and talk. Approve these visual/default choices, or name changes?”

MOCK/TEST USER: “For this test, approve that whole visual plan, sample strategy, plain output and consolidated review. The supplied talk remains fixed.”

ASSISTANT ACTION: Produced the three-page draft and the exact supplied talk. No audience re-interview, new style menu, note rewrite or per-page approval conversation. Exact notes are separately retained in supplied_notes.json and checked against the draft. Real sample generation and image acceptance are still pending; no approval ledger or managed job was manufactured.
""",
    "D3": """# D3 actual text-only interaction path

Every interaction below is SCRIPTED MOCK/TEST. The approved reference and compatible backend/ratio are supplied test preconditions, not a claim that an actual image was inspected here.

USER INPUT: “Use this approved clean technical visual reference. The topic is a shared-account model. I have not decided the audience or the desired decision.”

ASSISTANT: “The approved clean technical reference and its compatible backend and ratio are ready to reuse. Before I expand the shared-account story, who needs to understand it and what should they leave with? That will determine whether the deck explains an access journey or examines engineering decisions.”

MOCK/TEST USER: “Nontechnical operations colleagues; understand the access journey.”

ASSISTANT: “I recommend following one hypothetical colleague: start with their personal account, open a provider, move to a second provider, and recap what stays shared and what is still checked per provider. I would explain ‘shared account’ as one person's account across providers. Provider access remains a separate check; the sign-in and support details are open questions. I will use plain language in the existing visual style. Shall I draft that proposed journey?”

MOCK/TEST USER: “Yes, use that journey and those clearly proposed meanings.”

ASSISTANT ACTION: Reused the already approved clean reference; did not offer another style menu, backend menu or ratio choice. The test fixture is concretised as existing codex-gpt-image/gpt-image-2 at 16:9, 2560×1440. These concrete backend details are test assumptions because the scenario supplied compatibility rather than actual runtime metadata.

ASSISTANT: “Here is the complete five-slide access journey and talk. I recommend plain output without visible numbering and consolidated review. I propose reusing the supplied compatible approved clean reference as the style-only calibration sample: its simple account/provider diagrams and short labels suit this journey. Reusing it does not approve any new content page. Please review the new copy, diagram meanings and talk by exception; the existing style/backend/ratio decisions carry forward. Any exceptions, or approve this complete draft and these output/review choices?”

MOCK/TEST USER: “For this test, approve the complete draft and those choices. Reuse the existing style calibration.”

ASSISTANT ACTION: Produced new audience-appropriate copy and talk while retaining ready visual decisions. Actual reference bytes, accepted-sample provenance, input attachments and ratio remain unverified in this text-only fixture. A real run must verify the compatible reuse record; it must wait rather than redo a ready style interview or invent an acceptance ledger.
""",
    "mixed": """# Mixed readiness actual text-only interaction path

Scripted user turns are MOCK/TEST. Shared look is a supplied approved fixture; no actual image approval is asserted.

INPUT: D2 slides 1–2 supplied and fixed. Slide 3 contains only the intention “decide next steps”, with no fixed copy or notes. Audience/purpose remains an internal technical discussion to decide what to investigate next. The shared look is already approved.

ASSISTANT: “Slides 1 and 2 already settle their wording and notes. I will retain those exact paragraphs and use the approved look. Slide 3 still needs its actual words and talk. I recommend ‘Next steps to investigate’, with three proposed questions: who owns the account, how provider access is granted, and what a pilot should test. Those questions connect the shared-account diagram to the next investigation. Shall I expand only that unfinished page?”

MOCK/TEST USER: “Yes, propose those questions and notes for slide 3. Keep slides 1–2 fixed and reuse the look.”

ASSISTANT ACTION: Drafted only slide 3's content/talk; proposed local visual compositions for all three pages. Reused slide 1–2 notes exactly and did not add spoken transitions to their fixed text. The new slide 3 opening carries the transition from the earlier pages.

ASSISTANT: “The approved look can carry forward. Ratio/backend were not supplied for this case. I recommend 16:9; shall we lock that?”

MOCK/TEST USER: “Yes.”

ASSISTANT: “For this MOCK/TEST fixture, codex-gpt-image is the available specific backend, using gpt-image-2 through Codex OAuth at 2560×1440 with image-reference support. No live probe occurred. Shall the test lock it?”

MOCK/TEST USER: “Yes, for this test.”

ASSISTANT: “Here is the combined three-page plan. Slides 1–2 have exact fixed copy and talk; slide 3 has proposed new copy, diagram connections and talk. I recommend plain output, no numbering, consolidated review, and slide 2 as the composition sample in the existing look. Please name exceptions to the visual proposals or the new slide 3; otherwise approve those affected scopes and output/review choices.”

MOCK/TEST USER: “For this test, approve the visual proposals and new slide 3, plus those defaults. Slides 1–2 retain their fixed content and notes.”

ASSISTANT ACTION: Produced one combined draft while focusing expansion on the unfinished page. Did not classify the whole deck as topic-only, rewrite fixed notes or reopen the shared look. Real plan approval, reference verification and actual sample/image acceptance remain pending.
""",
}

for case, data in SCENARIOS.items():
    folder = ROOT / case
    write(folder / "deck_spec.draft.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    out = [f"# {case} combined draft: exact copy, visual meaning and talk", "",
           "TEXT-ONLY MOCK/TEST EVIDENCE — no real user approval or rendered image.", "",
           f"Audience: {data['deck']['audience']}", f"Purpose: {data['deck']['purpose']}",
           "Output recommendation: plain; no visible numbering; consolidated review.", ""]
    talk = []
    for item in data["slides"]:
        n = item["internal_order"]
        copy = item["visible_copy"]
        out += [f"## Slide {n}: {copy['title']}", "", "Exact visible title:", "", copy["title"], "",
                "Exact visible body:", "", *copy["body"], "",
                f"Source/proposal status: {item['source_mapping']['visible_copy']}", "",
                "Intended visual meaning:", "", item["visual_plan"]["subject"], "",
                "Objects: " + "; ".join(item["visual_plan"]["objects"]),
                "Connections: " + "; ".join(item["visual_plan"]["relationships"]),
                "Composition: " + item["visual_plan"]["approximate_composition"], "",
                "Dependencies: " + (", ".join(item["depends_on"]) or "opening; no earlier-page dependency"),
                "Audience after: " + item["audience_state"]["after"], "",
                "Speaker notes:", "", item["speaker_notes"]["text"], ""]
        talk += [f"## Slide {n}: {copy['title']}", "", item["speaker_notes"]["text"], ""]
    write(folder / "outline.draft.md", "\n".join(out))
    write(folder / "speech.draft.md", "\n".join(talk))
    write(folder / "interaction.md", TRANSCRIPTS[case])
    actions = {
        "case": case,
        "actually_performed": ["read current skill and phase-linked guides", "write UTF-8 draft plan, outline, speech and scripted interaction evidence"],
        "mock_only": ["scripted user decisions in interaction.md", "backend compatibility/availability fixture", "existing visual approvals where supplied"],
        "waiting_for_real_input_or_approval": ["actual human current plan/talk decision", "actual schema/backend and image-input verification", "source/reference bytes for supplied look or reused sample", "actual sample rendering/acceptance or verified existing sample reuse", "full production authorization and first-batch inspection", "actual final images, consolidated image approval and complete-sequence QA", "verified PPTX assembly"],
        "not_performed": ["live generation", "API calls", "job compilation", "approval-ledger writes", "worker dispatch", "image QA claims", "PPTX assembly", "commit", "push", "install"],
    }
    write(folder / "actions.json", json.dumps(actions, indent=2) + "\n")

write(ROOT / "D2" / "supplied_notes.json", json.dumps(FIXED_NOTES, ensure_ascii=False, indent=2) + "\n")
write(ROOT / "mixed" / "supplied_notes.json", json.dumps(FIXED_NOTES[:2], ensure_ascii=False, indent=2) + "\n")

# Check actual written artifacts, not an approval or a policy pass assessment.
checks = {"utf8_json_reads": [], "fixed_copy_and_note_equality": [], "speech_exact_note_mapping": [], "counts": {}}
for case, original in SCENARIOS.items():
    folder = ROOT / case
    loaded = json.loads((folder / "deck_spec.draft.json").read_text(encoding=ENC))
    assert loaded == original
    checks["utf8_json_reads"].append(case)
    text = (folder / "speech.draft.md").read_text(encoding=ENC)
    expected = "\n".join(part for s in loaded["slides"] for part in (f"## Slide {s['internal_order']}: {s['visible_copy']['title']}", "", s["speaker_notes"]["text"], ""))
    assert text == expected
    checks["speech_exact_note_mapping"].append(case)
    checks["counts"][case] = len(loaded["slides"])
for case, count in (("D2", 3), ("mixed", 2)):
    loaded = json.loads((ROOT / case / "deck_spec.draft.json").read_text(encoding=ENC))
    for i in range(count):
        assert loaded["slides"][i]["visible_copy"] == D2[i]["visible_copy"]
        assert loaded["slides"][i]["speaker_notes"]["text"] == FIXED_NOTES[i]
    checks["fixed_copy_and_note_equality"].append({"case": case, "preserved_slides": count, "equal": True})
write(ROOT / "verification.json", json.dumps(checks, indent=2) + "\n")
write(ROOT / "README.md", """# Input readiness behavioral evidence

Four fresh, independent text-only applications of the current codex-ppt skill are in D1/, D2/, D3/ and mixed/.

Each contains deck_spec.draft.json, outline.draft.md (exact copy, visual plan and talk together), speech.draft.md, interaction.md (actual written question/card wording with scripted MOCK/TEST user decisions) and actions.json. D2/ and mixed/ retain supplied_notes.json as preservation evidence. verification.json records UTF-8 reads, speech mappings, fixed-copy/note equality and actual content-page counts: 6, 3, 5 and 3.

The approved-reference/compatible-backend inputs are test fixtures. No actual reference image was attached or inspected. The bridge name, 16:9 ratio and gpt-image-2 size concretise the test, and are not a claim of measured live availability. No live image/API calls, managed approval ledger, compiled job, worker, rendered image, QA acceptance or PPTX exists. The draft JSON follows the guide's combined-plan fields; it was not validated against implementation schemas or installed as a canonical approved spec.

D1 presents a complete qualitative proposal and labels the current pattern, architecture choices and expected benefit as assumptions/proposals. No company metric, measured saving, real persona or historical customer evidence was invented. D2 preserves every supplied title, body line, note word and internal blank line. D3 clarifies audience/purpose once and reuses the existing visual decision without a style/backend/ratio interview. The mixed case keeps slides 1–2 ready while drafting only slide 3's content/talk; it still resolves missing ratio/backend decisions.

Limitations requiring a real run: backend/schema probing and reference bytes; verified reuse of an actual accepted sample; real plan/talk and output/review decisions; actual images and pixel/text inspection; first production-batch QA; user final-image acceptance; complete-sequence QA and verified assembly. Scripted approvals never satisfy those gates. No automatic behavioral pass verdict is made here.
""")
print(json.dumps({"root": str(ROOT), "content_slide_counts": checks["counts"], "fixed_note_checks": checks["fixed_copy_and_note_equality"], "live_generation": False}, indent=2))
