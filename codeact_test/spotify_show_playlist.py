# -*- coding: utf-8 -*-
"""The show_playlist tool — spotify app."""

from typing import List, Optional
import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class PlaylistSongArtist(BaseModel):
    id: int = Field(description="Artist ID")
    name: str = Field(description="Artist name")


class PlaylistSong(BaseModel):
    id: int = Field(description="Song ID")
    title: str = Field(description="Song title")
    album_id: int = Field(description="Album ID")
    album_title: str = Field(description="Album title")
    duration: int = Field(description="Duration in seconds")
    artists: List[PlaylistSongArtist] = Field(description="List of artists")


class PlaylistOwner(BaseModel):
    name: str = Field(description="Owner's full name")
    email: str = Field(description="Owner's email address")


class PlaylistOutput(BaseModel):
    playlist_id: int = Field(description="Unique playlist ID")
    title: str = Field(description="Playlist title")
    is_public: bool = Field(description="Whether the playlist is public")
    rating: float = Field(description="Playlist rating (0.0–5.0)")
    like_count: int = Field(description="Number of likes")
    review_count: int = Field(description="Number of reviews")
    owner: PlaylistOwner = Field(description="Playlist owner info")
    created_at: str = Field(description="ISO format creation timestamp")
    shareable_link: str = Field(description="Shareable URL for the playlist")
    songs: List[PlaylistSong] = Field(description="List of songs in the playlist")

def show_playlist(
    playlist_id: int,
    access_token: Optional[str] = None,
) -> ToolResponse:
    """Get detailed information about a specific playlist.

    Args:
        playlist_id (`int`): The playlist ID to retrieve.
        access_token (`str`, optional): Access token obtained from spotify app login.
            Required for private playlists.

    Returns:
        `ToolResponse`: The tool response containing the playlist details, or an error message.
    """
    code = f"print(apis.spotify.show_playlist(playlist_id={fmt(playlist_id)}, access_token={fmt(access_token)}))"
    output = world.world.execute(code)
    output = convert(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
