# -*- coding: utf-8 -*-
"""The show_app_descriptions tool — api_docs app."""

from typing import List

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock


class AppDescription(BaseModel):
    name: str = Field(description="App name")
    description: str = Field(description="Short description of what the app does")


class AppDescriptionsOutput(BaseModel):
    apps: List[AppDescription] = Field(description="List of available apps")


def show_app_descriptions() -> ToolResponse:
    """Show descriptions of all available apps.

    Returns:
        `ToolResponse`:
            The tool response containing a list of app names and descriptions,
            or an error message.
    """
    # TODO: implement
    raise NotImplementedError
