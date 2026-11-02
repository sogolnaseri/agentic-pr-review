import os
from pathlib import Path

# Import dotenv to load environment variables from the .env file
from dotenv import load_dotenv

# Import the OpenAI client to communicate with the AI model
from openai import OpenAI


# Step 1: Load environment variables from the .env file
load_dotenv()

# Step 2: Initialize the OpenAI client using our API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def review_code(file_path):
    """
    Code Review Agent

    This agent:
    1. Reads a Python source code file.
    2. Sends the code to an AI model for review.
    3. Identifies potential bugs, missing validations, and edge cases.
    4. Recommends unit tests.
    5. Returns the AI-generated code review report.
    """

    # Step 3: Read the Python source code from the given file path
    # Example: sample_app/order_service.py
    code = Path(file_path).read_text(encoding="utf-8")

    # Step 4: Define the System Prompt
    # The System Prompt tells the AI its role, responsibilities, and rules.
    system_prompt = """
    You are a senior Python code reviewer.

    Your responsibilities:
    - Analyze Python code for potential bugs.
    - Identify missing input validations.
    - Identify edge cases and possible security issues.
    - Recommend unit tests for the code.

    Rules:
    - Do not modify the source code.
    - Explain each issue clearly.
    - Suggest improvements when necessary.
    """

    # Step 5: Define the User Prompt
    # The User Prompt contains the specific task and the actual source code.
    user_prompt = f"""
    Review the following Python code.

    Identify:
    1. Potential bugs
    2. Missing validations
    3. Edge cases
    4. Recommended unit tests

    Python source code:
    {code}
    """

    # Step 6: Send the System Prompt and User Prompt to the AI model
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    # Step 7: Extract the AI-generated response
    review_report = response.output_text

    # Step 8: Return the code review report to the caller
    return review_report