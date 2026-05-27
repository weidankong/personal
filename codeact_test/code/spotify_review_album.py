# -*- coding: utf-8 -*-
"""The review_album tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class ReviewAlbumOutput(BaseModel):
    message: str = Field(description="Confirmation message")
    review_id: int = Field(description="ID of the created review")


def review_album(
    album_id: int,
    rating: int,
    title: str,
    text: str,
    access_token: str,
) -> ToolResponse:
    """Write a review for an album.

    Args:
        album_id (`int`): The ID of the album.
        rating (`int`): Rating (1-5).
        title (`str`): Review title.
        text (`str`): Review text.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message with review ID or error.
    """
    code = (
        f"print(apis.spotify.review_album("
        f"album_id={fmt(album_id)}, "
        f"rating={fmt(rating)}, "
        f"title={fmt(title)}, "
        f"text={fmt(text)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
