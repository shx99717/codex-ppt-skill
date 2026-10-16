# User-Supplied Assets

Read this before using paper figures, experiment result charts, screenshots, logos, or other assets that must appear in the deck.

When the user provides paper figures, experiment result charts, screenshots, logos, or other assets that must appear in the deck, treat them as source assets, not as loose visual inspiration.

Recommended project-local asset location:

```text
{base_dir}/{deck_name}/assets/
├── figures/
│   ├── result_01.png
│   └── result_02.png
└── logos/
    └── lab_logo.png
```

Do not place source assets in `origin_image/`; that directory is only for final `slide_XX.png` images.

For slides that must include a user-supplied figure:

- Record the exact asset, role and required fidelity in the canonical slide's `required_images` and readable whole-deck plan. Reuse supplied mappings; approve genuinely new mappings as part of combined plan review, rather than asking again for known choices.
- Stay on the already selected image backend. Do not switch between built-in image generation and CLI/API fallback only because a slide includes source images.
- Use the selected backend's reference-image or edit capability when available, with the supplied figure visible as an input image.
- Ask the model to preserve the supplied figure's data, labels, axes, colors, and visual content, and only compose the surrounding slide layout, title, captions, callouts, and background.
- Do not ask the model to "redraw", "recreate", "imagine", or "generate a similar chart" for result figures unless the user explicitly wants a stylized redraw.
- After generation, inspect the output and ask the user to pay special attention to whether required figures were used correctly.

Managed approval resolves asset paths against the draft directory before installation, preserves original source provenance, and stores byte-identical hash-named snapshots in `references/sources/`. Jobs use those exact snapshots; a same-named file in a different directory is not approved. Original or snapshot byte drift invalidates affected slides and dependent visual/talk bindings. Review the affected scope before recompiling. Put recurring asset identities in the shared visual registry. Keep style-only sample inputs distinct from strict source figures.

Example prompt fragment for a result-figure slide:

```json
{
  "source_assets": [
    {
      "path": "{base_dir}/{deck_name}/assets/figures/result_01.png",
      "usage": "embed as the main evidence figure",
      "fidelity": "preserve the figure content; do not redraw or change data, axes, labels, colors, curves, bars, or legends"
    }
  ],
  "visual_elements": {
    "main_visual": "place the supplied result_01.png as a large figure panel, with a short caption and two callouts around it"
  },
  "constraints": [
    "Use the provided figure as an input image, not as a loose style reference.",
    "Do not synthesize a replacement chart.",
    "Keep all numerical values and labels in the supplied figure unchanged."
  ]
}
```

Native references must use the live tool input mechanism: inspect required local images, then attach all through referenced_image_paths when supported; recent-image inclusion needs explicit complete mapping and must not be combined with paths. Inspection alone is not attachment. Follow [submission evidence](image-submission-evidence.md).
