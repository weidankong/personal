# -*- coding: utf-8 -*-
"""The move_song_in_queue tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class MoveSongInQueueOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def move_song_in_queue(
    current_position: int,
    new_position: int,
    access_token: str,
) -> ToolResponse:
    """Move a song to a different position in the queue.

    Args:
        current_position (`int`): Current position of the song in the queue.
        new_position (`int`): New position for the song.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.move_song_in_queue("
        f"current_position={fmt(current_position)}, "
        f"new_position={fmt(new_position)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
