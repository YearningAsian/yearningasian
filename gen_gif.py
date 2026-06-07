"""Generates assets/claude-idle.gif — the Claude Code mascot idle animation."""
from PIL import Image
import os, copy

SCALE = 6
SIZE = 16
CANVAS_H = SIZE + 1  # +1 row for bounce

TRANSPARENT = (0, 0, 0, 0)
BODY  = (255, 169, 41,  255)   # #ffa929
DARK  = (200, 120, 20,  255)
EYE   = (60,  35,  10,  255)

COLOR = {0: TRANSPARENT, 1: BODY, 2: DARK, 3: EYE}

BASE = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0],
    [0,0,0,1,1,1,1,0,0,1,1,1,1,0,0,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,3,3,1,1,1,1,1,3,3,1,1,1,0],
    [0,1,1,3,3,1,1,1,1,1,3,3,1,1,1,0],
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,1,1,1,1,1,2,1,2,1,1,1,1,1,1,0],   # V mouth - arms (x=6, x=8)
    [0,1,1,1,1,1,1,2,1,1,1,1,1,1,1,0],   # V mouth - tip (x=7)
    [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
    [0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0],
    [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
    [0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
]

BLINK_HALF = copy.deepcopy(BASE)
BLINK_HALF[6] = [0,1,1,2,2,1,1,1,1,1,2,2,1,1,1,0]
BLINK_HALF[7] = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]

BLINK_FULL = copy.deepcopy(BASE)
BLINK_FULL[6] = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]
BLINK_FULL[7] = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0]


def render(grid, y_off=0):
    img = Image.new('RGBA', (SIZE * SCALE, CANVAS_H * SCALE), TRANSPARENT)
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
    return img


def to_gif_frame(img_rgba):
    """Convert RGBA -> palette 'P' image with index 0 = transparent."""
    img_rgb = img_rgba.convert('RGB')
    img_p = img_rgb.quantize(colors=255)

    data = bytearray(img_p.tobytes())
    for i in range(len(data)):
        data[i] = data[i] + 1  # shift 0-254 -> 1-255 to free index 0

    alpha = img_rgba.split()[3].tobytes()
    for i, a in enumerate(alpha):
        if a < 128:
            data[i] = 0  # transparent

    result = Image.frombytes('P', img_rgba.size, bytes(data))
    old_pal = img_p.getpalette()
    new_pal = [0, 0, 0] + old_pal[:255 * 3]
    result.putpalette(new_pal)
    return result


# (grid, y_off, duration_ms)
FRAMES = [
    (BASE,       0, 180),
    (BASE,       0, 180),
    (BASE,       1, 180),
    (BASE,       0, 180),
    (BASE,       0, 120),
    (BLINK_HALF, 0, 70),
    (BLINK_FULL, 0, 70),
    (BLINK_HALF, 0, 70),
    (BASE,       0, 180),
    (BASE,       1, 180),
    (BASE,       0, 180),
    (BASE,       0, 350),
]

os.makedirs('assets', exist_ok=True)

frames_p = [to_gif_frame(render(g, y)) for g, y, _ in FRAMES]
durations = [d for _, _, d in FRAMES]

frames_p[0].save(
    'assets/dash-pet.gif',
    save_all=True,
    append_images=frames_p[1:],
    duration=durations,
    loop=0,
    transparency=0,
    disposal=2,
)
print(f"Saved assets/claude-idle.gif  ({SIZE*SCALE}x{CANVAS_H*SCALE}px per frame, {len(FRAMES)} frames)")
