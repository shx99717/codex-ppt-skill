# D1 combined draft: exact copy, visual meaning and talk

TEXT-ONLY MOCK/TEST EVIDENCE — no real user approval or rendered image.

Audience: engineering colleagues
Purpose: Help colleagues understand the proposal and its trade-offs.
Output recommendation: plain; no visible numbering; consolidated review.

## Slide 1: Shared login: a proposal to examine

Exact visible title:

Shared login: a proposal to examine

Exact visible body:

One personal account across services
Expected benefit: less repeated access work
Trade-offs need investigation

Source/proposal status: proposed

Intended visual meaning:

one personal identity across services

Objects: individual account; three illustrative service tiles
Connections: one account connects to multiple distinct services
Composition: account at left; three services stacked at right; restrained connecting lines

Dependencies: opening; no earlier-page dependency
Audience after: Know the proposal, the discussion purpose and the absence of measured benefit

Speaker notes:

Hi everyone.

I want to walk through a shared login proposal and the trade-offs it brings.

The idea we will examine is one personal account across services. We expect that could reduce some repeated access work, but we do not have measurements yet.

Let me start with the access pattern we are using as a working assumption.

## Slide 2: Access today: a working assumption

Exact visible title:

Access today: a working assumption

Exact visible body:

Separate service accounts
Repeated sign-in and account recovery
Confirm this matches our environment

Source/proposal status: proposed working assumption, not supplied organization fact

Intended visual meaning:

assumed current access pattern

Objects: one person; three service-account pairs
Connections: each illustrative service has a separate account path
Composition: three separate horizontal paths; no shared identity hub

Dependencies: slide_01
Audience after: Understand the illustrative current pattern and the need to confirm it

Speaker notes:

Imagine a colleague moving between three services. This is an illustration, not a report about a particular person.

For the discussion, I am assuming each service has its own account and access steps. That can mean choosing credentials again or dealing with recovery separately.

We need to confirm that pattern against our actual environment. With that assumption visible, we can look at what the proposal changes.

## Slide 3: The proposed model

Exact visible title:

The proposed model

Exact visible body:

One personal identity
Reusable sign-in session where supported
Separate permissions for each service

Source/proposal status: proposed

Intended visual meaning:

proposed identity/session model with separate permissions

Objects: individual account hub; three service tiles; a gate inside each service boundary
Connections: account links to each service; session reuse is conditional on service support; permissions are checked at each service
Composition: shared identity hub across top; three service boundaries below, each with its own small gate

Dependencies: slide_01, slide_02
Audience after: Distinguish personal identity, conditional session reuse and service permissions

Speaker notes:

Now, here is the model I propose we discuss. The account belongs to one person and can be recognised across services.

Where a service supports it, the sign-in session could be reused. That is a design condition to check, not something we have already proved.

Signing in tells a service who the person is. Permissions still decide what that person can do in that service. Keeping those responsibilities clear gives us a basis for discussing the benefit.

## Slide 4: Where time could be saved

Exact visible title:

Where time could be saved

Exact visible body:

Fewer account credentials to manage
Reuse sign-in where supported
No time-saving measurements yet

Source/proposal status: proposed

Intended visual meaning:

possible reduction in repeated access steps

Objects: current-pattern lane; proposed lane; same three illustrative services
Connections: current-pattern lane repeats separate account steps; proposed lane reuses the personal account; session reuse remains conditional
Composition: two horizontal lanes; illustrate account/sign-in actions with icons; no times, percentages, bar lengths or invented metric

Dependencies: slide_02, slide_03
Audience after: Understand qualitative expected benefit without interpreting it as measured outcome

Speaker notes:

So, where might the time saving come from?

First, a person could have fewer account credentials to keep track of. Second, where session reuse works, they may avoid some repeated sign-in steps as they move between services.

Those are the mechanisms we expect to help. We cannot say how much time they save yet, and the benefit will depend on how people actually move between services.

Now let us look at the questions that come with sharing the sign-in path.

## Slide 5: Trade-offs to investigate

Exact visible title:

Trade-offs to investigate

Exact visible body:

Shared sign-in dependency
Account recovery and revocation
Provider permissions and ownership

Source/proposal status: proposed

Intended visual meaning:

questions raised by a shared identity path

Objects: common identity hub; recovery loop; provider permission gates
Connections: services depend on a shared identity path; account lifecycle affects the shared identity; provider permissions still have distinct owners
Composition: three equally weighted panels; show dependency, recovery and permission concepts; no severity ranking

Dependencies: slide_03, slide_04
Audience after: Recognise common dependency, account lifecycle and permissions as unresolved trade-offs

Speaker notes:

A shared sign-in path gives us a common dependency to design carefully. What should happen if that path is unavailable?

We also need a clear account lifecycle. Who helps with recovery, and how should access be removed when it is no longer appropriate?

Then there is ownership: who manages the personal account, and who grants access inside each provider? These are investigation questions. I am not presenting settled implementation decisions.

That leaves us with a useful set of questions for the engineering discussion.

## Slide 6: Questions for investigation

Exact visible title:

Questions for investigation

Exact visible body:

Which assumptions need evidence?
Which trade-offs need a design spike?
How would we evaluate a trial?

Source/proposal status: proposed

Intended visual meaning:

questions that connect the proposal to possible investigation

Objects: current-pattern assumption card; trade-off cards; three discussion question cards
Connections: current assumptions inform evidence questions; trade-offs inform a possible design spike; a trial would need agreed evaluation criteria
Composition: inputs on the left; three question cards on the right; an open discussion area, no assigned people or dates

Dependencies: slide_02, slide_04, slide_05
Audience after: Be ready to discuss evidence and design questions without an implied rollout commitment

Speaker notes:

So, we have a proposal, a possible benefit mechanism and a set of trade-offs.

I would like us to check which assumptions need evidence and which design questions deserve a small investigation. If we later choose a trial, we should agree how to evaluate it before claiming a saving.

What have we missed, and where would you start?
