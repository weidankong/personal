# -*- coding: utf-8 -*-
"""The add_song_to_playlist tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class MessageOutput(BaseModel):
    message: str = Field(description="Confirmation message")

def add_song_to_playlist(
    playlist_id: int,
    song_id: int,
    access_token: str,
) -> ToolResponse:
    """Add a song to a playlist.

    Args:
        playlist_id (`int`): The playlist ID to add the song to.
        song_id (`int`): The song ID to add.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.add_song_to_playlist("
        f"playlist_id={fmt(playlist_id)}, "
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
