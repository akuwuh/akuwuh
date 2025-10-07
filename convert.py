# braille_to_svg_uniform_spacing.py
# Uniform dot spacing horizontally (and vertically), so the gap within a cell
# equals the gap across cell boundaries.

from pathlib import Path

# ===== set once =====
SRC_PATH   = Path('/Users/cute/Documents/vsc/akuwuh/ascii.txt')
OUT_PATH   = Path('/Users/cute/Documents/vsc/akuwuh/.inline_braille.svg')

STEP_X     = 3.0        # horizontal cell width (kept for overall layout)
Y_RATIO    = 2.0        # vertical cell height relative to STEP_X (1.0 = square)
SCALE      = 2.0        # pixel scale
WIDTH_ATTR = "460"      # SVG width attribute (e.g., "460" or "100%")
FILL       = "currentColor"

DOT_SIZE   = 0.35       # dot radius as a fraction of the smaller spacing (0..1)
# =====================

# 2x4 braille dot layout per unicode U+2800..U+28FF (bit order)
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

    # Derive vertical metrics from horizontal
    step_x = STEP_X
    step_y = STEP_X * Y_RATIO

    # Uniform spacing:
    #  - horizontally: two columns per cell => spacing_x = step_x / 2
    #  - vertically:   four rows per cell   => spacing_y = step_y / 4
    spacing_x = step_x / 2.0
    spacing_y = step_y / 4.0

    # Place the two columns at 25% and 75% of the cell width so
    # gap_inside_cell == gap_across_cells == spacing_x
    cx_base = {0: step_x * 0.25, 1: step_x * 0.75}
    # Place the four rows at 1/8, 3/8, 5/8, 7/8 of the cell height
    cy_base = {row: step_y * (row * 2 + 1) / 8.0 for row in range(4)}

    # Dot radius: tied to the smaller of the two spacings so dots never touch
    r = min(spacing_x, spacing_y) * DOT_SIZE

    circles = []
    for y, raw in enumerate(lines):
        line = raw.ljust(num_cols, " ")
        for x, ch in enumerate(line):
            code = ord(ch)
            if 0x2800 <= code <= 0x28FF:
                bits = code - 0x2800
                for bit_index, (dx, dy) in enumerate(DOT_OFFSETS):
                    if bits & (1 << bit_index):
                        cx = (x * step_x + cx_base[dx]) * SCALE
                        cy = (y * step_y + cy_base[dy]) * SCALE
                        circles.append(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r*SCALE:.3f}"/>')
            # other chars (including spaces) render nothing

    width = num_cols * step_x * SCALE
    height = num_rows * step_y * SCALE

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:.3f} {height:.3f}" '
        f'width="{WIDTH_ATTR}" fill="{FILL}" preserveAspectRatio="xMidYMid meet">'
        + "".join(circles)
        + "</svg>"
    )
    return svg

def main():
    text = SRC_PATH.read_text(encoding="utf-8")
    svg = braille_text_to_svg(text)
    OUT_PATH.write_text(svg, encoding="utf-8")
    print("WROTE", OUT_PATH, "bytes:", len(svg))

if __name__ == "__main__":
    main()
