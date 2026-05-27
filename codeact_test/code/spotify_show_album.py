# -*- coding: utf-8 -*-
"""The show_album tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class AlbumOutput(BaseModel):
    album_id: int = Field(description="Unique album ID")
    title: str = Field(description="Album title")
    genre: str = Field(description="Music genre")
    artist_id: int = Field(description="Artist ID")
    artist_name: str = Field(description="Artist name")
    release_date: str = Field(description="Release date")
    rating: float = Field(description="Average rating")
    like_count: int = Field(description="Number of likes")


def show_album(
    album_id: int,
) -> ToolResponse:
    """Show details of an album.

    Args:
        album_id (`int`): The ID of the album.

    Returns:
        `ToolResponse`: Album details or error.
    """
    code = (
        f"print(apis.spotify.show_album("
        f"album_id={fmt(album_id)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
