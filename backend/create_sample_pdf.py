import pymupdf
from pathlib import Path


OUTPUT_DIR = Path("inputs")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "inspection_report.pdf"


def create_pdf():

    document = pymupdf.open()

    page = document.new_page()

    content = """
INDUSTRIAL EQUIPMENT INSPECTION REPORT

Report ID: IR-2026-001
Equipment: Cooling Water Pump P-101
Inspection Date: 28-Aug-2026
Department: Maintenance

----------------------------------------
INSPECTION FINDINGS
----------------------------------------

1. Minor leakage was observed near the mechanical seal.

2. Abnormal vibration of approximately 4.8 mm/s
   was recorded during operation.

3. Coupling alignment was found to require correction.

4. No visible cracks were observed on the pump casing.

----------------------------------------
RECOMMENDATION
----------------------------------------

The maintenance team recommends:

1. Replacement of the mechanical seal.
2. Correction of coupling alignment.
3. Follow-up vibration measurement after maintenance.

The equipment should be monitored until corrective
maintenance is completed.

----------------------------------------
INSPECTOR
----------------------------------------

Maintenance Department
Industrial Operations Division
"""

    page.insert_text(
        (72, 72),
        content,
        fontsize=11
    )

    document.save(OUTPUT_FILE)
    document.close()

    print(f"Created: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_pdf()