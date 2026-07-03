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
)
from src.frameworks.base import StepDefinition


class TestBaseFramework:
    """Test base framework contract."""

    def test_fishbone_has_required_properties(self):
        fw = FishboneFramework()
        assert fw.name
        assert fw.description
        assert len(fw.steps) > 0
        for step in fw.steps:
            assert isinstance(step, StepDefinition)
            assert step.name
            assert step.description
            assert step.system_prompt

    def test_fault_tree_has_required_properties(self):
        fw = FaultTreeFramework()
        assert fw.name
        assert fw.description
        assert len(fw.steps) > 0

    def test_iceberg_has_required_properties(self):
        fw = IcebergFramework()
        assert fw.name
        assert fw.description
        assert len(fw.steps) > 0

    def test_apollo_rca_has_required_properties(self):
        fw = ApolloRCAFramework()
        assert fw.name
        assert fw.description
        assert len(fw.steps) > 0

    def test_stamp_has_required_properties(self):
        fw = STAMPFramework()
        assert fw.name
        assert fw.description
        assert len(fw.steps) > 0

    def test_swiss_cheese_has_required_properties(self):
        fw = SwissCheeseFramework()
        assert fw.name
        assert fw.description
        assert len(fw.steps) > 0

    def test_cynefin_has_required_properties(self):
        fw = CynefinFramework()
        assert fw.name
        assert fw.description
        assert len(fw.steps) > 0

    def test_dmaic_has_required_properties(self):
        fw = DMAICFramework()
        assert fw.name
        assert fw.description
        assert len(fw.steps) > 0


class TestFrameworkPromptGeneration:
    """Test that each framework generates valid prompts."""

    @pytest.mark.parametrize("framework_cls", [
        FishboneFramework,
        FaultTreeFramework,
        IcebergFramework,
        ApolloRCAFramework,
        STAMPFramework,
        SwissCheeseFramework,
        CynefinFramework,
        DMAICFramework,
    ])
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
        frameworks = [
            FishboneFramework(),
            FaultTreeFramework(),
            IcebergFramework(),
            ApolloRCAFramework(),
            STAMPFramework(),
            SwissCheeseFramework(),
            CynefinFramework(),
            DMAICFramework(),
        ]
        names = [fw.name for fw in frameworks]
        assert len(names) == len(set(names)), "Framework names must be unique"

    def test_all_frameworks_have_descriptions(self):
        frameworks = [
            FishboneFramework(),
            FaultTreeFramework(),
            IcebergFramework(),
            ApolloRCAFramework(),
            STAMPFramework(),
            SwissCheeseFramework(),
            CynefinFramework(),
            DMAICFramework(),
        ]
        for fw in frameworks:
            assert len(fw.description) > 20, f"{fw.name} description too short"

    def test_step_count_ranges(self):
        """Fishbone, Iceberg, Swiss Cheese, Cynefin = 4 steps.
        Fault Tree = 4 steps.
        Apollo RCA, STAMP, DMAIC = 5 steps."""
        assert FishboneFramework().total_steps == 4
        assert FaultTreeFramework().total_steps == 4
        assert IcebergFramework().total_steps == 4
        assert ApolloRCAFramework().total_steps == 5
        assert STAMPFramework().total_steps == 5
        assert SwissCheeseFramework().total_steps == 4
        assert CynefinFramework().total_steps == 4
        assert DMAICFramework().total_steps == 5


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
        assert len(frameworks) == 8
        keys = [fw["key"] for fw in frameworks]
        assert "fishbone" in keys
        assert "dmaic" in keys
        assert "stamp" in keys

    def test_framework_registry_keys(self):
        from src.framework_selector import FRAMEWORK_REGISTRY
        expected_keys = {
            "fishbone", "fault_tree", "iceberg", "apollo_rca",
            "stamp", "swiss_cheese", "cynefin", "dmaic",
        }
        assert set(FRAMEWORK_REGISTRY.keys()) == expected_keys