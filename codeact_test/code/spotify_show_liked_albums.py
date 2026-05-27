# -*- coding: utf-8 -*-
"""The show_liked_albums tool — spotify app."""

import json
from typing import List, Optional

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class LikedAlbum(BaseModel):
    album_id: int = Field(description="Unique album ID")
    title: str = Field(description="Album title")
    genre: str = Field(description="Music genre")
    artist_id: int = Field(description="Artist ID")
    artist_name: str = Field(description="Artist name")
    liked_at: str = Field(description="ISO format timestamp")


class LikedAlbumsOutput(RootModel[List[LikedAlbum]]):
    """List of liked albums"""


def show_liked_albums(
    access_token: str,
    page_index: int = 0,
    page_limit: int = 5,
    sort_by: str = "-liked_at",
) -> ToolResponse:
    """Get a list of albums you have liked.

    Args:
        access_token (`str`): Access token obtained from spotify app login.
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.
        sort_by (`str`): Sort attribute prefixed with +/- for ascending/descending.
            Valid: liked_at, title. Defaults to "-liked_at".

    Returns:
        `ToolResponse`: List of liked albums or error.
    """
    code = (
        f"print(apis.spotify.show_liked_albums("
        f"access_token={fmt(access_token)}, "
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
