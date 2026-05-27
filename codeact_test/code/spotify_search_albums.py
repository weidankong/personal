# -*- coding: utf-8 -*-
"""The search_albums tool — spotify app."""

import json
from typing import List, Optional

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class AlbumShortened(BaseModel):
    album_id: int = Field(description="Unique album ID")
    title: str = Field(description="Album title")
    genre: str = Field(description="Music genre")
    artist_id: int = Field(description="Artist ID")
    artist_name: str = Field(description="Artist name")
    rating: float = Field(description="Average rating")
    like_count: int = Field(description="Number of likes")


class SearchAlbumsOutput(RootModel[List[AlbumShortened]]):
    """List of albums matching the search query"""


def search_albums(
    query: str = "",
    page_index: int = 0,
    page_limit: int = 5,
    min_rating: float = 0,
    max_rating: float = 5,
    min_release_date: str = "0001-01-01",
    max_release_date: str = "9999-12-31",
    min_like_count: int = 0,
    max_like_count: int = 9223372036854775807,
    genre: Optional[str] = None,
    sort_by: Optional[str] = None,
) -> ToolResponse:
    """Search for albums with a query.

    Args:
        query (`str`): The search query string. Defaults to "".
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.
        min_rating (`float`): Minimum rating filter. Defaults to 0.
        max_rating (`float`): Maximum rating filter. Defaults to 5.
        min_release_date (`str`): Minimum release date filter. Defaults to "0001-01-01".
        max_release_date (`str`): Maximum release date filter. Defaults to "9999-12-31".
        min_like_count (`int`): Minimum like count filter. Defaults to 0.
        max_like_count (`int`): Maximum like count filter. Defaults to max int.
        genre (`str`, optional): Filter by genre.
        sort_by (`str`, optional): Sort attribute prefixed with +/- for ascending/descending.
            Valid: release_date, like_count, rating.

    Returns:
        `ToolResponse`: List of albums or error.
    """
    code = (
        f"print(apis.spotify.search_albums("
        f"query={fmt(query)}, "
        f"page_index={fmt(page_index)}, "
        f"page_limit={fmt(page_limit)}, "
        f"min_rating={fmt(min_rating)}, "
        f"max_rating={fmt(max_rating)}, "
        f"min_release_date={fmt(min_release_date)}, "
        f"max_release_date={fmt(max_release_date)}, "
        f"min_like_count={fmt(min_like_count)}, "
        f"max_like_count={fmt(max_like_count)}, "
        f"genre={fmt(genre)}, "
        f"sort_by={fmt(sort_by)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
