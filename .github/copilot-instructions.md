# Copilot Coding Agent — Instructions

## Project context

`autogen-cnp-shim` adapts `M00C1FER/contract-net-router` (FIPA Contract Net Protocol for LLM agent dispatch with formal lifecycle states + budget conservation) into a primitive consumable by Autogen. The 2025 *Agent Contracts* paper (arxiv 2601.08815, COINE 2026) explicitly notes Autogen lacks formal governance mechanisms — this shim closes that gap parasitically without requiring a fork.

This is a **shim**, not a competitor. It must:
- Be installable as a single `pip install` package alongside autogen.
- Add zero overhead to autogen workflows that don't use it.
- Surface CNP's lifecycle / budget conservation through autogen's native primitives (Crew/Agent for CrewAI; AgentChat / GroupChat for AutoGen).

## Coding rules

- Python 3.10+.
- `contract-net-router` is a runtime dependency (`pip install contract-net-router`); autogen is the integration target.
- No vendoring of router code — depend on the upstream package.
- Type hints on every public function.
- Imports sorted: stdlib, third-party, local.

## Tests

- `pytest` from repo root. Unit + integration tests.
- Integration test: end-to-end autogen workflow that uses the shim to award contracts with budget caps.
- Do NOT mock the router internals; mock only the LLM calls.

## Don't touch

- The contract-net-router public API — it's the upstream truth. Add adaptation layers, don't bypass.
- Autogen's public API contract — extend via documented extension points only.

## Acceptance signal

A PR is ready when:
1. `pytest` clean.
2. README has working install command + minimal end-to-end example.
3. Autogen workflows that don't import the shim continue to work unchanged.
