# -*- coding: utf-8 -*-
"""The show_song_privates tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class SongPrivatesOutput(BaseModel):
    liked: bool = Field(description="Whether the song is liked")
    reviewed: bool = Field(description="Whether the song is reviewed")
    in_library: bool = Field(description="Whether the song is in library")
    downloaded: bool = Field(description="Whether the song is downloaded")


def show_song_privates(
    song_id: int,
    access_token: str,
) -> ToolResponse:
    """Show private info (liked, reviewed, in library, downloaded) about a song for the logged-in user.

    Args:
        song_id (`int`): The ID of the song.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Private song info or error.
    """
    code = (
        f"print(apis.spotify.show_song_privates("
        f"song_id={fmt(song_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
