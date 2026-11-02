
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


def refine_code_review(source_file_path, review_file_path, reflection_file_path):
    """
    Refinement Agent

    This agent:
    1. Reads the original Python source code.
    2. Reads the initial code review (V1).
    3. Reads the reflection feedback.
    4. Produces an improved code review (V2).
    5. Returns the refined report.
    """

    # Step 3: Read the original source code
    source_code = Path(source_file_path).read_text(encoding="utf-8")

    # Step 4: Read the initial review (V1)
    review_v1 = Path(review_file_path).read_text(encoding="utf-8")

    # Step 5: Read the reflection feedback
    reflection_feedback = Path(reflection_file_path).read_text(
        encoding="utf-8"
    )

    # Step 6: Define the System Prompt
    system_prompt = """
    You are a senior Python code reviewer improving an earlier AI review.

    Your responsibilities:
    - Correct inaccurate claims in the initial review.
    - Use reflection feedback to improve the report.
    - Verify every finding against the original source code.
    - Identify missing validations and meaningful edge cases.
    - Recommend specific pytest unit tests.

    Rules:
    - Do not modify the original Python source code.
    - Do not blindly accept the reflection feedback.
    - Remove unsupported or incorrect claims.
    - Distinguish confirmed bugs from potential risks.
    - Do not invent bugs or test results.
    - Produce a complete, standalone Markdown review report.
    """

    # Step 7: Define the User Prompt
    user_prompt = f"""
    Improve the initial code review using the reflection feedback.

    ORIGINAL SOURCE CODE:
    {source_code}

    INITIAL CODE REVIEW (V1):
    {review_v1}

    REFLECTION FEEDBACK:
    {reflection_feedback}

    Produce Code Review V2 with these sections:

    1. Confirmed Issues
    2. Potential Risks and Missing Validations
    3. Edge Cases
    4. Recommended pytest Tests
    5. Summary of Improvements from V1

    Ensure all findings are technically accurate.
    """

    # Step 8: Send the refinement request to the AI model
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # Step 9: Return the refined review
    return response.output_text
