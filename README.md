# AI-Powered Code Review & Test Automation

A Python-based multi-agent AI workflow that automates code review, generates unit tests, evaluates execution results, and produces developer-facing quality reports using OpenAI models.

## Overview

This project demonstrates how multiple specialized AI agents can collaborate in a structured software quality assurance workflow.

Instead of relying on a single AI response, the system uses **reflection, refinement, automated test execution, evaluation, and human feedback** to improve the quality of its outputs.

The current implementation analyzes a local Python sample application. It does not yet connect to live GitHub pull requests.

## Key Features

- **AI Code Review:** Analyze Python source code and identify potential issues.
- **Reflection:** Critically evaluate the initial review for inaccuracies and missing details.
- **Review Refinement:** Improve the review based on reflection feedback.
- **Test Generation:** Generate pytest unit tests from the source code and refined review.
- **Automated Test Execution:** Run generated tests using pytest and capture actual results.
- **QA Evaluation:** Analyze test failures and distinguish potential production defects from test defects.
- **Test Refinement:** Generate an improved test suite using evaluation feedback.
- **Final Evaluation:** Summarize findings, test results, remaining risks, and recommended developer actions.
- **Human-in-the-Loop:** Allow human corrections when AI-generated assessments or tests are inaccurate.

## Workflow Architecture

```text
Python Source Code
       |
       v
Code Review Agent
       |
       v
Reflection Agent
       |
       v
Review Refinement Agent
       |
       v
Test Generation Agent
       |
       v
pytest Execution (V1)
       |
       v
QA Evaluation Agent
       |
       v
Test Refinement Agent
       |
       v
pytest Execution (V2)
       |
       v
Final Evaluation Agent
       |
       v
Developer Quality Report
```

The workflow is coordinated by a Python orchestrator (`main.py`). Existing output files are preserved to avoid unnecessary API calls and overwriting human-reviewed artifacts.

## Technology Stack

- Python
- OpenAI API (`gpt-4o-mini`)
- pytest
- python-dotenv
- Python subprocess
- Markdown reporting

## Project Structure

```text
agentic-pr-review/
├── agents/
│   ├── code_review_agent.py
│   ├── reflection_agent.py
│   ├── refinement_agent.py
│   ├── test_generation_agent.py
│   ├── qa_evaluation_agent.py
│   ├── test_refinement_agent.py
│   └── final_evaluation_agent.py
├── sample_app/
│   └── order_service.py
├── tests/
│   ├── test_order_service.py
│   └── test_order_service_v2.py
├── reports/
│   ├── code_review_v1.md
│   ├── code_review_reflection.md
│   ├── code_review_v2.md
│   ├── pytest_results_v1.txt
│   ├── qa_evaluation_v1.md
│   ├── pytest_results_v2.txt
│   └── final_evaluation.md
├── main.py
├── README.md
├── .env
└── .gitignore
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/sogolnaseri/agentic-pr-review.git
cd agentic-pr-review
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install openai python-dotenv pytest
```

### 4. Configure your API key

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
```

**Security:** Never commit your `.env` file or API key to GitHub.

### 5. Run the workflow

```bash
python main.py --step all
```

You can also run individual steps, for example:

```bash
python main.py --step review
python main.py --step reflection
python main.py --step test-generation
python main.py --step final-evaluation
```

**Note:** The orchestrator skips existing outputs during a full workflow run. If you modify source code or prompts, regenerate affected reports and tests before relying on their results.

**Safety:** AI-generated test files contain executable Python code. Review them before running pytest. For fully autonomous execution, use an isolated sandbox.

## Experimental Results

The workflow was evaluated using a sample order-processing application containing order-total, inventory, and shipping functions.

| Metric      | Test V1 | Test V2 |
| ----------- | ------: | ------: |
| Total tests |      13 |      13 |
| Passed      |       8 |       9 |
| Failed      |       5 |       4 |

### Key Findings

- An incorrect expected value in a large-number calculation test was identified and manually corrected.
- Test V2 improved from 8 to 9 passing tests.
- Four remaining failures concern negative-input validation.
- Those failures require confirmation of business requirements before being classified as production defects.

These results illustrate why generated tests and AI evaluations should not be accepted without verification.

## Human-in-the-Loop

Human review played an important role in this experiment.

The QA evaluation initially treated a failed arithmetic assertion as a production defect. Human inspection identified an incorrect expected value in the generated test instead.

The expected result was corrected from `995000000000.0` to `950000000000.0`.

This correction improved the passing-test count without modifying production code.

The workflow therefore demonstrates the value of combining automated AI evaluation with human judgment.

## Limitations

- The current version operates on a local Python sample rather than a live GitHub PR.
- Workflow execution is coordinated by deterministic Python logic.
- Generated tests are not executed in an isolated sandbox.
- Existing output files may become outdated if source files or prompts change.
- Human review is still needed to validate requirements and AI-generated conclusions.

## Future Improvements

- GitHub pull request integration
- Sandboxed test execution
- Structured evaluation metrics
- Automated detection of stale reports
- CI/CD integration using GitHub Actions
- Support for additional programming languages

## Conclusion

This project demonstrates a practical application of agentic AI patterns in software engineering through specialized agents, reflection, refinement, external test execution, and human oversight.

The objective is not to replace developers, but to support more efficient and reliable code review and testing workflows.
