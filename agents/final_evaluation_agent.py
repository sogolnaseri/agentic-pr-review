
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_final_evaluation(
    source_file_path,
    review_v2_path,
    qa_evaluation_path,
    pytest_v1_path,
    pytest_v2_path
):
    """
    Generate a final evaluation report for the developer.

    This agent combines:
    - Original production code
    - Refined code review
    - QA evaluation feedback
    - pytest V1 results
    - pytest V2 results

    It does not modify production code or tests.
    """

    # Read all required inputs
    source_code = Path(source_file_path).read_text(encoding="utf-8")
    review_v2 = Path(review_v2_path).read_text(encoding="utf-8")
    qa_feedback = Path(qa_evaluation_path).read_text(encoding="utf-8")
    pytest_v1 = Path(pytest_v1_path).read_text(encoding="utf-8")
    pytest_v2 = Path(pytest_v2_path).read_text(encoding="utf-8")

    # Define the system prompt
    system_prompt = """
    You are a senior software quality engineer.

    Your task is to produce a clear, accurate final evaluation
    report for a developer reviewing a pull request.

    Rules:
    - Do not modify any code or tests.
    - Use actual pytest results, not invented results.
    - Distinguish test defects from production defects.
    - Do not assume negative-input validation is a confirmed requirement.
    - Clearly identify requirements that need human confirmation.
    - Do not claim all tests passed when some failed.
    - Provide practical recommendations.
    - Return a Markdown report only.
    - Never classify missing negative-input validation as a confirmed
      production defect unless explicit requirements support it.
    - Recommend clarifying business requirements BEFORE implementing
      validation changes.
    - Distinguish observed behavior, confirmed defects,
      and potential improvements.
    """

    # Define the user prompt
    user_prompt = f"""
    Create a final evaluation report for this project.

    ORIGINAL PRODUCTION CODE:
    {source_code}

    REFINED CODE REVIEW:
    {review_v2}

    QA EVALUATION FEEDBACK:
    {qa_feedback}

    PYTEST VERSION 1 RESULTS:
    {pytest_v1}

    PYTEST VERSION 2 RESULTS:
    {pytest_v2}

    Write a Markdown report with these sections:

    1. Executive Summary
    2. Code Review Findings
    3. Test Results Comparison (V1 vs V2)
    4. Remaining Failed Tests and Root Causes
    5. Human Review and Corrections
    6. Recommended Developer Actions
    7. Final Conclusion

    Include a comparison table showing passed, failed,
    and total tests for V1 and V2.

    Explicitly state that the large-values test was corrected
    from an incorrect expected value of 995000000000.0
    to the correct value of 950000000000.0.

    Treat the four remaining negative-input test failures
    as unresolved validation requirements, not automatically
    confirmed production defects.
    IMPORTANT:
    The four negative-input failures represent unconfirmed
    business requirements. Do not recommend implementing
    validation immediately. Recommend confirming requirements first.
    """

    # Ask the AI model to generate the final report
    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # Return the report without writing any files
    return response.output_text
