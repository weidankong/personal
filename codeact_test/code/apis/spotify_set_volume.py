# -*- coding: utf-8 -*-
"""The set_volume tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class SetVolumeOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def set_volume(
    volume: int,
    access_token: str,
) -> ToolResponse:
    """Set the volume level.

    Args:
        volume (`int`): Volume level (0-100).
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.set_volume("
        f"volume={fmt(volume)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
