# -*- coding: utf-8 -*-
"""The login tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world


class LoginOutput(BaseModel):
    access_token: str = Field(description="Bearer access token for subsequent API calls")
    token_type: str = Field(description="Token type, usually 'Bearer'")


def _fmt(v):
    if v is None:
        return "None"
    if isinstance(v, str):
        return repr(v)
    return str(v)


def login(username: str, password: str) -> ToolResponse:
    """Login to a Spotify account and obtain an access token.

    Args:
        username (`str`): Your account email address.
        password (`str`): Your account password.

    Returns:
        `ToolResponse`:
            The tool response containing the access token,
            or an error message on invalid credentials.
    """
    code = f"print(apis.spotify.login(username={_fmt(username)}, password={_fmt(password)}))"
    output = world.world.execute(code)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
