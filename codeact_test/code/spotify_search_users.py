# -*- coding: utf-8 -*-
"""The search_users tool — spotify app."""

import json
from typing import List

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class ShortenedUser(BaseModel):
    first_name: str = Field(description="First name")
    last_name: str = Field(description="Last name")
    email: str = Field(description="Email address")


class SearchUsersOutput(RootModel[List[ShortenedUser]]):
    """List of users matching the search query"""


def search_users(
    query: str,
    page_index: int = 0,
    page_limit: int = 5,
) -> ToolResponse:
    """Search for Spotify users by name or email.

    Args:
        query (`str`): The search query string.
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page. Defaults to 5.

    Returns:
        `ToolResponse`: List of users or error.
    """
    code = (
        f"print(apis.spotify.search_users("
        f"query={fmt(query)}, "
        f"page_index={fmt(page_index)}, "
        f"page_limit={fmt(page_limit)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
