"""Render a lightweight dashboard preview PNG for the README."""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def main() -> None:
    fleet_path = PROJECT_ROOT / "data" / "processed" / "fleet_latest_predictions.csv"
    if not fleet_path.exists():
        sys.exit("Run scripts/train_model.py before rendering the preview.")
    fleet = pd.read_csv(fleet_path).sort_values(["failure_risk", "predicted_rul"])
    image = Image.new("RGB", (1280, 760), "#f3f6fa")
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 1280, 92), fill="#14213d")
    draw.text((42, 28), "AI Predictive Maintenance Deployment Toolkit", fill="#ffffff", font=font(30, bold=True))
    draw.text((42, 62), "Fleet RUL monitoring, intervention queue, and deployment governance", fill="#dce6f2", font=font(16))

    high = int((fleet["failure_risk"] == "high").sum())
    medium = int((fleet["failure_risk"] == "medium").sum())
    median_rul = float(fleet["predicted_rul"].median())
    metrics = [("Fleet assets", len(fleet), "#3d5a80"), ("High risk", high, "#d1495b"), ("Medium risk", medium, "#edae49"), ("Median RUL", f"{median_rul:.1f}", "#2a9d8f")]
    for idx, (label, value, color) in enumerate(metrics):
        x = 42 + idx * 273
        draw.rounded_rectangle((x, 125, x + 245, 230), radius=8, fill="#ffffff", outline="#d7dee8")
        draw.rectangle((x, 125, x + 5, 230), fill=color)
        draw.text((x + 22, 150), label, fill="#516070", font=font(18))
        draw.text((x + 22, 185), str(value), fill="#17202a", font=font(30, bold=True))

    output_path = PROJECT_ROOT / "docs" / "assets" / "dashboard_preview.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
