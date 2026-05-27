# -*- coding: utf-8 -*-
"""The show_downloaded_songs tool — spotify app."""

import json
from typing import List, Optional

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class DownloadedSongArtist(BaseModel):
    id: int = Field(description="Artist ID")
    name: str = Field(description="Artist name")


class DownloadedSong(BaseModel):
    song_id: int = Field(description="Unique song ID")
    title: str = Field(description="Song title")
    album_id: Optional[int] = Field(description="Album ID")
    album_title: Optional[str] = Field(description="Album title")
    duration: int = Field(description="Duration in seconds")
    artists: List[DownloadedSongArtist] = Field(description="List of artists")
    downloaded_at: str = Field(description="ISO format timestamp")


class DownloadedSongsOutput(RootModel[List[DownloadedSong]]):
    """List of downloaded songs"""


def show_downloaded_songs(
    access_token: str,
    query: str = "",
    min_downloaded_at: str = "0001-01-01",
    max_downloaded_at: str = "9999-12-31",
    page_index: int = 0,
    page_limit: int = 5,
    sort_by: Optional[str] = None,
) -> ToolResponse:
    """Get a list of songs you have downloaded.

    Args:
        access_token (`str`): Access token obtained from spotify app login.
        query (`str`): The search query string. Defaults to "".
        min_downloaded_at (`str`): Minimum download date filter. Defaults to "0001-01-01".
        max_downloaded_at (`str`): Maximum download date filter. Defaults to "9999-12-31".
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.
        sort_by (`str`, optional): Sort attribute prefixed with +/- for ascending/descending.
            Valid: downloaded_at, title.

    Returns:
        `ToolResponse`: List of downloaded songs or error.
    """
    code = (
        f"print(apis.spotify.show_downloaded_songs("
        f"access_token={fmt(access_token)}, "
        f"query={fmt(query)}, "
        f"min_downloaded_at={fmt(min_downloaded_at)}, "
        f"max_downloaded_at={fmt(max_downloaded_at)}, "
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
