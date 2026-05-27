# -*- coding: utf-8 -*-
"""The signup tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class SignupOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def signup(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
) -> ToolResponse:
    """Sign up for a new Spotify account.

    Args:
        first_name (`str`): First name of the user.
        last_name (`str`): Last name of the user.
        email (`str`): Email address for the account.
        password (`str`): Password for the account.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.signup("
        f"first_name={fmt(first_name)}, "
        f"last_name={fmt(last_name)}, "
        f"email={fmt(email)}, "
        f"password={fmt(password)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
