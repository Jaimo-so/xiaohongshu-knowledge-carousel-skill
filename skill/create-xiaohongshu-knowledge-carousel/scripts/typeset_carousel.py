#!/usr/bin/env python3
"""Deterministically typeset Chinese carousel pages from a JSON manifest."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    raise SystemExit(
        "Pillow is required. In Codex desktop, load workspace dependencies and run "
        "this script with the bundled Python executable."
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--only", action="append", default=[])
    parser.add_argument("--check-only", action="store_true")
    return parser.parse_args()


def load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size=size)


def fit_font(draw, text, path, max_size, min_size, max_width):
    for size in range(max_size, min_size - 1, -1):
        candidate = load_font(path, size)
        box = draw.textbbox((0, 0), text, font=candidate)
        if box[2] - box[0] <= max_width:
            return candidate
    return load_font(path, min_size)


def centered(draw, canvas_width, y, text, font, fill):
    box = draw.textbbox((0, 0), text, font=font)
    draw.text(((canvas_width - (box[2] - box[0])) / 2, y), text, font=font, fill=fill)


def panel(draw, box, fill, outline, width=4, radius=12):
    draw.rounded_rectangle(tuple(box), radius=radius, fill=fill, outline=outline, width=width)


def validate_manifest(data, root):
    if not isinstance(data.get("pages"), list) or not data["pages"]:
        raise ValueError("manifest.pages must be a non-empty list")
    ids = set()
    for page in data["pages"]:
        for key in ("id", "base", "output", "header", "body"):
            if key not in page:
                raise ValueError(f"page is missing {key}: {page}")
        if page["id"] in ids:
            raise ValueError(f"duplicate page id: {page['id']}")
        ids.add(page["id"])
        if not (root / page["base"]).exists():
            raise FileNotFoundError(root / page["base"])
        if not page["output"].endswith("-final.png"):
            raise ValueError(f"output must end with -final.png: {page['output']}")


def draw_corners(draw, width, height, fonts, corners):
    color = corners.get("color", "#25231F")
    fnt = load_font(fonts["latin"], 28)
    points = [
        (62, 46, corners.get("top_left", "")),
        (None, 46, corners.get("top_right", "")),
        (62, height - 69, corners.get("bottom_left", "")),
        (None, height - 69, corners.get("bottom_right", "")),
    ]
    for x, y, text in points:
        if not text:
            continue
        box = draw.textbbox((0, 0), text, font=fnt)
        if x is None:
            x = width - 62 - (box[2] - box[0])
        draw.text((x, y), text, font=fnt, fill=color)


def draw_header(draw, width, fonts, spec):
    box = spec.get("box", [38, 92, width - 38, 270])
    panel(draw, box, spec["fill"], spec.get("outline", "#25231F"))
    max_width = box[2] - box[0] - 70
    title_font = fit_font(draw, spec["title"], fonts["cn_bold"], 68, 42, max_width)
    centered(draw, width, box[1] + 20, spec["title"], title_font, spec["title_fill"])
    if spec.get("english"):
        english_font = fit_font(draw, spec["english"], fonts["latin"], 34, 22, max_width)
        centered(draw, width, box[1] + 121, spec["english"], english_font, spec["english_fill"])


def draw_lines_body(draw, width, fonts, spec):
    box = spec["box"]
    panel(draw, box, spec["fill"], spec.get("outline", "#25231F"))
    y = box[1] + spec.get("top_padding", 24)
    max_width = box[2] - box[0] - 60
    for line in spec["lines"]:
        if isinstance(line, str):
            line = {"text": line}
        path = fonts["cn_bold"] if line.get("bold") else fonts["cn_light"]
        size = line.get("size", 30)
        fnt = fit_font(draw, line["text"], path, size, max(20, size - 9), max_width)
        centered(draw, width, y, line["text"], fnt, line.get("fill", spec.get("text_fill", "#EFE4CC")))
        bounds = draw.textbbox((0, 0), line["text"], font=fnt)
        y += bounds[3] - bounds[1] + line.get("gap", spec.get("gap", 10))


def draw_grid_body(draw, fonts, spec):
    box = spec["box"]
    panel(draw, box, spec["fill"], spec.get("outline", "#287F98"))
    cards = spec["cards"]
    if len(cards) != 4:
        raise ValueError("grid body currently requires exactly four cards")
    pad, gutter = 20, 20
    inner_w = box[2] - box[0] - 2 * pad
    inner_h = box[3] - box[1] - 2 * pad
    card_w = (inner_w - gutter) // 2
    card_h = (inner_h - gutter) // 2
    positions = []
    for row in range(2):
        for col in range(2):
            x1 = box[0] + pad + col * (card_w + gutter)
            y1 = box[1] + pad + row * (card_h + gutter)
            positions.append([x1, y1, x1 + card_w, y1 + card_h])
    accents = ["#D65F45", "#E9BC2B", "#287F98", "#D65F45"]
    for card, card_box, accent in zip(cards, positions, accents):
        panel(draw, card_box, card.get("fill", "#F7EEDB"), card.get("outline", accent), width=3, radius=10)
        label = card["label"]
        label_font = fit_font(draw, label, fonts["cn_bold"], 29, 23, card_w - 36)
        draw.text((card_box[0] + 18, card_box[1] + 12), label, font=label_font, fill=card.get("label_fill", accent))
        y = card_box[1] + 54
        for text in card["text"]:
            body_font = fit_font(draw, text, fonts["cn_light"], 23, 18, card_w - 36)
            draw.text((card_box[0] + 18, y), text, font=body_font, fill=card.get("text_fill", "#25231F"))
            bounds = draw.textbbox((0, 0), text, font=body_font)
            y += bounds[3] - bounds[1] + 7


def render_page(page, root, output_dir, canvas, fonts, corners):
    base = Image.open(root / page["base"]).convert("RGB")
    base = base.resize(tuple(canvas), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(base)
    draw_header(draw, canvas[0], fonts, page["header"])
    body_type = page["body"].get("type", "lines")
    if body_type == "lines":
        draw_lines_body(draw, canvas[0], fonts, page["body"])
    elif body_type == "grid":
        draw_grid_body(draw, fonts, page["body"])
    else:
        raise ValueError(f"unknown body type: {body_type}")
    draw_corners(draw, canvas[0], canvas[1], fonts, page.get("corners", corners))
    output = output_dir / page["output"]
    output.parent.mkdir(parents=True, exist_ok=True)
    base.save(output, format="PNG", optimize=True)
    return output


def main():
    args = parse_args()
    manifest_path = args.manifest.resolve()
    root = manifest_path.parent
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    validate_manifest(data, root)
    selected = [p for p in data["pages"] if not args.only or p["id"] in args.only]
    if args.only and len(selected) != len(set(args.only)):
        missing = sorted(set(args.only) - {p["id"] for p in selected})
        raise ValueError(f"unknown --only page ids: {missing}")
    if args.check_only:
        print(f"Manifest OK: {len(selected)} page(s)")
        return
    output_dir = args.output_dir.resolve() if args.output_dir else root / "final"
    canvas = data.get("canvas", [1080, 1440])
    fonts = data["fonts"]
    outputs = [render_page(p, root, output_dir, canvas, fonts, data.get("corners", {})) for p in selected]
    for output in outputs:
        print(output)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
