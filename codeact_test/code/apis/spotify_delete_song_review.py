# -*- coding: utf-8 -*-
"""The delete_song_review tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class DeleteSongReviewOutput(BaseModel):
    message: str = Field(description="Confirmation message")

def delete_song_review(review_id: int, access_token: str) -> ToolResponse:
    """Delete a song review.

    Args:
        review_id (`int`): ID of the song review to delete.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`:
            The tool response containing a confirmation message,
            or an error message if review not found.
    """
    code = (
        f"print(apis.spotify.delete_song_review("
        f"review_id={fmt(review_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
