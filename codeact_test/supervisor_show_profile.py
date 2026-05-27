# -*- coding: utf-8 -*-
"""The show_profile tool — supervisor app."""

import json

from pydantic import BaseModel, Field, ValidationError

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world


class SupervisorProfileOutput(BaseModel):
    first_name: str = Field(description="Supervisor's first name")
    last_name: str = Field(description="Supervisor's last name")
    email: str = Field(description="Supervisor's email address")
    phone_number: str = Field(description="Supervisor's phone number")
    birthday: str = Field(description="Supervisor's birthday")
    sex: str = Field(description="Supervisor's sex")


def _fmt(v):
    if v is None:
        return "None"
    if isinstance(v, str):
        return repr(v)
    return str(v)


def _validate_output(output: str, model: type[BaseModel]) -> ToolResponse:
    try:
        data = json.loads(output)
        model.model_validate(data)
        return ToolResponse(
            content=[TextBlock(type="text", text=output)],
            metadata=data,
        )
    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError(f"Output validation failed: {e}\nRaw output: {output}") from e


def show_profile() -> ToolResponse:
    """Show your supervisor's profile information.

    Returns:
        `ToolResponse`: The tool response containing supervisor profile, or an error message.
    """
    code = "print(apis.supervisor.show_profile())"
    output = world.world.execute(code)
    return _validate_output(output, SupervisorProfileOutput)
