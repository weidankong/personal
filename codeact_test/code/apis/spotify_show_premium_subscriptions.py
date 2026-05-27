# -*- coding: utf-8 -*-
"""The show_premium_subscriptions tool — spotify app."""

import json
from typing import List

from pydantic import BaseModel, Field, RootModel

from agentscope.tool import ToolResponse
from agentscope.message import TextBlock

import world

from util import fmt, convert


class PremiumSubscription(BaseModel):
    premium_subscription_id: int = Field(description="Unique subscription ID")
    duration: str = Field(description="Subscription duration")
    payment_card_id: int = Field(description="Payment card ID used")
    start_date: str = Field(description="Subscription start date")
    end_date: str = Field(description="Subscription end date")
    is_active: bool = Field(description="Whether the subscription is active")


class PremiumSubscriptionsOutput(RootModel[List[PremiumSubscription]]):
    """List of premium subscriptions"""


def show_premium_subscriptions(
    access_token: str,
    page_index: int = 0,
    page_limit: int = 5,
) -> ToolResponse:
    """Show premium subscription history.

    Args:
        access_token (`str`): Access token obtained from spotify app login.
        page_index (`int`): The index of the page to return. Defaults to 0.
        page_limit (`int`): Max results per page (1-20). Defaults to 5.

    Returns:
        `ToolResponse`: List of premium subscriptions or error.
    """
    code = (
        f"print(apis.spotify.show_premium_subscriptions("
        f"access_token={fmt(access_token)}, "
        f"page_index={fmt(page_index)}, "
        f"page_limit={fmt(page_limit)}))"
    )
    output = world.world.execute(code)
    output = convert(output)
    data = json.loads(output)
    return ToolResponse(
        content=[TextBlock(type="text", text=output)],
        metadata=data,
    )
