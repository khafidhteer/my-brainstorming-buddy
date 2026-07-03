"""Tests for all framework implementations."""
import pytest
from src.frameworks import (
    FishboneFramework,
    FaultTreeFramework,
    IcebergFramework,
    ApolloRCAFramework,
    STAMPFramework,
    SwissCheeseFramework,
    CynefinFramework,
    DMAICFramework,
    JTBDFramework,
    ValuePropositionCanvasFramework,
    BeachheadMarketFramework,
    TechAdoptionLifecycleFramework,
    BlueOceanFramework,
    IdealCustomerProfileFramework,
    STPFramework,
    ThreeHorizonsFramework,
)
from src.frameworks.base import StepDefinition

# Collect all framework classes for parametrized tests
ALL_FRAMEWORKS = [
    FishboneFramework,
    FaultTreeFramework,
    IcebergFramework,
    ApolloRCAFramework,
    STAMPFramework,
    SwissCheeseFramework,
    CynefinFramework,
    DMAICFramework,
    JTBDFramework,
    ValuePropositionCanvasFramework,
    BeachheadMarketFramework,
    TechAdoptionLifecycleFramework,
    BlueOceanFramework,
    IdealCustomerProfileFramework,
    STPFramework,
    ThreeHorizonsFramework,
]


class TestBaseFramework:
    """Test base framework contract."""

    @pytest.mark.parametrize("fw_cls", ALL_FRAMEWORKS)
    def test_framework_has_required_properties(self, fw_cls):
        fw = fw_cls()
        assert fw.name
        assert fw.description
        assert len(fw.steps) > 0
        for step in fw.steps:
            assert isinstance(step, StepDefinition)
            assert step.name
            assert step.description
            assert step.system_prompt


class TestFrameworkPromptGeneration:
    """Test that each framework generates valid prompts."""

    @pytest.mark.parametrize("framework_cls", ALL_FRAMEWORKS)
    def test_generate_prompt_all_steps(self, framework_cls):
        fw = framework_cls()
        question = "Why did the production line stop?"
        previous_outputs = []

        for i in range(fw.total_steps):
            system_prompt, user_prompt = fw.generate_prompt(
                step_index=i,
                question=question,
                previous_outputs=previous_outputs,
            )
            assert system_prompt, f"Step {i} missing system prompt"
            assert user_prompt, f"Step {i} missing user prompt"
            assert question in user_prompt, f"Step {i} missing original question"
            previous_outputs.append(f"Mock output for step {i}")

    def test_generate_prompt_with_context(self):
        fw = FishboneFramework()
        question = "Why are customers leaving?"
        previous_outputs = [
            "Problem: High customer churn rate of 15% monthly",
            "Categories: People, Process, Product, Price",
        ]

        for i in range(2, fw.total_steps):
            system_prompt, user_prompt = fw.generate_prompt(
                step_index=i,
                question=question,
                previous_outputs=previous_outputs,
            )
            assert "customers" in user_prompt.lower()
            assert "churn" in user_prompt.lower()

    def test_invalid_step_raises_error(self):
        fw = FishboneFramework()
        with pytest.raises(ValueError):
            fw.generate_prompt(
                step_index=99,
                question="test",
                previous_outputs=[],
            )


class TestFrameworkMetadata:
    """Test framework metadata and descriptions."""

    def test_all_frameworks_have_unique_names(self):
        frameworks = [cls() for cls in ALL_FRAMEWORKS]
        names = [fw.name for fw in frameworks]
        assert len(names) == len(set(names)), "Framework names must be unique"

    def test_all_frameworks_have_descriptions(self):
        frameworks = [cls() for cls in ALL_FRAMEWORKS]
        for fw in frameworks:
            assert len(fw.description) > 20, f"{fw.name} description too short"

    def test_step_count_ranges(self):
        """4-step frameworks: Fishbone, Fault Tree, Iceberg, Swiss Cheese, Cynefin,
        Beachhead Market, Tech Adoption Lifecycle, Ideal Customer Profile, STP.
        5-step frameworks: Apollo RCA, STAMP, DMAIC, JTBD, Value Proposition Canvas,
        Blue Ocean, Three Horizons."""
        assert FishboneFramework().total_steps == 4
        assert FaultTreeFramework().total_steps == 4
        assert IcebergFramework().total_steps == 4
        assert ApolloRCAFramework().total_steps == 5
        assert STAMPFramework().total_steps == 5
        assert SwissCheeseFramework().total_steps == 4
        assert CynefinFramework().total_steps == 4
        assert DMAICFramework().total_steps == 5
        assert JTBDFramework().total_steps == 5
        assert ValuePropositionCanvasFramework().total_steps == 5
        assert BeachheadMarketFramework().total_steps == 4
        assert TechAdoptionLifecycleFramework().total_steps == 4
        assert BlueOceanFramework().total_steps == 5
        assert IdealCustomerProfileFramework().total_steps == 4
        assert STPFramework().total_steps == 4
        assert ThreeHorizonsFramework().total_steps == 5


class TestStepDefinition:
    """Test StepDefinition class."""

    def test_step_definition_creation(self):
        step = StepDefinition(
            index=0,
            name="Test Step",
            description="A test step",
            system_prompt="You are a test assistant",
            temperature=0.5,
            max_tokens=1024,
        )
        assert step.index == 0
        assert step.name == "Test Step"
        assert step.temperature == 0.5
        assert step.max_tokens == 1024

    def test_step_to_dict(self):
        step = StepDefinition(
            index=1,
            name="Analyze",
            description="Analysis step",
            system_prompt="Analyze the data",
        )
        d = step.to_dict()
        assert d["index"] == 1
        assert d["name"] == "Analyze"
        assert "system_prompt" not in d  # Should not be in serialized output


class TestFrameworkSelector:
    """Test framework selector logic."""

    def test_list_frameworks(self):
        from src.framework_selector import list_frameworks
        frameworks = list_frameworks()
        assert len(frameworks) == 16
        keys = [fw["key"] for fw in frameworks]
        assert "fishbone" in keys
        assert "dmaic" in keys
        assert "stamp" in keys
        assert "jtbd" in keys
        assert "blue_ocean" in keys
        assert "three_horizons" in keys

    def test_framework_registry_keys(self):
        from src.framework_selector import FRAMEWORK_REGISTRY
        expected_keys = {
            "fishbone", "fault_tree", "iceberg", "apollo_rca",
            "stamp", "swiss_cheese", "cynefin", "dmaic",
            "jtbd", "value_proposition_canvas", "beachhead_market",
            "tech_adoption_lifecycle", "blue_ocean", "ideal_customer_profile",
            "stp", "three_horizons",
        }
        assert set(FRAMEWORK_REGISTRY.keys()) == expected_keys