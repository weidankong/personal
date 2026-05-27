# -*- coding: utf-8 -*-
"""The create_directory tool — file_system app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class CreateDirectoryOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def create_directory(
    directory_path: str,
    access_token: str,
    recursive: bool = False,
    allow_if_exists: bool = True,
) -> ToolResponse:
    """Create a directory if it does not exist, optionally recursively.

    Args:
        directory_path (`str`): Path of the directory. Use ~/ for home directory.
        access_token (`str`): Access token obtained from file_system app login.
        recursive (`bool`): If True, create all parent directories recursively if they don't exist. Defaults to False.
        allow_if_exists (`bool`): If True, do not raise an error if the directory already exists. Defaults to True.

    Returns:
        `ToolResponse`:
            The tool response containing a confirmation message,
            or an error message on failure.
    """
    code = f"print(apis.file_system.create_directory(directory_path={fmt(directory_path)}, access_token={fmt(access_token)}, recursive={fmt(recursive)}, allow_if_exists={fmt(allow_if_exists)}))"
    output = world.world.execute(code)
    output = convert(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata={"confirm_message": output},
    )
