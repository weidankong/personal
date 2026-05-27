# -*- coding: utf-8 -*-
"""The complete_task tool — supervisor app."""

from typing import Union
import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world


class CompleteTaskOutput(BaseModel):
    message: str = Field(description="Confirmation message")


def _fmt(v):
    if v is None:
        return "None"
    if isinstance(v, str):
        return repr(v)
    return str(v)


def complete_task(
    answer: Union[str, int, float, None] = None,
    status: str = None,
) -> ToolResponse:
    """Mark the currently active task as complete with the given answer.

    Args:
        answer (`str | number | None`, optional):
            The answer to the task. Should be a single entity or number,
            not a full sentence. Skip or pass None if no answer is needed.
        status (`str`, optional):
            Use "fail" to explicitly mark the task as unsolvable.

    Returns:
        `ToolResponse`:
            The tool response with a confirmation message.
    """
    code = f"apis.supervisor.complete_task(answer={_fmt(answer)}, status={_fmt(status)})"
    output = world.world.execute(code)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
