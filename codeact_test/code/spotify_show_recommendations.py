# -*- coding: utf-8 -*-
"""The show_recommendations tool — spotify app."""

from typing import List, Optional
import json

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class RecommendationArtist(BaseModel):
    id: int = Field(description="Artist ID")
    name: str = Field(description="Artist name")


class Recommendation(BaseModel):
    song_id: int = Field(description="Unique song ID")
    title: str = Field(description="Song title")
    album_id: Optional[int] = Field(description="Album ID")
    album_title: Optional[str] = Field(description="Album title")
    duration: int = Field(description="Duration in seconds")
    artists: List[RecommendationArtist] = Field(description="List of artists")


class RecommendationsOutput(RootModel[List[Recommendation]]):
    """List of recommended songs"""


def show_recommendations(
    access_token: str,
    page_index: int = 0,
    page_limit: int = 5,
) -> ToolResponse:
    """Get personalized song recommendations for the user.

    Args:
        access_token (`str`): Access token obtained from spotify app login.
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): The maximum number of results to return per page (1-20). Defaults to 5.

    Returns:
        `ToolResponse`: The tool response containing a list of recommended songs, or an error message.
    """
    code = (
        f"print(apis.spotify.show_recommendations("
        f"access_token={fmt(access_token)}, "
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
