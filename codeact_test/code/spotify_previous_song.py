# -*- coding: utf-8 -*-
"""The previous_song tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class PreviousSongOutput(BaseModel):
    message: str = Field(description="Confirmation message")
    song_id: int = Field(description="ID of the previous song")


def previous_song(
    access_token: str,
) -> ToolResponse:
    """Go to the previous song in the queue.

    Args:
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message with song ID or error.
    """
    code = (
        f"print(apis.spotify.previous_song("
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
