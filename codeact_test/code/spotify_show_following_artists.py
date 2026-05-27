# -*- coding: utf-8 -*-
"""The show_following_artists tool — spotify app."""

import json
from typing import List, Optional

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class FollowingArtist(BaseModel):
    artist_id: int = Field(description="Unique artist ID")
    name: str = Field(description="Artist name")
    genre: str = Field(description="Music genre")
    follower_count: int = Field(description="Number of followers")


class FollowingArtistsOutput(RootModel[List[FollowingArtist]]):
    """List of followed artists"""


def show_following_artists(
    access_token: str,
    query: str = "",
    page_index: int = 0,
    page_limit: int = 5,
    sort_by: Optional[str] = None,
) -> ToolResponse:
    """Get a list of artists you are following.

    Args:
        access_token (`str`): Access token obtained from spotify app login.
        query (`str`): The search query string. Defaults to "".
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.
        sort_by (`str`, optional): Sort attribute prefixed with +/- for ascending/descending.
            Valid: follower_count, name.

    Returns:
        `ToolResponse`: List of followed artists or error.
    """
    code = (
        f"print(apis.spotify.show_following_artists("
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
