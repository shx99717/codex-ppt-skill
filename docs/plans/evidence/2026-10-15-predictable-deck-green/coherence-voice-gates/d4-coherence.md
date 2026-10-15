# D4 — account rename and changed role (MOCK/TEST)

## Original approved fixture

**MOCK supplied state:** The following four combined cards and talk were approved before this exercise. The shared identity `account_identity` is a teal key labeled **Shared account**. The key means account identity throughout. Original image handles, if a real run had any, are not provided here. This exercise therefore records content impact, not image inspection.

**MOCK proposed fixture defaults, explicitly accepted:** English; colleagues in a room; explain the account flow qualitatively; plain output, four content cards, locked 16:9; white background, dark text and teal key, otherwise neutral gray objects; consolidated review. Those defaults are not approval for live imagery or a backend.

| Internal ID/order | Original exact visible copy | Original visual/meaning | Meaningful dependency |
|---|---|---|---|
| `slide_01` / 1 | Title: `Meet the Shared account`; label: `Shared account`; body: `One account identity across the flow` | One large teal key, account name beneath it. Introduces the recurring identity. | None |
| `slide_02` / 2 | Title: `Shared account: start here`; step labels: `1. Identify the account`, `2. Choose the workspace`; object labels: `Shared account`, `Workspace` | Same teal key leads to a gray workspace rectangle. The key is the dominant subject; this card's local role is account identity applied to steps 1–2. | `slide_01` |
| `slide_03` / 3 | Title: `Shared account: continue`; step labels: `3. Open the resource`, `4. Return to the workspace`; object labels: `Shared account`, `Resource`, `Workspace` | Same key is carried into a resource panel and back to the workspace. It does not turn into a resource or a permission badge. | `slide_01`, `slide_02` |
| `slide_04` / 4 | Title: `Back to the Shared account`; labels: `Shared account`, `Workspace`, `Resource`; body: `The same identity connects the flow` | Same teal key centered, with workspace/resource as smaller context. Returns to the identity introduced on card 1. | `slide_01`, `slide_02`, `slide_03` |

Original approved talk, supplied as the test fixture:

### Slide 1: Meet the Shared account

Let's start with the Shared account. This teal key stands for the account identity, and we'll keep using it as we walk through the flow.

On the next slide, we'll see where that identity takes us first.

### Slide 2: Shared account: start here

First, identify the Shared account. Then choose the workspace you want to use.

The key is still the account identity. The gray box is the workspace we're choosing.

Those are steps one and two. Now we can continue with the resource.

### Slide 3: Shared account: continue

Now we're at step three: open the resource. Step four brings us back to the workspace.

The same Shared account goes through the whole sequence; we're following one identity rather than introducing another one here.

Let's bring that back to the starting point.

### Slide 4: Back to the Shared account

We're back to the Shared account we started with. The workspace and the resource are different parts of the flow, and the key ties them to the same account identity.

That's the picture I wanted us to keep in mind. What would you like to ask about the flow?

## Change request and scope interaction

**MOCK HUMAN D4-U1:** “Change its name to ‘Workspace account’ and its role on card 2 from identity to workspace boundary.”

**TEST ASSISTANT D4-A1:** “I recommend updating all four cards and their notes because the account is named on every card and the final card returns to that same identity. On card 2, I'll make the workspace boundary the main visual: a labeled enclosing box, with the teal key inside it. The key will keep meaning account identity wherever it appears. That avoids teaching the audience that a key suddenly means a boundary. Steps 1–2 stay on card 2 and steps 3–4 stay on card 3.

“The proposed cards below also revise card 3's reference to the boundary and the closing explanation on card 4. Please approve this affected scope, or tell me which part you want changed.”

**MOCK HUMAN D4-U2:** “Yes. Use the recommended scope: update all four cards and notes, keep the teal key as the identity, and make card 2 show the workspace boundary. Keep the step numbers.”

This is **scripted affected-plan acceptance**, not human approval of regenerated images. No real recorder was invoked.

## Concrete impact analysis

| Scope | Change | Required follow-through |
|---|---|---|
| Canonical term | `Shared account` → `Workspace account` | Replace exact visible account labels and spoken account names on all four cards. Do not run a partial replacement confined to card 2. |
| Shared identity | `account_identity`: same teal key and meaning, new account name | All four visual scopes use the renamed definition. Key color/shape do not change. |
| Boundary meaning | Add `workspace_boundary`: gray enclosing frame meaning the workspace being used | Card 2 becomes boundary-led. The frame is not a second account identity and is not an asserted access-permission boundary. |
| Card 2 relationship | Key is contained inside the workspace frame, steps 1–2 lead into/choose that workspace | Exact relationship now differs from the prior key-to-box scene; its old image contract is invalid. |
| Card 3 dependency | References the established enclosing workspace, continues steps 3–4 | Key and resource appear inside that same frame; return arrow targets the workspace, not the key. |
| Card 4 story | Concludes with the renamed identity and distinguishes identity from workspace grouping | Same key returns; smaller frame/resource context shows what card 2 introduced. |
| Talk | All names change; cards 2–4 explain grouping, continuation and return | All four note scopes require revised talk acceptance. No claims about permissions or measured benefit added. |
| Numbering | Internal `slide_01..04` remains file/order mapping | Visible steps remain `1`, `2`, `3`, `4`; no visible page numbers added. Card 3 starts with step 3. |
| Source facts/assets | Qualitative supplied fixture, no required image source | No source bytes invented; no asset reapproval manufactured. |
| Existing image/review evidence | All four exact-label/relationship contracts changed | In a real run stale all four content images, current image QA and human image acceptance. Preserve prior audit evidence without carrying it into the new content. |
| Sample style reference | Teal/white/gray style remains suitable | If a real accepted immutable reference existed, retain it only as a style reference after suitability review. It would not approve the renamed final content page. No such file is assumed here. |
| Policy/output/backend/ratio | No requested change | Preserve existing actual decisions if present; do not reset unrelated policy or invent a backend lock. |

## Revised complete cards and talk

### `slide_01` — introduce the renamed account

Language: English. Visible numbering: none.

Exact visible copy:

```text
Meet the Workspace account
Workspace account
One account identity across the flow
```

Visual: large teal key, label **Workspace account** directly below. No workspace enclosure is introduced until card 2. Objects: key + name + one supporting line. Key meaning: `account_identity`. Audience after card: recognizes the identity and name.

Talk:

Let's start with the Workspace account. This teal key stands for the account identity, and we'll keep using the same key as we walk through the flow.

The next slide adds the workspace around that identity.

### `slide_02` — workspace boundary, steps 1–2

Language: English. Visible numbering: steps **1** and **2**, no page number.

Exact visible copy:

```text
Workspace account: choose the workspace
1. Identify the account
2. Choose the workspace
Workspace account
Workspace
```

Visual: the large gray enclosing frame labeled **Workspace** is the main subject. The unchanged teal key labeled **Workspace account** is inside the frame. Step 1 identifies that key; step 2 leads to the enclosing workspace. Keep both step labels legible and separate. Frame means workspace grouping; key means identity. No lock symbol or unapproved permission claims.

Talk:

First, identify the Workspace account. Then choose the workspace you want to use.

Here, the big box is the workspace boundary. It gives us a place to group the next part of the flow. The teal key inside it still means the account identity.

Those are steps one and two. Now let's see what happens inside that workspace.

### `slide_03` — continue steps 3–4 inside the established workspace

Language: English. Visible numbering: steps **3** and **4**, no page number.

Exact visible copy:

```text
Workspace account: continue
3. Open the resource
4. Return to the workspace
Workspace account
Resource
Workspace
```

Visual: same gray enclosing frame labeled **Workspace**, same teal key labeled **Workspace account**, resource panel inside it. Step 3 arrow reaches the resource; step 4 returns to the surrounding workspace. The workspace frame is repeated for continuity; it is not a new account. Do not restart steps at 1–2.

Talk:

Now we're at step three: open the resource inside the workspace we just chose. Step four brings us back to that workspace.

The teal key is still the same Workspace account. The resource is one part of the workspace, so returning to the workspace doesn't introduce another account.

Let's return to the identity we started with and put those pieces together.

### `slide_04` — return to the same identity and conclude

Language: English. Visible numbering: none.

Exact visible copy:

```text
Back to the Workspace account
Workspace account
Workspace
Resource
The same identity connects the flow
```

Visual: teal key has the same silhouette/color as card 1 and is again the focus. A smaller gray workspace frame encloses a resource panel next to it. Make the connection understandable without changing the key into a frame. The account's label matches every preceding card.

Talk:

We're back to the Workspace account we started with. The key gives us the identity; the box gives us the workspace where we followed the steps.

So the four steps connect back to the same account, and the workspace stays a different part of the picture.

That's the flow. What would you like to ask about it?

## Revised render-brief packets (MOCK/TEST; not compiler-owned jobs)

These are actual authored packet contents for the test. They cannot be dispatched as managed jobs. In a real run the parent would record actual affected-plan acceptance and compile the current four scopes before any worker receives a packet.

| Test packet | Local card | Shared bindings | Reachable dependency context | Authorized output |
|---|---|---|---|---|
| D4-P1 | Exact revised card 1 copy/visual above | Teal key = identity; name = Workspace account | Introduction; no predecessors | One card 1 candidate only |
| D4-P2 | Exact revised card 2 copy/visual above | Key = identity; gray enclosing frame = workspace grouping | Card 1 introduced the named key; this card establishes boundary for later cards | One card 2 candidate, steps 1–2 |
| D4-P3 | Exact revised card 3 copy/visual above | Same key; same workspace frame | Card 1 identity + card 2 frame and steps 1–2 | One card 3 candidate, steps 3–4 |
| D4-P4 | Exact revised card 4 copy/visual above | Same key + frame | Card 1 introduction, card 2 boundary, card 3 resource/return | One concluding card candidate |

For each packet: preserve every exact word and relationship; approved style/ratio carry through; no rewrite, no final-overlay workaround, no rendering of internal IDs; dependencies are context rather than extra output. Notes remain parent-owned and are not copied into visible text. Backend is unbound in this text exercise: **no live generation permitted**. Required image inputs: none in the test fixture.

## Actual test actions and remaining state

Authored original and revised cards/talk, traced all dependencies, presented scope before scripted acceptance, and authored four revised briefs. No old image was mutated, regenerated or marked approved. Revised plan/talk state is MOCK accepted. Current-image QA, current-image human acceptance and complete sequence QA are unavailable. Assembly remains withheld. The scope contains all four cards because all four exact labels changed; it is not an arbitrary whole-deck reset.
