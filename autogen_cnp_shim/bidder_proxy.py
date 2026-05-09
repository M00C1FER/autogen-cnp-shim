"""Bridge AutoGen assistants into contract-net-router bidder capabilities."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from contract_net_router import AgentCapability


@dataclass(slots=True)
class BidderProxy:
    """A lightweight AssistantAgent -> CNP bidder bridge."""

    name: str
    description: str = ""
    specialties: list[str] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)

    @classmethod
    def from_assistant_agent(
        cls,
        assistant_agent: Any,
        specialties: list[str] | None = None,
        keywords: list[str] | None = None,
    ) -> "BidderProxy":
        return cls(
            name=getattr(assistant_agent, "name", assistant_agent.__class__.__name__),
            description=getattr(assistant_agent, "description", ""),
            specialties=specialties or [],
            keywords=keywords or [],
        )

    def to_agent_capability(self) -> AgentCapability:
        return AgentCapability(
            name=self.name,
            specialties=self.specialties,
            keywords=self.keywords,
            metadata={"description": self.description},
        )
