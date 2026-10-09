from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from scripts import title_logo_match_v187 as old

OUT = Path("work/qa/title_edges_v188")
OUT.mkdir(parents=True, exist_ok=True)


@lru_cache(maxsize=1)
def assets():
    base, _ = old.prior_art.sources()
    menu = PxlImage.from_bytes(old.prior_art.targets()["/_pxl/title/title03.pxl"])
    bg = PxlImage.from_bytes(base.read_file("/_pxl/title/title00.pxl"))
    lat = FlsArchive(base.read_file(old.FLS_PATH)).texture(5)
    water = (
        FlsArchive(base.read_file(old.FLS_PATH))
        .texture(2)
        .render()
        .resize((256, 192), Image.Resampling.BILINEAR)
        .convert("RGBA")
    )
    return menu, bg, lat, water


def gold():
    menu, bg, lat, _ = assets()
    core = {}
    samples = {}
    for y in range(64):
        for x in range(2, 256):
            if not lat.indices[y * 256 + x]:
                continue
            i = (y + 41) * 256 + x - 2
            s = menu.palette[menu.indices[i]][:3]
            b = bg.palette[bg.indices[i]][:3]
            delta = max(abs(c - d) for c, d in zip(s, b))
            samples[x, y] = (s, b, delta)
            r, g, bl = s
            if (r > g + 6 and g > bl + 18 and r > 90) or delta >= 96:
                core[x, y] = s
    # Keep only opaque components attached to actual warm gold, excluding scene.
    warm = {xy for xy, s in core.items() if s[0] > s[1] + 6 and s[1] > s[2] + 18 and s[0] > 90}
    unseen = set(core)
    keep = set()
    while unseen:
        seed = unseen.pop()
        group = {seed}
        todo = [seed]
        while todo:
            x, y = todo.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    xy = x + dx, y + dy
                    if xy in unseen:
                        unseen.remove(xy)
                        group.add(xy)
                        todo.append(xy)
        if group & warm:
            keep |= group
    core = {xy: core[xy] for xy in keep}
    out = Image.new("RGBA", (256, 64))
    for xy, (s, b, delta) in samples.items():
        if xy in core:
            out.putpixel(xy, s + (255,))
            continue
        if delta <= 25:
            continue  # original backgrounds differ by up to 25 from palette quantization
        x, y = xy
        candidates = []
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                if (x + dx, y + dy) in core:
                    candidates.append((dx * dx + dy * dy, core[x + dx, y + dy]))
        if not candidates:
            continue
        _, f = min(candidates)
        v = [a - c for a, c in zip(f, b)]
        den = sum(a * a for a in v)
        alpha = max(0, min(1, sum((a - c) * v0 for a, c, v0 in zip(s, b, v)) / max(1, den)))
        if alpha < 0.08:
            continue
        # Unmatte from the original sky/ship; recover foreground color and soft alpha.
        fg = tuple(round(max(0, min(255, (a - (1 - alpha) * c) / alpha))) for a, c in zip(s, b))
        out.putpixel(xy, fg + (round(alpha * 255),))
    return out


def blue():
    menu, bg, _, _ = assets()
    word, _ = old.prior_art.wordmark()
    out = Image.new("RGBA", word.size)
    for y in range(word.height):
        for x in range(word.width):
            a = word.getpixel((x, y))[3]
            if a < 8:
                continue
            i = (y + 8) * 256 + x + 40
            s = menu.palette[menu.indices[i]][:3]
            if a >= 96:
                out.putpixel((x, y), s + (255,))
                continue
            b = menu.palette[old.nearest(menu.palette, bg.palette[bg.indices[i]][:3])][:3]
            alpha = a / 255
            fg = tuple(round(max(0, min(255, (c - (1 - alpha) * d) / alpha))) for c, d in zip(s, b))
            out.putpixel((x, y), fg + (a,))
    return out


def preview():
    _, _, _, water = assets()
    opening = water.copy()
    word = blue()
    opening.alpha_composite(word, (40, 50))
    opening.alpha_composite(gold(), (0, 84))
    menu = PxlImage.from_bytes(old.prior_art.targets()["/_pxl/title/title03.pxl"]).render()
    sheet = Image.new("RGB", (1040, 412), "#303030")
    d = ImageDraw.Draw(sheet)
    for col, (label, im) in enumerate(
        (("Opening: edges matted to water", opening), ("Menu: unchanged", menu))
    ):
        d.text((8 + col * 520, 6), label, fill="white")
        sheet.paste(
            im.resize((512, 384), Image.Resampling.NEAREST).convert("RGB"), (8 + 520 * col, 24)
        )
    gold().save(OUT / "gold_soft.png")
    blue().save(OUT / "blue_soft.png")
    opening.save(OUT / "opening_unquantized.png")
    sheet.save(OUT / "comparison_experiment.png")


if __name__ == "__main__":
    preview()
