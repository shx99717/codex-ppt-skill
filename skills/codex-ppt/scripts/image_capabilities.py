"""Documented API capabilities scoped to one configured model/provider.

Missing facts are unknown. Native image tools do not use this API contract.
"""
from __future__ import annotations
from datetime import date


def resolve_model(explicit=None, configured=None):
    for value in (explicit, configured):
        if isinstance(value, str) and value.strip():
            return value.strip()
    raise ValueError("No API image model configured. Select a documented model and set --model or CODEX_PPT_IMAGE_MODEL.")


def validate_capabilities(profile, model, base_url, operation, parameters, has_images, *, managed=True):
    """Validate only requested facts; unknown standalone options defer to provider."""
    if profile is None:
        if managed:
            raise ValueError("Unknown API capabilities: document the selected model/provider operation before managed generation")
        return
    if not isinstance(profile, dict):
        raise ValueError("Capabilities must be an object")
    base = (base_url or "https://api.openai.com/v1").rstrip("/")
    if profile.get("model") != model or str(profile.get("provider_base_url", "")).rstrip("/") != base:
        raise ValueError("Capability evidence does not match selected model/provider")
    operations = profile.get("operations")
    if not isinstance(operations, dict):
        raise ValueError("Capabilities require an operations object")
    facts = operations.get(operation)
    if facts is None:
        if managed:
            raise ValueError("Unknown API operation capability: " + operation)
        return
    if not isinstance(facts, dict) or not isinstance(facts.get("source"), str) or not facts["source"].strip():
        raise ValueError("Capability facts need a documentation source")
    try:
        date.fromisoformat(facts.get("checked_on", ""))
    except (TypeError, ValueError) as exc:
        raise ValueError("Capability facts need checked_on YYYY-MM-DD") from exc

    def require(key, predicate):
        value = facts.get(key)
        if value is None:
            if managed:
                raise ValueError("Unknown API capability: " + key)
        elif not predicate(value):
            raise ValueError("Unsupported API setting: " + key)

    if has_images:
        require("supports_image_inputs", lambda v: v is True)
    if parameters.get("quality") is not None:
        require("qualities", lambda v: isinstance(v,list) and parameters["quality"] in v)
    if parameters.get("background") == "transparent":
        require("supports_transparency", lambda v: v is True)
    if parameters.get("input_fidelity") is not None:
        require("input_fidelity", lambda v: isinstance(v,list) and parameters["input_fidelity"] in v)
    size = parameters.get("size")
    if size and size != "auto":
        require("size_constraints", lambda v: isinstance(v,dict))
        limits = facts.get("size_constraints")
        if limits is not None:
            w,h = map(int,size.split("x"))
            for key,value in limits.items():
                if key not in {"max_edge","multiple","min_pixels","max_pixels","max_ratio"} or type(value) not in (int,float) or value <= 0:
                    raise ValueError("Invalid size capability constraint")
            if "multiple" in limits and (type(limits["multiple"]) is not int or w%limits["multiple"] or h%limits["multiple"]):
                raise ValueError("Size violates documented multiple")
            if (max(w,h)>limits.get("max_edge",float("inf")) or w*h<limits.get("min_pixels",0)
                or w*h>limits.get("max_pixels",float("inf")) or max(w,h)/min(w,h)>limits.get("max_ratio",float("inf"))):
                raise ValueError("Size violates documented capability")
