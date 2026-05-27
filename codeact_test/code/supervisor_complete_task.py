# -*- coding: utf-8 -*-
"""The complete_task tool — supervisor app."""

from typing import Union
import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class CompleteTaskOutput(BaseModel):
    complete_message: str = Field(description="Confirmation message")

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
    code = f"apis.supervisor.complete_task(answer={fmt(answer)}, status={fmt(status)})"
    output = world.world.execute(code)
    output = json.dumps({"complete_message": output})
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=json.loads(output),
    )
