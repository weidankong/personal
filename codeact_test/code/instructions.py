import inspect
import re
from typing import Type, get_type_hints

from pydantic import create_model, TypeAdapter
from pydantic.fields import FieldInfo
from pydantic import BaseModel


CODEACT_SYSTEM_PROMPT = """You have one primary tool: run_python_code.

Prefer one run_python_code call per request when possible.
Its tool description contains the current `call_tool(...)` guidance.

To surface results from `run_python_code`, end the code with `print(...)`; the sandbox does not \
return the value of the last expression.

Some tools may also appear directly, but prefer `run_python_code` whenever you need to combine Python \
control flow with sandbox tool calls.
"""


def _parse_docstring_param_descriptions(doc: str) -> dict[str, str]:
    """Extract param descriptions from a Google-style docstring Args section."""
    descriptions: dict[str, str] = {}
    # Match lines like "    arg_name (`type`): description..."
    pattern = re.compile(r"^\s+(\w+)\s+\(.*?\):\s+(.+)$", re.MULTILINE)
    for m in pattern.finditer(doc):
        descriptions[m.group(1)] = m.group(2).strip()
    return descriptions


def _build_input_schema_from_func(func: callable) -> dict:
    """Build a JSON Schema for the function's input parameters."""
    sig = inspect.signature(func)
    type_hints = get_type_hints(func)
    doc = inspect.getdoc(func) or ""
    param_descs = _parse_docstring_param_descriptions(doc)

    fields = {}
    for name, param in sig.parameters.items():
        if name == "return":
            continue
        hint = type_hints.get(name, None)
        has_default = param.default is not inspect.Parameter.empty
        default_val = param.default if has_default else ...
        field_info = FieldInfo(
            default=default_val,
            description=param_descs.get(name, ""),
        )
        fields[name] = (hint if hint is not None else str, field_info)

    input_model = create_model(f"{func.__name__}_Input", **fields)
    schema = input_model.model_json_schema()
    schema.pop("title", None)
    schema.pop("$defs", None)
    return schema


def _resolve_refs(obj, defs):
    """Recursively resolve $ref pointers using defs dict."""
    if isinstance(obj, dict):
        if "$ref" in obj:
            ref_name = obj["$ref"].split("/")[-1]
            return _resolve_refs(defs.get(ref_name, obj), defs)
        return {k: _resolve_refs(v, defs) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_resolve_refs(item, defs) for item in obj]
    return obj


def _build_registered_tools_str(
    callable_tools: dict,
    output_models: dict,
) -> str:
    lines = []
    for name, func in callable_tools.items():
        doc_first_line = (inspect.getdoc(func) or "").split("\n")[0]
        entry = f"  - {name}(): {doc_first_line}\n"

        # Input schema from function signature
        input_schema = _build_input_schema_from_func(func)
        if input_schema.get("properties"):
            entry += f"    Input schema: {input_schema}\n"
        else:
            entry += "    Input schema: no input parameters\n"

        # Output schema from registered model
        output_model = output_models.get(name)
        if output_model is not None:
            schema = output_model.model_json_schema()
            schema.pop("title", None)
            defs = schema.pop("$defs", {})
            schema = _resolve_refs(schema, defs)
            entry += f"    Output schema: {schema}\n"
        lines.append(entry)
    return "\n".join(lines)


def build_run_python_code_description(
    callable_tools: dict,
    output_models: dict,
) -> str:
    """Build the tool description for run_python_code."""
    registered_tools = _build_registered_tools_str(callable_tools, output_models)
    return (
        "Execute Python code in an IPython sandbox and return the output.\n\n"
        "The code runs as an **IPython cell** — **NEVER** wrap it in main function.\n"
        "Inside the sandbox, `call_tool(name, **kwargs)` is *ALREADY* available as a "
        "synchronous built-in for registered host callbacks. Use the tool name as the first "
        "argument and keyword arguments only — do not pass a dict or any other "
        "positional arguments after the tool name.\n\n"

        "Prefer `run_python_code` when you need to combine one or more"
        "`call_tool(...)` calls with Python control flow, loops, or"
        "post-processing.\n\n"


        "Registered sandbox tools:\n"
        f"    {registered_tools}\n\n"
        "Args:\n"
        "    code (`str`): The Python code to be executed.\n\n"
        "Returns:\n"
        "    `ToolResponse`: The response containing the execution output.\n"
    )
