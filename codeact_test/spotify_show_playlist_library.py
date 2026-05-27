# -*- coding: utf-8 -*-
"""The show_playlist_library tool — spotify app."""

from typing import List, Optional

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock


class PlaylistOwner(BaseModel):
    name: str = Field(description="Owner's full name")
    email: str = Field(description="Owner's email address")


class Playlist(BaseModel):
    playlist_id: int = Field(description="Unique playlist ID")
    title: str = Field(description="Playlist title")
    is_public: bool = Field(description="Whether the playlist is public")
    rating: float = Field(description="Playlist rating (0.0–5.0)")
    like_count: int = Field(description="Number of likes")
    review_count: int = Field(description="Number of reviews")
    owner: PlaylistOwner = Field(description="Playlist owner info")
    created_at: str = Field(description="ISO format creation timestamp")
    song_ids: List[int] = Field(description="List of song IDs in the playlist")


class PlaylistLibraryOutput(BaseModel):
    playlists: List[Playlist] = Field(description="List of playlists")


def show_playlist_library(access_token: str, query: Optional[str] = None) -> ToolResponse:
    """Search or show a list of playlists in the user's Spotify playlist library.

    Args:
        access_token (`str`): Access token obtained from spotify login.
        query (`str`, optional): Search query to filter playlists by title, artist, etc.

    Returns:
        `ToolResponse`:
            The tool response containing a list of playlists,
            or an error message on auth failure.
    """
    # TODO: implement
    raise NotImplementedError
