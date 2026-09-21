from backend.validation.validator import Validator


def main():

    print("\n==============================")
    print(" VALIDATOR TEST")
    print("==============================")

    validator = Validator()

    document_text = """
    Cooling Water Pump P-101 was inspected.

    Abnormal vibration of approximately 4.8 mm/s
    was recorded during operation.
    """

    good_output = """
    Subject: Approval Note

    Equipment: Cooling Water Pump P-101

    Inspection Findings:
    Minor leakage was observed near the mechanical seal.
    Abnormal vibration of approximately 4.8 mm/s was recorded.

    Recommended Actions:
    Replacement of the mechanical seal.
    Correction of coupling alignment.

    Requested Approval:
    Approval is requested to proceed with the recommended
    corrective actions.

    Supporting Documents:
    Inspection Report IR-2026-001
    """

    result = validator.validate(
        output=good_output,
        document_text=document_text
    )

    print("\nValidation Result:")
    print("--------------------------------")

    print("Passed:", result["passed"])

    print("\nChecks:")

    for check, value in result["checks"].items():
        print(f"- {check}: {value}")

    print("\nValidator test successful.")


if __name__ == "__main__":
    main()