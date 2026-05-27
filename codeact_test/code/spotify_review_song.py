# -*- coding: utf-8 -*-
"""The review_song tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class ReviewSongOutput(BaseModel):
    message: str = Field(description="Confirmation message")
    song_review_id: int = Field(description="ID of the newly created review")

def review_song(
    song_id: int,
    rating: int,
    access_token: str,
    title: str = "",
    text: str = "",
) -> ToolResponse:
    """Rate or review a song.

    Note: Returns 409 if a review already exists for this song.
    Use update_song_review instead in that case.

    Args:
        song_id (`int`): ID of the song to review.
        rating (`int`): Song rating (1-5).
        access_token (`str`): Access token obtained from spotify app login.
        title (`str`): Title of the review. Defaults to empty.
        text (`str`): Text content of the review. Defaults to empty.

    Returns:
        `ToolResponse`:
            The tool response containing a confirmation message and review ID,
            or an error message (409 if review already exists).
    """
    code = (
        f"print(apis.spotify.review_song("
        f"song_id={fmt(song_id)}, "
        f"rating={fmt(rating)}, "
        f"access_token={fmt(access_token)}, "
        f"title={fmt(title)}, "
        f"text={fmt(text)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
