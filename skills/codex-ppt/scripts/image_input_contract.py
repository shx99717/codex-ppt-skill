"""Attempt-bound input evidence and original output measurements.

Local adapter state is a consistency check, not malicious-worker attestation.
"""
from __future__ import annotations
import hashlib
from pathlib import Path

EXECUTION_CONTRACT_VERSION = 1


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require_version(jobs, job):
    if any(type(v.get("execution_contract_version")) is not int or v["execution_contract_version"] != EXECUTION_CONTRACT_VERSION for v in (jobs,job)):
        raise ValueError("Managed execution contract is missing or unsupported; recompile before new execution or assembly")


def attachments(images):
    return [{"index":i,"path":str(Path(v["path"]).resolve()),"sha256":v["sha256"],
             "role":v.get("role"),"fidelity":v.get("fidelity")} for i,v in enumerate(images)]


def make_receipt(job, slide, candidate, mechanism, *, origin="agent_reported"):
    dispatch=slide["dispatch"]
    return {"schema_version":1,"execution_contract_version":1,"attempt_id":dispatch["attempt_id"],
        "agent_id":dispatch["agent_id"],"job_sha256":slide["job_sha256"],
        "backend_used":job["expected_backend"],"tool_name":job.get("generation_config",{}).get("tool_name",job["expected_backend"]),
        "operation":job["execution"]["operation"],"mechanism":mechanism,"evidence_origin":origin,
        "call_reference":None,"candidate":{"path":str(Path(candidate).resolve()),"sha256":sha256(candidate)},
        "attachments":attachments(job["input_images"])}


def validate_receipt(receipt, job, slide, candidate, *, recorded=False):
    expected=make_receipt(job,slide,candidate,receipt.get("mechanism"))
    if recorded:
        expected["candidate"]["path"]=(slide.get("result") or {}).get("selected_source")
    for key in ("schema_version","execution_contract_version","attempt_id","agent_id","job_sha256",
                "backend_used","tool_name","operation","candidate","attachments"):
        if receipt.get(key)!=expected[key] or (key in {"schema_version","execution_contract_version"} and type(receipt.get(key)) is not int):
            raise ValueError("Submission evidence mismatch: " + key)
    if not isinstance(receipt.get("mechanism"),str) or not receipt["mechanism"].strip():
        raise ValueError("Submission evidence needs actual input mechanism")
    for image in job["input_images"]:
        if sha256(image["path"]) != image["sha256"]:
            raise ValueError("Submission input bytes changed")
    from generation_execution import is_cli_backend
    if is_cli_backend(job["expected_backend"]):
        completion=slide.get("execution_completion",{})
        if (receipt.get("evidence_origin")!="adapter" or completion.get("producer")!="run_slide_job.py"
            or completion.get("status")!="succeeded" or completion.get("dry_run") is not False
            or completion.get("receipt")!=receipt):
            raise ValueError("Submission has no matching registered adapter completion")
        return "adapter_verified"
    if receipt.get("evidence_origin") != "agent_reported":
        raise ValueError("Native/bridge submission evidence must remain agent_reported")
    return "agent_reported"


def require_recorded_submission(job, slide, final_image):
    result=slide.get("result") or {}
    receipt=result.get("submission")
    if not isinstance(receipt,dict):
        raise ValueError("Current submission evidence required; recompile and generate this final page")
    verification=validate_receipt(receipt,job,slide,final_image,recorded=True)
    if result.get("submission_verification")!=verification:
        raise ValueError("Recorded submission verification differs from actual evidence")


def validate_output_requirements(requirements):
    if requirements is None:
        return
    if not isinstance(requirements,dict):
        raise ValueError("Output requirements must be an object")
    for key,value in requirements.items():
        if key not in {"min_width","min_height","exact_width","exact_height"} or type(value) is not int or value<=0:
            raise ValueError("Invalid approved output requirement")
    for axis in ("width","height"):
        if requirements.get("exact_"+axis,float("inf"))<requirements.get("min_"+axis,0):
            raise ValueError("Exact output size conflicts with minimum")


def measured_output(path, ratio, requirements=None):
    from slide_image_ratio import RATIO_BY_LABEL,require_image_ratio
    validate_output_requirements(requirements)
    width,height=require_image_ratio(str(path),RATIO_BY_LABEL[ratio],ratio)
    for key,value in (requirements or {}).items():
        if key not in {"min_width","min_height","exact_width","exact_height"} or type(value) is not int or value<=0:
            raise ValueError("Invalid approved output requirement")
        actual=width if key.endswith("width") else height
        if (key.startswith("min_") and actual<value) or (key.startswith("exact_") and actual!=value):
            raise ValueError(f"Output requirement {key}={value} unmet; actual {width}x{height}")
    return {"measured_width":width,"measured_height":height,"measured_megapixels":width*height/1_000_000,
        "ratio_error":abs((width/height)/RATIO_BY_LABEL[ratio]-1)}
