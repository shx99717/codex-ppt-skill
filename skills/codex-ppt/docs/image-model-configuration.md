# Image Model Configuration

Use this only for deliberately selected API/CLI fallback with missing/invalid configuration, authentication/model errors, or an explicit configuration change. Native Codex image_gen and Cursor GenerateImage need no API model selection or API key from this skill.

- OPENAI_API_KEY is required for real API calls. Never request the key in chat; configure it locally.
- OPENAI_BASE_URL is optional; absent means the official OpenAI API. For compatible providers use the API root, normally ending /v1, rather than /images/generations or /images/edits.
- CODEX_PPT_IMAGE_MODEL or --model must explicitly select a documented provider model. There is no permanent default image model.

The CLI loads the shared ~/.codex-ppt-skill/.env automatically; do not manually parse secrets. Process environment overrides the file, and --model overrides model configuration for one command. Reuse the configured model. If absent, check current official/provider documentation and obtain selection rather than guessing a latest alias.

Configure using the existing runtime:

```text
python scripts/codex_ppt_runtime.py config --model YOUR_SELECTED_MODEL_ID
```

The existing config command also accepts --api-key and --base-url. Keep secrets out of shared command examples/history. An AtlasCloud model must use its provider-documented route; do not infer a new model route from an older one.

## Document capabilities for managed jobs

Record capabilities for the selected model/provider and used operations in planning.generation.capabilities. Unknown is different from unsupported: missing facts must be checked for managed approval, without reselecting an already configured model. Do not infer restrictions from a model-name substring.

```json
{
  "model": "YOUR_SELECTED_MODEL_ID",
  "provider_base_url": "https://api.openai.com/v1",
  "operations": {
    "edit": {
      "supports_image_inputs": true,
      "qualities": ["medium"],
      "size_constraints": {"multiple": 16, "max_edge": 3840, "max_ratio": 3, "min_pixels": 655360, "max_pixels": 8294400},
      "source": "https://developers.openai.com/api/docs/guides/image-generation",
      "checked_on": "2026-10-16"
    }
  }
}
```

This illustrates the schema, not a supported profile for every model. Verify facts for the selected model and add a separate generate entry if used. Record transparency/input-fidelity capabilities only when verified and needed. Managed jobs reject unknown required facts; explicit standalone API calls may defer unknown facts to actual provider errors. Known unsupported settings fail locally. Profiles are passed with --capabilities-file and never enter provider SDK payloads. API access/model documentation does not prove a native tool's capabilities.
