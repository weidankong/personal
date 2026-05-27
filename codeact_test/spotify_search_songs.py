# -*- coding: utf-8 -*-
"""The search_songs tool — spotify app."""

from typing import List, Optional
import json

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class SearchSongArtist(BaseModel):
    id: int = Field(description="Artist ID")
    name: str = Field(description="Artist name")


class SearchSong(BaseModel):
    song_id: int = Field(description="Unique song ID")
    title: str = Field(description="Song title")
    album_id: Optional[int] = Field(description="Album ID")
    album_title: Optional[str] = Field(description="Album title")
    duration: int = Field(description="Duration in seconds")
    artists: List[SearchSongArtist] = Field(description="List of artists")
    release_date: str = Field(description="ISO format release date")
    genre: str = Field(description="Music genre")
    play_count: float = Field(description="Number of plays")
    rating: float = Field(description="Song rating (0.0–5.0)")
    like_count: int = Field(description="Number of likes")
    review_count: int = Field(description="Number of reviews")
    shareable_link: str = Field(description="Shareable URL for the song")


class SearchSongsOutput(RootModel[List[SearchSong]]):
    """List of songs matching the search query"""

def search_songs(
    query: str = "",
    artist_id: Optional[int] = None,
    album_id: Optional[int] = None,
    genre: Optional[str] = None,
    min_release_date: str = "1500-01-01",
    max_release_date: str = "3000-01-01",
    min_duration: int = 0,
    max_duration: int = 9223372036854775807,
    min_rating: float = 0.0,
    max_rating: float = 5.0,
    min_like_count: int = 0,
    max_like_count: int = 9223372036854775807,
    min_play_count: int = 0,
    max_play_count: int = 9223372036854775807,
    page_index: int = 0,
    page_limit: int = 5,
    sort_by: Optional[str] = None,
) -> ToolResponse:
    """Search for songs with a query.

    Args:
        query (`str`): The search query string. Defaults to "".
        artist_id (`int`, optional): Filter by artist ID.
        album_id (`int`, optional): Filter by album ID.
        genre (`str`, optional): Filter by genre.
        min_release_date (`str`): Minimum release date (YYYY-MM-DD). Defaults to "1500-01-01".
        max_release_date (`str`): Maximum release date (YYYY-MM-DD). Defaults to "3000-01-01".
        min_duration (`int`): Minimum duration in seconds. Defaults to 0.
        max_duration (`int`): Maximum duration in seconds.
        min_rating (`float`): Minimum rating (0.0-5.0). Defaults to 0.0.
        max_rating (`float`): Maximum rating (0.0-5.0). Defaults to 5.0.
        min_like_count (`int`): Minimum like count. Defaults to 0.
        max_like_count (`int`): Maximum like count.
        min_play_count (`int`): Minimum play count. Defaults to 0.
        max_play_count (`int`): Maximum play count.
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.
        sort_by (`str`, optional): Sort attribute prefixed with +/- for ascending/descending.
            Valid: rating, like_count, play_count.

    Returns:
        `ToolResponse`: The tool response containing a list of songs, or an error message.
    """
    code = (
        f"print(apis.spotify.search_songs("
        f"query={fmt(query)}, "
        f"artist_id={fmt(artist_id)}, "
        f"album_id={fmt(album_id)}, "
        f"genre={fmt(genre)}, "
        f"min_release_date={fmt(min_release_date)}, "
        f"max_release_date={fmt(max_release_date)}, "
        f"min_duration={fmt(min_duration)}, "
        f"max_duration={fmt(max_duration)}, "
        f"min_rating={fmt(min_rating)}, "
        f"max_rating={fmt(max_rating)}, "
        f"min_like_count={fmt(min_like_count)}, "
        f"max_like_count={fmt(max_like_count)}, "
        f"min_play_count={fmt(min_play_count)}, "
        f"max_play_count={fmt(max_play_count)}, "
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
