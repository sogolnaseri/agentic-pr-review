
import argparse
from pathlib import Path

# Import our specialized agents
from agents.code_review_agent import review_code
from agents.reflection_agent import reflect_on_review
# Import the Refinement Agent
from agents.refinement_agent import refine_code_review
# Import the Test Generation Agent (Writer)
from agents.test_generation_agent import generate_tests
# Import the QA Evaluation Agent (Editor)
from agents.qa_evaluation_agent import evaluate_tests
# Import the Test Refinement Agent
from agents.test_refinement_agent import refine_tests
import subprocess
import sys
# Import the Final Evaluation Agent
from agents.final_evaluation_agent import generate_final_evaluation

# Define project file paths
SOURCE_FILE = "sample_app/order_service.py"
REPORTS_DIR = Path("reports")
REVIEW_V1_FILE = REPORTS_DIR / "code_review_v1.md"
REFLECTION_FILE = REPORTS_DIR / "code_review_reflection.md"
REVIEW_V2_FILE = REPORTS_DIR / "code_review_v2.md"
# Define the output path for AI-generated pytest tests
TESTS_DIR = Path("tests")
GENERATED_TEST_FILE = TESTS_DIR / "test_order_service.py"
# Define paths for pytest results and QA evaluation report
PYTEST_RESULTS_V1_FILE = REPORTS_DIR / "pytest_results_v1.txt"
QA_EVALUATION_V1_FILE = REPORTS_DIR / "qa_evaluation_v1.md"
# Path for refined tests (Version 2)
REFINED_TEST_FILE = TESTS_DIR / "test_order_service_v2.py"
PYTEST_RESULTS_V2_FILE = REPORTS_DIR / "pytest_results_v2.txt"
# Path for the final evaluation report
FINAL_EVALUATION_FILE = REPORTS_DIR / "final_evaluation.md"

def run_code_review():
    """
    Step 1: Generate the initial code review (V1).
    """

    # Ask the Code Review Agent to analyze the source code
    review_report = review_code(SOURCE_FILE)

    # Save the initial review for future workflow steps
    REPORTS_DIR.mkdir(exist_ok=True)
    REVIEW_V1_FILE.write_text(review_report, encoding="utf-8")

    print("\n=== CODE REVIEW V1 ===\n")
    print(review_report)
    print(f"\nSaved to: {REVIEW_V1_FILE}")


def run_reflection():
    """
    Step 2: Reflect on the existing V1 code review.
    """

    # Make sure the previous workflow output exists
    if not REVIEW_V1_FILE.exists():
        print("V1 review not found. Run the review step first.")
        return

    # Ask the Reflection Agent to evaluate the existing review
    reflection_feedback = reflect_on_review(
        SOURCE_FILE,
        REVIEW_V1_FILE
    )

    # Save the reflection feedback for the refinement step
    REPORTS_DIR.mkdir(exist_ok=True)
    REFLECTION_FILE.write_text(reflection_feedback, encoding="utf-8")

    print("\n=== CODE REVIEW REFLECTION ===\n")
    print(reflection_feedback)
    print(f"\nSaved to: {REFLECTION_FILE}")


def run_refinement():
    """
    Step 3: Generate an improved code review (V2)
    using the initial review and reflection feedback.
    """

    # Check that the required previous reports exist
    if not REVIEW_V1_FILE.exists() or not REFLECTION_FILE.exists():
        print("Missing V1 review or reflection report.")
        print("Run the previous workflow steps first.")
        return

    # Run the Refinement Agent
    refined_report = refine_code_review(
        SOURCE_FILE,
        REVIEW_V1_FILE,
        REFLECTION_FILE
    )

    # Create the reports directory if needed
    REPORTS_DIR.mkdir(exist_ok=True)

    # Save the improved review as V2
    REVIEW_V2_FILE.write_text(refined_report, encoding="utf-8")

    # Display the result in the terminal
    print("\n=== CODE REVIEW V2 ===\n")
    print(refined_report)
    print(f"\nSaved to: {REVIEW_V2_FILE}")



def run_test_generation():
    """
    Step 4: Generate pytest unit tests using the Writer Agent.

    The agent reads the original source code and refined review (V2).
    The orchestrator saves the generated Python tests.
    """

    # Check that the refined code review exists
    if not REVIEW_V2_FILE.exists():
        print("Code Review V2 not found. Run refinement first.")
        return

    # Ask the Writer Agent to generate pytest tests
    generated_tests = generate_tests(
        SOURCE_FILE,
        REVIEW_V2_FILE
    )

    # Create the tests directory if it does not exist
    TESTS_DIR.mkdir(exist_ok=True)

    # Avoid overwriting an existing test file
    if GENERATED_TEST_FILE.exists():
        print(f"Test file already exists: {GENERATED_TEST_FILE}")
        print("Generation was not saved to avoid overwriting existing tests.")
        return

    # Save the generated tests to a Python file
    GENERATED_TEST_FILE.write_text(generated_tests, encoding="utf-8")

    # Display the generated test code
    print("\n=== GENERATED PYTEST TESTS ===\n")
    print(generated_tests)
    print(f"\nSaved to: {GENERATED_TEST_FILE}")



def run_qa_evaluation():
    """
    Step 5: Evaluate generated tests using real pytest feedback.

    The Editor Agent analyzes the tests and execution results.
    It does not modify production code or test files.
    """

    # Check that all required files exist
    required_files = [
        Path(SOURCE_FILE),
        REVIEW_V2_FILE,
        GENERATED_TEST_FILE,
        PYTEST_RESULTS_V1_FILE
    ]

    for file_path in required_files:
        if not file_path.exists():
            print(f"Required file not found: {file_path}")
            return

    # Run the QA Evaluation Agent (Editor)
    evaluation_report = evaluate_tests(
        SOURCE_FILE,
        REVIEW_V2_FILE,
        GENERATED_TEST_FILE,
        PYTEST_RESULTS_V1_FILE
    )

    # Save the evaluation report
    REPORTS_DIR.mkdir(exist_ok=True)
    QA_EVALUATION_V1_FILE.write_text(
        evaluation_report,
        encoding="utf-8"
    )

    # Display the evaluation feedback
    print("\n=== QA EVALUATION V1 ===\n")
    print(evaluation_report)
    print(f"\nSaved to: {QA_EVALUATION_V1_FILE}")



def run_test_refinement():
    """
    Step 6: Generate Test V2 using QA evaluation feedback.

    Preserves Test V1 and does not modify production code.
    """

    # Check required input files
    required_files = [
        Path(SOURCE_FILE),
        GENERATED_TEST_FILE,
        QA_EVALUATION_V1_FILE
    ]

    for file_path in required_files:
        if not file_path.exists():
            print(f"Required file not found: {file_path}")
            return

    # Prevent overwriting an existing Test V2
    if REFINED_TEST_FILE.exists():
        print(f"Test V2 already exists: {REFINED_TEST_FILE}")
        return

    # Ask the Test Refinement Agent to improve the tests
    refined_tests = refine_tests(
        SOURCE_FILE,
        GENERATED_TEST_FILE,
        QA_EVALUATION_V1_FILE
    )

    # Save the refined tests in a separate file
    TESTS_DIR.mkdir(exist_ok=True)
    REFINED_TEST_FILE.write_text(
        refined_tests,
        encoding="utf-8"
    )

    print("\n=== TEST REFINEMENT V2 ===\n")
    print(refined_tests)
    print(f"\nSaved to: {REFINED_TEST_FILE}")



def run_pytest_v2():
    """
    Step 7: Automatically execute Test V2 using pytest.

    This function:
    - Runs pytest as a subprocess.
    - Captures the actual execution results.
    - Saves results to a report file.
    - Does not modify production code.
    """

    # Check that the refined test file exists
    if not REFINED_TEST_FILE.exists():
        print(f"Test file not found: {REFINED_TEST_FILE}")
        return

    print("\n=== RUNNING PYTEST V2 ===\n")

    # Execute pytest using the current Python environment
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pytest",
            str(REFINED_TEST_FILE),
            "-v"
        ],
        capture_output=True,
        text=True,
        timeout=60
    )

    # Combine standard output and errors
    pytest_output = result.stdout + "\n" + result.stderr

    # Save the execution results
    REPORTS_DIR.mkdir(exist_ok=True)
    pytest_results_file = REPORTS_DIR / "pytest_results_v2.txt"

    pytest_results_file.write_text(
        pytest_output,
        encoding="utf-8"
    )

    # Display results in the terminal
    print(pytest_output)
    print(f"\nSaved to: {pytest_results_file}")

    if result.returncode == 0:
        print("All tests passed!")
    elif result.returncode == 1:
        print("Some tests failed.")
    else:
        print(f"pytest execution error: exit code {result.returncode}")


def run_step_if_needed(step_name, output_file, run_function):
    """
    Run a workflow step only if its output file does not exist.

    This prevents:
    - Unnecessary OpenAI API calls
    - Overwriting previous results
    - Losing human-reviewed feedback
    """

    if Path(output_file).exists():
        print(f"[SKIPPED] {step_name}: Output already exists.")
        return

    print(f"[RUNNING] {step_name}")

    run_function()

    if Path(output_file).exists():
        print(f"[COMPLETED] {step_name}")
    else:
        raise RuntimeError(
            f"{step_name} did not create its expected output: {output_file}"
        )


def run_full_workflow():
    """
    Run the complete AI-powered code review and testing workflow.

    Skip existing outputs to avoid unnecessary API calls
    and preserve previous reports and human feedback.
    """

    print("\n=== STARTING FULL WORKFLOW ===\n")

    # Step 1: Generate the initial code review
    run_step_if_needed(
        "Code Review V1",
        REVIEW_V1_FILE,
        run_code_review
    )

    # Step 2: Reflect on the initial review
    run_step_if_needed(
        "Reflection",
        REFLECTION_FILE,
        run_reflection
    )

    # Step 3: Refine the code review
    run_step_if_needed(
        "Code Review V2",
        REVIEW_V2_FILE,
        run_refinement
    )

    # Step 4: Generate the initial pytest tests
    run_step_if_needed(
        "Test Generation V1",
        GENERATED_TEST_FILE,
        run_test_generation
    )

    # Step 5: Automatically run pytest V1
    run_pytest_v1()

    # Step 6: Evaluate the generated tests
    run_step_if_needed(
        "QA Evaluation",
        QA_EVALUATION_V1_FILE,
        run_qa_evaluation
    )

    # Step 7: Refine tests using QA feedback
    run_step_if_needed(
        "Test Refinement V2",
        REFINED_TEST_FILE,
        run_test_refinement
    )

    # Step 8: Use existing pytest V2 results
    if PYTEST_RESULTS_V2_FILE.exists():
        print("[SKIPPED] pytest V2: Results already exist.")
    else:
        print("[RUNNING] pytest V2")
        run_pytest_v2()

    # Step 9: Generate the final evaluation report
    run_step_if_needed(
        "Final Evaluation",
        FINAL_EVALUATION_FILE,
        run_final_evaluation
    )

    print("\n=== FULL WORKFLOW COMPLETED ===\n")


def run_pytest_v1():
    """
    Automatically execute Test V1 and save pytest results.

    This step provides external feedback for the QA Evaluation Agent.
    """

    # Skip execution if results already exist
    if PYTEST_RESULTS_V1_FILE.exists():
        print("[SKIPPED] pytest V1: Results already exist.")
        return

    # Check that generated tests exist
    if not GENERATED_TEST_FILE.exists():
        raise FileNotFoundError(
            f"Test V1 file not found: {GENERATED_TEST_FILE}"
        )

    print("\n=== RUNNING PYTEST V1 ===\n")

    # Execute pytest using the current Python environment
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                str(GENERATED_TEST_FILE),
                "-v"
            ],
            capture_output=True,
            text=True,
            timeout=60
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("pytest V1 timed out.") from exc

    # Combine actual pytest output and errors
    pytest_output = result.stdout + "\n" + result.stderr

    # Stop if pytest could not execute correctly
    # Exit code 1 means tests ran but some failed.
    if result.returncode not in (0, 1):
        raise RuntimeError(
            f"pytest V1 execution error:\n{pytest_output}"
        )

    # Save external feedback
    REPORTS_DIR.mkdir(exist_ok=True)
    PYTEST_RESULTS_V1_FILE.write_text(
        pytest_output,
        encoding="utf-8"
    )

    print(pytest_output)
    print(f"\nSaved to: {PYTEST_RESULTS_V1_FILE}")


def run_final_evaluation():
    """
    Step 9: Generate the final developer evaluation report.

    Combines code review, QA feedback, and pytest results.
    Preserves all existing project artifacts.
    """

    # Skip if the final report already exists
    if FINAL_EVALUATION_FILE.exists():
        print("[SKIPPED] Final Evaluation: Report already exists.")
        return

    # Verify all required input files exist
    required_files = [
        Path(SOURCE_FILE),
        REVIEW_V2_FILE,
        QA_EVALUATION_V1_FILE,
        PYTEST_RESULTS_V1_FILE,
        PYTEST_RESULTS_V2_FILE
    ]

    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Required file not found: {file_path}"
            )

    # Ask the Final Evaluation Agent to generate the report
    final_report = generate_final_evaluation(
        SOURCE_FILE,
        REVIEW_V2_FILE,
        QA_EVALUATION_V1_FILE,
        PYTEST_RESULTS_V1_FILE,
        PYTEST_RESULTS_V2_FILE
    )

    # Save the final report
    REPORTS_DIR.mkdir(exist_ok=True)
    FINAL_EVALUATION_FILE.write_text(
        final_report,
        encoding="utf-8"
    )

    print("\n=== FINAL EVALUATION REPORT ===\n")
    print(final_report)
    print(f"\nSaved to: {FINAL_EVALUATION_FILE}")


def main():
    """
    Orchestrate the Agentic AI workflow.

    Each step can be executed independently.
    """

    # Read the workflow step selected by the user
    parser = argparse.ArgumentParser(
        description="AI-Powered PR Review & Test Automation Agent"
    )

    parser.add_argument(
        "--step",
        choices=["review", "reflection", "refinement", "test-generation", "qa-evaluation", "test-refinement", "pytest-v2", "all", "final-evaluation"],
        required=True,
        help="Choose which workflow step to execute"
    )

    args = parser.parse_args()

    # Execute only the requested workflow step
    if args.step == "review":
        run_code_review()

    elif args.step == "reflection":
        run_reflection()

    elif args.step == "refinement":
        run_refinement()

    elif args.step == "test-generation":
        run_test_generation()

    elif args.step == "qa-evaluation":
        run_qa_evaluation()

    elif args.step == "test-refinement":
        run_test_refinement()

    elif args.step == "pytest-v2":
        run_pytest_v2()

    elif args.step == "all":
        run_full_workflow()
    
    elif args.step == "final-evaluation":
        run_final_evaluation()


if __name__ == "__main__":
    main()
