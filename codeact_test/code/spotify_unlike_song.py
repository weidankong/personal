# -*- coding: utf-8 -*-
"""The unlike_song tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class UnlikeSongOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def unlike_song(
    song_id: int,
    access_token: str,
) -> ToolResponse:
    """Remove a like from a song.

    Args:
        song_id (`int`): The ID of the song to unlike.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.unlike_song("
        f"song_id={fmt(song_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
