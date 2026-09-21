from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


OUTPUT_DIR = Path("inputs")
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "scanned_inspection.png"


def create_scan_image():

    width = 1400
    height = 1800

    image = Image.new(
        "RGB",
        (width, height),
        "white"
    )

    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(
            "arial.ttf",
            30
        )
    except OSError:
        font = ImageFont.load_default()

    text = """
INDUSTRIAL EQUIPMENT INSPECTION REPORT

Report ID: IR-2026-001
Equipment: Cooling Water Pump P-101
Inspection Date: 28-Aug-2026
Department: Maintenance

INSPECTION FINDINGS

1. Minor leakage was observed near the mechanical seal.

2. Abnormal vibration of approximately 4.8 mm/s
   was recorded during operation.

3. Coupling alignment was found to require correction.

4. No visible cracks were observed on the pump casing.

RECOMMENDATION

1. Replacement of the mechanical seal.
2. Correction of coupling alignment.
3. Follow-up vibration measurement after maintenance.

The equipment should be monitored until corrective
maintenance is completed.

INSPECTOR

Maintenance Department
Industrial Operations Division
"""

    draw.multiline_text(
        (80, 80),
        text,
        fill="black",
        font=font,
        spacing=15
    )

    image.save(OUTPUT_FILE)

    print(f"Created: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_scan_image()