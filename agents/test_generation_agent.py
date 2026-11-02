
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


def generate_tests(source_file_path, review_file_path):
    """
    Test Generation Agent (Writer)

    This agent:
    1. Reads the original Python source code.
    2. Reads the refined code review report (V2).
    3. Plans unit test scenarios.
    4. Generates pytest test code.
    5. Returns the generated tests as a string.
    """

    # Step 3: Read the original source code
    source_code = Path(source_file_path).read_text(encoding="utf-8")

    # Step 4: Read the refined code review (V2)
    review_v2 = Path(review_file_path).read_text(encoding="utf-8")

    # Step 5: Define the System Prompt
    system_prompt = """
    You are a senior Python QA automation engineer.

    Your role is to generate high-quality pytest unit tests.

    Responsibilities:
    - Analyze the original Python source code.
    - Use the refined code review as guidance.
    - Plan tests for normal behavior, boundaries, and invalid inputs.
    - Generate executable pytest tests.

    Rules:
    - Use pytest, not unittest.
    - Import functions from sample_app.order_service.
    - Do not modify production source code.
    - Do not blindly trust the review report.
    - Verify expected numeric results before writing assertions.
    - Distinguish current behavior from desired behavior.
    - Tests for missing validation may intentionally fail.
    - Do not change expected results merely to make tests pass.
    - Return only valid Python code.
    - Do not include Markdown code fences or explanations.
    """

    # Step 6: Define the User Prompt
    user_prompt = f"""
    Generate a pytest test module for this application.

    ORIGINAL PYTHON SOURCE CODE:
    {source_code}

    REFINED CODE REVIEW (V2):
    {review_v2}

    Requirements:
    1. Test calculate_order_total.
    2. Test check_inventory.
    3. Test calculate_shipping.
    4. Include normal cases and boundary cases.
    5. Include tests for invalid inputs where appropriate.
    6. Add descriptive test function names.
    7. Add English comments explaining important test cases.
    8. Return a complete Python test module.

    Important:
    A failing test can reveal a real application defect.
    Do not invent test execution results.
    """

    # Step 7: Ask the AI model to generate pytest tests
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # Step 8: Return the generated test code
    return response.output_text
