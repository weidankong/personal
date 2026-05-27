# -*- coding: utf-8 -*-
"""The add_to_queue tool — spotify app."""

import json
from typing import Optional

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class AddToQueueOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def add_to_queue(
    access_token: str,
    song_id: Optional[int] = None,
    album_id: Optional[int] = None,
    playlist_id: Optional[int] = None,
) -> ToolResponse:
    """Add a song, album, or playlist to the queue.

    Args:
        access_token (`str`): Access token obtained from spotify app login.
        song_id (`int`, optional): The ID of the song to add.
        album_id (`int`, optional): The ID of the album to add.
        playlist_id (`int`, optional): The ID of the playlist to add.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.add_to_queue("
        f"access_token={fmt(access_token)}, "
        f"song_id={fmt(song_id)}, "
        f"album_id={fmt(album_id)}, "
        f"playlist_id={fmt(playlist_id)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
