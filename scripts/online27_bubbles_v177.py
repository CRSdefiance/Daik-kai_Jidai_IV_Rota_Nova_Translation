"""Faithful, bounded bubble artwork; reduced chat/status remain explicitly pending."""

import argparse
import copy
import json
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
from scripts.fleet_row_graphics_v162 import save

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
PRIOR = Path("out/all_routes_combined_v176_candidate.nds")
PRIOR_SHA = "cd23f79777fa9f22d41dd45ce01609de335a37284494f429a96ae90c26a1f79e"
CANDIDATE = Path("out/all_routes_combined_v177_candidate.nds")
PROFILE = "all-routes-unified-v177"
PATH = "/_pxl/online/Online27.pxl"
BATCH = Path("translations/online27_bubbles_art_v1.json")
OUT = Path("work/qa/online27_bubbles_v177")
PROOF = Path("work/analysis/online27_bubbles_v177_saved_proof.json")
FONT = Path("C:/Windows/Fonts/arial.ttf")
OFFICIAL = Path("work/research/online_official_sources/m_02.png")
OFFICIAL_SHA = "842e2440bdd21cc2ac0a9bea8025e6f1f6527c7d63773fb81bb1f18b5b050e51"
SPECS = [
    {
        "id": "DK4_ONLINE27_THANKS_BUBBLE_V1",
        "box": [47, 66, 81, 76],
        "japanese": "ありがとうございます",
        "english": "Thank you!",
        "size": 6,
        "source_meaning": "A customer politely thanks the seller.",
        "note": "Natural polite thanks; not an invented exchange.",
    },
    {
        "id": "DK4_ONLINE27_BARGAIN_BUBBLE_V1",
        "box": [68, 78, 100, 89],
        "japanese": "もってけ！どろぼー",
        "english": "It's a steal!",
        "size": 6,
        "source_meaning": "A vendor advertises a bargain using a playful expression implying the buyer is getting it for almost nothing.",
        "note": "Localizes the vendor idiom by effect. It is not an accusation of theft.",
    },
    {
        "id": "DK4_ONLINE27_RETURN_BUBBLE_V1",
        "box": [221, 68, 252, 80],
        "japanese": "ではまたご贔屓くださいませ",
        "english": "Come again!",
        "size": 5,
        "source_meaning": "A shopkeeper cordially invites repeat custom.",
        "note": "Idiomatic invitation to return, preserving the shop context.",
    },
    {
        "id": "DK4_ONLINE27_WELCOME_BUBBLE_V1",
        "box": [105, 106, 133, 113],
        "japanese": "いらっしゃーい",
        "english": "Welcome!",
        "size": 6,
        "source_meaning": "A vendor calls out a cheerful welcome.",
        "note": "Keeps the inviting call and exclamation.",
    },
]


@lru_cache(maxsize=1)
def sources():
    if sha(BASE.read_bytes()) != CANONICAL_BASELINE_SHA256 or sha(PRIOR.read_bytes()) != PRIOR_SHA:
        raise ValueError("Exact canonical and V176 required")
    if sha(OFFICIAL.read_bytes()) != OFFICIAL_SHA:
        raise ValueError("Exact official bubble source required")
    base, prior, clean = [NdsImage.open(p) for p in (BASE, PRIOR, Path("work/clean.nds"))]
    if not base.read_file(PATH) == prior.read_file(PATH) == clean.read_file(PATH):
        raise ValueError("Untouched original screenshot required")
    return base, prior


def nearest(palette, rgb):
    return min(
        range(len(palette)),
        key=lambda i: sum((a - b) ** 2 for a, b in zip(palette[i][:3], rgb, strict=True)),
    )


@lru_cache(maxsize=1)
def artwork():
    base, _ = sources()
    p = PxlImage.from_bytes(base.read_file(PATH))
    payloads = []
    cases = []
    for spec in SPECS:
        x0, y0, x1, y1 = spec["box"]
        w, h = x1 - x0, y1 - y0
        mask = Image.new("L", (w, h))
        d = ImageDraw.Draw(mask)
        font = ImageFont.truetype(str(FONT), size=spec["size"])
        text = spec["english"]
        b = font.getbbox(text)
        ww, hh = b[2] - b[0], b[3] - b[1]
        if ww > w or hh > h:
            raise ValueError("Complete English bubble cannot fit")
        x, y = (w - ww) // 2, (h - hh) // 2
        d.text((x - b[0], y - b[1]), text, font=font, fill=255)
        glyphs = []
        # Each character is independently rendered whole, before compositing the full run.
        for index, ch in enumerate(text):
            if ch == " ":
                continue
            gb = font.getbbox(ch)
            single = Image.new("L", (max(1, gb[2] - gb[0]), max(1, gb[3] - gb[1])))
            sd = ImageDraw.Draw(single)
            sd.text((-gb[0], -gb[1]), ch, font=font, fill=255)
            if max(single.tobytes()) < 64:
                raise ValueError("A complete bubble character has no visible ink")
            glyphs.append(
                {"character": ch, "index": index, "complete_raster_sha256": sha(single.tobytes())}
            )
        white = nearest(p.palette, (255, 255, 255))
        ink = nearest(p.palette, (25, 25, 30))
        pixels = bytearray([white] * (w * h))
        shades = {}
        for i, v in enumerate(mask.tobytes()):
            if v:
                grey = 255 - round(230 * (v / 255) ** 0.9)
                if grey not in shades:
                    shades[grey] = nearest(p.palette, (grey, grey, grey))
                pixels[i] = shades[grey]
        if not mask.getbbox() or mask.getbbox()[2] > w or mask.getbbox()[3] > h:
            raise ValueError("English ink escapes bubble")
        payloads.append(bytes(pixels))
        cases.append(
            {
                "id": spec["id"],
                "english": text,
                "box": spec["box"],
                "full_glyph_box": [x0 + x, y0 + y, x0 + x + ww, y0 + y + hh],
                "font_size": spec["size"],
                "font_sha256": sha(FONT.read_bytes()),
                "full_ink_mask_sha256": sha(mask.tobytes()),
                "each_visible_nonspace_character": glyphs,
                "ink_index": ink,
                "background_index": white,
                "anti_aliasing": "Complete vector raster quantized to original palette greys; no binary fattening",
            }
        )
    return payloads, cases


def target():
    return apply_pxl_indexed_region_batch(BATCH, sources()[0].read_file(PATH))[0]


def preservation(raw):
    old = PxlImage.from_bytes(sources()[0].read_file(PATH))
    new = PxlImage.from_bytes(raw)
    payloads, cases = artwork()
    if len(raw) != len(old.source) or raw[: new.pixels_offset] != old.source[: old.pixels_offset]:
        raise ValueError("Original metadata/palette/extent differs")
    expected = bytearray(old.indices)
    owned = set()
    for spec, pixels in zip(SPECS, payloads, strict=True):
        x0, y0, x1, y1 = spec["box"]
        for y in range(y0, y1):
            for x in range(x0, x1):
                i = y * old.width + x
                expected[i] = pixels[(y - y0) * (x1 - x0) + x - x0]
                owned.add(i)
    if bytes(new.indices) != bytes(expected):
        raise ValueError("Complete English bubble or unowned border/scene/chat differs")
    if any(old.indices[i] != new.indices[i] for i in range(len(old.indices)) if i not in owned):
        raise ValueError("Unowned screenshot differs")
    return {
        "path": PATH,
        "changed_indices": sum(a != b for a, b in zip(old.indices, new.indices, strict=True)),
        "original_palette_header_extent_bubble_borders_tails_scene_chat_status_exact": True,
        "cases": cases,
        "entire_screenshot_localized": False,
        "remaining": "Reduced chat, town/status text and player labels still need faithful transcription.",
    }


def materialize():
    base, _ = sources()
    p = PxlImage.from_bytes(base.read_file(PATH))
    payloads, cases = artwork()
    OUT.mkdir(parents=True, exist_ok=True)
    batch = {
        "format": "dk4-pxl-indexed-region-batch-v1",
        "file_path": PATH,
        "source_file_sha256": sha(p.source),
        "target_locale": "en-US",
        "editorial_policy": "natural-dialogue-v2",
        "scope": "Four readable merchant/customer bubbles only; untranslated chat/status remain pending.",
        "official_source_url": "https://www.gamecity.ne.jp/dol/game/image04/m_02.png",
        "official_source_sha256": OFFICIAL_SHA,
        "records": [],
    }
    for spec, pixels, proof in zip(SPECS, payloads, cases, strict=True):
        x0, y0, x1, y1 = spec["box"]
        original = bytes(p.indices[y * p.width + x] for y in range(y0, y1) for x in range(x0, x1))
        batch["records"].append(
            {
                "id": spec["id"],
                "box": spec["box"],
                "source_region_sha256": sha(original),
                "indices_zlib_hex": zlib.compress(pixels).hex(),
                "indices_sha256": sha(pixels),
                "source_japanese": spec["japanese"],
                "source_meaning": spec["source_meaning"],
                "english": spec["english"],
                "speaker": "Anonymous bazaar vendor/customer",
                "context": "Baked promotional PC bazaar screenshot; adjacent bubbles are a welcome, bargain call, thanks and invitation to return.",
                "localization_note": spec["note"],
                "review": {
                    "source": True,
                    "context": True,
                    "localization": True,
                    "naturalness": True,
                    "formatting": True,
                },
                "artwork_proof": proof,
            }
        )
    save(BATCH, batch)
    raw = target()
    evidence = preservation(raw)
    old = p.render()
    new = PxlImage.from_bytes(raw).render()
    sheet = Image.new("RGB", (2072, 802), "#303030")
    d = ImageDraw.Draw(sheet)
    for i, (label, im) in enumerate(
        (("Original", old), ("English bubbles; chat/status pending", new))
    ):
        d.text((8 + i * 1032, 8), label, fill="white")
        sheet.paste(
            im.resize((1024, 768), Image.Resampling.NEAREST).convert("RGB"), (8 + i * 1032, 26)
        )
    sheet.save(OUT / "review.png")
    new.save(OUT / "english.png")
    save(OUT / "evidence.json", {"case": evidence, "visual_review": False})
    print("Prepared four faithful bubble captions; screenshot chat/status remain pending.")


def register():
    if not json.loads((OUT / "evidence.json").read_text(encoding="utf-8"))["visual_review"]:
        raise ValueError("Review all bubble letters/borders first")
    s = load_release_stack()
    p = copy.deepcopy(s["profiles"]["all-routes-unified-v176"])
    p["batches"].append(BATCH.as_posix())
    p.update(
        description="All 461 V176 batches/stages unchanged plus four source-backed Online27 bubble captions; 462 batches.",
        note="Merchant/customer bubble artwork only; reduced chat/status and other Online screenshots remain untranslated. Original bubble borders/tails/palette/header/unowned scene retained. Native usage/display/gameplay pending; experimental.",
    )
    s["profiles"][PROFILE] = p
    save(RELEASE_STACK_PATH, s)


def verify():
    base, prior = sources()
    new = NdsImage.open(CANDIDATE)
    m = json.loads(CANDIDATE.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    old = json.loads(PRIOR.with_suffix(".manifest.json").read_text(encoding="utf-8"))
    s = load_release_stack()
    previous_proof = json.loads(
        Path("work/analysis/porto_titles_v176_saved_proof.json").read_text(encoding="utf-8")
    )
    if previous_proof["builder_sha256"] != sha(
        Path("scripts/build_integrated_release.py").read_bytes()
    ):
        raise ValueError("Unexpected builder change requires full prior reproduction")
    if (
        m["base_sha256"] != CANONICAL_BASELINE_SHA256
        or m["candidate_sha256"] != sha(CANDIDATE.read_bytes())
        or m["profile"] != PROFILE
        or m["release_stack_sha256"] != sha(RELEASE_STACK_PATH.read_bytes())
        or m["batches"] != old["batches"] + [str(BATCH)]
        or m["batches"] != [str(p) for p in resolve_release_batches(PROFILE, [], s)]
        or len(m["batches"]) != 462
        or m["required_batches"] != [str(p) for p in accepted_batch_paths(s)]
        or not all(m["checks"].values())
        or m["relocations"] != old["relocations"]
    ):
        raise ValueError("Saved identity/inheritance differs")
    before, after = rom_files(prior), rom_files(new)
    changed = sorted(p for p in before.keys() | after.keys() if before.get(p) != after.get(p))
    if changed != [PATH] or m["changed_paths"] != sorted(old["changed_paths"] + [PATH]):
        raise ValueError("Unexpected changed files")
    if any(m["changed_records"][path] != ids for path, ids in old["changed_records"].items()):
        raise ValueError("Prior IDs lost")
    if new.read_file(PATH) != target() or m["changed_records"][PATH] != [
        spec["id"] for spec in SPECS
    ]:
        raise ValueError("Saved bubble letters differ")
    evidence = preservation(new.read_file(PATH))
    verify_golden_content(base, new)
    clean = Path("work/clean.nds")
    clean_sha = sha(clean.read_bytes())
    if clean_sha != "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d":
        raise ValueError("Wrong clean base")
    patch = CANDIDATE.with_suffix(".xdelta")
    reconstruction = Path("work/analysis/online27_v177_patch_reconstruction.nds")
    make_xdelta(clean, CANDIDATE, patch)
    apply_xdelta(clean, patch, reconstruction)
    if reconstruction.read_bytes() != CANDIDATE.read_bytes():
        raise ValueError("Patch reconstruction differs")
    save(
        PROOF,
        {
            "status": "pass-saved-v177-four-bubbles-only-with-complete-inheritance",
            "case": evidence,
            "candidate": str(CANDIDATE),
            "candidate_sha256": sha(CANDIDATE.read_bytes()),
            "canonical_base": str(BASE),
            "canonical_base_sha256": CANONICAL_BASELINE_SHA256,
            "previous_sha256": PRIOR_SHA,
            "profile": PROFILE,
            "profile_status": "experimental",
            "batch_count": 462,
            "candidate_arm9_sha256": sha(new.read_file("/__arm9__.bin")),
            "registry_sha256": m["release_stack_sha256"],
            "builder_sha256": sha(Path("scripts/build_integrated_release.py").read_bytes()),
            "builder_unchanged_vs_v176": True,
            "changed_paths_vs_v176": changed,
            "changed_paths_vs_canonical": m["changed_paths"],
            "patch": str(patch),
            "patch_bytes": patch.stat().st_size,
            "patch_sha256": sha(patch.read_bytes()),
            "clean_patch_base_sha256": clean_sha,
            "patch_reconstruction_exact": True,
            "actual_native_loading_composition_gameplay_verified": False,
        },
    )
    print("Saved exact V177 bubble identity/preservation and patch proof:", PROOF)


def native():
    import struct

    from scripts.probe_button_prompt_native import STACK, call, machine
    from scripts.probe_name_treasure_graphics_v161 import sizing

    saved = json.loads(PROOF.read_text(encoding="utf-8"))
    if sha(CANDIDATE.read_bytes()) != saved["candidate_sha256"]:
        raise ValueError("Saved candidate identity differs")
    rom = NdsImage.open(CANDIDATE)
    arm9 = rom.read_file("/__arm9__.bin")
    raw = rom.read_file(PATH)
    header = sizing(arm9, raw, 20, 0x024A0000, supplied_table=True)
    crops = []
    for spec in SPECS:
        x0, y0, x1, y1 = spec["box"]
        uc = machine(arm9)
        view, owner = 0x02480000, 0x02490000
        uc.mem_write(view - 16, b"\xA5" * 80)
        uc.mem_write(view, bytes(48))
        uc.mem_write(STACK, struct.pack("<4I", x1 - x0, y1 - y0, 0, 0))
        executed = call(uc, 0xD3B34, (view, owner, x0, y0))
        if (
            struct.unpack("<I", uc.mem_read(view + 12, 4))[0] != owner
            or struct.unpack("<2I", uc.mem_read(view + 28, 8)) != (x0, y0)
            or struct.unpack("<2I", uc.mem_read(view + 40, 8)) != (x1 - x0, y1 - y0)
            or not {0x020D3B34, 0x020D3ED0, 0x020D41A4} <= executed
            or bytes(uc.mem_read(view - 16, 16)) != b"\xA5" * 16
            or bytes(uc.mem_read(view + 48, 16)) != b"\xA5" * 16
        ):
            raise ValueError("Supplied crop origin/extent/owner/ABI/canary differs")
        crops.append({"id": spec["id"], "supplied_cell": spec["box"], "ABI_canaries": True})
    save(
        OUT / "native.json",
        {
            "status": "pass-controlled-PXL-header-and-four-supplied-crop-contracts",
            "candidate_sha256": saved["candidate_sha256"],
            "controlled_header": header,
            "supplied_crop_constructors": crops,
            "limits": [
                "Source owner/table/crop inputs are supplied; actual Online gallery loading/parent usage/live cropping is not proved.",
                "Actual palette/alpha, GPU presentation, small-letter readability and physical input/gameplay remain pending.",
                "These are static screenshot pixels, not runtime progressive dialogue/font commands.",
            ],
        },
    )
    print("Pass: controlled image header and four supplied crop contracts; actual gameplay pending.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["materialize", "register", "verify", "native"])
    globals()[parser.parse_args().action]()
