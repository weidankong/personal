# -*- coding: utf-8 -*-
"""The show_artist_following tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class ArtistFollowingOutput(BaseModel):
    is_following: bool = Field(description="Whether the user is following the artist")


def show_artist_following(
    artist_id: int,
    access_token: str,
) -> ToolResponse:
    """Check if the logged-in user is following an artist.

    Args:
        artist_id (`int`): The ID of the artist.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Following status or error.
    """
    code = (
        f"print(apis.spotify.show_artist_following("
        f"artist_id={fmt(artist_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
