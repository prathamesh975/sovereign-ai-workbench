from backend.models.llm_generator import LLMGenerator


def main():

    print("\n==============================")
    print(" LLM GENERATOR TEST")
    print("==============================")

    generator = LLMGenerator()

    prompt = """
You are an assistant for a confidential industrial organization.

Prepare a professional approval note using ONLY the information
provided below.

INSPECTION REPORT:
Report ID: IR-2026-001
Equipment: Cooling Water Pump P-101
Inspection Date: 28-Aug-2026
Department: Maintenance

Findings:
1. Minor leakage was observed near the mechanical seal.
2. Abnormal vibration of approximately 4.8 mm/s was recorded.
3. Coupling alignment requires correction.
4. No visible cracks were observed on the pump casing.

Recommended actions:
1. Replace the mechanical seal.
2. Correct coupling alignment.
3. Perform follow-up vibration measurement.
4. Monitor the equipment until corrective maintenance is completed.

Write a concise professional approval note.
Do not invent information.
"""

    print("\nSending request to local Qwen model...")

    result = generator.generate(prompt)

    print("\nGenerated approval note:")
    print("--------------------------------")
    print(result)
    print("--------------------------------")

    print("\nLLM generation successful.")


if __name__ == "__main__":
    main()