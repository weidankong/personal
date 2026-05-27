# -*- coding: utf-8 -*-
"""The add_song_to_library tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class AddSongToLibraryOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def add_song_to_library(
    song_id: int,
    access_token: str,
) -> ToolResponse:
    """Add a song to your library.

    Args:
        song_id (`int`): The ID of the song to add.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.add_song_to_library("
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
