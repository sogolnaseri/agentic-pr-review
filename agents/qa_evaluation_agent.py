
import os
from pathlib import Path

# Load environment variables from the .env file
from dotenv import load_dotenv

# Import the OpenAI client
from openai import OpenAI

# Step 1: Load environment variables
load_dotenv()

# Step 2: Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def evaluate_tests(source_file_path, review_file_path,
                   test_file_path, pytest_results_path):
    """
    QA Evaluation Agent (Editor)

    This agent:
    1. Reads the original production code.
    2. Reads the refined code review (V2).
    3. Reads the AI-generated pytest tests.
    4. Reads the actual pytest execution results.
    5. Classifies test failures and provides feedback.
    6. Returns an evaluation report for test refinement.
    """

    # Step 3: Read the original production code
    source_code = Path(source_file_path).read_text(encoding="utf-8")

    # Step 4: Read the refined code review
    review_v2 = Path(review_file_path).read_text(encoding="utf-8")

    # Step 5: Read the generated pytest tests
    generated_tests = Path(test_file_path).read_text(encoding="utf-8")

    # Step 6: Read the actual pytest results (External Feedback)
    pytest_results = Path(pytest_results_path).read_text(
        encoding="utf-8"
    )

    # Step 7: Define the System Prompt
    system_prompt = """
    You are a senior Python QA engineer and test quality evaluator.

    You act as an Editor reviewing tests produced by a Writer Agent.

    Responsibilities:
    - Evaluate generated pytest tests against the original source code.
    - Analyze real pytest execution results.
    - Identify incorrect assertions and expected values.
    - Identify tests that reveal missing production validations.
    - Recommend improvements for the next test version.

    Rules:
    - Do not modify production code.
    - Do not assume every failed test is a bad test.
    - Do not change correct assertions just to make tests pass.
    - Distinguish confirmed test defects from possible application defects.
    - If expected behavior is not specified, mark it as unclear.
    - Do not invent execution results.
    - Provide specific and actionable feedback.
    """

    # Step 8: Define the User Prompt
    user_prompt = f"""
    Evaluate these AI-generated pytest tests using actual test results.

    ORIGINAL SOURCE CODE:
    {source_code}

    REFINED CODE REVIEW:
    {review_v2}

    GENERATED TESTS (V1):
    {generated_tests}

    ACTUAL PYTEST RESULTS:
    {pytest_results}

    Produce a Markdown evaluation report with these sections:

    1. Test Execution Summary
    2. Correct and Valuable Tests
    3. Failed Tests and Root Cause Analysis
    4. Incorrect Generated Tests
    5. Potential Production Code Defects
    6. Recommendations for Test V2

    For each failed test, classify it as:
    - TEST_DEFECT
    - PRODUCTION_DEFECT
    - REQUIREMENT_UNCLEAR

    Explain the reasoning for each classification.
    """

    # Step 9: Send the evaluation request to the AI model
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # Step 10: Return the evaluation report
    return response.output_text
