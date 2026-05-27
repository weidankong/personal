# -*- coding: utf-8 -*-
"""The search_artists tool — spotify app."""

from typing import List, Optional
import json

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class SearchArtist(BaseModel):
    artist_id: int = Field(description="Unique artist ID")
    name: str = Field(description="Artist name")
    genre: str = Field(description="Music genre")
    follower_count: int = Field(description="Number of followers")
    created_at: str = Field(description="ISO format creation date")


class SearchArtistsOutput(RootModel[List[SearchArtist]]):
    """List of artists matching the search query"""


def search_artists(
    query: str = "",
    genre: Optional[str] = None,
    min_follower_count: int = 0,
    max_follower_count: int = 9223372036854775807,
    page_index: int = 0,
    page_limit: int = 5,
    sort_by: Optional[str] = None,
) -> ToolResponse:
    """Search for artists with a query.

    Args:
        query (`str`): The search query string. Defaults to "".
        genre (`str`, optional): Filter by genre.
        min_follower_count (`int`): Minimum number of followers. Defaults to 0.
        max_follower_count (`int`): Maximum number of followers.
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.
        sort_by (`str`, optional): Sort attribute prefixed with +/- for ascending/descending.
            Valid: follower_count.

    Returns:
        `ToolResponse`: The tool response containing a list of artists, or an error message.
    """
    code = (
        f"print(apis.spotify.search_artists("
        f"query={fmt(query)}, "
        f"genre={fmt(genre)}, "
        f"min_follower_count={fmt(min_follower_count)}, "
        f"max_follower_count={fmt(max_follower_count)}, "
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
