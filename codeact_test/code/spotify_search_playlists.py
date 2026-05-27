# -*- coding: utf-8 -*-
"""The search_playlists tool — spotify app."""

import json
from typing import List, Optional

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class PlaylistShortened(BaseModel):
    playlist_id: int = Field(description="Unique playlist ID")
    title: str = Field(description="Playlist title")
    owner_name: str = Field(description="Owner name")
    is_public: bool = Field(description="Whether the playlist is public")
    rating: float = Field(description="Average rating")
    like_count: int = Field(description="Number of likes")


class SearchPlaylistsOutput(RootModel[List[PlaylistShortened]]):
    """List of playlists matching the search query"""


def search_playlists(
    query: str = "",
    page_index: int = 0,
    page_limit: int = 5,
    min_like_count: int = 0,
    max_like_count: int = 9223372036854775807,
    min_rating: float = 0,
    max_rating: float = 5,
    owner_email: Optional[str] = None,
    sort_by: Optional[str] = None,
    access_token: Optional[str] = None,
) -> ToolResponse:
    """Search for playlists with a query.

    Args:
        query (`str`): The search query string. Defaults to "".
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.
        min_like_count (`int`): Minimum like count filter. Defaults to 0.
        max_like_count (`int`): Maximum like count filter. Defaults to max int.
        min_rating (`float`): Minimum rating filter. Defaults to 0.
        max_rating (`float`): Maximum rating filter. Defaults to 5.
        owner_email (`str`, optional): Filter by owner email.
        sort_by (`str`, optional): Sort attribute prefixed with +/- for ascending/descending.
            Valid: like_count, rating.
        access_token (`str`, optional): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: List of playlists or error.
    """
    code = (
        f"print(apis.spotify.search_playlists("
        f"query={fmt(query)}, "
        f"min_like_count={fmt(min_like_count)}, "
        f"max_like_count={fmt(max_like_count)}, "
        f"min_rating={fmt(min_rating)}, "
        f"max_rating={fmt(max_rating)}, "
        f"owner_email={fmt(owner_email)}, "
        f"page_index={fmt(page_index)}, "
        f"page_limit={fmt(page_limit)}, "
        f"sort_by={fmt(sort_by)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
