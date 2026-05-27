# -*- coding: utf-8 -*-
"""The show_song_library tool — spotify app."""

from typing import List, Optional
import json

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class LibrarySongArtist(BaseModel):
    id: int = Field(description="Artist ID")
    name: str = Field(description="Artist name")


class LibrarySong(BaseModel):
    song_id: int = Field(description="Unique song ID")
    title: str = Field(description="Song title")
    album_id: int = Field(description="Album ID")
    album_title: str = Field(description="Album title")
    duration: int = Field(description="Duration in seconds")
    artists: List[LibrarySongArtist] = Field(description="List of artists")
    added_at: str = Field(description="ISO format date when added to library")


class SongLibraryOutput(RootModel[List[LibrarySong]]):
    """List of songs in the song library"""


def show_song_library(
    access_token: str,
    query: str = "",
    page_index: int = 0,
    page_limit: int = 5,
    sort_by: Optional[str] = None,
) -> ToolResponse:
    """Search or show a list of songs in your song library.

    Args:
        access_token (`str`): Access token obtained from spotify app login.
        query (`str`): The search query string. Defaults to "".
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.
        sort_by (`str`, optional): Sort attribute prefixed with +/- for ascending/descending.
            Valid: added_at, title.

    Returns:
        `ToolResponse`: The tool response containing a list of songs in library, or an error message.
    """
    code = (
        f"print(apis.spotify.show_song_library("
        f"access_token={fmt(access_token)}, "
        f"query={fmt(query)}, "
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
