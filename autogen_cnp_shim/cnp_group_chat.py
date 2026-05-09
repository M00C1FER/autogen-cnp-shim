"""AutoGen CNP-enabled GroupChat manager scaffold."""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Mapping, Sequence

from autogen_agentchat.messages import BaseAgentEvent, BaseChatMessage, MessageFactory
from autogen_agentchat.teams._group_chat._base_group_chat_manager import BaseGroupChatManager
from contract_net_router import ContractNetRouter

from .bidder_proxy import BidderProxy
from .budget_tracker import BudgetTracker


class ContractState(str, Enum):
    """Lifecycle states surfaced by the shim."""

    AWARDED = "awarded"
    FULFILLED = "fulfilled"
    VIOLATED = "violated"


@dataclass(slots=True)
class ContractAward:
    """Outcome of a CNP routing + budget decision."""

    task: str
    winning_agent: str | None
    state: ContractState
    requested_budget: Decimal
    remaining_budget: Decimal
    bids: dict[str, float]


class CNPGroupChatManager(BaseGroupChatManager):
    """Scaffold manager that routes speaker selection via contract-net-router."""

    def __init__(
        self,
        bidders: Sequence[BidderProxy],
        parent_budget: float = 1.0,
        name: str = "cnp_group_chat_manager",
    ) -> None:
        self._bidders = list(bidders)
        if not self._bidders:
            raise ValueError("At least one bidder is required.")

        participant_names = [bidder.name for bidder in self._bidders]
        participant_topic_types = [f"participant.{bidder.name}" for bidder in self._bidders]
        participant_descriptions = [bidder.description for bidder in self._bidders]

        super().__init__(
            name=name,
            group_topic_type=f"{name}.group",
            output_topic_type=f"{name}.output",
            participant_topic_types=participant_topic_types,
            participant_names=participant_names,
            participant_descriptions=participant_descriptions,
            output_message_queue=asyncio.Queue(),
            termination_condition=None,
            max_turns=None,
            message_factory=MessageFactory(),
            emit_team_events=False,
        )

        self._budget_tracker = BudgetTracker(parent_budget)
        self._initial_parent_budget = parent_budget
        self._router = ContractNetRouter()
        for bidder in self._bidders:
            self._router.register(bidder.to_agent_capability())
        self._latest_award: ContractAward | None = None

    @property
    def latest_award(self) -> ContractAward | None:
        return self._latest_award

    def route_contract(
        self,
        task: str,
        subtask_budgets: Mapping[str, float] | None = None,
    ) -> ContractAward:
        requested_budget = Decimal("0.00")
        if subtask_budgets:
            requested_budget = sum((Decimal(str(value)) for value in subtask_budgets.values()), Decimal("0.00"))

        budget_ok = self._budget_tracker.reserve(requested_budget)
        route_result = self._router.route(task)
        fulfilled = budget_ok and route_result.winning_agent is not None
        state = ContractState.FULFILLED if fulfilled else ContractState.VIOLATED
        winning_agent = route_result.winning_agent if budget_ok else None

        self._latest_award = ContractAward(
            task=task,
            winning_agent=winning_agent,
            state=state,
            requested_budget=requested_budget,
            remaining_budget=self._budget_tracker.remaining_budget,
            bids=route_result.all_bids or {},
        )
        return self._latest_award

    async def validate_group_state(self, messages: list[BaseChatMessage] | None) -> None:
        pass

    async def reset(self) -> None:
        self._budget_tracker = BudgetTracker(self._initial_parent_budget)
        self._latest_award = None

    async def select_speaker(self, thread: Sequence[BaseAgentEvent | BaseChatMessage]) -> list[str] | str:
        task_text = ""
        if thread:
            last_message = thread[-1]
            content = getattr(last_message, "content", "")
            if isinstance(content, str):
                task_text = content
            else:
                task_text = str(content)
        award = self.route_contract(task_text)
        if award.winning_agent:
            return self._participant_name_to_topic_type[award.winning_agent]
        raise RuntimeError("No winning agent selected by contract-net-router.")
