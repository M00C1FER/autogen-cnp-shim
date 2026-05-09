from autogen_cnp_shim import BidderProxy, CNPGroupChatManager
from autogen_agentchat.teams._group_chat._base_group_chat_manager import BaseGroupChatManager


def test_cnp_group_chat_manager_is_base_group_chat_manager() -> None:
    manager = CNPGroupChatManager(
        bidders=[
            BidderProxy(name="research", specialties=["research"], keywords=["paper"]),
            BidderProxy(name="code", specialties=["python"], keywords=["code"]),
            BidderProxy(name="review", specialties=["qa"], keywords=["review"]),
        ],
        parent_budget=1.0,
    )

    assert isinstance(manager, BaseGroupChatManager)
