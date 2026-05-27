# -*- coding: utf-8 -*-
"""The get_current_date_and_time tool — phone app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class DateTimeOutput(BaseModel):
    date: str = Field(description="Current date")
    time: str = Field(description="Current time")


def get_current_date_and_time() -> ToolResponse:
    """Show current date and time.

    Returns:
        `ToolResponse`: Current date and time, or an error message.
    """
    code = "print(apis.phone.get_current_date_and_time())"
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
