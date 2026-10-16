# CLI/API Fallback

Use this reference only after CLI/API fallback has been selected and confirmed with the user. The main `SKILL.md` owns the backend decision rules; this document owns fallback commands, runtime setup, image-input limits, editing, transparency, and troubleshooting.

Let `{skill_root}` mean the directory containing `SKILL.md`.
Let `{runtime_python}` mean the shared venv interpreter under `~/.codex-ppt-skill/.venv` (Windows: `Scripts/python.exe`; Unix/macOS: `bin/python`).

## Runtime Setup

CLI/API fallback commands use the shared runtime environment. Before running `scripts/assemble_ppt.py` or fallback image commands, make sure the shared runtime exists. If `{runtime_python}` is missing, or if importing script dependencies fails, create or refresh the environment:

```bash
python3 {skill_root}/scripts/codex_ppt_runtime.py bootstrap
```

This is an internal setup step for the skill. Do not ask the user to run it unless dependency installation fails and user approval or troubleshooting is required.

The fallback CLI loads `~/.codex-ppt-skill/.env` automatically for `OPENAI_API_KEY`, `OPENAI_BASE_URL`, and `CODEX_PPT_IMAGE_MODEL`. Do not manually parse `.env`. For API key, base URL, model, and config troubleshooting, read `image-model-configuration.md` only after the fallback CLI reports missing or invalid configuration, when the user explicitly wants to change those settings, or when a real API call reports authentication, permission, base URL, or model availability failure.

## Execute a managed slide

Approve `planning.generation` before compilation, including exact model, size, quality and operation policy. For example, a supported CLI plan can use `mode: generate` without images and `reference_mode: edit` with approved style/source images. Both use the same approved backend/configuration. Capability changes require an approved method update and calibration where needed.

Use the adapter to consume the current compiled job and all verified inputs:

```bash
{runtime_python} {skill_root}/scripts/run_slide_job.py {deck_dir} \
  --slide slide_01 --out {deck_dir}/candidates/slide_01-attempt-1.png --dry-run

# After recorded dispatch to this agent and authorized generation:
{runtime_python} {skill_root}/scripts/run_slide_job.py {deck_dir} \
  --slide slide_01 --agent-id {agent_id} --out {deck_dir}/candidates/slide_01-attempt-1.png
```

Dry-run previews the effective provider endpoint, exact prompt, parameters and image list without an API call. Execution requires matching current dispatch. Candidates must be new PNGs under `candidates/`; the parent validates and records final files. Unsupported fields, missing reference operations and stale jobs fail before dispatch. Do not feed managed job JSON to `generate-batch`: it does not consume nested configuration or the image-input contract.

## Unmanaged utility generation

Basic generation command:

```bash
{runtime_python} {skill_root}/scripts/image_gen.py generate \
  --model YOUR_SELECTED_MODEL_ID \
  --prompt-file {prompt_file} \
  --size {2560x1440|2560x1920} \
  --quality medium \
  --out {candidate_path}
```

The fallback CLI requires an explicitly configured provider-documented model ID; there is no fixed default model.

The following prompt extraction is an unmanaged utility example only. Managed jobs must use the adapter. Use a job's `prompt` alone only when it has no input images:

```bash
python3 -c 'import json, pathlib; print(json.loads(pathlib.Path("{base_dir}/{deck_name}/prompts/slide_01.json").read_text())["prompt"])' | \
{runtime_python} {skill_root}/scripts/image_gen.py generate \
  --prompt-file - \
  --size {2560x1440|2560x1920} \
  --quality medium \
  --out {candidate_path}
```

Before using this text-only `generate` path, inspect the assigned `prompts/slide_XX.json`. If `input_images` is non-empty or `requires_context_images` is true, this command is not sufficient because it does not attach those images. Use a selected backend/path that can pass the required images, such as a host-native tool (`GenerateImage` / `image_gen`) or bridge (`codex-gpt-image`) with the images visible in context, or a CLI/API edit/image-input path that supplies every required source image. If no such path is available, stop and ask the user whether to switch backend. Do not generate a text-only replacement for a strict input asset.

## Capabilities And Sizes

The fallback CLI supports:

- `generate`: create one or more images from a prompt.
- `edit`: edit one or more existing images, optionally with a mask.

For API execution, use the approved model and size supported by its documented capability profile. Suggested slide sizes are 2560x1440 (16:9) and 2560x1920 (4:3); these are not native-tool requirements. Measure saved pixels and honor explicitly approved minimum/exact output requirements.

## Editing Slides

Managed repairs are recorded from agent QA, compiled with `--phase repair`, dispatched within their current authorization budget, and executed by the adapter. They retain calibration/production prerequisites and the approved operation policy. Do not patch prompts or replace official images by hand.

For an explicitly unmanaged utility edit:

```bash
{runtime_python} {skill_root}/scripts/image_gen.py edit \
  --image {slide_path} \
  --prompt {edit_prompt} \
  --out {new_slide_path}
```

Validate edited pixels before accepting any final replacement.

## Transparent Backgrounds

Transparent-background requests:

- Built-in mode should use a flat chroma-key background and local removal when appropriate.
- CLI/API fallback should also prefer chroma-key generation plus `scripts/remove_chroma_key.py` for simple opaque subjects.
- Check transparency and input-fidelity support for the explicitly selected model; do not apply an older model rule by name substring.

## Assembly And Doctor

`assemble_ppt.py` supports `16:9` and `4:3` for `--template none|medavis|both`. Pass the locked `--aspect-ratio`. Medavis template mode requires `--landing-title` and loads the matching bundled 3-page file.

Run the API doctor only when troubleshooting fallback API access:

```bash
python3 {skill_root}/scripts/codex_ppt_runtime.py doctor --check-api
```

See [submission evidence](image-submission-evidence.md) for contract versions, native input mapping, adapter completion and measured output records.
