# -*- coding: utf-8 -*-
"""The show_profile tool — supervisor app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class SupervisorProfileOutput(BaseModel):
    first_name: str = Field(description="Supervisor's first name")
    last_name: str = Field(description="Supervisor's last name")
    email: str = Field(description="Supervisor's email address")
    phone_number: str = Field(description="Supervisor's phone number")
    birthday: str = Field(description="Supervisor's birthday")
    sex: str = Field(description="Supervisor's sex")

def show_profile() -> ToolResponse:
    """Show your supervisor's profile information.

    Returns:
        `ToolResponse`: The tool response containing supervisor profile, or an error message.
    """
    code = "print(apis.supervisor.show_profile())"
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
