---
name: Agent Evaluations
description: Comprehensive guide for building evaluations (evals) for AI agents, based on Anthropic's engineering best practices
---

# Agent Evaluations Guide

This skill provides a comprehensive methodology for evaluating AI agents, based on [Anthropic's engineering blog post on demystifying evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents).

## Why Evals Matter

Good evaluations help teams ship AI agents more confidently by catching issues before production rather than reactively fixing failures in live systems. Without them, teams get stuck in reactive loops—catching issues only in production, where fixing one failure creates others.

Teams investing early find development accelerates as failures become tests and tests prevent regressions.

---

## Core Terminology

| Term | Definition |
|------|------------|
| **Task/Problem** | Single test with defined inputs and success criteria |
| **Trial** | Individual attempt at a task (run multiple times for consistency) |
| **Grader** | Logic that scores agent performance on specific aspects |
| **Transcript/Trace** | Complete record of trial interactions, tool calls, and outputs |
| **Outcome** | Final environment state after task completion |
| **Evaluation Harness** | Infrastructure that runs evals end-to-end |
| **Agent Harness** | System enabling models to act as agents |

---

## Three Types of Graders

### 1. Code-Based Graders

**Methods:**
- String matching and regex
- Static analysis (linting, type checking)
- Outcome/state verification
- Tool call checking
- Unit test execution

**Strengths:**
- Fast and cheap to run
- Objective and reproducible
- Easy to debug

**Weaknesses:**
- Brittle to valid variations in output
- Lacks nuance for subjective tasks

**When to use:** Always prefer deterministic graders when possible. Use for verifying concrete outcomes like "did the code compile?", "did the test pass?", "was the correct API called?"

### 2. Model-Based Graders

**Methods:**
- Rubric scoring with defined criteria
- Natural language assertions
- Pairwise comparisons between outputs

**Strengths:**
- Flexible and scalable
- Captures nuance in responses
- Handles open-ended tasks well

**Weaknesses:**
- Non-deterministic results
- More expensive to run
- Requires human calibration to validate accuracy

**When to use:** For evaluating quality, tone, completeness, or other subjective aspects. Always calibrate against human judgment.

### 3. Human Graders

**Methods:**
- Subject matter expert (SME) review
- Crowdsourced judgment
- Spot-check sampling
- A/B testing with real users

**Strengths:**
- Gold-standard quality
- Matches real expert judgment

**Weaknesses:**
- Expensive and slow
- Requires domain experts at scale
- Inconsistent coverage

**When to use:** For calibrating model-based graders, handling edge cases, and validating that automated graders align with human expectations.

---

## Handling Non-Determinism

Agents are non-deterministic—the same input can produce different outputs. Use these metrics:

### pass@k
Likelihood of getting at least one correct solution in k attempts.

- As attempts increase, pass@k approaches 100%
- Use when one success is sufficient (e.g., code generation where any working solution is acceptable)

### pass^k
Probability that ALL k trials succeed.

- Demands consistency: 75% per-trial success = ~42% pass^3
- Use for agents requiring reliability (e.g., customer service where every interaction must succeed)

**Choose based on product needs:** pass@k for tools where one success matters; pass^k for agents requiring consistent reliability.

---

## Agent Type-Specific Approaches

### Coding Agents

Use deterministic testing as the primary grader: "Does the code run and do tests pass?"

**Recommended grading combination:**
1. Deterministic tests verifying the fix works
2. Static analysis (ruff, mypy, bandit for security)
3. LLM rubrics evaluating code quality
4. State checking for logs, files, or security concerns
5. Tool call verification (did it use the right tools?)

### Conversational Agents

The quality of the interaction itself is part of what you're evaluating.

**Approach:**
- Use a second LLM to simulate the user
- Define multidimensional success criteria:
  - Was the issue resolved?
  - How many turns did it take?
  - Was the tone appropriate?
  - Did it stay within policy?

### Research Agents

Face unique challenges: subjective quality, constantly shifting ground truth, open-ended outputs.

**Combine graders checking:**
- Groundedness: Are claims supported by cited sources?
- Coverage: Are key facts included?
- Source quality: Are sources authoritative and relevant?

LLM-based rubrics should be frequently calibrated against expert human judgment.

### Computer Use Agents

Interact through screenshots and clicks rather than APIs.

**Considerations:**
- Requires real or sandboxed environments
- Balance token efficiency vs. latency
- DOM extraction is efficient for text-heavy tasks
- Screenshots are better for visual tasks

---

## The 8-Step Roadmap

### Step 0: Start Early
Begin with 20-50 tasks derived from real failures. Large effect sizes in early development mean small samples are sufficient to see signal.

### Step 1: Manual Testing
Convert existing manual checks and user-reported failures into automated test cases. Every bug report is a potential eval.

### Step 2: Unambiguous Tasks
Two domain experts should independently reach the same pass/fail verdict. Create reference solutions proving the task is solvable.

### Step 3: Balanced Problem Sets
Test where behaviors should AND shouldn't occur. Avoid class-imbalanced evals.

**Example:** Claude.ai web search required balancing:
- Queries that SHOULD trigger search (weather, news)
- Queries that SHOULD NOT trigger search (factual knowledge like "Who founded Apple?")

### Step 4: Stable Environment
Isolate trials from a clean state. Prevent shared state (cached files, resource exhaustion) from causing correlated failures between trials.

### Step 5: Thoughtful Graders
1. Prefer deterministic graders first
2. Use LLM graders when flexibility is needed
3. Apply human graders judiciously for calibration

**Important:** Grade outputs, not paths. Agents find valid solutions that eval designers didn't anticipate.

### Step 6: Read Transcripts
Verify graders work properly by reading actual transcripts. Failures should seem fair—it should be clear what the agent got wrong and why.

### Step 7: Monitor Saturation
When agents pass all solvable tasks, capability evals graduate to regression suites. Add harder tasks to continue measuring progress.

### Step 8: Maintain Long-Term
Treat evals like unit tests:
- Dedicated infrastructure teams support domain experts contributing tasks
- Practice **eval-driven development**: build evals before agents fulfill capabilities
- When new models release, run suites to see which improvements landed

---

## Complementary Evaluation Methods

| Method | Pros | Cons |
|--------|------|------|
| **Automated Evals** | Fast iteration, reproducible, runs on every commit | Upfront investment, maintenance required |
| **Production Monitoring** | Reveals real user behavior at scale | Reactive; problems reach users first |
| **A/B Testing** | Measures actual outcomes with controls | Slow (days/weeks); requires traffic |
| **User Feedback** | Surfaces unanticipated problems | Sparse, self-selected, skews severe |
| **Manual Transcript Review** | Builds intuition; catches subtle issues | Time-intensive; doesn't scale |
| **Systematic Human Studies** | Gold-standard quality | Expensive, slow, requires experts |

---

## Common Pitfalls

### Overly Rigid Grading
Opus 4.5 initially scored 42% on CORE-Bench due to:
- Grading "96.12" as wrong when answer was "96.124991..."
- Ambiguous specifications
- Stochastic task elements

After fixing grader bugs, score jumped to 95%.

### Ambiguous Success Criteria
METR discovered benchmark tasks asking agents to "optimize to thresholds" but grading required *exceeding* them, penalizing instruction-following models.

### Grading Paths Instead of Outcomes
Agents often find valid solutions that eval designers didn't anticipate. Grade the final outcome, not whether the agent took the expected path.

---

## Eval-Driven Development

Build evals defining planned capabilities **before** agents fulfill them:

1. Define what success looks like for a new feature
2. Write eval tasks that test that capability
3. Run evals—they should fail initially
4. Develop the agent capability
5. Iterate until evals pass
6. Keep evals as regression tests

When new models release, running your eval suite quickly reveals which capabilities improved.

---

## Quick Start Checklist

- [ ] Identify 20-50 real failure cases or user-reported issues
- [ ] Convert failures into task definitions with clear success criteria
- [ ] Ensure two people would agree on pass/fail for each task
- [ ] Create balanced test sets (should do X, should NOT do Y)
- [ ] Implement deterministic graders for concrete outcomes
- [ ] Add model-based graders for subjective quality aspects
- [ ] Set up isolated, clean-state environments for each trial
- [ ] Run multiple trials per task to handle non-determinism
- [ ] Read transcripts to verify graders are working correctly
- [ ] Integrate evals into CI/CD pipeline
- [ ] Schedule regular human review to calibrate model graders

---

## Implementation in This Project

This starter project includes an evaluation framework in the `evals/` directory:

```
evals/
├── harness.py           # Runs evals, collects transcripts
├── graders/
│   ├── code_based.py    # Deterministic graders
│   └── model_based.py   # LLM-powered graders
├── tasks/               # Task definitions (YAML or Python)
├── transcripts/         # Stored trial results
└── conftest.py          # Pytest integration
```

Run evals with:
```bash
uv run pytest evals/ -v
```

See the `evals/README.md` for detailed usage instructions.
