"""Pytest fixtures for the evaluation framework."""

from pathlib import Path

import pytest
from dotenv import load_dotenv
from pydantic_evals import Dataset

from evals.tasks.agent_task import AgentInput, AgentOutput, run_agent_task

# Load environment variables from .env file
load_dotenv()

DATASETS_DIR = Path(__file__).parent / "datasets"


@pytest.fixture
def tool_usage_dataset() -> Dataset[AgentInput, AgentOutput, dict]:
    """Load the tool usage evaluation dataset."""
    return Dataset[AgentInput, AgentOutput, dict].from_file(DATASETS_DIR / "tool_usage.yaml")


@pytest.fixture
def agent_task():
    """Return the agent task function."""
    return run_agent_task
