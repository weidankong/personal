# -*- coding: utf-8 -*-
"""The create_playlist tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class CreatePlaylistOutput(BaseModel):
    message: str = Field(description="Confirmation message")
    playlist_id: int = Field(description="ID of the created playlist")


def create_playlist(
    title: str,
    is_public: bool = True,
    access_token: str = "",
) -> ToolResponse:
    """Create a new playlist.

    Args:
        title (`str`): The title of the playlist.
        is_public (`bool`): Whether the playlist is public. Defaults to True.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message with playlist ID or error.
    """
    code = (
        f"print(apis.spotify.create_playlist("
        f"title={fmt(title)}, "
        f"is_public={fmt(is_public)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
