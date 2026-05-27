# -*- coding: utf-8 -*-
"""The update_payment_card tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class UpdatePaymentCardOutput(BaseModel):
    confirm_message: str = Field(description="Confirmation message")


def update_payment_card(
    payment_card_id: int,
    card_name: str,
    access_token: str,
) -> ToolResponse:
    """Update a payment card's name.

    Args:
        payment_card_id (`int`): The ID of the payment card.
        card_name (`str`): New name for the card.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message or error.
    """
    code = (
        f"print(apis.spotify.update_payment_card("
        f"payment_card_id={fmt(payment_card_id)}, "
        f"card_name={fmt(card_name)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output) if output.startswith("{") else {"message": output}
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
