from autogen_cnp_shim import BidderProxy


class FakeAssistant:
    name = "research_agent"
    description = "Handles research tasks"


def test_bidder_proxy_maps_assistant_agent_to_capability() -> None:
    proxy = BidderProxy.from_assistant_agent(
        FakeAssistant(),
        specialties=["research"],
        keywords=["paper", "survey"],
    )

    capability = proxy.to_agent_capability()

    assert capability.name == "research_agent"
    assert capability.specialties == ["research"]
    assert capability.keywords == ["paper", "survey"]
