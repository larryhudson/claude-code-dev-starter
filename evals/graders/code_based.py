"""Deterministic code-based graders for agent evaluation."""

from dataclasses import dataclass

from pydantic_evals.evaluators import Evaluator, EvaluatorContext

from evals.tasks.agent_task import AgentInput, AgentOutput


@dataclass
class UsedExpectedTool(Evaluator[AgentInput, AgentOutput]):
    """Check if the agent used the expected tool."""

    expected_tool: str

    def evaluate(self, ctx: EvaluatorContext[AgentInput, AgentOutput]) -> bool:
        """Return True if the expected tool was called."""
        return self.expected_tool in ctx.output.tool_calls


@dataclass
class ResponseContains(Evaluator[AgentInput, AgentOutput]):
    """Check if response contains expected substring."""

    expected_substring: str
    case_sensitive: bool = False

    def evaluate(self, ctx: EvaluatorContext[AgentInput, AgentOutput]) -> bool:
        """Return True if the expected substring is in the response."""
        response = ctx.output.response
        expected = self.expected_substring
        if not self.case_sensitive:
            response = response.lower()
            expected = expected.lower()
        return expected in response


@dataclass
class NoToolsCalled(Evaluator[AgentInput, AgentOutput]):
    """Verify the agent answered without using tools."""

    def evaluate(self, ctx: EvaluatorContext[AgentInput, AgentOutput]) -> bool:
        """Return True if no tools were called."""
        return len(ctx.output.tool_calls) == 0
