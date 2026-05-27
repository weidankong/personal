# -*- coding: utf-8 -*-
"""The create_file tool — file_system app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class CreateFileOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")
    file_path: str = Field(description="Path of the created file")


def create_file(
    file_path: str,
    access_token: str,
    content: str = "",
    overwrite: bool = False,
) -> ToolResponse:
    """Create a new file with the given content.

    Args:
        file_path (`str`): Path of the file. Use ~/ for home directory. Must have an extension.
        access_token (`str`): Access token obtained from file_system app login.
        content (`str`): The content of the file. Defaults to empty string.
        overwrite (`bool`): Whether to overwrite the file if it already exists. Defaults to False.

    Returns:
        `ToolResponse`:
            The tool response containing a confirmation message and file path,
            or an error message on failure.
    """
    code = f"print(apis.file_system.create_file(file_path={fmt(file_path)}, access_token={fmt(access_token)}, content={fmt(content)}, overwrite={fmt(overwrite)}))"
    output = world.world.execute(code)
    output = convert(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata={"confirm_message": output},
    )
