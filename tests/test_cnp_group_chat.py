import asyncio

import pytest
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams._group_chat._base_group_chat_manager import BaseGroupChatManager

from autogen_cnp_shim import BidderProxy, CNPGroupChatManager


def _make_manager() -> CNPGroupChatManager:
    return CNPGroupChatManager(
        bidders=[
            BidderProxy(name="research", specialties=["research"], keywords=["research"]),
            BidderProxy(name="code", specialties=["python"], keywords=["python", "implement"]),
            BidderProxy(name="review", specialties=["qa"], keywords=["review"]),
        ],
        parent_budget=1.0,
    )


def test_cnp_group_chat_manager_is_base_group_chat_manager() -> None:
    manager = _make_manager()

    assert isinstance(manager, BaseGroupChatManager)


def test_select_speaker_returns_topic_type_for_winner() -> None:
    manager = _make_manager()
    thread = [TextMessage(source="user", content="implement this in python")]

    selected = asyncio.run(manager.select_speaker(thread))

    assert selected == "participant.code"


def test_select_speaker_raises_when_no_winner() -> None:
    manager = CNPGroupChatManager(
        bidders=[BidderProxy(name="silent", specialties=["none"], keywords=[])],
        parent_budget=1.0,
    )
    thread = [TextMessage(source="user", content="unmatched tokens only")]

    with pytest.raises(RuntimeError, match="No winning agent"):
        asyncio.run(manager.select_speaker(thread))


def test_validate_group_state_is_noop_and_reset_clears_latest_award() -> None:
    manager = _make_manager()
    manager.route_contract("implement this in python", {"a": 0.25})

    asyncio.run(manager.validate_group_state(None))
    asyncio.run(manager.reset())

    assert manager.latest_award is None
