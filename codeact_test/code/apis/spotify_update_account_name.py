# -*- coding: utf-8 -*-
"""The update_account_name tool — spotify app."""

import json
from typing import Optional

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class UpdateAccountNameOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def update_account_name(
    access_token: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> ToolResponse:
    """Update the account name of the logged-in Spotify user.

    Args:
        access_token (`str`): Access token obtained from spotify app login.
        first_name (`str`, optional): New first name.
        last_name (`str`, optional): New last name.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.update_account_name("
        f"access_token={fmt(access_token)}, "
        f"first_name={fmt(first_name)}, "
        f"last_name={fmt(last_name)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
