# -*- coding: utf-8 -*-
"""The show_payment_cards tool — spotify app."""

import json
from typing import List

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class PaymentCard(BaseModel):
    payment_card_id: int = Field(description="Unique payment card ID")
    card_name: str = Field(description="Card name")
    owner_name: str = Field(description="Card owner name")
    card_number: int = Field(description="Card number (last 4 digits)")
    expiry_year: int = Field(description="Expiry year")
    expiry_month: int = Field(description="Expiry month")


class PaymentCardsOutput(RootModel[List[PaymentCard]]):
    """List of payment cards"""


def show_payment_cards(
    access_token: str,
) -> ToolResponse:
    """Get a list of payment cards on file.

    Args:
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: List of payment cards or error.
    """
    code = (
        f"print(apis.spotify.show_payment_cards("
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
