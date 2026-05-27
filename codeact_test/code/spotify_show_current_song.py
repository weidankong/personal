# -*- coding: utf-8 -*-
"""The show_current_song tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class CurrentSongOutput(BaseModel):
    song_id: int = Field(description="Unique song ID")
    title: str = Field(description="Song title")
    album_id: int = Field(description="Album ID")
    album_title: str = Field(description="Album title")
    duration: int = Field(description="Duration in seconds")
    progress: int = Field(description="Current playback position in seconds")
    is_playing: bool = Field(description="Whether the song is currently playing")


def show_current_song(
    access_token: str,
) -> ToolResponse:
    """Show the currently playing song and playback status.

    Args:
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Current song info or error.
    """
    code = (
        f"print(apis.spotify.show_current_song("
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
