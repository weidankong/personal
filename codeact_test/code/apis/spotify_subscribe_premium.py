# -*- coding: utf-8 -*-
"""The subscribe_premium tool — spotify app."""

import json
from typing import Literal

from pydantic import BaseModel, Field

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class SubscribePremiumOutput(BaseModel):
    message: str = Field(description="Confirmation message")
    premium_subscription_id: int = Field(description="ID of the premium subscription")


def subscribe_premium(
    payment_card_id: int,
    duration: str,
    access_token: str,
) -> ToolResponse:
    """Subscribe to a premium plan.

    Args:
        payment_card_id (`int`): The ID of the payment card to use.
        duration (`str`): Subscription duration - "monthly" or "yearly".
        access_token (`str`): Access token obtained from spotify app login.

    Returns:
        `ToolResponse`: Confirmation message with subscription ID or error.
    """
    code = (
        f"print(apis.spotify.subscribe_premium("
        f"payment_card_id={fmt(payment_card_id)}, "
        f"duration={fmt(duration)}, "
        f"access_token={fmt(access_token)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
