# -*- coding: utf-8 -*-
"""The show_playlist_review tool — spotify app."""

import json
from typing import Optional

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class PlaylistReviewOutput(BaseModel):
    review_id: int = Field(description="Unique review ID")
    rating: int = Field(description="Rating (1-5)")
    title: str = Field(description="Review title")
    text: str = Field(description="Review text")
    user_email: str = Field(description="Reviewer email")
    created_at: str = Field(description="ISO format creation date")


def show_playlist_review(
    review_id: int,
    access_token: Optional[str] = None,
) -> ToolResponse:
    """Show a specific playlist review.

    Args:
        review_id (`int`): The ID of the review.
        access_token (`str`, optional): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Review details or error.
    """
    code = (
        f"print(apis.spotify.show_playlist_review("
        f"review_id={fmt(review_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
