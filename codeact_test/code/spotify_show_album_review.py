# -*- coding: utf-8 -*-
"""The show_album_review tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class AlbumReviewOutput(BaseModel):
    review_id: int = Field(description="Unique review ID")
    rating: int = Field(description="Rating (1-5)")
    title: str = Field(description="Review title")
    text: str = Field(description="Review text")
    user_email: str = Field(description="Reviewer email")
    created_at: str = Field(description="ISO format creation date")


def show_album_review(
    review_id: int,
) -> ToolResponse:
    """Show a specific album review.

    Args:
        review_id (`int`): The ID of the review.

    Returns:
        `ToolResponse`: Review details or error.
    """
    code = (
        f"print(apis.spotify.show_album_review("
        f"review_id={fmt(review_id)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
