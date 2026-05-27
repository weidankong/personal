# -*- coding: utf-8 -*-
"""The show_premium_plans tool — spotify app."""

import json

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import convert


def show_premium_plans() -> ToolResponse:
    """Show available premium subscription plans.

    Returns:
        `ToolResponse`: Premium plan details or error.
    """
    code = "print(apis.spotify.show_premium_plans())"
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
