# Deck plan — draft

- audience: engineering colleagues
- purpose: Help colleagues understand the proposal and its trade-offs.
- notes_language: English
- tone: Natural, clear presenter voice; supplied notes remain exact
- output_profile: none
- landing_title: None

Story: Know the proposal, the discussion purpose and the absence of measured benefit → Understand the illustrative current pattern and the need to confirm it → Distinguish personal identity, conditional session reuse and service permissions → Understand qualitative expected benefit without interpreting it as measured outcome → Recognise common dependency, account lifecycle and permissions as unresolved trade-offs → Be ready to discuss evidence and design questions without an implied rollout commitment
Input readiness: {"content": "topic and lack of measurements provided; complete story/copy/talk proposed", "visual": "unresolved; clean technical system proposed"}
Review: consolidated
Shared identities: {"individual_account": {"meaning": "one personal account symbol; same meaning and appearance throughout", "appearance": "one personal account symbol; same meaning and appearance throughout"}, "provider_tile": {"meaning": "repeated provider shape; distinct providers, no claim about real provider count", "appearance": "repeated provider shape; distinct providers, no claim about real provider count"}}

## Slide 1: Shared login: a proposal to examine

Purpose (Shared login: a proposal to examine): Know the proposal, the discussion purpose and the absence of measured benefit
Exact visible copy: {"title": "Shared login: a proposal to examine", "body": ["One personal account across services", "Expected benefit: less repeated access work", "Trade-offs need investigation"], "labels": []}
Visual: {"type": "proposal overview", "subject": "one personal identity across services", "objects": ["individual account", "three illustrative service tiles"], "relationships": [{"from": "individual account", "to": "three illustrative service tiles", "description": "one account connects to multiple distinct services"}], "composition": "account at left; three services stacked at right; restrained connecting lines"}
Sources / proposals: [{"status": "proposed", "claim": "Shared login: a proposal to examine", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "One personal account across services", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Expected benefit: less repeated access work", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Trade-offs need investigation", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "one personal identity across services", "source": "D1 original visual proposal; object and relationship wording retained exactly"}, {"status": "proposed", "claim": "Presenter talk for this page", "source": "D1 original speech.draft.md: exact unchanged speaker_notes.text"}]
Source assets: []
Shared elements: individual_account, provider_tile
Depends on: 
Spoken time: None seconds
Transition: Move from the proposal to the current-pattern assumption

## Slide 2: Access today: a working assumption

Purpose (Access today: a working assumption): Understand the illustrative current pattern and the need to confirm it
Exact visible copy: {"title": "Access today: a working assumption", "body": ["Separate service accounts", "Repeated sign-in and account recovery", "Confirm this matches our environment"], "labels": []}
Visual: {"type": "separate paths", "subject": "assumed current access pattern", "objects": ["one person", "three service-account pairs"], "relationships": [{"from": "one person", "to": "three service-account pairs", "description": "each illustrative service has a separate account path"}], "composition": "three separate horizontal paths; no shared identity hub"}
Sources / proposals: [{"status": "proposed", "claim": "Access today: a working assumption", "source": "D1 interaction.md and original outline.draft.md: proposed working assumption, not supplied organization fact"}, {"status": "proposed", "claim": "Separate service accounts", "source": "D1 interaction.md and original outline.draft.md: proposed working assumption, not supplied organization fact"}, {"status": "proposed", "claim": "Repeated sign-in and account recovery", "source": "D1 interaction.md and original outline.draft.md: proposed working assumption, not supplied organization fact"}, {"status": "proposed", "claim": "Confirm this matches our environment", "source": "D1 interaction.md and original outline.draft.md: proposed working assumption, not supplied organization fact"}, {"status": "proposed", "claim": "assumed current access pattern", "source": "D1 original visual proposal; object and relationship wording retained exactly"}, {"status": "proposed", "claim": "Presenter talk for this page", "source": "D1 original speech.draft.md: exact unchanged speaker_notes.text"}]
Source assets: []
Shared elements: individual_account, provider_tile
Depends on: slide_01
Spoken time: None seconds
Transition: Compare the separate paths with the proposed shared identity

## Slide 3: The proposed model

Purpose (The proposed model): Distinguish personal identity, conditional session reuse and service permissions
Exact visible copy: {"title": "The proposed model", "body": ["One personal identity", "Reusable sign-in session where supported", "Separate permissions for each service"], "labels": []}
Visual: {"type": "identity and access diagram", "subject": "proposed identity/session model with separate permissions", "objects": ["individual account hub", "three service tiles", "a gate inside each service boundary"], "relationships": [{"from": "individual account hub", "to": "three service tiles", "description": "account links to each service"}, {"from": "individual account hub", "to": "three service tiles", "description": "session reuse is conditional on service support"}, {"from": "a gate inside each service boundary", "to": "three service tiles", "description": "permissions are checked at each service"}], "composition": "shared identity hub across top; three service boundaries below, each with its own small gate"}
Sources / proposals: [{"status": "proposed", "claim": "The proposed model", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "One personal identity", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Reusable sign-in session where supported", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Separate permissions for each service", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "proposed identity/session model with separate permissions", "source": "D1 original visual proposal; object and relationship wording retained exactly"}, {"status": "proposed", "claim": "Presenter talk for this page", "source": "D1 original speech.draft.md: exact unchanged speaker_notes.text"}]
Source assets: []
Shared elements: individual_account, provider_tile
Depends on: slide_01, slide_02
Spoken time: None seconds
Transition: Explain the possible benefit mechanism without numerical claims

## Slide 4: Where time could be saved

Purpose (Where time could be saved): Understand qualitative expected benefit without interpreting it as measured outcome
Exact visible copy: {"title": "Where time could be saved", "body": ["Fewer account credentials to manage", "Reuse sign-in where supported", "No time-saving measurements yet"], "labels": []}
Visual: {"type": "qualitative journey comparison", "subject": "possible reduction in repeated access steps", "objects": ["current-pattern lane", "proposed lane", "same three illustrative services"], "relationships": [{"from": "current-pattern lane", "to": "same three illustrative services", "description": "current-pattern lane repeats separate account steps"}, {"from": "proposed lane", "to": "same three illustrative services", "description": "proposed lane reuses the personal account; session reuse remains conditional"}], "composition": "two horizontal lanes; illustrate account/sign-in actions with icons; no times, percentages, bar lengths or invented metric"}
Sources / proposals: [{"status": "proposed", "claim": "Where time could be saved", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Fewer account credentials to manage", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Reuse sign-in where supported", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "No time-saving measurements yet", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "possible reduction in repeated access steps", "source": "D1 original visual proposal; object and relationship wording retained exactly"}, {"status": "proposed", "claim": "Presenter talk for this page", "source": "D1 original speech.draft.md: exact unchanged speaker_notes.text"}]
Source assets: []
Shared elements: individual_account, provider_tile
Depends on: slide_02, slide_03
Spoken time: None seconds
Transition: Move from possible benefit to trade-offs

## Slide 5: Trade-offs to investigate

Purpose (Trade-offs to investigate): Recognise common dependency, account lifecycle and permissions as unresolved trade-offs
Exact visible copy: {"title": "Trade-offs to investigate", "body": ["Shared sign-in dependency", "Account recovery and revocation", "Provider permissions and ownership"], "labels": []}
Visual: {"type": "three investigation lenses", "subject": "questions raised by a shared identity path", "objects": ["common identity hub", "recovery loop", "provider permission gates"], "relationships": [{"from": "common identity hub", "to": "provider permission gates", "description": "services depend on a shared identity path"}, {"from": "recovery loop", "to": "common identity hub", "description": "account lifecycle affects the shared identity"}, {"from": "common identity hub", "to": "provider permission gates", "description": "provider permissions still have distinct owners"}], "composition": "three equally weighted panels; show dependency, recovery and permission concepts; no severity ranking"}
Sources / proposals: [{"status": "proposed", "claim": "Trade-offs to investigate", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Shared sign-in dependency", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Account recovery and revocation", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Provider permissions and ownership", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "questions raised by a shared identity path", "source": "D1 original visual proposal; object and relationship wording retained exactly"}, {"status": "proposed", "claim": "Presenter talk for this page", "source": "D1 original speech.draft.md: exact unchanged speaker_notes.text"}]
Source assets: []
Shared elements: individual_account, provider_tile
Depends on: slide_03, slide_04
Spoken time: None seconds
Transition: Turn unresolved trade-offs into discussion questions

## Slide 6: Questions for investigation

Purpose (Questions for investigation): Be ready to discuss evidence and design questions without an implied rollout commitment
Exact visible copy: {"title": "Questions for investigation", "body": ["Which assumptions need evidence?", "Which trade-offs need a design spike?", "How would we evaluate a trial?"], "labels": []}
Visual: {"type": "discussion map", "subject": "questions that connect the proposal to possible investigation", "objects": ["current-pattern assumption card", "trade-off cards", "three discussion question cards"], "relationships": [{"from": "current-pattern assumption card", "to": "three discussion question cards", "description": "current assumptions inform evidence questions"}, {"from": "trade-off cards", "to": "three discussion question cards", "description": "trade-offs inform a possible design spike"}, {"from": "trade-off cards", "to": "three discussion question cards", "description": "a trial would need agreed evaluation criteria"}], "composition": "inputs on the left; three question cards on the right; an open discussion area, no assigned people or dates"}
Sources / proposals: [{"status": "proposed", "claim": "Questions for investigation", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Which assumptions need evidence?", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Which trade-offs need a design spike?", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "How would we evaluate a trial?", "source": "D1 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "questions that connect the proposal to possible investigation", "source": "D1 original visual proposal; object and relationship wording retained exactly"}, {"status": "proposed", "claim": "Presenter talk for this page", "source": "D1 original speech.draft.md: exact unchanged speaker_notes.text"}]
Source assets: []
Shared elements: individual_account, provider_tile
Depends on: slide_02, slide_04, slide_05
Spoken time: None seconds
Transition: Invite the room to discuss

Unresolved: []
