"""Render a lightweight dashboard preview PNG for the README."""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        "C:/Windows/Fonts/msyhbd.ttc" if bold else "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    ]
    for candidate in candidates:
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    return ImageFont.load_default()


def rounded_rect(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill: str, outline: str = "#d7dee8") -> None:
    draw.rounded_rectangle(xy, radius=8, fill=fill, outline=outline, width=1)


def draw_metric(draw: ImageDraw.ImageDraw, xy: tuple[int, int], label: str, value: str, accent: str) -> None:
    x, y = xy
    rounded_rect(draw, (x, y, x + 245, y + 105), "#ffffff")
    draw.rectangle((x, y, x + 5, y + 105), fill=accent)
    draw.text((x + 22, y + 18), label, fill="#516070", font=font(18))
    draw.text((x + 22, y + 50), value, fill="#17202a", font=font(30, bold=True))


def main() -> None:
    fleet_path = PROJECT_ROOT / "data" / "processed" / "fleet_latest_predictions.csv"
    if not fleet_path.exists():
        sys.exit("Run scripts/train_model.py before rendering the preview.")
    fleet = pd.read_csv(fleet_path).sort_values(["failure_risk", "predicted_rul"])
    width, height = 1280, 760
    image = Image.new("RGB", (width, height), "#f3f6fa")
    draw = ImageDraw.Draw(image)

    draw.rectangle((0, 0, width, 92), fill="#14213d")
    draw.text((42, 18), "AI 预测性维护部署工具包", fill="#ffffff", font=font(30, bold=True))
    draw.text((42, 56), "AI Predictive Maintenance Deployment Toolkit", fill="#dce6f2", font=font(17))
    draw.text((560, 62), "RUL monitoring, intervention queue, governance / RUL 监控、维护队列、部署治理", fill="#dce6f2", font=font(14))

    high = int((fleet["failure_risk"] == "high").sum())
    medium = int((fleet["failure_risk"] == "medium").sum())
    median_rul = float(fleet["predicted_rul"].median())
    draw_metric(draw, (42, 125), "资产数量 / Fleet assets", f"{len(fleet):,}", "#3d5a80")
    draw_metric(draw, (315, 125), "高风险 / High risk", f"{high:,}", "#d1495b")
    draw_metric(draw, (588, 125), "中风险 / Medium risk", f"{medium:,}", "#edae49")
    draw_metric(draw, (861, 125), "RUL 中位数 / Median RUL", f"{median_rul:.1f}", "#2a9d8f")

    rounded_rect(draw, (42, 265, 760, 700), "#ffffff")
    draw.text((66, 290), "维护干预队列 / Maintenance Intervention Queue", fill="#17202a", font=font(23, bold=True))
    header_y = 335
    headers = ["设备", "周期", "预测 RUL", "风险", "维护建议 / Action"]
    xs = [66, 144, 235, 350, 457]
    for x, header in zip(xs, headers):
        draw.text((x, header_y), header, fill="#516070", font=font(16, bold=True))
    y = 372
    risk_colors = {"high": "#d1495b", "medium": "#edae49", "low": "#2a9d8f"}
    for _, row in fleet.head(10).iterrows():
        draw.line((66, y - 10, 735, y - 10), fill="#edf1f5", width=1)
        risk = row["failure_risk"]
        draw.text((66, y), str(int(row["unit_id"])), fill="#17202a", font=font(16))
        draw.text((144, y), str(int(row["cycle"])), fill="#17202a", font=font(16))
        draw.text((235, y), f"{float(row['predicted_rul']):.1f}", fill="#17202a", font=font(16))
        draw.rounded_rectangle((350, y - 2, 433, y + 23), radius=6, fill=risk_colors.get(risk, "#6c757d"))
        risk_label = {"high": "高 / HIGH", "medium": "中 / MED", "low": "低 / LOW"}.get(risk, risk.upper())
        draw.text((361, y + 1), risk_label, fill="#ffffff", font=font(13, bold=True))
        action = {
            "Plan intervention in next maintenance window": "下个维护窗口安排干预",
            "Inspect and monitor trend weekly": "每周检查并跟踪趋势",
            "Continue routine monitoring": "继续常规监控",
        }.get(str(row["maintenance_action"]), str(row["maintenance_action"]))
        draw.text((457, y), action, fill="#17202a", font=font(15))
        y += 32

    rounded_rect(draw, (800, 265, 1238, 700), "#ffffff")
    draw.text((824, 288), "各设备预测 RUL", fill="#17202a", font=font(22, bold=True))
    draw.text((824, 318), "Predicted RUL by Asset", fill="#516070", font=font(17, bold=True))
    chart_left, chart_top, chart_right, chart_bottom = 835, 345, 1208, 650
    draw.line((chart_left, chart_bottom, chart_right, chart_bottom), fill="#ccd4dd", width=2)
    draw.line((chart_left, chart_top, chart_left, chart_bottom), fill="#ccd4dd", width=2)
    subset = fleet.head(14).copy()
    max_value = max(125, float(subset["predicted_rul"].max()))
    bar_gap = 6
    bar_width = int((chart_right - chart_left - bar_gap * (len(subset) - 1)) / len(subset))
    for idx, (_, row) in enumerate(subset.iterrows()):
        value = float(row["predicted_rul"])
        bar_height = int((value / max_value) * (chart_bottom - chart_top - 20))
        x0 = chart_left + idx * (bar_width + bar_gap)
        y0 = chart_bottom - bar_height
        color = risk_colors.get(row["failure_risk"], "#6c757d")
        draw.rectangle((x0, y0, x0 + bar_width, chart_bottom), fill=color)
    draw.text((835, 665), "柱子越低，越需要优先关注 / Lower bars need earlier attention", fill="#516070", font=font(14))

    output_path = PROJECT_ROOT / "docs" / "assets" / "dashboard_preview.png"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
