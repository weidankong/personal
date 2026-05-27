# -*- coding: utf-8 -*-
"""The show_playlist_privates tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class PlaylistPrivatesOutput(BaseModel):
    liked: bool = Field(description="Whether the playlist is liked")
    reviewed: bool = Field(description="Whether the playlist is reviewed")
    in_library: bool = Field(description="Whether the playlist is in library")


def show_playlist_privates(
    playlist_id: int,
    access_token: str,
) -> ToolResponse:
    """Show private info (liked, reviewed, in library) about a playlist for the logged-in user.

    Args:
        playlist_id (`int`): The ID of the playlist.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Private playlist info or error.
    """
    code = (
        f"print(apis.spotify.show_playlist_privates("
        f"playlist_id={fmt(playlist_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
