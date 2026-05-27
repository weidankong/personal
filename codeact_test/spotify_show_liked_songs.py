# -*- coding: utf-8 -*-
"""The show_liked_songs tool — spotify app."""

from typing import List, Optional
import json

from pydantic import BaseModel, Field, RootModel, ValidationError

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world


class LikedSongArtist(BaseModel):
    id: int = Field(description="Artist ID")
    name: str = Field(description="Artist name")


class LikedSong(BaseModel):
    song_id: int = Field(description="Unique song ID")
    title: str = Field(description="Song title")
    album_id: Optional[int] = Field(description="Album ID")
    album_title: Optional[str] = Field(description="Album title")
    duration: int = Field(description="Duration in seconds")
    artists: List[LikedSongArtist] = Field(description="List of artists")
    liked_at: str = Field(description="ISO format timestamp of when the song was liked")


class LikedSongsOutput(RootModel[List[LikedSong]]):
    """List of liked songs"""


def _fmt(v):
    if v is None:
        return "None"
    if isinstance(v, str):
        return repr(v)
    return str(v)


def _validate_output(output: str, model: type[BaseModel]) -> ToolResponse:
    """Parse JSON output and validate against the model. Raises on failure."""
    try:
        data = json.loads(output)
        model.model_validate(data)
        return ToolResponse(
            content=[TextBlock(type="text", text=output)],
            metadata=data,
        )
    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError(f"Output validation failed: {e}\nRaw output: {output}") from e


def show_liked_songs(
    access_token: str,
    page_index: int = 0,
    page_limit: int = 5,
    sort_by: str = "-liked_at",
) -> ToolResponse:
    """Get a list of songs you have liked on Spotify.

    Args:
        access_token (`str`): Access token obtained from spotify app login.
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): The maximum number of results to return per page. Defaults to 5.
        sort_by (`str`): The attribute to sort by, prefixed with +/- for ascending/descending.
            Valid attributes: liked_at, play_count, title. Defaults to "-liked_at".

    Returns:
        `ToolResponse`:
            The tool response containing a list of liked songs,
            or an error message.
    """
    code = (
        f"print(apis.spotify.show_liked_songs("
        f"access_token={_fmt(access_token)}, "
        f"page_index={_fmt(page_index)}, "
        f"page_limit={_fmt(page_limit)}, "
        f"sort_by={_fmt(sort_by)}))"
    )
    output = world.world.execute(code)
    return _validate_output(output, LikedSongsOutput)
