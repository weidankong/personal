# -*- coding: utf-8 -*-
"""The show_volume tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class VolumeOutput(BaseModel):
    volume: int = Field(description="Current volume level (0-100)")


def show_volume(
    access_token: str,
) -> ToolResponse:
    """Show the current volume level.

    Args:
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Volume level or error.
    """
    code = (
        f"print(apis.spotify.show_volume("
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
