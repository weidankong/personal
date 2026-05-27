# -*- coding: utf-8 -*-
"""The delete_payment_card tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class DeletePaymentCardOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def delete_payment_card(
    payment_card_id: int,
    access_token: str,
) -> ToolResponse:
    """Delete a payment card.

    Args:
        payment_card_id (`int`): The ID of the payment card to delete.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.delete_payment_card("
        f"payment_card_id={fmt(payment_card_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
