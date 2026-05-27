# -*- coding: utf-8 -*-
"""The show_song_queue tool — spotify app."""

import json
from typing import List

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class QueueSongArtist(BaseModel):
    id: int = Field(description="Artist ID")
    name: str = Field(description="Artist name")


class QueueSong(BaseModel):
    song_id: int = Field(description="Unique song ID")
    title: str = Field(description="Song title")
    album_id: int = Field(description="Album ID")
    album_title: str = Field(description="Album title")
    duration: int = Field(description="Duration in seconds")
    artists: List[QueueSongArtist] = Field(description="List of artists")
    position: int = Field(description="Position in the queue")


class SongQueueOutput(RootModel[List[QueueSong]]):
    """List of songs in the queue"""


def show_song_queue(
    access_token: str,
) -> ToolResponse:
    """Show the current song queue.

    Args:
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: List of songs in queue or error.
    """
    code = (
        f"print(apis.spotify.show_song_queue("
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
