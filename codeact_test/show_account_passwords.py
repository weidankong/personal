# -*- coding: utf-8 -*-
"""The show_account_passwords tool — supervisor app."""

from typing import List
import json

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world


class PasswordEntry(BaseModel):
    account_name: str = Field(description="The app name of the account")
    password: str = Field(description="The password for this account")


class AccountPasswordsOutput(RootModel[List[PasswordEntry]]):
    """List of account/password pairs"""


def show_account_passwords() -> ToolResponse:
    """Show all app account passwords stored in the APIs.

    Returns:
        `ToolResponse`:
            The tool response containing a list of account/password pairs,
            or an error message.
    """
    code = "print(apis.supervisor.show_account_passwords())"
    output = world.world.execute(code)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output)
    )
