# -*- coding: utf-8 -*-
"""The pause_music tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class PauseMusicOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def pause_music(
    access_token: str,
) -> ToolResponse:
    """Pause the currently playing music.

    Args:
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.pause_music("
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
