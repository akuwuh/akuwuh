# braille_to_svg_uniform_spacing.py
# Converts a block of Unicode braille (U+2800–U+28FF) to an SVG of dots
# with *uniform pitch*: the gap inside each 2×4 cell equals the gap
# across neighbouring cells horizontally and vertically.

from pathlib import Path

# ========= defaults you can set once =========
SRC_PATH   = Path('/Users/cute/Documents/vsc/akuwuh/ascii.txt')
OUT_PATH   = Path('/Users/cute/Documents/vsc/akuwuh/.inline_braille.svg')

STEP_X     = 2.0        # cell width (in abstract grid units)
Y_RATIO    = 2.0        # cell height = STEP_X * Y_RATIO (2.0 keeps braille proportions)
SCALE      = 12.0       # px per grid unit (controls output size only)
WIDTH_ATTR = "100%"     # SVG width attribute
FILL       = "currentColor"

DOT_DIAM_RATIO = 0.48   # dot diameter as a fraction of pitch (≈ your screenshot)
                        # → radius = DOT_DIAM_RATIO / 2 of the smaller pitch
MARGIN_CELLS   = 0.0    # optional empty border (in cells) around the art
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

def braille_text_to_svg(text: str) -> str:
    lines = text.splitlines()
    num_rows = len(lines)
    num_cols = max((len(l) for l in lines), default=0)

    # Derived metrics
    step_x = float(STEP_X)
    step_y = float(STEP_X) * float(Y_RATIO)

    # Uniform pitch: 2 columns × 4 rows per cell
    spacing_x = step_x / 2.0
    spacing_y = step_y / 4.0

    # Column centers at 25% and 75% → same gap inside/between cells
    cx_base = {0: step_x * 0.25, 1: step_x * 0.75}
    # Row centers at 1/8, 3/8, 5/8, 7/8 of cell height
    cy_base = {row: step_y * (row * 2 + 1) / 8.0 for row in range(4)}

    # Dot radius from pitch (never larger than half the smaller pitch)
    r = min(spacing_x, spacing_y) * (DOT_DIAM_RATIO / 2.0)

    # Optional margin (empty cells all around)
    mx = MARGIN_CELLS * step_x
    my = MARGIN_CELLS * step_y

    circles = []
    for y, raw in enumerate(lines):
        line = raw.ljust(num_cols, " ")
        for x, ch in enumerate(line):
            code = ord(ch)
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

    width  = (num_cols * step_x + 2 * MARGIN_CELLS * step_x) * SCALE
    height = (num_rows * step_y + 2 * MARGIN_CELLS * step_y) * SCALE

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
