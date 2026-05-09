"""Budget tracking for AutoGen-side CNP allocations."""

from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Mapping


_CURRENCY_QUANTUM = Decimal("0.01")


def _to_currency(value: float | Decimal) -> Decimal:
    return Decimal(str(value)).quantize(_CURRENCY_QUANTUM, rounding=ROUND_HALF_UP)


class BudgetTracker:
    """Track and enforce a parent budget for awarded contracts."""

    def __init__(self, parent_budget: float | Decimal) -> None:
        self._parent_budget = _to_currency(parent_budget)
        self._allocated_budget = Decimal("0.00")

    @property
    def parent_budget(self) -> Decimal:
        return self._parent_budget

    @property
    def allocated_budget(self) -> Decimal:
        return self._allocated_budget

    @property
    def remaining_budget(self) -> Decimal:
        return self._parent_budget - self._allocated_budget

    def reserve(self, amount: float | Decimal) -> bool:
        normalized = _to_currency(amount)
        if normalized <= Decimal("0.00"):
            return True
        if normalized > self.remaining_budget:
            return False
        self._allocated_budget += normalized
        return True

    def reserve_many(self, allocations: Mapping[str, float | Decimal]) -> bool:
        requested = sum((_to_currency(amount) for amount in allocations.values()), Decimal("0.00"))
        return self.reserve(requested)

    def reset(self) -> None:
        self._allocated_budget = Decimal("0.00")
