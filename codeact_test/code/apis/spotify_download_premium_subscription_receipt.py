# -*- coding: utf-8 -*-
"""The download_premium_subscription_receipt tool — spotify app."""

import json
from typing import Optional

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class DownloadReceiptOutput(BaseModel):
    message: str = Field(description="Confirmation message")
    file_path: str = Field(description="Path to the downloaded receipt")


def download_premium_subscription_receipt(
    premium_subscription_id: int,
    file_system_access_token: str,
    access_token: str,
    download_to_file_path: Optional[str] = None,
    overwrite: bool = False,
) -> ToolResponse:
    """Download a receipt for a premium subscription.

    Args:
        premium_subscription_id (`int`): The ID of the premium subscription.
        file_system_access_token (`str`): Access token for the file system app.
        access_token (`str`): Access token obtained from spotify app login.
        download_to_file_path (`str`, optional): File path to download the receipt to.
        overwrite (`bool`): Whether to overwrite existing file. Defaults to False.

    Returns:
        `ToolResponse`: Confirmation message with file path or error.
    """
    code = (
        f"print(apis.spotify.download_premium_subscription_receipt("
        f"premium_subscription_id={fmt(premium_subscription_id)}, "
        f"file_system_access_token={fmt(file_system_access_token)}, "
        f"download_to_file_path={fmt(download_to_file_path)}, "
        f"overwrite={fmt(overwrite)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
