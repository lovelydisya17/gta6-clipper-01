#!/usr/bin/env python3
"""Render the three original background stills for the gta6-clipper-01 Short.

Every pixel here is drawn from scratch with Pillow: a neon Vice City style
sunset, a night skyline, and a clean dark pitch card. No Rockstar footage,
audio, artwork, logos, or screenshots are used anywhere in this entry.

Usage: python3 scripts/render-clip.py <outdir>
Writes sunset.png, skyline.png and pitch.png (1080x1920 each) into <outdir>.
"""

import math
import os
import random
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(BOLD, size)


def vgrad(size, stops):
    """Vertical gradient through (position 0..1, (r, g, b)) stops."""
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        t = y / max(h - 1, 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i + 1]
            if p0 <= t <= p1:
                f = 0 if p1 == p0 else (t - p0) / (p1 - p0)
                col = tuple(int(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))
                break
        else:
            col = stops[-1][1]
        for x in range(w):
            px[x, y] = col
    return img


def text_center(draw, cx, y, line, size, fill, stroke=4, stroke_fill=(0, 0, 0),
               max_w=980):
    # Shrink until the line fits the frame; never let text run off the sides.
    while size > 24:
        f = font(size)
        bbox = draw.textbbox((0, 0), line, font=f, stroke_width=stroke)
        if bbox[2] - bbox[0] <= max_w:
            break
        size -= 4
    f = font(size)
    bbox = draw.textbbox((0, 0), line, font=f, stroke_width=stroke)
    tw = bbox[2] - bbox[0]
    draw.text((cx - tw / 2, y), line, font=f, fill=fill,
              stroke_width=stroke, stroke_fill=stroke_fill)
    return bbox[3] - bbox[1]


def palm(draw, bx, by, s, lean, col):
    """A simple palm silhouette: curved trunk + drooping fronds."""
    height = 520 * s
    pts = []
    for i in range(21):
        t = i / 20
        pts.append((bx + lean * height * 0.35 * t * t, by - height * t))
    draw.line(pts, fill=col, width=max(8, int(14 * s)))
    tx, ty = pts[-1]
    for a in range(-160, 21, 20):
        rad = math.radians(a)
        # Drooping curved frond: outward, then bending down with distance.
        frond = []
        for k in range(9):
            t = k / 8
            px = tx + math.cos(rad) * 150 * s * t
            py = ty + abs(math.sin(rad)) * 90 * s * t + 70 * s * t * t
            frond.append((px, py))
        draw.line(frond, fill=col, width=max(5, int(10 * s)))


def sunset(path):
    img = vgrad((W, H), [
        (0.00, (24, 4, 64)),
        (0.35, (96, 16, 110)),
        (0.55, (214, 48, 120)),
        (0.68, (255, 122, 48)),
        (0.78, (255, 196, 110)),
        (1.00, (40, 8, 60)),
    ])
    d = ImageDraw.Draw(img, "RGBA")
    # Sun, low over the horizon.
    d.ellipse([W // 2 - 260, 1080, W // 2 + 260, 1600],
              fill=(255, 214, 130, 255))
    d.ellipse([W // 2 - 200, 1140, W // 2 + 200, 1540],
              fill=(255, 240, 200, 255))
    # Sea: horizontal shimmer bands below the horizon.
    rnd = random.Random(6)
    for y in range(1420, H, 26):
        alpha = rnd.randint(40, 130)
        x0 = rnd.randint(0, 300)
        d.rectangle([x0, y, x0 + rnd.randint(200, 700), y + 8],
                    fill=(255, 170, 90, alpha))
    # Ground silhouette strip.
    d.rectangle([0, 1560, W, H], fill=(16, 4, 34, 255))
    palm(d, 120, 1620, 1.15, -0.55, (12, 2, 28))
    palm(d, 980, 1640, 1.35, 0.5, (12, 2, 28))
    palm(d, 880, 1600, 0.8, 0.35, (16, 4, 36))
    # Birds.
    for bx, by, s in [(300, 420, 26), (700, 330, 20), (520, 520, 16)]:
        d.arc([bx - s, by - s // 2, bx, by + s // 2], 200, 340,
              fill=(20, 4, 40), width=6)
        d.arc([bx, by - s // 2, bx + s, by + s // 2], 200, 340,
              fill=(20, 4, 40), width=6)
    # Hook text, high in the frame, clear of Shorts buttons.
    text_center(d, W // 2, 300, "GTA 6", 260, (255, 255, 255), stroke=10)
    text_center(d, W // 2, 580, "IS HERE", 190, (255, 214, 90), stroke=8)
    text_center(d, W // 2, 820, "VICE CITY IS CALLING", 92,
                (255, 255, 255), stroke=6)
    img.save(path)


def skyline(path):
    img = vgrad((W, H), [
        (0.00, (6, 8, 40)),
        (0.55, (16, 16, 64)),
        (1.00, (48, 12, 70)),
    ])
    d = ImageDraw.Draw(img, "RGBA")
    rnd = random.Random(19)
    # Stars.
    for _ in range(120):
        x, y = rnd.randint(0, W), rnd.randint(0, 700)
        r = rnd.randint(1, 3)
        d.ellipse([x - r, y - r, x + r, y + r],
                  fill=(255, 255, 255, rnd.randint(120, 255)))
    # Moon.
    d.ellipse([820, 140, 960, 280], fill=(240, 240, 220, 255))
    d.ellipse([850, 160, 930, 240], fill=(210, 210, 195, 255))
    # Buildings with lit windows.
    x = -20
    while x < W:
        bw = rnd.randint(110, 210)
        bh = rnd.randint(500, 1050)
        top = 1560 - bh
        d.rectangle([x, top, x + bw, 1560], fill=(10, 10, 30, 255))
        d.rectangle([x, top, x + bw, top + 10],
                    fill=rnd.choice([(255, 60, 160), (0, 220, 255),
                                     (255, 190, 60)]))
        for wy in range(top + 40, 1520, 52):
            for wx in range(x + 16, x + bw - 16, 44):
                if rnd.random() < 0.42:
                    col = rnd.choice([(255, 210, 120), (120, 220, 255),
                                      (255, 120, 200)])
                    d.rectangle([wx, wy, wx + 20, wy + 26], fill=col + (255,))
        x += bw + rnd.randint(8, 30)
    d.rectangle([0, 1560, W, H], fill=(8, 6, 24, 255))
    # Neon road glow at the bottom.
    d.rectangle([0, 1640, W, 1652], fill=(0, 220, 255, 255))
    d.rectangle([0, 1700, W, 1710], fill=(255, 60, 160, 255))
    text_center(d, W // 2, 330, "13 YEARS", 170, (255, 255, 255), stroke=8)
    text_center(d, W // 2, 520, "OF WAITING.", 130, (255, 214, 90), stroke=7)
    text_center(d, W // 2, 700, "ONE CITY.", 130, (0, 220, 255), stroke=7)
    img.save(path)


def pitch(path):
    img = vgrad((W, H), [
        (0.00, (10, 6, 28)),
        (0.55, (22, 10, 48)),
        (1.00, (8, 4, 22)),
    ])
    d = ImageDraw.Draw(img, "RGBA")
    # Faint diagonal accent lines.
    for i in range(-4, 12):
        x0 = i * 220
        d.line([(x0, 0), (x0 + 500, H)], fill=(120, 60, 200, 26), width=10)
    # make.fun wordmark as plain text (no logo asset used).
    text_center(d, W // 2, 330, "MAKE CLIPS", 150, (255, 255, 255), stroke=7)
    text_center(d, W // 2, 500, "LIKE THIS", 150, (255, 255, 255), stroke=7)
    text_center(d, W // 2, 670, "WITH AI", 150, (0, 220, 255), stroke=7)
    text_center(d, W // 2, 900, "AND EARN MONEY", 96, (255, 214, 90), stroke=6)
    text_center(d, W // 2, 1010, "ON MAKE.FUN", 110, (255, 214, 90), stroke=6)
    d.rectangle([90, 1240, W - 90, 1500], outline=(0, 220, 255), width=6)
    text_center(d, W // 2, 1280, "make.fun/bounty/", 56,
                (255, 255, 255), stroke=4)
    text_center(d, W // 2, 1360, "gta6-clipper-01", 56,
                (255, 255, 255), stroke=4)
    img.save(path)


def main():
    outdir = sys.argv[1] if len(sys.argv) > 1 else "clip/frames"
    os.makedirs(outdir, exist_ok=True)
    sunset(os.path.join(outdir, "sunset.png"))
    skyline(os.path.join(outdir, "skyline.png"))
    pitch(os.path.join(outdir, "pitch.png"))
    print(f"wrote 3 stills to {outdir}")


if __name__ == "__main__":
    main()
