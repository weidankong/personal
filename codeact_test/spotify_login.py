# -*- coding: utf-8 -*-
"""The login tool — spotify app."""

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock


class LoginOutput(BaseModel):
    access_token: str = Field(description="Bearer access token for subsequent API calls")
    token_type: str = Field(description="Token type, usually 'Bearer'")


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
    # TODO: implement
    raise NotImplementedError
