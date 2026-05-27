# -*- coding: utf-8 -*-
"""The shuffle_song_queue tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class ShuffleSongQueueOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def shuffle_song_queue(
    access_token: str,
) -> ToolResponse:
    """Shuffle the song queue.

    Args:
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.shuffle_song_queue("
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
