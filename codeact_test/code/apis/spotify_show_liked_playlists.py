# -*- coding: utf-8 -*-
"""The show_liked_playlists tool — spotify app."""

import json
from typing import List

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class LikedPlaylist(BaseModel):
    playlist_id: int = Field(description="Unique playlist ID")
    title: str = Field(description="Playlist title")
    owner_name: str = Field(description="Owner name")
    is_public: bool = Field(description="Whether the playlist is public")
    liked_at: str = Field(description="ISO format timestamp")


class LikedPlaylistsOutput(RootModel[List[LikedPlaylist]]):
    """List of liked playlists"""


def show_liked_playlists(
    access_token: str,
    page_index: int = 0,
    page_limit: int = 5,
    sort_by: str = "-liked_at",
) -> ToolResponse:
    """Get a list of playlists you have liked.

    Args:
        access_token (`str`): Access token obtained from spotify app login.
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.
        sort_by (`str`): Sort attribute prefixed with +/- for ascending/descending.
            Valid: liked_at, title. Defaults to "-liked_at".

    Returns:
        `ToolResponse`: List of liked playlists or error.
    """
    code = (
        f"print(apis.spotify.show_liked_playlists("
        f"access_token={fmt(access_token)}, "
        f"page_index={fmt(page_index)}, "
        f"page_limit={fmt(page_limit)}, "
        f"sort_by={fmt(sort_by)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
