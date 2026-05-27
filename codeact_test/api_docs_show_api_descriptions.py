# -*- coding: utf-8 -*-
"""The show_api_descriptions tool — api_docs app."""

from typing import List, Optional

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock


class ApiDescription(BaseModel):
    name: str = Field(description="API name")
    description: str = Field(description="Short description of what the API does")


class ApiDescriptionsOutput(BaseModel):
    apis: List[ApiDescription] = Field(description="List of available APIs under the app")


def show_api_descriptions(app_name: str, access_token: Optional[str] = None) -> ToolResponse:
    """List all available API endpoints under a specific app.

    Args:
        app_name (`str`): Name of the app, e.g. 'spotify', 'supervisor', 'venmo'.
        access_token (`str`, optional): Access token (required for some apps).

    Returns:
        `ToolResponse`:
            The tool response containing a list of API names and descriptions,
            or an error message.
    """
    # TODO: implement
    raise NotImplementedError
