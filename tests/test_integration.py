from autogen_cnp_shim import BidderProxy, CNPGroupChatManager, ContractState


def _make_manager() -> CNPGroupChatManager:
    return CNPGroupChatManager(
        bidders=[
            BidderProxy(name="research", specialties=["research"], keywords=["research", "paper"]),
            BidderProxy(name="coding", specialties=["coding"], keywords=["python", "implement"]),
            BidderProxy(name="review", specialties=["review"], keywords=["review", "validate"]),
        ],
        parent_budget=1.0,
    )


def test_three_agent_budget_capped_contract_fulfilled() -> None:
    manager = _make_manager()
    award = manager.route_contract(
        "research and implement a Python prototype",
        subtask_budgets={"research": 0.40, "implementation": 0.30, "validation": 0.30},
    )

    assert award.state is ContractState.FULFILLED
    assert award.winning_agent in {"research", "coding", "review"}


def test_over_budget_contract_is_violated() -> None:
    manager = _make_manager()
    award = manager.route_contract(
        "research and implement a Python prototype",
        subtask_budgets={"research": 0.50, "implementation": 0.40, "validation": 0.30},
    )

    assert award.state is ContractState.VIOLATED
