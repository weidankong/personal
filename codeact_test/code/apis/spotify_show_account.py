# -*- coding: utf-8 -*-
"""The show_account tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class SpotifyAccountOutput(BaseModel):
    first_name: str = Field(description="First name")
    last_name: str = Field(description="Last name")
    email: str = Field(description="Email address")


def show_account(
    access_token: str,
) -> ToolResponse:
    """Show the full account details of the logged-in Spotify user.

    Args:
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Account details or error.
    """
    code = (
        f"print(apis.spotify.show_account("
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
