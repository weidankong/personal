# -*- coding: utf-8 -*-
"""The show_song_review tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class ReviewUser(BaseModel):
    name: str = Field(description="Reviewer name")
    email: str = Field(description="Reviewer email")


class SongReviewOutput(BaseModel):
    song_review_id: int = Field(description="Review ID")
    song_id: int = Field(description="Song ID")
    rating: float = Field(description="Song rating (1-5)")
    title: str = Field(description="Review title")
    text: str = Field(description="Review text")
    created_at: str = Field(description="ISO format timestamp")
    user: ReviewUser = Field(description="Reviewer information")

def show_song_review(review_id: int) -> ToolResponse:
    """Show a song review.

    Args:
        review_id (`int`): The song review ID to retrieve.

    Returns:
        `ToolResponse`:
            The tool response containing the review details,
            or an error message if not found.
    """
    code = f"print(apis.spotify.show_song_review(review_id={fmt(review_id)}))"
    output = world.world.execute(code)
    output = convert(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
