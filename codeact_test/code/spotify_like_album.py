# -*- coding: utf-8 -*-
"""The like_album tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class LikeAlbumOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def like_album(
    album_id: int,
    access_token: str,
) -> ToolResponse:
    """Like an album.

    Args:
        album_id (`int`): The ID of the album to like.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.like_album("
        f"album_id={fmt(album_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
