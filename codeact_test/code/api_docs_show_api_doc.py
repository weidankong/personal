# -*- coding: utf-8 -*-
"""The show_api_doc tool — api_docs app."""

from typing import List, Optional
import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class ApiParameter(BaseModel):
    name: str = Field(description="Parameter name")
    type: str = Field(description="Parameter type, e.g. 'string', 'integer'")
    required: bool = Field(description="Whether this parameter is required")
    description: str = Field(description="Parameter description")
    default: Optional[str] = Field(description="Default value, or null if none")
    constraints: List[str] = Field(description="Any constraints on the parameter")


class ResponseSchema(BaseModel):
    schema: dict = Field(description="JSON response schema for success or failure")


class ApiDocOutput(BaseModel):
    app_name: str = Field(description="App name")
    api_name: str = Field(description="API name")
    path: str = Field(description="HTTP path, e.g. '/spotify/library/playlists'")
    method: str = Field(description="HTTP method, e.g. 'GET', 'POST'")
    description: str = Field(description="Full API description")
    parameters: List[ApiParameter] = Field(description="List of input parameters")
    response_schemas: dict = Field(description="Success and failure response schemas")

def show_api_doc(app_name: str, api_name: str, access_token: Optional[str] = None) -> ToolResponse:
    """Show detailed API doc.

    Args:
        app_name (`str`): Name of the app.
        api_name (`str`): Name of the API.
        access_token (`str`, optional): Access token (required for some apps).

    Returns:
        `ToolResponse`:
            The tool response containing the full API spec including
            path, method, parameters, and response schemas,
            or an error message.
    """
    if access_token is not None:
        code = f"print(apis.api_docs.show_api_doc(app_name={fmt(app_name)}, api_name={fmt(api_name)}, access_token={fmt(access_token)}))"
    else:
        code = f"print(apis.api_docs.show_api_doc(app_name={fmt(app_name)}, api_name={fmt(api_name)}))"
    output = world.world.execute(code)
    output = convert(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
