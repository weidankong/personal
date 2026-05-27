# -*- coding: utf-8 -*-
"""The show_api_descriptions tool — api_docs app."""

from typing import List, Optional
import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class ApiDescription(BaseModel):
    name: str = Field(description="API name")
    description: str = Field(description="Short description of what the API does")


class ApiDescriptionsOutput(BaseModel):
    apis: List[ApiDescription] = Field(description="List of available APIs under the app")


def show_api_descriptions(app_name: str, access_token: Optional[str] = None) -> ToolResponse:
    """Show descriptions for all APIs available for a given app.

    Args:
        app_name (`str`): Name of the app, e.g. 'spotify', 'supervisor', 'venmo'.
        access_token (`str`, optional): Access token (required for some apps).

    Returns:
        `ToolResponse`:
            The tool response containing a list of API names and descriptions,
            or an error message.
    """
    if access_token is not None:
        code = f"print(apis.api_docs.show_api_descriptions(app_name={fmt(app_name)}, access_token={fmt(access_token)}))"
    else:
        code = f"print(apis.api_docs.show_api_descriptions(app_name={fmt(app_name)}))"
    output = world.world.execute(code)
    output = convert(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )

