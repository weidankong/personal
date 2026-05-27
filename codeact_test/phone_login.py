# -*- coding: utf-8 -*-
"""The login tool — phone app."""

import json

from pydantic import BaseModel, Field, ValidationError

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world


class LoginOutput(BaseModel):
    access_token: str = Field(description="JWT access token for authentication")
    token_type: str = Field(description="Token type, typically 'Bearer'")


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


def login(
    username: str,
    password: str,
) -> ToolResponse:
    """Login to your phone account.

    Args:
        username (`str`): Your account phone number.
        password (`str`): Your account password.

    Returns:
        `ToolResponse`: The tool response containing access_token, or an error message.
    """
    code = f"print(apis.phone.login(username={_fmt(username)}, password={_fmt(password)}))"
    output = world.world.execute(code)
    return _validate_output(output, LoginOutput)
