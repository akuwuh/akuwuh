# braille_to_svg_uniform_spacing_trimmed.py
# Converts a block of Unicode braille (U+2800–U+28FF) to a tightly-cropped SVG
# with *uniform pitch*: the gap inside each 2×4 cell equals the gap across
# neighbouring cells horizontally and vertically. Leading/trailing blank rows
# and columns are removed automatically.

from pathlib import Path
from typing import List, Tuple

# ========= defaults you can set once =========
SRC_PATH   = Path('/Users/cute/Documents/vsc/akuwuh/assets/ascii.txt')
OUT_PATH   = Path('/Users/cute/Documents/vsc/akuwuh/assets/.inline_braille.svg')

STEP_X     = 2.0        # cell width (in abstract grid units)
Y_RATIO    = 2.0        # cell height = STEP_X * Y_RATIO (2.0 keeps braille proportions)
SCALE      = 12.0       # px per grid unit (controls output size only)
WIDTH_ATTR = "100%"     # SVG width attribute
FILL       = "white"

DOT_DIAM_RATIO = 0.48   # dot diameter as a fraction of pitch (≈ your screenshot)
MARGIN_CELLS   = 0.0    # optional empty border (in cells) around the trimmed art
# ============================================

# 2×4 braille bit order (U+2800 base)
DOT_OFFSETS = [
    (0, 0),  # dot 1
    (0, 1),  # dot 2
    (0, 2),  # dot 3
    (1, 0),  # dot 4
    (1, 1),  # dot 5
    (1, 2),  # dot 6
    (0, 3),  # dot 7
    (1, 3),  # dot 8
]

def is_braille_dot(ch: str) -> bool:
    """True if ch is a braille char with any dot set (not U+2800 blank)."""
    if not ch:
        return False
    code = ord(ch)
    if 0x2800 <= code <= 0x28FF:
        return (code - 0x2800) != 0
    return False

def find_trim_bounds(lines: List[str]) -> Tuple[int, int, int, int]:
    """
    Return (row_start, row_end_excl, col_start, col_end_excl) that tightly
    bounds any real braille dots. If no dots, returns (0, 0, 0, 0).
    """
    num_rows = len(lines)
    num_cols = max((len(l) for l in lines), default=0)

    min_r, max_r = num_rows, -1
    min_c, max_c = num_cols, -1

    for r, line in enumerate(lines):
        # Scan only actual characters; missing tail is blank
        for c in range(len(line)):
            if is_braille_dot(line[c]):
                if r < min_r: min_r = r
                if r > max_r: max_r = r
                if c < min_c: min_c = c
                if c > max_c: max_c = c

    if max_r == -1:  # no dots
        return 0, 0, 0, 0

    return min_r, max_r + 1, min_c, max_c + 1

def braille_text_to_svg(text: str) -> str:
    lines = text.splitlines()

    r0, r1, c0, c1 = find_trim_bounds(lines)
    if r1 == r0 or c1 == c0:
        # No dots → minimal empty SVG
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1" '
            f'width="{WIDTH_ATTR}" fill="{FILL}" preserveAspectRatio="xMidYMid meet"/>'
        )

    # Crop logical grid to bounds
    cropped = [line[c0:c1] for line in lines[r0:r1]]
    rows = len(cropped)
    cols = max((len(l) for l in cropped), default=0)

    # Derived metrics
    step_x = float(STEP_X)
    step_y = float(STEP_X) * float(Y_RATIO)

    # Uniform pitch (2×4 per cell)
    spacing_x = step_x / 2.0
    spacing_y = step_y / 4.0

    # Dot centers (uniform gaps in/out of cells)
    cx_base = {0: step_x * 0.25, 1: step_x * 0.75}
    cy_base = {row: step_y * (row * 2 + 1) / 8.0 for row in range(4)}

    # Dot radius from pitch
    r = min(spacing_x, spacing_y) * (DOT_DIAM_RATIO / 2.0)

    # Optional margin
    mx = MARGIN_CELLS * step_x
    my = MARGIN_CELLS * step_y

    circles = []
    for y, raw in enumerate(cropped):
        line = raw.ljust(cols, " ")  # normalize row width for consistent layout
        for x, ch in enumerate(line):
            code = ord(ch) if x < len(raw) else 0
            if 0x2800 <= code <= 0x28FF:
                bits = code - 0x2800
                if bits == 0:
                    continue
                base_x = mx + x * step_x
                base_y = my + y * step_y
                for bit_index, (dx, dy) in enumerate(DOT_OFFSETS):
                    if bits & (1 << bit_index):
                        cx = (base_x + cx_base[dx]) * SCALE
                        cy = (base_y + cy_base[dy]) * SCALE
                        circles.append(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r*SCALE:.3f}"/>')

    width  = (cols * step_x + 2 * MARGIN_CELLS * step_x) * SCALE
    height = (rows * step_y + 2 * MARGIN_CELLS * step_y) * SCALE

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width:.3f} {height:.3f}" width="{WIDTH_ATTR}" '
        f'fill="{FILL}" shape-rendering="geometricPrecision" '
        f'preserveAspectRatio="xMidYMid meet">'
        + "".join(circles) +
        '</svg>'
    )
    return svg

def main():
    text = SRC_PATH.read_text(encoding="utf-8")
    svg = braille_text_to_svg(text)
    OUT_PATH.write_text(svg, encoding="utf-8")
    print("WROTE", OUT_PATH, "bytes:", len(svg))

if __name__ == "__main__":
    main()
