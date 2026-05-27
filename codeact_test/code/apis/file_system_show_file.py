# -*- coding: utf-8 -*-
"""The show_file tool — file_system app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class ShowFileOutput(BaseModel):
    file_id: int = Field(description="Unique file ID")
    path: str = Field(description="File path")
    content: str = Field(description="File content")
    created_at: str = Field(description="ISO format creation timestamp")
    updated_at: str = Field(description="ISO format update timestamp")


def show_file(file_path: str, access_token: str) -> ToolResponse:
    """Show a file's content and other details, if it exists.

    Args:
        file_path (`str`): Path of the file. Use ~/ for home directory. Must have an extension.
        access_token (`str`): Access token obtained from file_system app login.

    Returns:
        `ToolResponse`:
            The tool response containing file details,
            or an error message on failure.
    """
    code = f"print(apis.file_system.show_file(file_path={fmt(file_path)}, access_token={fmt(access_token)}))"
    output = world.world.execute(code)
    output = convert(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
