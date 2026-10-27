"""Reuse the menu gold logo in opening copies; keep the broader goal paused."""

import argparse
import copy
import json
import zlib
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts import title_logo_matte_v188 as matte
from scripts import title_restyle_v186 as prior_art
from scripts.build_integrated_release import (
    CANONICAL_BASELINE_SHA256,
    RELEASE_STACK_PATH,
    accepted_batch_paths,
    apply_fls_indexed_region_batch,
    apply_pxl_indexed_region_batch,
    load_release_stack,
    resolve_release_batches,
    rom_files,
    verify_golden_content,
)
from scripts.rota_title_copies_v175 import nearest

PRIOR = Path("out/all_routes_combined_v187_candidate.nds")
PRIOR_SHA = "a04d405c5e2de45d268dd999d8de65e260c0d1746c32d022b1d5f88d7c9b638e"
CANDIDATE = Path("out/all_routes_combined_v188_candidate.nds")
PROFILE = "all-routes-unified-v188"
OUT = Path("work/qa/title_edges_v188")
PROOF = Path("work/analysis/title_edges_v188_saved_proof.json")
PXL_PATH = "/_pxl/logo.pxl"
FLS_PATH = prior_art.FLS_PATH
PXL_BATCH = Path("translations/rota_title_logo_art_v4.json")
FLS_BATCH = Path("translations/opening_m28_title_art_v4.json")
LOGO_BOX = [4, 50, 252, 148]
ASSET = Path("translations/assets/menu_gold_logo_v188.png")


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replacements():
    return {
        "translations/rota_title_logo_art_v3.json": PXL_BATCH.as_posix(),
        "translations/opening_m28_title_art_v3.json": FLS_BATCH.as_posix(),
    }


@lru_cache(maxsize=1)
def gold_asset():
    return matte.gold()


def project_gold(palette):
    asset = gold_asset()
    water = matte.assets()[3]
    lookup = {}
    pixels = bytearray(256 * 64)
    for i in range(256 * 64):
        r, g, b, alpha = asset.getpixel((i % 256, i // 256))
        if not alpha:
            continue
        bg = water.getpixel((i % 256, i // 256 + 84))[:3]
        rgb = tuple(round((c * alpha + d * (255 - alpha)) / 255) for c, d in zip((r, g, b), bg))
        if rgb not in lookup:
            lookup[rgb] = nearest(palette, rgb)
        pixels[i] = lookup[rgb]
    return pixels


@lru_cache(maxsize=1)
def menu_wordmark():
    return matte.blue()


def project_wordmark(palette, width, height):
    word = menu_wordmark()
    black = nearest(palette, (0, 0, 0))
    pixels = bytearray([black]) * (width * height)
    lookup = {}
    ox = (width - word.width) // 2
    water = matte.assets()[3]
    for y in range(word.height):
        for x in range(word.width):
            r, g, b, alpha = word.getpixel((x, y))
            if alpha:
                bg = water.getpixel((x + 40, y + 50))[:3]
                rgb = tuple(
                    round((c * alpha + d * (255 - alpha)) / 255) for c, d in zip((r, g, b), bg)
                )
                if rgb not in lookup:
                    lookup[rgb] = nearest(palette, rgb)
                pixels[y * width + x + ox] = lookup[rgb]
    return pixels


def expected_pxl():
    base, _ = prior_art.sources()
    original = PxlImage.from_bytes(base.read_file(PXL_PATH))
    result = PxlImage.from_bytes(prior_art.targets()[PXL_PATH])
    # Replace the complete opening composition, not only the pronunciation caption.
    x0, y0, x1, y1 = LOGO_BOX
    background_index = nearest(original.palette, (0, 0, 0))
    for y in range(y0, y1):
        result.indices[y * 256 + x0 : y * 256 + x1] = bytes([background_index]) * (x1 - x0)
    pixels = project_wordmark(original.palette, 248, 49)
    for y in range(49):
        result.indices[(y + 50) * 256 + 4 : (y + 50) * 256 + 252] = pixels[y * 248 : (y + 1) * 248]
    gold = project_gold(original.palette)
    for y in range(64):
        for x in range(256):
            if gold[y * 256 + x]:
                result.indices[(y + 84) * 256 + x] = gold[y * 256 + x]
    return result


def materialize():
    base, _ = prior_art.sources()
    OUT.mkdir(parents=True, exist_ok=True)
    gold_asset().save(ASSET)
    menu_wordmark().save(OUT / "menu_wordmark.png")
    original = PxlImage.from_bytes(base.read_file(PXL_PATH))
    result = expected_pxl()
    box = LOGO_BOX
    source_region = bytes(
        original.indices[y * 256 + x] for y in range(box[1], box[3]) for x in range(box[0], box[2])
    )
    payload = bytes(
        result.indices[y * 256 + x] for y in range(box[1], box[3]) for x in range(box[0], box[2])
    )
    save(
        PXL_BATCH,
        {
            "format": "dk4-pxl-indexed-region-batch-v1",
            "file_path": PXL_PATH,
            "source_file_sha256": sha(original.source),
            "target_locale": "en-US",
            "scope": "Complete opening title composition with approved blue wordmark and menu-derived gold logo; white outer fringe omitted.",
            "records": [
                {
                    "id": "DK4_ROTA_LOGO_COMPLETE_V3",
                    "box": box,
                    "source_region_sha256": sha(source_region),
                    "indices_zlib_hex": zlib.compress(payload).hex(),
                    "indices_sha256": sha(payload),
                    "english": "Uncharted Waters IV / Rota Nova",
                    "artwork_proof": {
                        "gold_asset": str(ASSET),
                        "gold_asset_sha256": sha(ASSET.read_bytes()),
                        "wordmark_asset_sha256": prior_art.ASSET_SHA,
                        "matte": "gold soft alpha recovered from canonical menu/background difference; blue menu face shades with soft edges; both matted against opening water",
                        "original_alpha_claimed": False,
                    },
                }
            ],
        },
    )
    batch = json.loads(prior_art.FLS_BATCH.read_text(encoding="utf-8"))
    archive = FlsArchive(base.read_file(FLS_PATH))
    box = prior_art.FLS_BOXES[4]
    main = bytes(project_wordmark(archive.texture(4).palette, box[2] - box[0], box[3] - box[1]))
    batch["records"][0].update(
        indices_zlib_hex=zlib.compress(main).hex(),
        indices_sha256=sha(main),
        artwork_proof={"menu_face_colors_reused": True, "edges_matted_against_opening_water": True},
    )
    payload = bytes(project_gold(archive.texture(5).palette))
    row = batch["records"][1]
    row.update(
        box=[0, 0, 256, 64],
        indices_zlib_hex=zlib.compress(payload).hex(),
        indices_sha256=sha(payload),
        english=["Rota Nova"],
        artwork_proof={
            "gold_asset": str(ASSET),
            "gold_asset_sha256": sha(ASSET.read_bytes()),
            "complete_menu_gold_logo_reused": True,
            "duplicate_caption_omitted": True,
        },
    )
    save(FLS_BATCH, batch)
    check_assets(targets())
    opening = result.render()
    black = nearest(result.palette, (0, 0, 0))
    opening.putalpha(
        Image.frombytes("L", (256, 192), bytes(0 if i == black else 255 for i in result.indices))
    )
    # Background projection is illustrative, not a native video/UV proof.
    background = archive.texture(2).render().resize((256, 192), Image.Resampling.BILINEAR)
    preview = Image.alpha_composite(background, opening)
    preview.save(OUT / "opening_preview.png")
    preview.resize((768, 576), Image.Resampling.NEAREST).save(OUT / "opening_preview_large.png")
    menu = PxlImage.from_bytes(prior_art.targets()["/_pxl/title/title03.pxl"]).render()
    review = Image.new("RGB", (1040, 412), "#303030")
    d = ImageDraw.Draw(review)
    for col, (label, im) in enumerate(
        (("Opening on water; offline preview", preview), ("Menu; unchanged", menu))
    ):
        d.text((8 + 520 * col, 8), label, fill="white")
        review.paste(
            im.resize((512, 384), Image.Resampling.NEAREST).convert("RGB"), (8 + col * 520, 24)
        )
    review.save(OUT / "comparison.png")
    save(
        OUT / "evidence.json",
        {
            "visual_review": False,
            "native_display_verified": False,
            "matte_is_color_derived": True,
            "broader_graphics_goal_status": "paused",
        },
    )
    print(
        "Prepared cleaned soft gold edges and blue menu shading against opening water; menu unchanged."
    )


def targets():
    base, _ = prior_art.sources()
    return {
        PXL_PATH: apply_pxl_indexed_region_batch(PXL_BATCH, base.read_file(PXL_PATH))[0],
        FLS_PATH: apply_fls_indexed_region_batch(FLS_BATCH, base.read_file(FLS_PATH))[0],
    }


def check_assets(result):
    prior_art.sources()
    previous = NdsImage.open(PRIOR)
    p = PxlImage.from_bytes(result[PXL_PATH])
    old = PxlImage.from_bytes(previous.read_file(PXL_PATH))
    assert p.source[: p.pixels_offset] == old.source[: old.pixels_offset], "PXL header/palette"
    assert p.indices == expected_pxl().indices, "Complete expected wordmark/gold composition"
    x0, y0, x1, y1 = LOGO_BOX
    assert all(
        p.indices[i] == old.indices[i]
        for i in range(len(p.indices))
        if not (x0 <= i % 256 < x1 and y0 <= i // 256 < y1)
    ), "Unowned PXL pixels"
    f, before = FlsArchive(result[FLS_PATH]), FlsArchive(previous.read_file(FLS_PATH))
    assert f.records == before.records, "Movie records and dimensions"
    assert f.texture(5).indices == project_gold(f.texture(5).palette), "Complete gold texture"
    main = before.texture(4).indices.copy()
    x0, y0, x1, y1 = prior_art.FLS_BOXES[4]
    payload = project_wordmark(f.texture(4).palette, x1 - x0, y1 - y0)
    for y in range(y0, y1):
        main[y * 256 + x0 : y * 256 + x1] = payload[(y - y0) * (x1 - x0) : (y - y0 + 1) * (x1 - x0)]
    assert f.texture(4).indices == main, "Soft menu wordmark complete"
    slots = [
        (f.data_offset + f.records[i][4], f.data_offset + f.records[i][4] + f.records[i][5])
        for i in (4, 5)
    ]
    pos = 0
    for start, end in slots:
        assert f.source[pos:start] == before.source[pos:start], (
            "Other movie bytes/palettes/textures"
        )
        pos = end
    assert f.source[pos:] == before.source[pos:], "Other movie bytes/textures"
    assert sha(prior_art.BASE.read_bytes()) == CANONICAL_BASELINE_SHA256
    return {
        "opening_gold_reuses_menu_source": True,
        "PXL_header_palette_unowned_exact": True,
        "FLS_records_palette_all_other_movie_bytes_exact": True,
        "native_display_verified": False,
    }


def register():
    assert json.loads((OUT / "evidence.json").read_text())["visual_review"]
    stack = load_release_stack()
    profile = copy.deepcopy(stack["profiles"]["all-routes-unified-v187"])
    replacements_ = replacements()
    assert all(profile["batches"].count(k) == 1 for k in replacements_)
    profile["batches"] = [replacements_.get(p, p) for p in profile["batches"]]
    profile.update(
        description="Full V187 stack; cleaned gold cutout and water-matted soft edges with menu blue shading.",
        note="Focused title correction only; broader graphics goal paused. Menu title/scenery/copyright and runtime rendering unchanged. Experimental.",
    )
    stack["profiles"][PROFILE] = profile
    save(RELEASE_STACK_PATH, stack)


def verify():
    assert sha(PRIOR.read_bytes()) == PRIOR_SHA
    base, _ = prior_art.sources()
    previous, new = NdsImage.open(PRIOR), NdsImage.open(CANDIDATE)
    cases = check_assets({p: new.read_file(p) for p in (PXL_PATH, FLS_PATH)})
    assert all(new.read_file(p) == v for p, v in targets().items())
    old = json.loads(PRIOR.with_suffix(".manifest.json").read_text())
    manifest = json.loads(CANDIDATE.with_suffix(".manifest.json").read_text())
    stack = load_release_stack()
    assert manifest["candidate_sha256"] == sha(CANDIDATE.read_bytes())
    assert manifest["base_sha256"] == CANONICAL_BASELINE_SHA256 and manifest["profile"] == PROFILE
    assert manifest["release_stack_sha256"] == sha(RELEASE_STACK_PATH.read_bytes())
    assert manifest["batches"] == [str(p) for p in resolve_release_batches(PROFILE, [], stack)]
    assert manifest["batches"] == [
        str(Path(replacements().get(Path(p).as_posix(), Path(p).as_posix())))
        for p in old["batches"]
    ]
    assert len(manifest["batches"]) == 463
    assert manifest["required_batches"] == [str(p) for p in accepted_batch_paths(stack)]
    assert manifest["relocations"] == old["relocations"] and all(manifest["checks"].values())
    assert manifest["changed_paths"] == old["changed_paths"]
    assert manifest["changed_records"] == old["changed_records"], "All inherited record IDs"
    before, after = rom_files(previous), rom_files(new)
    changed = sorted(p for p in before if before[p] != after[p])
    assert changed == sorted([PXL_PATH, FLS_PATH]), changed
    repro = Path("work/analysis/v187_soft_edges_reproduction.nds")
    assert sha(repro.read_bytes()) == PRIOR_SHA
    verify_golden_content(base, new)
    clean = Path("work/clean.nds")
    assert (
        sha(clean.read_bytes())
        == "f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d"
    )
    patch = CANDIDATE.with_suffix(".xdelta")
    make_xdelta(clean, CANDIDATE, patch)
    reconstruction = Path("work/analysis/title_v188_patch_reconstruction.nds")
    apply_xdelta(clean, patch, reconstruction)
    assert reconstruction.read_bytes() == CANDIDATE.read_bytes()
    save(
        PROOF,
        {
            "status": "pass-saved-v188-soft-opening-logo-edges",
            "cases": cases,
            "candidate": str(CANDIDATE),
            "candidate_sha256": sha(CANDIDATE.read_bytes()),
            "canonical_base": str(prior_art.BASE),
            "canonical_base_sha256": CANONICAL_BASELINE_SHA256,
            "profile": PROFILE,
            "experimental": True,
            "batch_count": 463,
            "changed_paths_vs_v187": changed,
            "changed_paths_vs_canonical": manifest["changed_paths"],
            "prior_v187_reproduction_exact": True,
            "terminal_stages_and_unrelated_records_retained": True,
            "ARM9_sha256": sha(new.read_file("/__arm9__.bin")),
            "patch": str(patch),
            "patch_sha256": sha(patch.read_bytes()),
            "patch_reconstruction_exact": True,
            "gold_asset_sha256": sha(ASSET.read_bytes()),
            "native_display_verified": False,
            "matte_is_color_derived": True,
            "broader_graphics_goal_status": "paused",
        },
    )
    print(
        "Verified complete V188 stack, two opening assets, unchanged menu and exact patch reconstruction."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["materialize", "register", "verify"])
    globals()[parser.parse_args().action]()
