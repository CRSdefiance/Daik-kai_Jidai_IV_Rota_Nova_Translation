"""Source-backed Online screenshot headers; unreadable body/chat stay pending."""

import argparse
import copy
import json
import math
import zlib
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    apply_pxl_indexed_region_batch,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.online27_bubbles_v177 import nearest

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
PRIOR = Path("out/all_routes_combined_v188_candidate.nds")
PRIOR_SHA = "a2783f08ea8920cfa3fdaddc3fb0e2f61755d268f99c4d9ea557c97157c0a251"
CANDIDATE = Path("out/all_routes_combined_v189_candidate.nds")
PROFILE = "all-routes-unified-v189"
OUT = Path("work/qa/online_headers_v189")
PROOF = Path("work/analysis/online_headers_v189_saved_proof.json")
FONT = Path("C:/Windows/Fonts/arial.ttf")
SOURCE_HASHES = {
    24: "0b4e5d14ddaa99fb7b7921ab859f2d5abe0c3de31fe7a0989e3be557c9bd491e",
    33: "35ef5d386f61d887ce71a864ae9aea4051e789a7a0f4c51ccea0c9906ddc9e68",
}
SPECS = [
    {
        "number": 24,
        "id": "DK4_ONLINE24_CHARACTER_HEADER_V1",
        "box": [11, 2, 35, 8],
        "source_japanese": "人物情報",
        "english": "Profile",
        "size": 6,
        "donor_x": 10,
        "foreground": [235, 240, 248],
        "source_meaning": "Information about the player's character.",
        "localization_note": "Profile is the natural English tab label for character information; the adjacent description states its character scope explicitly.",
    },
    {
        "number": 24,
        "id": "DK4_ONLINE24_CHARACTER_DESCRIPTION_V1",
        "box": [41, 2, 115, 8],
        "source_japanese": "あなたの情報です",
        "english": "Your character information.",
        "size": 5,
        "donor_x": 120,
        "foreground": [25, 45, 62],
        "source_meaning": "This is your information.",
        "localization_note": "Clarifies the character-information context already identified by the neighboring Japanese heading.",
    },
    {
        "number": 33,
        "id": "DK4_ONLINE33_QUEST_HEADER_V1",
        "box": [12, 2, 46, 8],
        "source_japanese": "クエスト情報",
        "english": "Quest Info",
        "size": 6,
        "donor_x": 11,
        "foreground": [235, 240, 248],
        "source_meaning": "Quest information.",
        "localization_note": "Uses a familiar English UI abbreviation without changing the feature.",
    },
    {
        "number": 33,
        "id": "DK4_ONLINE33_QUEST_DESCRIPTION_V1",
        "box": [54, 2, 119, 8],
        "source_japanese": "クエスト情報を表示します",
        "english": "View quest information.",
        "size": 5,
        "donor_x": 125,
        "foreground": [25, 45, 62],
        "source_meaning": "Displays quest information.",
        "localization_note": "Natural action-oriented description of the same menu function.",
    },
]


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def image_path(number):
    return f"/_pxl/online/Online{number}.pxl"


def batch_path(number):
    return Path(f"translations/online{number}_headers_art_v1.json")


@lru_cache(maxsize=1)
def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError("Exact canonical and V188 sources required")
    base, prior, clean = (NdsImage.open(p) for p in (BASE, PRIOR, Path("work/clean.nds")))
    for n, digest in SOURCE_HASHES.items():
        raw = base.read_file(image_path(n))
        if (
            sha(raw) != digest
            or raw != prior.read_file(image_path(n))
            or raw != clean.read_file(image_path(n))
        ):
            raise ValueError("Untouched Japanese screenshot required")
    return base, prior


@lru_cache(maxsize=1)
def artwork():
    base, _ = sources()
    results = {}
    for n in SOURCE_HASHES:
        p = PxlImage.from_bytes(base.read_file(image_path(n)))
        if (p.width, p.height, p.bits_per_pixel) != (256, 192, 8):
            raise ValueError("Screenshot format differs")
        rows = []
        for spec in (r for r in SPECS if r["number"] == n):
            x0, y0, x1, y1 = spec["box"]
            w, h = x1 - x0, y1 - y0
            f = ImageFont.truetype(str(FONT), spec["size"])
            bbox = f.getbbox(spec["english"])
            ww, hh = bbox[2] - bbox[0], bbox[3] - bbox[1]
            if ww > w or hh > h:
                raise ValueError("Complete English label cannot fit")
            mask = Image.new("L", (w, h))
            ox, oy = (w - ww) // 2, (h - hh) // 2
            ImageDraw.Draw(mask).text(
                (ox - bbox[0], oy - bbox[1]), spec["english"], font=f, fill=255
            )
            glyphs = []
            for i, ch in enumerate(spec["english"]):
                if ch.isspace():
                    continue
                b = f.getbbox(ch)
                single = Image.new("L", (max(1, b[2] - b[0]), max(1, b[3] - b[1])))
                ImageDraw.Draw(single).text((-b[0], -b[1]), ch, font=f, fill=255)
                if max(single.tobytes()) < 64:
                    raise ValueError("A complete English glyph has no ink")
                glyphs.append(
                    {"index": i, "character": ch, "full_glyph_sha256": sha(single.tobytes())}
                )
            payload = bytearray(w * h)
            for y in range(h):
                donor = p.indices[(y + y0) * p.width + spec["donor_x"]]
                bg = p.palette[donor][:3]
                for x in range(w):
                    a = mask.getpixel((x, y)) / 255
                    rgb = tuple(
                        round(b + a * (c - b)) for b, c in zip(bg, spec["foreground"], strict=True)
                    )
                    payload[y * w + x] = nearest(p.palette, rgb) if a else donor
            source_region = bytes(
                p.indices[y * p.width + x] for y in range(y0, y1) for x in range(x0, x1)
            )
            proof = {
                "full_ink_box": [x0 + ox, y0 + oy, x0 + ox + ww, y0 + oy + hh],
                "full_mask_sha256": sha(mask.tobytes()),
                "font_sha256": sha(FONT.read_bytes()),
                "font_size": spec["size"],
                "each_nonspace_character": glyphs,
                "restoration": "Text rectangle filled from a text-free same-row header donor; background beneath old text is an estimate.",
                "border_pixels_owned": False,
                "native_display_verified": False,
            }
            row = {
                "id": spec["id"],
                "box": spec["box"],
                "source_region_sha256": sha(source_region),
                "indices_zlib_hex": zlib.compress(payload).hex(),
                "indices_sha256": sha(payload),
                "english": spec["english"],
                "source_japanese": spec["source_japanese"],
                "source_meaning": spec["source_meaning"],
                "localization_note": spec["localization_note"],
                "speaker": "Promotional PC screenshot UI",
                "context": "Top menu heading and neighboring description in the exact original reduced screenshot.",
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
                "artwork_proof": proof,
            }
            rows.append(row)
        results[n] = rows
    return results


def expected(number):
    p = PxlImage.from_bytes(sources()[0].read_file(image_path(number)))
    for row in artwork()[number]:
        x0, y0, x1, y1 = row["box"]
        payload = zlib.decompress(bytes.fromhex(row["indices_zlib_hex"]))
        for y in range(y0, y1):
            p.indices[y * p.width + x0 : y * p.width + x1] = payload[
                (y - y0) * (x1 - x0) : (y - y0 + 1) * (x1 - x0)
            ]
    return p.to_bytes()


def preservation(number, raw):
    original = sources()[0].read_file(image_path(number))
    if raw != expected(number):
        raise ValueError("Complete English letters or unowned screenshot pixels differ")
    old, new = (PxlImage.from_bytes(r) for r in (original, raw))
    if raw[: new.pixels_offset] != original[: old.pixels_offset] or len(raw) != len(original):
        raise ValueError("Header, original palette or native extent differs")
    return {
        "path": image_path(number),
        "changed_pixels": sum(a != b for a, b in zip(old.indices, new.indices, strict=True)),
        "original_header_palette_dimensions_borders_unowned_pixels_exact": True,
        "entire_screenshot_localized": False,
        "native_display_verified": False,
        "remaining": "Body UI, status, player names and chat need source transcription/localization.",
    }


def materialize():
    OUT.mkdir(parents=True, exist_ok=True)
    base, _ = sources()
    cases = []
    for n, rows in artwork().items():
        raw = base.read_file(image_path(n))
        save(
            batch_path(n),
            {
                "format": "dk4-pxl-indexed-region-batch-v1",
                "file_path": image_path(n),
                "source_file_sha256": sha(raw),
                "target_locale": "en-US",
                "editorial_policy": "natural-dialogue-v2",
                "scope": "Source-backed top header and description only; body/chat remain pending.",
                "records": rows,
            },
        )
        new = apply_pxl_indexed_region_batch(batch_path(n), raw)[0]
        cases.append(preservation(n, new))
        source, target = PxlImage.from_bytes(raw).render(), PxlImage.from_bytes(new).render()
        target.save(OUT / f"Online{n}_english.png")
        sheet = Image.new("RGB", (1040, 148), "#303030")
        d = ImageDraw.Draw(sheet)
        for i, (label, image) in enumerate(
            (("Original source", source), ("English headers; body/chat pending", target))
        ):
            d.text((8 + i * 520, 4), label, fill="white")
            sheet.paste(
                image.crop((0, 0, 256, 12))
                .resize((512, 24), Image.Resampling.NEAREST)
                .convert("RGB"),
                (8 + i * 520, 24),
            )
            sheet.paste(
                image.crop((0, 0, 130, 12))
                .resize((520, 48), Image.Resampling.NEAREST)
                .convert("RGB"),
                (i * 520, 76),
            )
        sheet.save(OUT / f"Online{n}_header_review.png")
    save(
        OUT / "evidence.json",
        {"cases": cases, "visual_review": False, "native_display_verified": False},
    )
    print("Prepared four complete source-backed header labels; body/chat remain pending.")


def register():
    if not json.loads((OUT / "evidence.json").read_text(encoding="utf-8"))["visual_review"]:
        raise ValueError("Review complete labels and original borders first")
    stack = load_release_stack()
    profile = copy.deepcopy(stack["profiles"]["all-routes-unified-v188"])
    profile["batches"].extend(batch_path(n).as_posix() for n in SOURCE_HASHES)
    profile.update(
        description="Full V188 stack plus four source-backed Online24/33 screenshot header labels; 465 batches.",
        note="Broader graphics goal active/incomplete. Screenshot body/chat and actual native/gameplay review remain pending; experimental.",
    )
    stack["profiles"][PROFILE] = profile
    save(RELEASE_STACK_PATH, stack)


def verify():
    base, prior = sources()
    new = NdsImage.open(CANDIDATE)
    m = json.loads(CANDIDATE.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    old = json.loads(PRIOR.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    stack = load_release_stack()
    if (
        m["base_sha256"] != CANONICAL_BASELINE_SHA256
        or m["candidate_sha256"] != sha(CANDIDATE.read_bytes())
        or m["profile"] != PROFILE
        or m["release_stack_sha256"] != sha(RELEASE_STACK_PATH.read_bytes())
        or m["batches"] != old["batches"] + [str(batch_path(n)) for n in SOURCE_HASHES]
        or m["batches"] != [str(p) for p in resolve_release_batches(PROFILE, [], stack)]
        or len(m["batches"]) != 465
        or m["required_batches"] != [str(p) for p in accepted_batch_paths(stack)]
        or not all(m["checks"].values())
        or m["relocations"] != old["relocations"]
    ):
        raise ValueError("Saved identity or complete inheritance differs")
    before, after = rom_files(prior), rom_files(new)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if changed != sorted(image_path(n) for n in SOURCE_HASHES):
        raise ValueError("Unexpected changes versus V188")
    if m["changed_paths"] != sorted(old["changed_paths"] + changed):
        raise ValueError("Changed-path manifest differs")
    for path, ids in old["changed_records"].items():
        if m["changed_records"][path] != ids:
            raise ValueError("Inherited record IDs lost")
    cases = []
    for n in SOURCE_HASHES:
        if m["changed_records"][image_path(n)] != [r["id"] for r in artwork()[n]]:
            raise ValueError("Header record IDs differ")
        cases.append(preservation(n, new.read_file(image_path(n))))
    reproduction = Path("work/analysis/v188_online_headers_reproduction.nds")
    if sha(reproduction.read_bytes()) != PRIOR_SHA:
        raise ValueError("Complete V188 reproduction differs")
    # Remove actual first/last glyph rectangles, including terminal punctuation.
    # Exact-artwork comparison must reject every damaged row, not just metadata.
    glyph_probes = []
    for spec in SPECS:
        n = spec["number"]
        p = PxlImage.from_bytes(new.read_file(image_path(n)))
        original = PxlImage.from_bytes(base.read_file(image_path(n)))
        font = ImageFont.truetype(str(FONT), spec["size"])
        record = next(r for r in artwork()[n] if r["id"] == spec["id"])
        full = record["artwork_proof"]["full_ink_box"]
        origin_x = full[0] - font.getbbox(spec["english"])[0]
        for position in (0, len(spec["english"]) - 1):
            ch = spec["english"][position]
            bb = font.getbbox(ch)
            gx = origin_x + font.getlength(spec["english"][:position])
            left, right = math.floor(gx + bb[0]), math.ceil(gx + bb[2])
            damaged = PxlImage.from_bytes(p.to_bytes())
            changed_pixels = 0
            for y in range(spec["box"][1], spec["box"][3]):
                background = original.indices[y * 256 + spec["donor_x"]]
                for x in range(max(left, spec["box"][0]), min(right, spec["box"][2])):
                    changed_pixels += damaged.indices[y * 256 + x] != background
                    damaged.indices[y * 256 + x] = background
            if not changed_pixels:
                raise ValueError("Leading/trailing glyph has no visible native palette ink")
            try:
                preservation(n, damaged.to_bytes())
            except ValueError:
                pass
            else:
                raise ValueError("Dropped leading/trailing glyph accepted")
            glyph_probes.append(
                {
                    "id": spec["id"],
                    "character": ch,
                    "position": position,
                    "removed_native_ink_pixels": changed_pixels,
                    "rejected": True,
                }
            )
    verify_golden_content(base, new)
    clean = Path("work/clean.nds")
    if (
        sha(clean.read_bytes())
        != "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    ):
        raise ValueError("Wrong patch base")
    patch = CANDIDATE.with_suffix(".xdelta")
    make_xdelta(clean, CANDIDATE, patch)
    restored = Path("work/analysis/online_headers_v189_patch_reconstruction.nds")
    apply_xdelta(clean, patch, restored)
    if restored.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError("Patch reconstruction differs")
    save(
        PROOF,
        {
            "status": "pass-saved-v189-four-source-backed-headers",
            "cases": cases,
            "candidate": str(CANDIDATE),
            "candidate_sha256": sha(CANDIDATE.read_bytes()),
            "canonical_base": str(BASE),
            "canonical_base_sha256": CANONICAL_BASELINE_SHA256,
            "profile": PROFILE,
            "experimental": True,
            "batch_count": 465,
            "changed_paths_vs_v188": changed,
            "changed_paths_vs_canonical": m["changed_paths"],
            "prior_v188_reproduction_exact": True,
            "terminal_stages_and_prior_record_ids_retained": True,
            "corrupt_label_probes_rejected": True,
            "leading_trailing_glyph_probes": glyph_probes,
            "ARM9_sha256": sha(new.read_file("/__arm9__.bin")),
            "patch": str(patch),
            "patch_sha256": sha(patch.read_bytes()),
            "patch_reconstruction_exact": True,
            "entire_screenshots_localized": False,
            "native_display_verified": False,
            "goal_status": "active",
        },
    )
    print(
        "Verified four complete labels, exact screenshot preservation, full inheritance and patch."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["materialize", "register", "verify"])
    globals()[parser.parse_args().action]()
