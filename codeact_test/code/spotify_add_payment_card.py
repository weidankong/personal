# -*- coding: utf-8 -*-
"""The add_payment_card tool — spotify app."""

import json

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class AddPaymentCardOutput(BaseModel):
    message: str = Field(description="Confirmation message")
    payment_card_id: int = Field(description="ID of the added payment card")


def add_payment_card(
    card_name: str,
    owner_name: str,
    card_number: int,
    expiry_year: int,
    expiry_month: int,
    cvv_number: int,
    access_token: str,
) -> ToolResponse:
    """Add a payment card to your account.

    Args:
        card_name (`str`): Name for the card.
        owner_name (`str`): Name of the card owner.
        card_number (`int`): Card number.
        expiry_year (`int`): Expiry year.
        expiry_month (`int`): Expiry month.
        cvv_number (`int`): CVV number.
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message with card ID or error.
    """
    code = (
        f"print(apis.spotify.add_payment_card("
        f"card_name={fmt(card_name)}, "
        f"owner_name={fmt(owner_name)}, "
        f"card_number={fmt(card_number)}, "
        f"expiry_year={fmt(expiry_year)}, "
        f"expiry_month={fmt(expiry_month)}, "
        f"cvv_number={fmt(cvv_number)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
