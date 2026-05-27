# -*- coding: utf-8 -*-
"""The search_text_messages tool — phone app."""

from typing import List, Optional
import json

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class MessageContact(BaseModel):
    contact_id: Optional[int] = Field(description="Contact ID (null if not in contacts)")
    name: str = Field(description="Contact name")
    phone_number: str = Field(description="Phone number")


class TextMessage(BaseModel):
    text_message_id: int = Field(description="Unique message ID")
    sender: MessageContact = Field(description="Message sender")
    receiver: MessageContact = Field(description="Message receiver")
    message: str = Field(description="Message content")
    sent_at: str = Field(description="ISO format timestamp")


class TextMessagesOutput(RootModel[List[TextMessage]]):
    """List of text messages"""

def search_text_messages(
    access_token: str,
    query: str = "",
    phone_number: Optional[str] = None,
    only_latest_per_contact: bool = False,
    page_index: int = 0,
    page_limit: int = 5,
    sort_by: Optional[str] = None,
) -> ToolResponse:
    """Show or search your text messages.

    Args:
        access_token (`str`): Access token obtained from phone app login.
        query (`str`): The search query string. Defaults to "".
        phone_number (`str`, optional): The phone number of the contact to show messages with.
        only_latest_per_contact (`bool`): If True, only the latest message from each contact.
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.
        sort_by (`str`, optional): Sort attribute prefixed with +/- for ascending/descending.
            Valid: created_at.

    Returns:
        `ToolResponse`: The tool response containing a list of text messages, or an error message.
    """
    code = (
        f"print(apis.phone.search_text_messages("
        f"access_token={fmt(access_token)}, "
        f"query={fmt(query)}, "
        f"phone_number={fmt(phone_number)}, "
        f"only_latest_per_contact={fmt(only_latest_per_contact)}, "
        f"page_index={fmt(page_index)}, "
        f"page_limit={fmt(page_limit)}, "
        f"sort_by={fmt(sort_by)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
