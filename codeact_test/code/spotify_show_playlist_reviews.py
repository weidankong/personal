# -*- coding: utf-8 -*-
"""The show_playlist_reviews tool — spotify app."""

import json
from typing import List, Optional

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class PlaylistReview(BaseModel):
    review_id: int = Field(description="Unique review ID")
    rating: int = Field(description="Rating (1-5)")
    title: str = Field(description="Review title")
    text: str = Field(description="Review text")
    user_email: str = Field(description="Reviewer email")
    created_at: str = Field(description="ISO format creation date")


class PlaylistReviewsOutput(RootModel[List[PlaylistReview]]):
    """List of playlist reviews"""


def show_playlist_reviews(
    playlist_id: int,
    query: str = "",
    user_email: Optional[str] = None,
    min_rating: int = 1,
    max_rating: int = 5,
    page_index: int = 0,
    page_limit: int = 5,
    sort_by: Optional[str] = None,
    access_token: Optional[str] = None,
) -> ToolResponse:
    """Show reviews for a playlist.

    Args:
        playlist_id (`int`): The ID of the playlist.
        query (`str`): Search query string. Defaults to "".
        user_email (`str`, optional): Filter by reviewer email.
        min_rating (`int`): Minimum rating filter. Defaults to 1.
        max_rating (`int`): Maximum rating filter. Defaults to 5.
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.
        sort_by (`str`, optional): Sort attribute prefixed with +/- for ascending/descending.
        access_token (`str`, optional): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: List of playlist reviews or error.
    """
    code = (
        f"print(apis.spotify.show_playlist_reviews("
        f"playlist_id={fmt(playlist_id)}, "
        f"query={fmt(query)}, "
        f"user_email={fmt(user_email)}, "
        f"min_rating={fmt(min_rating)}, "
        f"max_rating={fmt(max_rating)}, "
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
