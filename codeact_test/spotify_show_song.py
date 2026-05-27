# -*- coding: utf-8 -*-
"""The show_song tool — spotify app."""

from typing import List
import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world


class SongArtist(BaseModel):
    id: int = Field(description="Artist ID")
    name: str = Field(description="Artist name")
    genre: str = Field(description="Music genre")
    follower_count: int = Field(description="Number of followers")


class SongOutput(BaseModel):
    song_id: int = Field(description="Unique song ID")
    title: str = Field(description="Song title")
    album_id: int = Field(description="Album ID")
    album_title: str = Field(description="Album title")
    duration: int = Field(description="Duration in seconds")
    artists: List[SongArtist] = Field(description="List of artists")
    release_date: str = Field(description="ISO format release date")
    genre: str = Field(description="Music genre")
    play_count: int = Field(description="Number of plays")
    rating: float = Field(description="Song rating (0.0–5.0)")
    like_count: int = Field(description="Number of likes")
    review_count: int = Field(description="Number of reviews")
    shareable_link: str = Field(description="Shareable URL for the song")


def _fmt(v):
    if v is None:
        return "None"
    if isinstance(v, str):
        return repr(v)
    return str(v)


def show_song(song_id: int) -> ToolResponse:
    """Get details of a specific song from Spotify.

    Args:
        song_id (`int`): The song ID to retrieve.

    Returns:
        `ToolResponse`:
            The tool response containing the song details,
            or an error message if not found.
    """
    code = f"print(apis.spotify.show_song(song_id={_fmt(song_id)}))"
    output = world.world.execute(code)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
