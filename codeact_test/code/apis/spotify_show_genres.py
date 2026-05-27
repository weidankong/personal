# -*- coding: utf-8 -*-
"""The show_genres tool — spotify app."""

import json

from pydantic import BaseModel, Field, RootModel
from typing import List

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class GenresOutput(RootModel[List[str]]):
    """List of available genres"""


def show_genres() -> ToolResponse:
    """Get a list of all available music genres.

    Returns:
        `ToolResponse`: List of genre names or error.
    """
    code = "print(apis.spotify.show_genres())"
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
