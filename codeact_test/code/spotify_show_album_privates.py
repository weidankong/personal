# -*- coding: utf-8 -*-
"""The show_album_privates tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class AlbumPrivatesOutput(BaseModel):
    liked: bool = Field(description="Whether the album is liked")
    reviewed: bool = Field(description="Whether the album is reviewed")
    in_library: bool = Field(description="Whether the album is in library")


def show_album_privates(
    album_id: int,
    access_token: str,
) -> ToolResponse:
    """Show private info (liked, reviewed, in library) about an album for the logged-in user.

    Args:
        album_id (`int`): The ID of the album.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Private album info or error.
    """
    code = (
        f"print(apis.spotify.show_album_privates("
        f"album_id={fmt(album_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
