# Image Submission Evidence

New managed jobs/envelopes always contain compiler-owned execution_contract_version=1. Authors cannot omit it to skip input evidence. Old files remain readable for inspection; new execution, result, QA and assembly require recompilation and fresh attempt evidence. Preserve historical approvals; only actually changed method/content scopes need reapproval. Old final images cannot be labeled as new verified submissions. Existing approved samples may remain style inputs, but old final-page acceptance alone does not establish current generation evidence.

## Actual inputs

Every job's ordered input_images contains immutable source/style snapshot paths, hashes, roles and fidelity. Inspect all required local inputs, then attach each through the actual tool mechanism. With native image_gen, use referenced_image_paths when supported and every target has a path; do not also pass num_last_images_to_include. Use recent-context inclusion only where needed and map all included images explicitly, within its live limit. A view_image call is inspection, not generation attachment. Cursor/bridge input names and limits must be inspected, not invented.

Keep style-only references distinct from strict figures. Stop before generation if all inputs cannot be attached; no silent truncation or text-only replacements. Inspect actual generated figures/text and obtain user image approval separately from submission evidence.

## Native / bridge worker receipt

Return a UTF-8 JSON receipt with schema_version=1, execution_contract_version=1, actual dispatch attempt_id/agent_id, job_sha256, exact backend_used/tool_name, operation, actual mechanism, evidence_origin=agent_reported, optional real call_reference, candidate path/sha256, and ordered attachments (index, approved snapshot path, sha256, role, fidelity). Use actual submitted call inputs, not just a copy of the planned list. Paths and hashes must match the job; report inability to confirm inclusion as a blocker. Do not invent host call records or claim adapter verification.

The parent supplies --submission-receipt FILE to record_slide_result.py with the existing result arguments. It validates inputs, attempt, candidate bytes and current job, records the evidence trust level and measures actual output pixels. This is an audit record, not independent proof of a native model's internal inputs.

## Bundled CLI adapter

Use run_slide_job.py DECK --slide ID --agent-id ID --out DECK/candidates/NEW.png. It forwards every verified staged file via --image, selects the approved generate/edit operation, and creates NEW.submission.json only after real successful execution and current-dispatch validation. It registers execution_completion under the jobs lock. Pass that receipt to record_slide_result.py. Adapter verification is derived from matching registered completion, receipt hash, current attempt and candidate, never from a worker-authored verification label. Dry-run/failed/stale execution creates no successful completion. New dispatches invalidate prior completion.

Local records are consistency/provenance checks, not cryptographic attestation against a malicious writer with shared filesystem access. Agent QA and human acceptance remain required.
