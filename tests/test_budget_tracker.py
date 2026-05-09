from decimal import Decimal

from autogen_cnp_shim import BudgetTracker


def test_reserve_many_sums_allocations() -> None:
    tracker = BudgetTracker(1.00)

    assert tracker.reserve_many({"a": 0.40, "b": Decimal("0.30")})
    assert tracker.allocated_budget == Decimal("0.70")
    assert tracker.remaining_budget == Decimal("0.30")


def test_reset_restores_remaining_budget() -> None:
    tracker = BudgetTracker(1.00)
    tracker.reserve(0.25)

    tracker.reset()

    assert tracker.allocated_budget == Decimal("0.00")
    assert tracker.remaining_budget == Decimal("1.00")
