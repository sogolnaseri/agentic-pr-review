
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def refine_tests(source_file_path, test_v1_path,
                 qa_evaluation_path):
    """
    Refine generated pytest tests using QA feedback.

    Inputs:
    - Original production source code
    - Generated tests V1
    - QA evaluation report (including human feedback)

    Output:
    - Improved pytest test code (V2) as a string

    This agent does not modify any files.
    """

    # Read the production code
    source_code = Path(source_file_path).read_text(
        encoding="utf-8"
    )

    # Read the original generated tests
    test_v1 = Path(test_v1_path).read_text(
        encoding="utf-8"
    )

    # Read QA evaluation feedback
    qa_feedback = Path(qa_evaluation_path).read_text(
        encoding="utf-8"
    )

    # Define the system prompt
    system_prompt = """
    You are a senior Python test automation engineer.

    Your role is to refine pytest tests using feedback
    from a QA Evaluation Agent and human review.

    Rules:
    - Do not modify production code.
    - Preserve valuable existing test cases.
    - Correct incorrect expected values and assertions.
    - Do not delete failing tests merely to make them pass.
    - Keep negative-input tests when they expose potential
      missing validation, but mark their expected behavior
      as requiring specification confirmation.
    - Treat the QA report as feedback, not unquestionable truth.
    - Verify numerical expectations independently.
    - Use pytest conventions and clear test names.
    - Return only valid Python code.
    - Do not include Markdown code fences.
    """

    # Define the user prompt
    user_prompt = f"""
    Refine the following pytest test suite.

    ORIGINAL PRODUCTION CODE:
    {source_code}

    TESTS VERSION 1:
    {test_v1}

    QA EVALUATION FEEDBACK:
    {qa_feedback}

    Generate Test Version 2.

    Requirements:
    1. Preserve useful existing test coverage.
    2. Fix the incorrect expected value in the large-values test.
    3. Preserve negative-input tests and add comments explaining
       that validation requirements need confirmation.
    4. Improve test clarity and maintainability.
    5. Return a complete, runnable pytest test module.
    6. Return Python code only.
    """

    # Ask the model to generate the refined tests
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # Return refined test code without writing files
    return response.output_text
