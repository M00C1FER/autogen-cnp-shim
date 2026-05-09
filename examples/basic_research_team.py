"""Minimal AutoGen 0.4+ CNP shim example."""

from autogen_cnp_shim import BidderProxy, CNPGroupChatManager


def main() -> None:
    manager = CNPGroupChatManager(
        bidders=[
            BidderProxy(name="research", specialties=["research"], keywords=["research", "paper"]),
            BidderProxy(name="coding", specialties=["coding"], keywords=["python", "implement"]),
            BidderProxy(name="review", specialties=["review"], keywords=["review", "validate"]),
        ],
        parent_budget=1.00,
    )

    award = manager.route_contract(
        task="research and implement a Python prototype",
        subtask_budgets={"research": 0.40, "implementation": 0.30, "validation": 0.30},
    )
    print(award)


if __name__ == "__main__":
    main()
