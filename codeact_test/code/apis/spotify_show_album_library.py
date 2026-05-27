# -*- coding: utf-8 -*-
"""The show_album_library tool — spotify app."""

from typing import List, Optional
import json

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class LibraryAlbumArtist(BaseModel):
    id: int = Field(description="Artist ID")
    name: str = Field(description="Artist name")


class LibraryAlbum(BaseModel):
    album_id: int = Field(description="Unique album ID")
    title: str = Field(description="Album title")
    genre: str = Field(description="Music genre")
    artists: List[LibraryAlbumArtist] = Field(description="List of artists")
    rating: float = Field(description="Album rating (0.0-5.0)")
    like_count: int = Field(description="Number of likes")
    review_count: int = Field(description="Number of reviews")
    release_date: str = Field(description="ISO format release date")
    song_ids: List[int] = Field(description="List of song IDs in the album")
    added_at: str = Field(description="ISO format date when added to library")


class AlbumLibraryOutput(RootModel[List[LibraryAlbum]]):
    """List of albums in the album library"""


def show_album_library(
    access_token: str,
    query: str = "",
    page_index: int = 0,
    page_limit: int = 5,
    sort_by: Optional[str] = None,
) -> ToolResponse:
    """Search or show a list of albums in your album library.

    Args:
        access_token (`str`): Access token obtained from spotify app login.
        query (`str`): The search query string. Defaults to "".
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.
        sort_by (`str`, optional): Sort attribute prefixed with +/- for ascending/descending.
            Valid: added_at, title.

    Returns:
        `ToolResponse`: The tool response containing a list of albums in library, or an error message.
    """
    code = (
        f"print(apis.spotify.show_album_library("
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
