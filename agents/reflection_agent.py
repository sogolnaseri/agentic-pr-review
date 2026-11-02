
import os
from pathlib import Path

# Load environment variables from the .env file
from dotenv import load_dotenv

# Import the OpenAI client
from openai import OpenAI

# Step 1: Load the API key from .env
load_dotenv()

# Step 2: Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def reflect_on_review(source_file_path, review_file_path):
    """
    Reflection Agent

    This agent:
    1. Reads the original Python source code.
    2. Reads the initial Code Review report (V1).
    3. Evaluates the accuracy and completeness of V1.
    4. Identifies unsupported claims and missing issues.
    5. Returns constructive feedback for refinement.
    """

    # Step 3: Read the original source code
    source_code = Path(source_file_path).read_text(encoding="utf-8")

    # Step 4: Read the initial Code Review report (V1)
    review_v1 = Path(review_file_path).read_text(encoding="utf-8")

    # Step 5: Define the System Prompt
    # The AI acts as an independent reviewer of the first agent's work.
    system_prompt = """
    You are a senior Python code review quality evaluator.

    Your task is to critically evaluate an AI-generated code review
    against the actual Python source code.

    Rules:
    - Identify technically incorrect or unsupported claims.
    - Identify important bugs or edge cases missing from the review.
    - Distinguish confirmed bugs from possible risks.
    - Check whether recommended tests are relevant.
    - Do not modify the source code.
    - Do not rewrite the full review yet.
    - Provide specific, actionable feedback.
    """

    # Step 6: Define the User Prompt
    # Provide both the original code and the V1 report.
    user_prompt = f"""
    Evaluate the accuracy and completeness of this code review.

    ORIGINAL PYTHON SOURCE CODE:
    {source_code}

    INITIAL CODE REVIEW (V1):
    {review_v1}

    Provide reflection feedback in these sections:

    1. Correct Findings
    2. Incorrect or Unsupported Claims
    3. Missing Bugs and Edge Cases
    4. Improvements Needed for V2
    """

    # Step 7: Ask the AI model to reflect on V1
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # Step 8: Return the reflection feedback
    return response.output_text
