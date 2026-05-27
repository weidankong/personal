# -*- coding: utf-8 -*-
"""The unfollow_artist tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class UnfollowArtistOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def unfollow_artist(
    artist_id: int,
    access_token: str,
) -> ToolResponse:
    """Unfollow an artist.

    Args:
        artist_id (`int`): The ID of the artist to unfollow.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.unfollow_artist("
        f"artist_id={fmt(artist_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
