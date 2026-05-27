# -*- coding: utf-8 -*-
"""The play_music tool — spotify app."""

import json
from typing import Optional

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class PlayMusicOutput(BaseModel):
    message: str = Field(description="Confirmation message")
    song_id: int = Field(description="ID of the song now playing")


def play_music(
    access_token: str,
    song_id: Optional[int] = None,
    album_id: Optional[int] = None,
    playlist_id: Optional[int] = None,
    queue_position: Optional[int] = None,
) -> ToolResponse:
    """Play a song, album, or playlist.

    Args:
        access_token (`str`): Access token obtained from spotify app login.
        song_id (`int`, optional): The ID of the song to play.
        album_id (`int`, optional): The ID of the album to play.
        playlist_id (`int`, optional): The ID of the playlist to play.
        queue_position (`int`, optional): Position in queue to start from.

    Returns:
        `ToolResponse`: Confirmation message with song ID or error.
    """
    code = (
        f"print(apis.spotify.play_music("
        f"access_token={fmt(access_token)}, "
        f"song_id={fmt(song_id)}, "
        f"album_id={fmt(album_id)}, "
        f"playlist_id={fmt(playlist_id)}, "
        f"queue_position={fmt(queue_position)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
