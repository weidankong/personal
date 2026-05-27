# -*- coding: utf-8 -*-
"""The unlike_playlist tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class UnlikePlaylistOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def unlike_playlist(
    playlist_id: int,
    access_token: str,
) -> ToolResponse:
    """Remove a like from a playlist.

    Args:
        playlist_id (`int`): The ID of the playlist to unlike.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.unlike_playlist("
        f"playlist_id={fmt(playlist_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
