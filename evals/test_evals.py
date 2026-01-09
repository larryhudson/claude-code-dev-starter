"""Main test entry point for agent evaluations."""

import pytest
from pydantic_evals import Case, Dataset

from evals.tasks.agent_task import AgentInput, AgentOutput


class TestToolUsage:
    """Evaluate agent tool usage behavior."""

    @pytest.mark.asyncio
    async def test_tool_usage_eval(self, tool_usage_dataset, agent_task):
        """Run the full tool usage evaluation suite."""
        report = await tool_usage_dataset.evaluate(agent_task)
        report.print(include_input=True, include_output=True)

        # Assert minimum pass rate using assertions average
        averages = report.averages()
        if averages is not None and averages.assertions is not None:
            pass_rate = averages.assertions
            assert pass_rate >= 0.8, f"Tool usage pass rate {pass_rate:.1%} below 80% threshold"

    @pytest.mark.asyncio
    async def test_should_use_tools(self, tool_usage_dataset, agent_task):
        """Test cases where tools should be used."""
        should_use_cases: list[Case[AgentInput, AgentOutput, dict]] = [
            c
            for c in tool_usage_dataset.cases
            if c.metadata is not None and c.metadata.get("expected_behavior") == "should_use_tool"
        ]
        subset: Dataset[AgentInput, AgentOutput, dict] = Dataset(
            cases=should_use_cases,
            evaluators=tool_usage_dataset.evaluators,
        )
        report = await subset.evaluate(agent_task)

        for case_result in report.cases:
            metadata = case_result.metadata
            if metadata is not None and metadata.get("expected_tool"):
                expected = metadata["expected_tool"]
                assert expected in case_result.output.tool_calls, (
                    f"Expected tool {expected} not used in {case_result.name}"
                )

    @pytest.mark.asyncio
    async def test_should_not_use_tools(self, tool_usage_dataset, agent_task):
        """Test cases where tools should NOT be used."""
        should_not_use_cases: list[Case[AgentInput, AgentOutput, dict]] = [
            c
            for c in tool_usage_dataset.cases
            if c.metadata is not None
            and c.metadata.get("expected_behavior") == "should_not_use_tool"
        ]
        subset: Dataset[AgentInput, AgentOutput, dict] = Dataset(
            cases=should_not_use_cases,
            evaluators=tool_usage_dataset.evaluators,
        )
        report = await subset.evaluate(agent_task)

        for case_result in report.cases:
            assert len(case_result.output.tool_calls) == 0, (
                f"Unexpected tool usage in {case_result.name}: {case_result.output.tool_calls}"
            )
