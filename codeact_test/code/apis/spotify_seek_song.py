# -*- coding: utf-8 -*-
"""The seek_song tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class SeekSongOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def seek_song(
    seek_seconds: int,
    access_token: str,
) -> ToolResponse:
    """Seek to a specific position in the currently playing song.

    Args:
        seek_seconds (`int`): The position to seek to in seconds.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.seek_song("
        f"seek_seconds={fmt(seek_seconds)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
