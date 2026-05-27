# -*- coding: utf-8 -*-
"""The show_song_reviews tool — spotify app."""

from typing import List, Optional
import json

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class ReviewUser(BaseModel):
    name: str = Field(description="Reviewer name")
    email: str = Field(description="Reviewer email")


class SongReviewEntry(BaseModel):
    song_review_id: int = Field(description="Review ID")
    song_id: int = Field(description="Song ID")
    rating: float = Field(description="Song rating (1-5)")
    title: str = Field(description="Review title")
    text: str = Field(description="Review text")
    created_at: str = Field(description="ISO format timestamp")
    user: ReviewUser = Field(description="Reviewer information")


class SongReviewsOutput(RootModel[List[SongReviewEntry]]):
    """List of reviews for the song"""

def show_song_reviews(
    song_id: int,
    query: Optional[str] = None,
    user_email: Optional[str] = None,
    min_rating: Optional[int] = None,
    max_rating: Optional[int] = None,
    page_index: int = 0,
    page_limit: int = 5,
    sort_by: Optional[str] = None,
) -> ToolResponse:
    """Search or show a list of reviews for a song.

    Use this to find reviews by song_id and get review_id for update_song_review.

    Args:
        song_id (`int`): ID of the song.
        query (`str`): Optional search query for filtering reviews.
        user_email (`str`): Optional filter by reviewer email.
        min_rating (`int`): Optional minimum rating filter.
        max_rating (`int`): Optional maximum rating filter.
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): The maximum number of results per page. Defaults to 5.
        sort_by (`str`): Optional sort attribute.

    Returns:
        `ToolResponse`:
            The tool response containing a list of review objects,
            or an error message.
    """
    code = (
        f"print(apis.spotify.show_song_reviews("
        f"song_id={fmt(song_id)}"
    )
    if query is not None:
        code += f", query={fmt(query)}"
    if user_email is not None:
        code += f", user_email={fmt(user_email)}"
    if min_rating is not None:
        code += f", min_rating={fmt(min_rating)}"
    if max_rating is not None:
        code += f", max_rating={fmt(max_rating)}"
    code += f", page_index={fmt(page_index)}, page_limit={fmt(page_limit)}"
    if sort_by is not None:
        code += f", sort_by={fmt(sort_by)}"
    code += "))"

    output = world.world.execute(code)
    output = convert(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
