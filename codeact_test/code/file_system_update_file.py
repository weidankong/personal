# -*- coding: utf-8 -*-
"""The update_file tool — file_system app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class UpdateFileOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")
    file_path: str = Field(description="Path of the updated file")


def update_file(
    file_path: str,
    content: str,
    access_token: str,
) -> ToolResponse:
    """Update a file's content.

    Args:
        file_path (`str`): Path of the file. Use ~/ for home directory. Must have an extension.
        content (`str`): The updated content of the file.
        access_token (`str`): Access token obtained from file_system app login.

    Returns:
        `ToolResponse`:
            The tool response containing a confirmation message and file path,
            or an error message on failure.
    """
    code = f"print(apis.file_system.update_file(file_path={fmt(file_path)}, content={fmt(content)}, access_token={fmt(access_token)}))"
    output = world.world.execute(code)
    output = convert(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata={"confirm_message": output},
    )
