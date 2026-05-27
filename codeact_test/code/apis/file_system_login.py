# -*- coding: utf-8 -*-
"""The login tool — file_system app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class FileSystemLoginOutput(BaseModel):
    access_token: str = Field(description="Bearer access token for subsequent API calls")
    token_type: str = Field(description="Token type, usually 'Bearer'")


def file_system_login(username: str, password: str) -> ToolResponse:
    """Login to your file system account.

    Args:
        username (`str`): Your account email address.
        password (`str`): Your account password.

    Returns:
        `ToolResponse`:
            The tool response containing the access token,
            or an error message on invalid credentials.
    """
    code = f"print(apis.file_system.login(username={fmt(username)}, password={fmt(password)}))"
    output = world.world.execute(code)
    output = convert(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
