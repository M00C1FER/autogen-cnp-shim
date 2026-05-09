# autogen-cnp-shim

AutoGen 0.4+ adapter for `contract-net-router` that lets you use Contract Net Protocol governance (formal lifecycle + budget conservation) through familiar AgentChat group-chat primitives.

## Install

```bash
pip install autogen-cnp-shim
```

For local development:

```bash
pip install -e .
```

## Minimal example

```python
from autogen_cnp_shim import BidderProxy, CNPGroupChatManager

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
print(award.state)
```

See `examples/basic_research_team.py` for a runnable script.

## Decision matrix

| Need | Use |
| --- | --- |
| Simple deterministic turn order | `RoundRobinGroupChat` |
| LLM-selected next speaker with no formal budget governance | `SelectorGroupChat` |
| CNP-style bid/award lifecycle + explicit parent budget enforcement | `CNPGroupChatManager` |

## Compatibility

- Targets **AutoGen 0.4+ AgentChat** APIs.
- Does **not** target AutoGen 0.2/AG2 (separate fork).
- Uses upstream `contract-net-router` as a dependency (no vendoring).

## References

- Upstream router: https://github.com/M00C1FER/contract-net-router
- Agent Contracts paper: https://arxiv.org/abs/2601.08815
