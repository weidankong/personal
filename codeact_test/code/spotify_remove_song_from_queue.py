# -*- coding: utf-8 -*-
"""The remove_song_from_queue tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class RemoveSongFromQueueOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def remove_song_from_queue(
    position: int,
    access_token: str,
) -> ToolResponse:
    """Remove a song from the queue by position.

    Args:
        position (`int`): The position of the song in the queue to remove.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.remove_song_from_queue("
        f"position={fmt(position)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
