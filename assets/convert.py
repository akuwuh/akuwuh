# braille_to_svg_asymmetric_pitch.py
# Convert Unicode braille (U+2800–U+28FF) to an SVG of dots where the
# spacing *inside a cell* can differ slightly from the spacing *between cells*
# (both horizontally and vertically). Also trims empty padding rows/cols.

from pathlib import Path

# ========= tweak these defaults =========
SRC_PATH   = Path('/Users/cute/Documents/vsc/akuwuh/ascii.txt')
OUT_PATH   = Path('/Users/cute/Documents/vsc/akuwuh/.inline_braille.svg')

STEP_X     = 2.0     # cell width in abstract units (controls overall width)
Y_RATIO    = 1.0     # cell height = STEP_X * Y_RATIO (1.0 = square pitch)
SCALE      = 12.0    # pixels per abstract unit (output size only)
WIDTH_ATTR = "100%"  # SVG width attribute
FILL       = "currentColor"

# --- Asymmetric pitch controls ---
# m_x_ratio, m_y_ratio define the margin from the cell edges to the first/last
# dot centers. They directly control the *between-cells* gap:
#   inter_gap_x = 2 * m_x,    intra_gap_x = STEP_X - 2 * m_x
#   inter_gap_y = 2 * m_y,    intra_gap_y = (STEP_Y - 2 * m_y) / 3
# For *uniform* pitch use 0.25 and 1/8 (0.125) respectively.
# To make the between-cell gap slightly larger than within-cell, increase them a bit.
MARGIN_X_RATIO = 0.28   # was 0.25; >0.25 -> wider gap between cells than within
MARGIN_Y_RATIO = 0.150  # was 0.125; >0.125 -> wider vertical gap between cells

DOT_DIAM_RATIO = 0.48   # dot diameter as a fraction of the *smallest* gap
                        # (keeps dots from touching even in tightest direction)
# =======================================
# 2×4 braille bit order (U+2800 base)
DOT_OFFSETS = [
    (0, 0), (0, 1), (0, 2), (1, 0),
    (1, 1), (1, 2), (0, 3), (1, 3),
]

def trim_braille_rect(lines: list[str]) -> tuple[list[str], int, int]:
    """Trim empty rows/cols (only spaces or U+2800). Returns (trimmed, left, top)."""
    if not lines:
        return [], 0, 0

    n_rows = len(lines)
    n_cols = max(len(l) for l in lines) if lines else 0
    pad   = lambda s, w: s + " " * (w - len(s))

    # quick helpers
    def is_blank_ch(ch: str) -> bool:
        return ch == " " or ord(ch) == 0x2800

    # find top
    top = 0
    while top < n_rows and all(is_blank_ch(c) for c in pad(lines[top], n_cols)):
        top += 1
    # find bottom
    bottom = n_rows - 1
    while bottom >= top and all(is_blank_ch(c) for c in pad(lines[bottom], n_cols)):
        bottom -= 1
    if top > bottom:
        return [], 0, 0

    # find left/right
    left = 0
    right = n_cols - 1
    # left
    while left <= right:
        if all(is_blank_ch(pad(lines[r], n_cols)[left]) for r in range(top, bottom + 1)):
            left += 1
        else:
            break
    # right
    while right >= left:
        if all(is_blank_ch(pad(lines[r], n_cols)[right]) for r in range(top, bottom + 1)):
            right -= 1
        else:
            break

    trimmed = [pad(lines[r], n_cols)[left:right+1] for r in range(top, bottom + 1)]
    return trimmed, left, top

def braille_text_to_svg(text: str) -> str:
    raw_lines = text.splitlines()
    lines, _, _ = trim_braille_rect(raw_lines)
    num_rows = len(lines)
    num_cols = max((len(l) for l in lines), default=0)
    if num_rows == 0 or num_cols == 0:
        return '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 0 0" width="0"></svg>'

    step_x = float(STEP_X)
    step_y = float(STEP_X) * float(Y_RATIO)

    # Asymmetric pitch parameters
    m_x = step_x * float(MARGIN_X_RATIO)               # margin from cell edge to first/last column center
    m_y = step_y * float(MARGIN_Y_RATIO)               # margin from cell edge to first/last row center
    intra_gap_x = step_x - 2.0 * m_x                   # inside-cell gap horizontally
    inter_gap_x = 2.0 * m_x                            # between-cells gap horizontally
    intra_gap_y = (step_y - 2.0 * m_y) / 3.0           # inside-cell gap vertically
    inter_gap_y = 2.0 * m_y                            # between-cells gap vertically

    # Column centers (left/right) and row centers (4 rows)
    cx_base = {0: m_x, 1: step_x - m_x}
    cy_base = {i: m_y + i * intra_gap_y for i in range(4)}

    # Choose radius from the tightest gap (so circles never touch)
    smallest_gap = min(intra_gap_x, inter_gap_x, intra_gap_y, inter_gap_y)
    r = smallest_gap * (DOT_DIAM_RATIO / 2.0)

    circles: list[str] = []
    for y, raw in enumerate(lines):
        line = raw.ljust(num_cols, " ")
        for x, ch in enumerate(line):
            code = ord(ch)
            if 0x2800 <= code <= 0x28FF:
                bits = code - 0x2800
                if bits == 0:
                    continue
                base_x = x * step_x
                base_y = y * step_y
                for bit_index, (dx, dy) in enumerate(DOT_OFFSETS):
                    if bits & (1 << bit_index):
                        cx = (base_x + cx_base[dx]) * SCALE
                        cy = (base_y + cy_base[dy]) * SCALE
                        circles.append(f'<circle cx="{cx:.3f}" cy="{cy:.3f}" r="{r*SCALE:.3f}"/>')

    width  = (num_cols * step_x) * SCALE
    height = (num_rows * step_y) * SCALE

    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width:.3f} {height:.3f}" width="{WIDTH_ATTR}" '
        f'fill="{FILL}" shape-rendering="geometricPrecision" '
        f'preserveAspectRatio="xMidYMid meet">'
        + "".join(circles) +
        "</svg>"
    )
    return svg

def main():
    text = SRC_PATH.read_text(encoding="utf-8")
    svg = braille_text_to_svg(text)
    OUT_PATH.write_text(svg, encoding="utf-8")
    print("WROTE", OUT_PATH, "bytes:", len(svg))

if __name__ == "__main__":
    main()
