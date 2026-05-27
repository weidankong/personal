# -*- coding: utf-8 -*-
"""The show_profile tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class SpotifyProfileOutput(BaseModel):
    first_name: str = Field(description="First name")
    last_name: str = Field(description="Last name")
    email: str = Field(description="Email address")


def show_profile(
    email: str,
) -> ToolResponse:
    """Show the public profile of a Spotify user by email.

    Args:
        email (`str`): Email address of the user.

    Returns:
        `ToolResponse`: User profile or error.
    """
    code = (
        f"print(apis.spotify.show_profile("
        f"email={fmt(email)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
