from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "media"
ENGINE = ROOT.parents[1] / "engine"
FONT_REG = ENGINE / "assets" / "fonts" / "NotoSans-Regular.ttf"
FONT_BOLD = ENGINE / "assets" / "fonts" / "NotoSans-Bold.ttf"


def font(size: int, bold: bool = False):
    return ImageFont.truetype(str(FONT_BOLD if bold else FONT_REG), size)


def context_image():
    w, h = 1600, 900
    im = Image.new("RGB", (w, h), "#0c1728")
    d = ImageDraw.Draw(im)
    for y in range(h):
        p = y / h
        d.line((0, y, w, y), fill=(12 + int(12 * p), 23 + int(18 * p), 40 + int(24 * p)))
    d.ellipse((1130, -260, 1770, 380), fill="#173e61")
    d.rectangle((0, 700, w, h), fill="#101b2d")
    d.polygon([(100, 765), (1420, 765), (1540, 900), (0, 900)], fill="#a9784d")
    d.rounded_rectangle((300, 150, 1320, 720), 35, fill="#17283e", outline="#5ba9ff", width=5)
    d.rounded_rectangle((345, 200, 1275, 650), 18, fill="#f7f9fc")
    d.text((390, 235), "Weekly service level", fill="#17283e", font=font(38, True))
    d.text((390, 290), "Percent within target", fill="#64748b", font=font(23))
    left, top, right, bottom = 430, 350, 1180, 575
    d.line((left, top, left, bottom, right, bottom), fill="#94a3b8", width=3)
    pts = [(480, 540), (630, 500), (780, 455), (930, 410), (1080, 350)]
    d.line(pts, fill="#3f8fe8", width=9, joint="curve")
    for x, y in pts:
        d.ellipse((x - 10, y - 10, x + 10, y + 10), fill="#3f8fe8")
    d.rectangle((770, 720, 850, 795), fill="#17283e")
    d.rounded_rectangle((650, 790, 970, 825), 16, fill="#17283e")
    d.rounded_rectangle((1080, 745, 1290, 805), 20, fill="#e8edf4")
    d.text((1125, 760), "FIELD NOTES", fill="#334155", font=font(22, True))
    d.line((1110, 820, 1320, 820), fill="#dde3ec", width=8)
    im.save(OUT / "analysis-context.png", optimize=True)


def dashboard_image():
    w, h = 1600, 900
    im = Image.new("RGB", (w, h), "#eef2f7")
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, 86), fill="#17283e")
    d.text((52, 22), "OPS PULSE", fill="#ffffff", font=font(30, True))
    d.text((1320, 27), "WEEK 18", fill="#b9c9dc", font=font(22, True))
    d.rounded_rectangle((55, 125, 1545, 845), 22, fill="#ffffff", outline="#cbd5e1", width=2)
    d.text((105, 170), "Checkout error rate", fill="#17283e", font=font(42, True))
    d.text((105, 225), "Percent of sessions · weekly view", fill="#64748b", font=font(26))
    d.rounded_rectangle((1215, 155, 1460, 225), 14, fill="#e9f4ff")
    d.text((1270, 177), "LAST 5 WEEKS", fill="#2d6fa8", font=font(20, True))
    left, top, right, bottom = 175, 320, 1430, 720
    for i, value in enumerate([0, 2, 4, 6, 8]):
        y = bottom - i * 90
        d.line((left, y, right, y), fill="#dbe3ed", width=2)
        d.text((105, y - 14), f"{value}%", fill="#64748b", font=font(22))
    weeks = ["APR 01", "APR 08", "APR 15", "APR 22", "APR 29"]
    vals = [2.0, 2.2, 7.1, 2.3, 2.4]
    pts = []
    for i, (label, value) in enumerate(zip(weeks, vals)):
        x = left + i * ((right - left) / 4)
        y = bottom - value / 8 * 360
        pts.append((x, y))
        d.text((x - 43, 750), label, fill="#64748b", font=font(19, True))
    d.line(pts, fill="#3f8fe8", width=8, joint="curve")
    for i, (x, y) in enumerate(pts):
        color = "#e25d6f" if i == 2 else "#3f8fe8"
        d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=color)
    d.text((760, 287), "WEEKLY ERROR RATE", fill="#475569", font=font(20, True))
    im.save(OUT / "operations-dashboard.png", optimize=True)


def comparison_charts():
    cases = {
        "trend-case.png": [18, 27, 39, 52, 66],
        "anomaly-case.png": [2.0, 2.2, 7.1, 2.3, 2.4],
    }
    for name, values in cases.items():
        w, h = 800, 330
        im = Image.new("RGB", (w, h), "#f7f9fc")
        d = ImageDraw.Draw(im)
        left, top, right, bottom = 70, 35, 745, 270
        d.line((left, top, left, bottom, right, bottom), fill="#94a3b8", width=3)
        high = max(values) * 1.12
        points = []
        for index, value in enumerate(values):
            x = left + index * ((right - left) / 4)
            y = bottom - value / high * (bottom - top)
            points.append((x, y))
        d.line(points, fill="#3f8fe8", width=8, joint="curve")
        for index, (x, y) in enumerate(points):
            color = "#e25d6f" if name.startswith("anomaly") and index == 2 else "#3f8fe8"
            d.ellipse((x - 10, y - 10, x + 10, y + 10), fill=color)
        im.save(OUT / name, optimize=True)


def trend_video():
    frames = OUT / ".trend-frames"
    shutil.rmtree(frames, ignore_errors=True)
    frames.mkdir(parents=True)
    w, h, fps, seconds = 1920, 1080, 30, 6
    values = [18, 27, 39, 52, 66]
    labels = ["W1", "W2", "W3", "W4", "W5"]
    for n in range(fps * seconds):
        im = Image.new("RGB", (w, h), "#0d1626")
        d = ImageDraw.Draw(im)
        d.text((150, 105), "A trend emerges across observations", fill="#f2f6fa", font=font(58, True))
        d.text((150, 188), "Weekly completion rate", fill="#a9b8ca", font=font(30))
        left, top, right, bottom = 250, 310, 1680, 850
        d.line((left, top, left, bottom, right, bottom), fill="#6c7d91", width=4)
        elapsed = n / fps
        visible = min(len(values), max(1, int(elapsed // 0.85) + 1))
        pts = []
        for i in range(visible):
            x = left + i * ((right - left) / 4)
            y = bottom - values[i] / 75 * (bottom - top)
            pts.append((x, y))
            d.ellipse((x - 13, y - 13, x + 13, y + 13), fill="#5ba9ff")
            d.text((x - 22, bottom + 35), labels[i], fill="#a9b8ca", font=font(25, True))
            d.text((x - 18, y - 62), str(values[i]), fill="#f2f6fa", font=font(25, True))
        if len(pts) > 1:
            d.line(pts, fill="#5ba9ff", width=9, joint="curve")
        if elapsed > 4.4:
            d.rounded_rectangle((1170, 205, 1660, 285), 18, fill="#143a38")
            d.text((1235, 224), "SUSTAINED DIRECTION", fill="#71d8b1", font=font(27, True))
        im.save(frames / f"f{n:04d}.png")
    subprocess.run(
        [
            "ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
            "-i", str(frames / "f%04d.png"), "-c:v", "libx264", "-preset", "veryfast",
            "-crf", "20", "-pix_fmt", "yuv420p", str(OUT / "trend-build-demo.mp4")
        ],
        check=True,
    )
    shutil.rmtree(frames)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    context_image()
    dashboard_image()
    comparison_charts()
    trend_video()
    print(f"Created reference media in {OUT}")
