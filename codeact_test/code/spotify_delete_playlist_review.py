# -*- coding: utf-8 -*-
"""The delete_playlist_review tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class DeletePlaylistReviewOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def delete_playlist_review(
    review_id: int,
    access_token: str,
) -> ToolResponse:
    """Delete a playlist review.

    Args:
        review_id (`int`): The ID of the review to delete.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.delete_playlist_review("
        f"review_id={fmt(review_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
