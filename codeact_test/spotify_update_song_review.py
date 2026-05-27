# -*- coding: utf-8 -*-
"""The update_song_review tool — spotify app."""

from typing import Optional
import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world


class UpdateSongReviewOutput(BaseModel):
    message: str = Field(description="Confirmation message")


def _fmt(v):
    if v is None:
        return "None"
    if isinstance(v, str):
        return repr(v)
    return str(v)


def update_song_review(
    review_id: int,
    access_token: str,
    rating: Optional[int] = None,
    title: Optional[str] = None,
    text: Optional[str] = None,
) -> ToolResponse:
    """Update an existing song review on Spotify.

    Args:
        review_id (`int`): ID of the song review to update (not song_id).
        access_token (`str`): Access token obtained from spotify app login.
        rating (`int`): New song rating (1-5). Optional.
        title (`str`): New review title. Optional.
        text (`str`): New review text. Optional.

    Returns:
        `ToolResponse`:
            The tool response containing a confirmation message,
            or an error message if review not found.
    """
    code = (
        f"print(apis.spotify.update_song_review("
        f"review_id={_fmt(review_id)}, "
        f"access_token={_fmt(access_token)}"
    )
    if rating is not None:
        code += f", rating={_fmt(rating)}"
    if title is not None:
        code += f", title={_fmt(title)}"
    if text is not None:
        code += f", text={_fmt(text)}"
    code += "))"

    output = world.world.execute(code)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
