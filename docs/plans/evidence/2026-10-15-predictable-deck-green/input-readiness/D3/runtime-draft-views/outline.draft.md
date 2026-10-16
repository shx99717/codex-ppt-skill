# Deck plan — draft

- audience: nontechnical operations colleagues
- purpose: Understand the access journey
- notes_language: English
- tone: Natural, clear presenter voice; supplied notes remain exact
- output_profile: none
- landing_title: None

Story: Understand the deck explains a proposed personal-account journey → Understand where sign-in sits in the journey → Understand that provider permission is a separate check → Understand account reuse without assuming automatic access or proven session reuse → Be able to explain the proposed journey and identify support questions without a technical decision request
Input readiness: {"content": "topic ready; audience/purpose clarified once; all copy and talk proposed", "visual": "supplied approved clean technical reference; compatible backend/ratio fixture reused"}
Review: consolidated
Shared identities: {"individual_account": {"meaning": "one personal account symbol; same meaning and appearance throughout", "appearance": "one personal account symbol; same meaning and appearance throughout"}, "provider_tile": {"meaning": "repeated provider shape; distinct providers, no claim about real provider count", "appearance": "repeated provider shape; distinct providers, no claim about real provider count"}}

## Slide 1: One account across providers

Purpose (One account across providers): Understand the deck explains a proposed personal-account journey
Exact visible copy: {"title": "One account across providers", "body": ["A proposed way to move between providers"], "labels": []}
Visual: {"type": "journey overview", "subject": "one person's account across two illustrative providers", "objects": ["person/account symbol", "two provider tiles"], "relationships": [{"from": "person/account symbol", "to": "two provider tiles", "description": "the same account links to both providers"}], "composition": "a short left-to-right journey in the existing clean reference style"}
Sources / proposals: [{"status": "proposed", "claim": "One account across providers", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "A proposed way to move between providers", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "one person's account across two illustrative providers", "source": "D3 original visual proposal; object and relationship wording retained exactly"}, {"status": "proposed", "claim": "Presenter talk for this page", "source": "D3 original speech.draft.md: exact unchanged speaker_notes.text"}]
Source assets: []
Shared elements: individual_account, provider_tile
Depends on: 
Spoken time: None seconds
Transition: Start at the personal account

## Slide 2: Start with your account

Purpose (Start with your account): Understand where sign-in sits in the journey
Exact visible copy: {"title": "Start with your account", "body": ["Use your own account", "Sign in before opening a provider"], "labels": []}
Visual: {"type": "journey start", "subject": "a person signs in using their personal account", "objects": ["same person/account symbol", "sign-in doorway", "first provider tile"], "relationships": [{"from": "same person/account symbol", "to": "first provider tile", "description": "person uses the account before entering the provider path"}], "composition": "large account symbol on left; sign-in doorway in middle; first provider at right"}
Sources / proposals: [{"status": "proposed", "claim": "Start with your account", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Use your own account", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Sign in before opening a provider", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "a person signs in using their personal account", "source": "D3 original visual proposal; object and relationship wording retained exactly"}, {"status": "proposed", "claim": "Presenter talk for this page", "source": "D3 original speech.draft.md: exact unchanged speaker_notes.text"}]
Source assets: []
Shared elements: individual_account, provider_tile
Depends on: slide_01
Spoken time: None seconds
Transition: Move into the first provider

## Slide 3: Open a provider

Purpose (Open a provider): Understand that provider permission is a separate check
Exact visible copy: {"title": "Open a provider", "body": ["Choose the provider", "Your access is checked there"], "labels": []}
Visual: {"type": "provider entry", "subject": "recognised person opens a provider and access is checked", "objects": ["same account symbol", "highlighted first provider", "entry gate"], "relationships": [{"from": "same account symbol", "to": "highlighted first provider", "description": "account connects to selected provider"}, {"from": "entry gate", "to": "highlighted first provider", "description": "gate belongs to that provider"}], "composition": "first provider highlighted; second provider quieter in background; simple gate at entry"}
Sources / proposals: [{"status": "proposed", "claim": "Open a provider", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Choose the provider", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Your access is checked there", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "recognised person opens a provider and access is checked", "source": "D3 original visual proposal; object and relationship wording retained exactly"}, {"status": "proposed", "claim": "Presenter talk for this page", "source": "D3 original speech.draft.md: exact unchanged speaker_notes.text"}]
Source assets: []
Shared elements: individual_account, provider_tile
Depends on: slide_01, slide_02
Spoken time: None seconds
Transition: Switch providers without implying automatic permission

## Slide 4: Switch to another provider

Purpose (Switch to another provider): Understand account reuse without assuming automatic access or proven session reuse
Exact visible copy: {"title": "Switch to another provider", "body": ["Use the same account", "Access can differ by provider"], "labels": []}
Visual: {"type": "provider switch", "subject": "the same account reaches a second provider with its own permission check", "objects": ["same account", "first provider", "highlighted second provider", "one gate per provider"], "relationships": [{"from": "same account", "to": "same account", "description": "identity remains the same"}, {"from": "one gate per provider", "to": "highlighted second provider", "description": "provider permissions are distinct"}], "composition": "journey advances right; account appearance stays constant; second provider highlighted"}
Sources / proposals: [{"status": "proposed", "claim": "Switch to another provider", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Use the same account", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Access can differ by provider", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "the same account reaches a second provider with its own permission check", "source": "D3 original visual proposal; object and relationship wording retained exactly"}, {"status": "proposed", "claim": "Presenter talk for this page", "source": "D3 original speech.draft.md: exact unchanged speaker_notes.text"}]
Source assets: []
Shared elements: individual_account, provider_tile
Depends on: slide_02, slide_03
Spoken time: None seconds
Transition: Recap what the access journey changes

## Slide 5: What this changes

Purpose (What this changes): Be able to explain the proposed journey and identify support questions without a technical decision request
Exact visible copy: {"title": "What this changes", "body": ["One account to recognise", "Provider access still matters", "Support details need investigation"], "labels": []}
Visual: {"type": "journey recap", "subject": "account continuity and distinct provider access", "objects": ["same account", "both providers with entry gates", "support question symbol"], "relationships": [{"from": "same account", "to": "both providers with entry gates", "description": "account is reused across both provider paths"}, {"from": "both providers with entry gates", "to": "both providers with entry gates", "description": "each gate remains distinct"}, {"from": "support question symbol", "to": "both providers with entry gates", "description": "support handling remains an open question"}], "composition": "compact journey across top; account and access concepts beneath; open support question at right"}
Sources / proposals: [{"status": "proposed", "claim": "What this changes", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "One account to recognise", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Provider access still matters", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "Support details need investigation", "source": "D3 interaction.md and original outline.draft.md: proposed"}, {"status": "proposed", "claim": "account continuity and distinct provider access", "source": "D3 original visual proposal; object and relationship wording retained exactly"}, {"status": "proposed", "claim": "Presenter talk for this page", "source": "D3 original speech.draft.md: exact unchanged speaker_notes.text"}]
Source assets: []
Shared elements: individual_account, provider_tile
Depends on: slide_01, slide_03, slide_04
Spoken time: None seconds
Transition: Invite understanding questions

Unresolved: []
