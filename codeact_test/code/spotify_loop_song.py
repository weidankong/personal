# -*- coding: utf-8 -*-
"""The loop_song tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class LoopSongOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def loop_song(
    loop: bool,
    access_token: str,
) -> ToolResponse:
    """Toggle loop mode for the current song.

    Args:
        loop (`bool`): True to enable loop, False to disable.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.loop_song("
        f"loop={fmt(loop)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
