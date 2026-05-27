# -*- coding: utf-8 -*-
"""The show_artist tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class ArtistOutput(BaseModel):
    artist_id: int = Field(description="Unique artist ID")
    name: str = Field(description="Artist name")
    genre: str = Field(description="Music genre")
    follower_count: int = Field(description="Number of followers")


def show_artist(
    artist_id: int,
) -> ToolResponse:
    """Show details of an artist.

    Args:
        artist_id (`int`): The ID of the artist.

    Returns:
        `ToolResponse`: Artist details or error.
    """
    code = (
        f"print(apis.spotify.show_artist("
        f"artist_id={fmt(artist_id)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
