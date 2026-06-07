"""Generates assets/dash-pet.gif - a Claude Code style idle animation."""
from PIL import Image
import copy
import os

SCALE = 6
SIZE = 16
CANVAS_H = SIZE + 1  # +1 row for bounce
GAP = 3

TEXT = "CODING"
TEXT_SCALE = 2
TEXT_Y = 1
TEXT_SPACING = 1
TEXT_PIXEL_H = 7

TRANSPARENT = (0, 0, 0, 0)
BODY = (255, 169, 41, 255)  # #ffa929
DARK = (200, 120, 20, 255)
EYE = (60, 35, 10, 255)
TEXT_COLOR = BODY
TEXT_SHADOW = (120, 67, 20, 255)
SHINE = (255, 255, 255, 255)

COLOR = {0: TRANSPARENT, 1: BODY, 2: DARK, 3: EYE}

FONT = {
    "C": [
        "01110",
        "10001",
        "10000",
        "10000",
        "10000",
        "10001",
        "01110",
    ],
    "D": [
        "11110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "11110",
    ],
    "G": [
        "01110",
        "10001",
        "10000",
        "10111",
        "10001",
        "10001",
        "01110",
    ],
    "I": [
        "111",
        "010",
        "010",
        "010",
        "010",
        "010",
        "111",
    ],
    "N": [
        "10001",
        "11001",
        "10101",
        "10011",
        "10001",
        "10001",
        "10001",
    ],
    "O": [
        "01110",
        "10001",
        "10001",
        "10001",
        "10001",
        "10001",
        "01110",
    ],
}

TEXT_PIXEL_W = sum(len(FONT[ch][0]) for ch in TEXT) + TEXT_SPACING * (len(TEXT) - 1)
CANVAS_W = SIZE + GAP + TEXT_PIXEL_W * TEXT_SCALE + 1

BASE = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 3, 3, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 0],
    [0, 1, 1, 3, 3, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

BLINK_HALF = copy.deepcopy(BASE)
BLINK_HALF[6] = [0, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 0]
BLINK_HALF[7] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]

BLINK_FULL = copy.deepcopy(BASE)
BLINK_FULL[6] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]
BLINK_FULL[7] = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]


def fill_pixel(img, x, y, size, color):
    pix = img.load()
    for dy in range(size):
        for dx in range(size):
            pix[x + dx, y + dy] = color


def draw_coding_text(img, shine_x):
    start_x = (SIZE + GAP) * SCALE
    start_y = TEXT_Y * SCALE
    pixel = TEXT_SCALE * SCALE
    cursor_x = start_x

    for ch in TEXT:
        glyph = FONT[ch]
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit == "1":
                    fill_pixel(img, cursor_x + gx * pixel + SCALE, start_y + gy * pixel + SCALE, pixel, TEXT_SHADOW)
        cursor_x += (len(glyph[0]) + TEXT_SPACING) * pixel

    cursor_x = start_x
    for ch in TEXT:
        glyph = FONT[ch]
        for gy, row in enumerate(glyph):
            for gx, bit in enumerate(row):
                if bit != "1":
                    continue

                x = cursor_x + gx * pixel
                y = start_y + gy * pixel
                text_x = (x - start_x) // SCALE
                text_y = (y - start_y) // SCALE
                slash_distance = abs((text_x - text_y) - shine_x)
                color = SHINE if slash_distance <= 2 else TEXT_COLOR
                fill_pixel(img, x, y, pixel, color)
        cursor_x += (len(glyph[0]) + TEXT_SPACING) * pixel


def render(grid, y_off=0, shine_x=0):
    img = Image.new("RGBA", (CANVAS_W * SCALE, CANVAS_H * SCALE), TRANSPARENT)
    pix = img.load()
    for gy, row in enumerate(grid):
        y = gy + y_off
        if y < 0 or y >= CANVAS_H:
            continue
        for gx, c in enumerate(row):
            col = COLOR.get(c, TRANSPARENT)
            if col == TRANSPARENT:
                continue
            px, py = gx * SCALE, y * SCALE
            for dy in range(SCALE):
                for dx in range(SCALE):
                    pix[px + dx, py + dy] = col
    draw_coding_text(img, shine_x)
    return img


# (grid, y_off, duration_ms)
FRAMES = [
    (BASE, 0, 180),
    (BASE, 0, 180),
    (BASE, 1, 180),
    (BASE, 0, 180),
    (BASE, 0, 120),
    (BLINK_HALF, 0, 70),
    (BLINK_FULL, 0, 70),
    (BLINK_HALF, 0, 70),
    (BASE, 0, 180),
    (BASE, 1, 180),
    (BASE, 0, 180),
    (BASE, 0, 350),
]

os.makedirs("assets", exist_ok=True)

shine_span = TEXT_PIXEL_W * TEXT_SCALE + TEXT_PIXEL_H * TEXT_SCALE + 8
frames = [
    render(g, y, -TEXT_PIXEL_H * TEXT_SCALE + round(i * shine_span / len(FRAMES)))
    for i, (g, y, _) in enumerate(FRAMES)
]
durations = [d for _, _, d in FRAMES]

frames[0].save(
    "assets/dash-pet.gif",
    save_all=True,
    append_images=frames[1:],
    duration=durations,
    loop=0,
    transparency=0,
    disposal=2,
    optimize=False,
)
print(f"Saved assets/dash-pet.gif  ({CANVAS_W*SCALE}x{CANVAS_H*SCALE}px per frame, {len(FRAMES)} frames)")
