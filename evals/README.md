# Agent Evaluations

This directory contains the evaluation framework for testing AI agent behavior using `pydantic-evals`.

## Quick Start

```bash
# Run all evaluations
make eval

# Run quick evaluations (excludes slow tests)
make eval-quick

# Run with verbose output and save report
make eval-report
```

## Directory Structure

```
evals/
├── __init__.py          # Package exports
├── conftest.py          # Pytest fixtures
├── test_evals.py        # Main test entry point
├── README.md            # This file
│
├── datasets/            # YAML test case files
│   └── tool_usage.yaml  # Tests for MCP tool selection
│
├── graders/             # Evaluation graders
│   ├── code_based.py    # Deterministic graders
│   └── llm_based.py     # LLM judge configurations
│
└── tasks/               # Task wrappers
    └── agent_task.py    # Wraps the agent for evaluation
```

## Writing New Test Cases

### Adding to Existing Datasets

Edit the YAML files in `datasets/` to add new test cases:

```yaml
cases:
  - name: my_new_test_case
    inputs:
      user_message: "What is the project name?"
    metadata:
      difficulty: easy
      expected_behavior: should_use_tool
      expected_tool: get_project_info
```

### Test Case Fields

- `name`: Unique identifier for the test case
- `inputs`: The `AgentInput` fields (currently just `user_message`)
- `metadata`: Additional data for filtering and assertions
  - `expected_behavior`: `should_use_tool` or `should_not_use_tool`
  - `expected_tool`: The tool name that should be called
  - `difficulty`: `easy`, `medium`, or `hard`

## Writing Custom Graders

### Code-Based Graders

For deterministic checks, add to `graders/code_based.py`:

```python
from dataclasses import dataclass
from pydantic_evals.evaluators import Evaluator, EvaluatorContext
from evals.tasks.agent_task import AgentInput, AgentOutput

@dataclass
class MyCustomGrader(Evaluator[AgentInput, AgentOutput]):
    """Description of what this grader checks."""

    some_parameter: str

    def evaluate(self, ctx: EvaluatorContext[AgentInput, AgentOutput]) -> bool:
        # ctx.input contains the AgentInput
        # ctx.output contains the AgentOutput
        return some_condition(ctx.output)
```

### LLM-Based Graders

For subjective evaluations, add to `graders/llm_based.py`:

```python
from pydantic_evals.evaluators import LLMJudge

my_judge = LLMJudge(
    rubric="Clear description of what makes a good response",
    include_input=True,
    model="anthropic:claude-sonnet-4-20250514",
)
```

## Available Graders

### Code-Based

- `UsedExpectedTool(expected_tool)`: Checks if a specific tool was called
- `ResponseContains(expected_substring)`: Checks if response contains text
- `NoToolsCalled()`: Verifies no tools were used

### LLM-Based

- `accuracy_judge`: Evaluates factual accuracy
- `helpfulness_judge`: Evaluates helpfulness and actionability
- `safety_judge`: Checks for appropriate refusals
- `tool_appropriateness_judge`: Evaluates tool usage decisions

## Running Specific Tests

```bash
# Run only tool usage tests
uv run pytest evals/test_evals.py::TestToolUsage -v

# Run a specific test
uv run pytest evals/test_evals.py::TestToolUsage::test_should_use_tools -v

# Run with specific markers
uv run pytest evals/ -v -k "not slow"
```

## Environment Variables

- `ANTHROPIC_API_KEY`: Required for running the agent and LLM judges

## Best Practices

1. **Start simple**: Begin with code-based graders before adding LLM judges
2. **Use meaningful names**: Test case names should describe the scenario
3. **Group related tests**: Use metadata to categorize tests
4. **Set realistic thresholds**: Start with lower pass rates and increase as the agent improves
5. **Document expected behavior**: Use metadata to make expectations explicit

## References

- [Anthropic: Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [Pydantic Evals Documentation](https://ai.pydantic.dev/evals/)
