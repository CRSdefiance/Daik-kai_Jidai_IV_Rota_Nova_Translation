"""Source-locked PC Porto Estado title lettering and native-sized embedded copy."""

import argparse
import copy
import json
import struct
import zlib
from collections import Counter
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage, bgr555
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    apply_ilnk_indexed_region_batch,
    apply_pxl_indexed_region_batch,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.fleet_row_graphics_v162 import save
from scripts.inventory_embedded_graphics_v151 import decode

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
PRIOR = Path("out/all_routes_combined_v175_candidate.nds")
PRIOR_SHA = "55e229aa9d19d894b3197b7f0d179741e26a73619b139ce117f1c9376abaab47"
CANDIDATE = Path("out/all_routes_combined_v176_candidate.nds")
PROFILE = "all-routes-unified-v176"
REPRO = Path("work/analysis/v175_ilnk_art_builder_reproduction.nds")
OUT = Path("work/qa/porto_titles_v176")
PROOF = Path("work/analysis/porto_titles_v176_saved_proof.json")
FONT = Path("C:/Windows/Fonts/timesbd.ttf")
SPECS = [
    {
        "path": "/_pxl/startmenu0.pxl",
        "name": "startmenu0",
        "main": [4, 54, 252, 104],
        "caption": [146, 120, 231, 136],
        "size": 24,
        "draw_h": 43,
        "water": True,
    },
    {
        "path": "/_pxl/winframe00.pxl",
        "name": "winframe00",
        "main": [4, 25, 252, 75],
        "caption": [146, 90, 231, 108],
        "size": 24,
        "draw_h": 39,
    },
    {
        "path": "/GRP/WINFRAME.DK4",
        "name": "embedded",
        "main": [5, 31, 315, 95],
        "caption": [182, 113, 289, 137],
        "size": 30,
        "draw_h": 49,
        "block": 0,
    },
]


def batch_path(spec):
    return Path("translations/porto_title_" + spec["name"] + "_art_v1.json")


@lru_cache(maxsize=1)
def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError("Exact canonical and V175 required")
    base, prior, clean = [NdsImage.open(p) for p in (BASE, PRIOR, Path("work/clean.nds"))]
    for spec in SPECS:
        if (
            not base.read_file(spec["path"])
            == prior.read_file(spec["path"])
            == clean.read_file(spec["path"])
        ):
            raise ValueError("Untouched PC source required")
    return base, prior


def asset(spec, raw=None):
    raw = sources()[0].read_file(spec["path"]) if raw is None else raw
    if "block" not in spec:
        p = PxlImage.from_bytes(raw)
        return p.width, p.height, bytes(p.indices), p.palette
    block = IlnkContainer.parse(raw).blocks[spec["block"]]
    d = decode(block)
    if (d["depth"], d["width"], d["height"], d["palette_banks"]) != (8, 320, 240, 1):
        raise ValueError("Original native PC image required")
    return (
        d["width"],
        d["height"],
        d["indices"],
        [bgr555(v) for (v,) in struct.iter_unpack("<H", d["palette"])],
    )


def nearest(palette, rgb):
    return min(
        range(len(palette)),
        key=lambda i: sum((a - b) ** 2 for a, b in zip(palette[i][:3], rgb, strict=True)),
    )


def gold(rgb):
    r, g, b = rgb[:3]
    return r > g + 10 and g > b + 30 and r > 120


def latin_gold(spec, x, y, rgb):
    scale = 1.25 if "block" in spec else 1
    shift = 29 if spec.get("water") else 0
    x = x / scale
    y = y / scale - shift
    return gold(rgb) and ((18 <= x < 237 and 73 <= y < 95) or (108 <= x < 146 and 65 <= y < 105))


def water_mapping(indices, palette):
    donor = PxlImage.from_bytes(sources()[0].read_file("/_pxl/title/title04.pxl"))
    counts = [Counter() for _ in donor.palette]
    for y in list(range(49)) + list(range(143, 192)):
        for x in range(256):
            counts[donor.indices[y * 256 + x]][indices[y * 256 + x]] += 1
    mapping = [
        c.most_common(1)[0][0] if c else nearest(palette, color[:3])
        for c, color in zip(counts, donor.palette, strict=True)
    ]
    return donor, mapping


def restore(rgb, mask, w, h):
    """Harmonic reconstruction confined to old glyph/shadow mask; not recovered scenery."""
    offsets = [i for i, v in enumerate(mask) if v]
    values = [list(c) for c in rgb]
    # Each unknown starts with the nearest unmasked sample in its own row.
    for i in offsets:
        x, y = i % w, i // w
        samples = []
        for dx in (-1, 1):
            xx = x + dx
            while 0 <= xx < w and mask[y * w + xx]:
                xx += dx
            if 0 <= xx < w:
                samples.append(rgb[y * w + xx])
        values[i] = (
            [sum(c[k] for c in samples) / len(samples) for k in range(3)]
            if samples
            else [sum(c[k] for c in rgb) / len(rgb) for k in range(3)]
        )
    neighbors = {
        i: [
            j
            for j in (i - 1, i + 1, i - w, i + w)
            if 0 <= j < w * h and (j // w == i // w or j % w == i % w)
        ]
        for i in offsets
    }
    for _ in range(180):
        for i in offsets:
            ns = neighbors[i]
            values[i] = [sum(values[j][k] for j in ns) / len(ns) for k in range(3)]
    return [tuple(round(v) for v in values[i]) for i in range(w * h)]


@lru_cache(maxsize=3)
def regions(name):
    spec = next(s for s in SPECS if s["name"] == name)
    width, height, indices, palette = asset(spec)
    result = []
    cases = []
    precise = []
    for kind in ("main", "caption"):
        box = spec[kind]
        x0, y0, x1, y1 = box
        w, h = x1 - x0, y1 - y0
        original = bytes(indices[y * width + x] for y in range(y0, y1) for x in range(x0, x1))
        pixels = bytearray(original)
        rgb = [palette[i][:3] for i in original]
        seed = Image.new("L", (w, h))
        donor = mapping = None
        if spec.get("water"):
            donor, mapping = water_mapping(indices, palette)
            backgrounds = [
                mapping[donor.indices[y * width + x]] for y in range(y0, y1) for x in range(x0, x1)
            ]
            seed.putdata(
                [
                    255
                    if sum(abs(a - b) for a, b in zip(c, palette[backgrounds[i]][:3], strict=True))
                    >= 55
                    else 0
                    for i, c in enumerate(rgb)
                ]
            )
        else:
            seed.putdata([255 if c[2] > c[0] + 8 and c[2] > c[1] + 8 else 0 for c in rgb])
        radius = 2 if width == 256 else 3
        mask = list(seed.filter(ImageFilter.MaxFilter(radius * 2 + 1)).tobytes())
        # Gold lettering and ornate E always retain their original indices.
        protected = Image.new("L", (w, h))
        protected.putdata(
            [255 if latin_gold(spec, x0 + i % w, y0 + i // w, c) else 0 for i, c in enumerate(rgb)]
        )
        protected = bytearray(protected.filter(ImageFilter.MaxFilter(3)).tobytes())
        for i, c in enumerate(rgb):
            if c[2] > c[0] + 8 and c[2] > c[1] + 8:
                protected[i] = 0  # Nearby Japanese ink is not part of a gold bevel.
        for i, c in enumerate(rgb):
            if protected[i]:
                mask[i] = 0
        reconstructed = restore(rgb, mask, w, h) if not donor else None
        cache = {}
        for i, v in enumerate(mask):
            if v:
                if donor:
                    pixels[i] = backgrounds[i]
                else:
                    c = reconstructed[i]
                    if c not in cache:
                        cache[c] = nearest(palette, c)
                    pixels[i] = cache[c]
        size = spec["size"] if kind == "main" else (9 if width == 256 else 11)
        font = ImageFont.truetype(str(FONT), size=size)
        lines = ["UNCHARTED", "WATERS IV"] if kind == "main" else ["Porto Estado"]
        ink = Image.new("L", (w, h))
        d = ImageDraw.Draw(ink)
        bs = [font.getbbox(s) for s in lines]
        hs = [b[3] - b[1] for b in bs]
        gap = 2 if width == 256 else 3
        total = sum(hs) + gap * (len(lines) - 1)
        draw_h = spec["draw_h"] if kind == "main" else h
        y = (draw_h - total) // 2
        if kind == "caption":
            y = max(y, 9 if width == 320 else (6 if spec.get("water") else 7))
        line_cases = []
        for text, b, hh in zip(lines, bs, hs, strict=True):
            extra_space = 3 if kind == "caption" else 0
            ww = b[2] - b[0] + extra_space
            x = (w - ww) // 2
            if x < 1 or y < 1 or y + hh > draw_h - 1:
                raise ValueError("Complete English title cannot fit")
            if extra_space:
                first, second = text.split(" ")
                d.text((x - b[0], y - b[1]), first, font=font, fill=255)
                advance = font.getlength(first + " ") + extra_space
                d.text((x - b[0] + advance, y - b[1]), second, font=font, fill=255)
            else:
                d.text((x - b[0], y - b[1]), text, font=font, fill=255)
            line_cases.append(
                {"text": text, "full_glyph_box": [x + x0, y + y0, x + x0 + ww, y + y0 + hh]}
            )
            y += hh + gap
        outline = ink.filter(ImageFilter.MaxFilter(3))
        allowed = {i for i, v in enumerate(mask) if v}
        for i, v in enumerate(outline.tobytes()):
            if v >= 128:
                if protected[i]:
                    raise ValueError("English outline overlaps original gold")
                allowed.add(i)
                pixels[i] = nearest(palette, (235, 232, 217))
        for i, v in enumerate(ink.tobytes()):
            if v >= 128:
                allowed.add(i)
                pixels[i] = nearest(palette, (16, 40, 205 if kind == "main" else 155))
        cases.append(
            {
                "kind": kind,
                "box": box,
                "font_size": size,
                "font_sha256": sha(FONT.read_bytes()),
                "lines": line_cases,
                "ink_mask_sha256": sha(ink.tobytes()),
                "old_glyph_restoration_pixels": sum(bool(v) for v in mask),
                "reconstruction": "Original title04 water donor with modal palette correspondence in difference-selected glyph/shadow mask"
                if donor
                else "180-sweep harmonic fill of selected blue glyphs and dilated shadows only; approximate hidden scenery",
                "background_source_sha256": sha(sources()[0].read_file("/_pxl/title/title04.pxl"))
                if donor
                else None,
                "all_original_gold_indices_preserved": True,
                "gold_and_adjacent_bevel_shadow_pixels_preserved": sum(bool(v) for v in protected),
                "width": width,
                "height": height,
            }
        )
        precise.append(allowed)
        result.append(bytes(pixels))
    return result, cases, precise


def apply(spec, raw):
    return (apply_ilnk_indexed_region_batch if "block" in spec else apply_pxl_indexed_region_batch)(
        batch_path(spec), raw
    )


def preservation(spec, target):
    oldraw = sources()[0].read_file(spec["path"])
    w, h, old, palette = asset(spec)
    nw, nh, new, np = asset(spec, target)
    if (nw, nh, np) != (w, h, palette):
        raise ValueError("Original dimensions/palette differ")
    payloads, cases, precise = regions(spec["name"])
    expected = bytearray(old)
    allowed = set()
    gold_count = 0
    for kind, payload, local in zip(("main", "caption"), payloads, precise, strict=True):
        x0, y0, x1, y1 = spec[kind]
        rw = x1 - x0
        for y in range(y0, y1):
            for x in range(x0, x1):
                i = (y - y0) * rw + x - x0
                offset = y * w + x
                expected[offset] = payload[i]
                if i in local:
                    allowed.add(offset)
    if new != expected:
        raise ValueError("Complete English artwork or original scene differs")
    for i, (a, b) in enumerate(zip(old, new, strict=True)):
        if i not in allowed and a != b:
            raise ValueError("Unowned scene pixel changed")
        if latin_gold(spec, i % w, i // w, palette[a]):
            gold_count += 1
            if a != b:
                raise ValueError("Original gold pixel changed")
    if "block" in spec:
        oa, na = IlnkContainer.parse(oldraw), IlnkContainer.parse(target)
        for i, (a, b) in enumerate(zip(oa.blocks, na.blocks, strict=True)):
            if i != spec["block"] and a != b:
                raise ValueError("Unrelated block differs")
        a, b = oa.blocks[spec["block"]], na.blocks[spec["block"]]
        if a[:544] != b[:544] or a[544 + w * h :] != b[544 + w * h :]:
            raise ValueError("Native header/palette/trailer differs")
    else:
        a, b = PxlImage.from_bytes(oldraw), PxlImage.from_bytes(target)
        if oldraw[: a.pixels_offset] != target[: b.pixels_offset]:
            raise ValueError("PXL header/palette differs")
    if len(oldraw) != len(target):
        raise ValueError("Original allocation differs")
    return {
        "path": spec["path"],
        "complete_artwork_exact": True,
        "unowned_scene_header_palette_border_copyright_exact": True,
        "original_gold_pixels_exact": gold_count,
        "changed_pixel_count": sum(a != b for a, b in zip(old, new, strict=True)),
        "cases": cases,
    }


def render(spec, raw=None):
    w, h, indices, palette = asset(spec, raw)
    im = Image.new("RGBA", (w, h))
    im.putdata([palette[i] for i in indices])
    return im


def materialize():
    base, _ = sources()
    OUT.mkdir(parents=True, exist_ok=True)
    evidence = []
    for spec in SPECS:
        raw = base.read_file(spec["path"])
        w, h, indices, _ = asset(spec)
        payloads, cases, _ = regions(spec["name"])
        batch = {
            "format": "dk4-ilnk-indexed-region-batch-v1"
            if "block" in spec
            else "dk4-pxl-indexed-region-batch-v1",
            "file_path": spec["path"],
            "source_file_sha256": sha(raw),
            "target_locale": "en-US",
            "records": [],
        }
        for kind, pixels, proof in zip(("main", "caption"), payloads, cases, strict=True):
            box = spec[kind]
            original = bytes(
                indices[y * w + x] for y in range(box[1], box[3]) for x in range(box[0], box[2])
            )
            row = {
                "id": "DK4_PORTO_" + spec["name"].upper() + "_" + kind.upper() + "_V1",
                "box": box,
                "source_region_sha256": sha(original),
                "indices_zlib_hex": zlib.compress(pixels).hex(),
                "indices_sha256": sha(pixels),
                "source_japanese": "大航海時代IV" if kind == "main" else "ポルト・エシュタード",
                "english": "Uncharted Waters IV" if kind == "main" else "Porto Estado",
                "artwork_proof": proof,
            }
            if "block" in spec:
                row.update(
                    block_index=spec["block"],
                    source_block_sha256=sha(IlnkContainer.parse(raw).blocks[spec["block"]]),
                )
            batch["records"].append(row)
        save(batch_path(spec), batch)
        target, _ = apply(spec, raw)
        evidence.append(preservation(spec, target))
        old, new = render(spec), render(spec, target)
        sheet = Image.new("RGB", (w * 4 + 24, h * 2 + 34), "#303030")
        d = ImageDraw.Draw(sheet)
        for i, (title, im) in enumerate((("Original", old), ("English", new))):
            d.text((8 + i * (w * 2 + 8), 8), title, fill="white")
            sheet.paste(
                im.resize((w * 2, h * 2), Image.Resampling.NEAREST).convert("RGB"),
                (8 + i * (w * 2 + 8), 26),
            )
        sheet.save(OUT / (spec["name"] + "_review.png"))
        new.save(OUT / (spec["name"] + "_english.png"))
    save(
        OUT / "evidence.json",
        {
            "cases": evidence,
            "visual_review": False,
            "actual_native_loading_composition_gameplay": False,
        },
    )
    print("Prepared three original-sized Porto Estado title copies.")


def register():
    if not json.loads((OUT / "evidence.json").read_text(encoding="utf-8"))["visual_review"]:
        raise ValueError("Preview review required")
    s = load_release_stack()
    p = copy.deepcopy(s["profiles"]["all-routes-unified-v175"])
    p["batches"] += [batch_path(spec).as_posix() for spec in SPECS]
    p.update(
        description="All 458 V175 batches/stages unchanged plus three bounded Porto Estado title artworks; 461 batches.",
        note="Two loose PC title copies and original-sized 320x240 embedded WINFRAME title; original Latin gold/header/palette/extent preserved. Hidden scenery reconstruction within old glyph masks is approximate. Native loading/composition/gameplay pending; experimental.",
    )
    s["profiles"][PROFILE] = p
    save(RELEASE_STACK_PATH, s)


def verify():
    base, prior = sources()
    if REPRO.read_bytes() != PRIOR.read_bytes():
        raise ValueError("Full V175 reproduction required")
    new = NdsImage.open(CANDIDATE)
    m = json.loads(CANDIDATE.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    old = json.loads(PRIOR.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    s = load_release_stack()
    if (
        m["base_sha256"] != CANONICAL_BASELINE_SHA256
        or m["candidate_sha256"] != sha(CANDIDATE.read_bytes())
        or m["profile"] != PROFILE
        or m["release_stack_sha256"] != sha(RELEASE_STACK_PATH.read_bytes())
        or m["batches"] != old["batches"] + [str(batch_path(spec)) for spec in SPECS]
        or m["batches"] != [str(p) for p in resolve_release_batches(PROFILE, [], s)]
        or len(m["batches"]) != 461
        or m["required_batches"] != [str(p) for p in accepted_batch_paths(s)]
        or not all(m["checks"].values())
        or m["relocations"] != old["relocations"]
    ):
        raise ValueError("Saved identity/inheritance differs")
    before, after = rom_files(prior), rom_files(new)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    paths = sorted(spec["path"] for spec in SPECS)
    if changed != paths or m["changed_paths"] != sorted(old["changed_paths"] + paths):
        raise ValueError("Unexpected changed files")
    if any(m["changed_records"][path] != ids for path, ids in old["changed_records"].items()):
        raise ValueError("Prior IDs lost")
    evidence = []
    for spec in SPECS:
        path = spec["path"]
        target, ids = apply(spec, base.read_file(path))
        if target != new.read_file(path) or m["changed_records"][path] != ids:
            raise ValueError("Saved title artwork differs")
        evidence.append(preservation(spec, target))
    verify_golden_content(base, new)
    clean = Path("work/clean.nds")
    clean_sha = sha(clean.read_bytes())
    if clean_sha != "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d":
        raise ValueError("Wrong clean base")
    patch = CANDIDATE.with_suffix(".xdelta")
    reconstruction = Path("work/analysis/porto_v176_patch_reconstruction.nds")
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError("Patch reconstruction differs")
    save(
        PROOF,
        {
            "status": "pass-saved-v176-three-porto-title-copies-and-inheritance",
            "cases": evidence,
            "candidate": str(CANDIDATE),
            "candidate_sha256": sha(CANDIDATE.read_bytes()),
            "canonical_base": str(BASE),
            "canonical_base_sha256": CANONICAL_BASELINE_SHA256,
            "previous_sha256": PRIOR_SHA,
            "profile": PROFILE,
            "profile_status": "experimental",
            "batch_count": 461,
            "candidate_arm9_sha256": sha(new.read_file("/__arm9__.bin")),
            "registry_sha256": m["release_stack_sha256"],
            "builder_sha256": sha(Path("scripts/build_integrated_release.py").read_bytes()),
            "complete_v175_reproduction_exact": True,
            "changed_paths_vs_v175": changed,
            "changed_paths_vs_canonical": m["changed_paths"],
            "patch": str(patch),
            "patch_bytes": patch.stat().st_size,
            "patch_sha256": sha(patch.read_bytes()),
            "clean_patch_base_sha256": clean_sha,
            "patch_reconstruction_exact": True,
            "actual_native_loading_crops_composition_gameplay_verified": False,
        },
    )
    print("Saved exact V176 identity, preservation and patch proof:", PROOF)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["materialize", "register", "verify"])
    globals()[parser.parse_args().action]()
