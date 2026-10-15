"""Executable backend policy shared by compiler, consumers and CLI adapter."""
from __future__ import annotations

_CONTROL = {"backend_used", "tool_name", "mode", "reference_mode", "aspect_ratio"}
_CLI_FIELDS = {"model", "size", "quality", "background", "output_format",
               "output_compression", "moderation", "input_fidelity", "n"}


def is_cli_backend(backend: str) -> bool:
    from record_slide_result import _backend_family
    return _backend_family(backend) == "cli-api-fallback"


def execution_contract(config: dict, images: list, backend: str) -> dict:
    from planning_contract import ContractError
    operation = config.get("reference_mode", config["mode"]) if images else config["mode"]
    if not isinstance(operation, str) or not operation.strip():
        raise ContractError("Missing executable generation operation")
    if not is_cli_backend(backend):
        return {"operation": operation, "parameters": {k: v for k, v in config.items() if k not in _CONTROL}}
    unknown = set(config) - _CONTROL - _CLI_FIELDS
    if unknown:
        raise ContractError("Unsupported CLI generation fields: " + ", ".join(sorted(unknown)))
    for field in ("model", "size", "quality"):
        if not isinstance(config.get(field), str) or not config[field].strip():
            raise ContractError(f"CLI generation requires explicit {field}")
    if operation not in {"generate", "edit"}:
        raise ContractError("CLI operation must be generate or edit")
    if bool(images) != (operation == "edit"):
        raise ContractError("Image inputs require an explicitly approved reference_mode=edit; edit requires inputs")
    if type(config.get("n", 1)) is not int or config.get("n", 1) != 1:
        raise ContractError("Managed slide execution requires n=1")
    compression=config.get("output_compression")
    if compression is not None and (type(compression) is not int or not 0<=compression<=100):
        raise ContractError("output_compression must be an integer from 0 to 100")
    if config.get("output_format", "png") != "png":
        raise ContractError("Managed slide execution requires PNG output")
    parameters = {k: v for k, v in config.items() if k in _CLI_FIELDS}
    parameters.setdefault("n", 1)
    parameters.setdefault("output_format", "png")
    if operation == "generate" and parameters.get("input_fidelity") is not None:
        raise ContractError("input_fidelity applies only to the approved edit operation")
    import image_gen
    try:
        image_gen._validate_generate_payload(parameters)
        image_gen._validate_input_fidelity(parameters.get("input_fidelity"))
        image_gen._validate_model_specific_options(model=parameters["model"],
            background=parameters.get("background"), input_fidelity=parameters.get("input_fidelity"))
        image_gen._validate_transparency(parameters.get("background"), "png")
        from slide_image_ratio import RATIO_BY_LABEL
        width, height = (int(v) for v in parameters["size"].split("x"))
        target = RATIO_BY_LABEL[config["aspect_ratio"]]
        if abs(width / height - target) > 0.01:
            raise ContractError("CLI size conflicts with the approved aspect ratio")
    except (SystemExit, TypeError, ValueError, KeyError) as exc:
        raise ContractError("Invalid approved CLI generation parameters") from exc
    return {"operation": operation, "parameters": parameters}
