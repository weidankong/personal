# -*- coding: utf-8 -*-
"""The show_payment_card tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class PaymentCardOutput(BaseModel):
    payment_card_id: int = Field(description="Unique payment card ID")
    card_name: str = Field(description="Card name")
    owner_name: str = Field(description="Card owner name")
    card_number: int = Field(description="Card number (last 4 digits)")
    expiry_year: int = Field(description="Expiry year")
    expiry_month: int = Field(description="Expiry month")


def show_payment_card(
    payment_card_id: int,
    access_token: str,
) -> ToolResponse:
    """Show details of a specific payment card.

    Args:
        payment_card_id (`int`): The ID of the payment card.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Payment card details or error.
    """
    code = (
        f"print(apis.spotify.show_payment_card("
        f"payment_card_id={fmt(payment_card_id)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
