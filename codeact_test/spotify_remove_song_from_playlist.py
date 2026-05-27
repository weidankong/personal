# -*- coding: utf-8 -*-
"""The remove_song_from_playlist tool — spotify app."""

import json

from pydantic import BaseModel, Field, ValidationError

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world


class MessageOutput(BaseModel):
    message: str = Field(description="Confirmation message")


def _fmt(v):
    if v is None:
        return "None"
    if isinstance(v, str):
        return repr(v)
    return str(v)


def _validate_output(output: str, model: type[BaseModel]) -> ToolResponse:
    try:
        data = json.loads(output)
        model.model_validate(data)
        return ToolResponse(
            content=[TextBlock(type="text", text=output)],
            metadata=data,
        )
    except (json.JSONDecodeError, ValidationError) as e:
        raise RuntimeError(f"Output validation failed: {e}\nRaw output: {output}") from e


def remove_song_from_playlist(
    playlist_id: int,
    song_id: int,
    access_token: str,
) -> ToolResponse:
    """Remove a song from a playlist.

    Args:
        playlist_id (`int`): The playlist ID to remove the song from.
        song_id (`int`): The song ID to remove.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.remove_song_from_playlist("
        f"playlist_id={_fmt(playlist_id)}, "
        f"song_id={_fmt(song_id)}, "
        f"access_token={_fmt(access_token)}))"
    )
    output = world.world.execute(code)
    return _validate_output(output, MessageOutput)
