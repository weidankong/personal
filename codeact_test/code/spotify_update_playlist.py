# -*- coding: utf-8 -*-
"""The update_playlist tool — spotify app."""

import json
from typing import Optional

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class UpdatePlaylistOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def update_playlist(
    playlist_id: int,
    access_token: str,
    title: Optional[str] = None,
    is_public: Optional[bool] = None,
) -> ToolResponse:
    """Update a playlist's title or visibility.

    Args:
        playlist_id (`int`): The ID of the playlist.
        access_token (`str`): Access token obtained from spotify app login.
        title (`str`, optional): New title for the playlist.
        is_public (`bool`, optional): Whether the playlist is public.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.update_playlist("
        f"playlist_id={fmt(playlist_id)}, "
        f"access_token={fmt(access_token)}, "
        f"title={fmt(title)}, "
        f"is_public={fmt(is_public)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
