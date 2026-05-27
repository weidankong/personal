# -*- coding: utf-8 -*-
"""The login tool — phone app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class PhoneLoginOutput(BaseModel):
    access_token: str = Field(description="JWT access token for authentication")
    token_type: str = Field(description="Token type, typically 'Bearer'")

def phone_login(
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
    code = f"print(apis.phone.login(username={fmt(username)}, password={fmt(password)}))"
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
