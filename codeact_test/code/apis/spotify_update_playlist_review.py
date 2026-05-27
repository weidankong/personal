# -*- coding: utf-8 -*-
"""The update_playlist_review tool — spotify app."""

import json
from typing import Optional

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class UpdatePlaylistReviewOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def update_playlist_review(
    review_id: int,
    access_token: str,
    rating: Optional[int] = None,
    title: Optional[str] = None,
    text: Optional[str] = None,
) -> ToolResponse:
    """Update a playlist review.

    Args:
        review_id (`int`): The ID of the review to update.
        access_token (`str`): Access token obtained from spotify app login.
        rating (`int`, optional): New rating (1-5).
        title (`str`, optional): New title.
        text (`str`, optional): New text.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.update_playlist_review("
        f"review_id={fmt(review_id)}, "
        f"access_token={fmt(access_token)}, "
        f"rating={fmt(rating)}, "
        f"title={fmt(title)}, "
        f"text={fmt(text)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
