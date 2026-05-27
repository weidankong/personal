# -*- coding: utf-8 -*-
"""The show_account_passwords tool — supervisor app."""

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock


class PasswordEntry(BaseModel):
    account_name: str = Field(description="The name of the app account")
    password: str = Field(description="The password for this account")


def show_account_passwords() -> ToolResponse:
    """Show all app account passwords stored in the supervisor app.

    Returns:
        `ToolResponse`:
            The tool response containing a list of account/password pairs,
            or an error message.
    """
    # TODO: implement
    raise NotImplementedError
