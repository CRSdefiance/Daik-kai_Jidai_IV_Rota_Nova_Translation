"""Verify item category wording, native rendering and the focused Gallery visit."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import unpack

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import audit_ceuta_lesson_20261119 as boot
from scripts import replay_item_category_labels_20261119 as play
from scripts import stage_item_category_labels_20261119 as build
from scripts.stage_source_item_cards_and_coin_v1 import DIRECTORY_OFFSET, TABLE_OFFSET, make_execute, oracle
from scripts.verify_all_items_gallery_v535 import glyph_pixels
from scripts.verify_item_interface_research import glyph_codes

base, native = build.base, build.native
ROOT = build.ROOT / "verification"
PROOF, LIVE = ROOT / "native_item_category.json", ROOT / "item_gallery_replay.json"
STARTUP = build.ROOT / "own_startup_verification.json"
FONT = "/GRP/KANJI.FNT"


def native_items():
    assert not PROOF.exists()
    stage = base.load(build.PROOF)
    old, current = map(base.NdsImage.open, (build.parent.ROM, build.ROM))
    before, arm = [im.read_file(build.ARM) for im in (old, current)]
    common, font = [current.read_file(p) for p in (build.COMMON, FONT)]
    assert all(old.read_file(p) == current.read_file(p) for p in (build.COMMON, FONT))
    assert base.digest(build.ROM) == stage["candidate_sha256"]
    draw_old, draw = [make_execute(native.digest(a[DIRECTORY_OFFSET:TABLE_OFFSET]), a) for a in (before, arm)]
    expected_pixels, _ = oracle()
    labels = stage["records"]
    index = {r["current_reference"]["runtime_pointer"]: r for r in labels}
    special = build.word(arm, 0x102E40) - build.BASE
    ids = [(n, arm[0x11E210 + 24 * n + 16] if n < 188 else arm[special + 24 * (n - 188) + 16])
           for n in range(218)]
    representatives = set()
    for category in set(cat for _, cat in ids):
        representatives.add(next(n for n, cat in ids if cat == category))
    views, cases = [], []
    for ident, category in ids:
        if category and ident not in representatives:
            continue
        for page, config in (("main", (0, 4)), ("standalone", (0, 1))):
            for mode in (4, 16):
                settings = dict(item_page=page, item_case=config, surface_size=(240, 96),
                                kanji_font=font, mode=mode, item_resource_index=ident, item_common=common)
                new = draw(arm, "fixture", **settings)
                baseline = draw_old(before, "fixture", **settings)
                row, = (d for d in new["item_draws"] if (d["x"], d["y"]) == (0, 12))
                original, = (d for d in baseline["item_draws"] if (d["x"], d["y"]) == (0, 12))
                review = index[row["pointer"]]
                assert review is labels[category] and row["text"].strip() == review["english"]
                assert original["text"].strip() == review["previous_English"]
                assert [{**d, "text": row["text"]} if d == original else d for d in baseline["item_draws"]] == new["item_draws"]
                assert new["item_actual_common_ids"] == baseline["item_actual_common_ids"]
                events = new["glyph_events"]
                assert [g["code"] for g in events] == [c for d in new["item_draws"]
                                                       for c in glyph_codes(d["text"], d["tracking"])]
                assert all(0 <= g["x"] <= 234 and 0 <= g["y"] <= 84 for g in events)
                assert new["pixels"] == expected_pixels(arm, font, events, mode, background=0)
                stride = 256 * (2 if mode == 16 else 1)
                if mode == 4:
                    stride //= 2
                width_bytes = 88 * stride // 256
                if category:
                    assert new["pixels"] == baseline["pixels"]
                else:
                    assert new["pixels"] != baseline["pixels"]
                    for at, (a, b) in enumerate(zip(new["pixels"], baseline["pixels"], strict=True)):
                        if a != b:
                            y, x = divmod(at, stride)
                            assert 12 <= y < 24 and x < width_bytes
                cases.append(dict(item_ID=ident, category=review["id"], page=page, mode=mode,
                                  actual_native_row=row, complete_native_ink_sha256=native.digest(new["pixels"])))
                if mode == 16 and (ident in (0, 19) or category and ident in representatives):
                    pixels = unpack("<49152H", new["pixels"])
                    canvas = Image.new("L", (256, 192))
                    canvas.putdata([0 if pixel else 245 for pixel in pixels])
                    views.append((f"{ident} {page} - {row['text'].strip()}", canvas.crop((0, 0, 240, 96))))
    assert sum(r["category"] == "ITEM_CATEGORY_00" for r in cases) == 80
    assert len(cases) == 124 and {cat for _, cat in ids} == set(range(13)) - {11}
    ROOT.mkdir(exist_ok=True)
    sheets = []
    for start in range(0, len(views), 8):
        group = views[start:start + 8]
        sheet = Image.new("RGB", (980, 214 * ((len(group) + 1) // 2)), "#263238")
        pen = ImageDraw.Draw(sheet)
        for i, (label, panel) in enumerate(group):
            x, y = 490 * (i % 2), 214 * (i // 2)
            pen.text((x + 4, y + 2), label, fill="white")
            sheet.paste(panel.resize((480, 192), Image.Resampling.NEAREST), (x + 4, y + 18))
        path = ROOT / f"native_categories_{start // 8 + 1}.png"
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    base.save(PROOF, dict(candidate_sha256=stage["candidate_sha256"], staged_sha256=base.digest(build.PROOF),
        cases=cases, sheets=sheets, category_11_no_stock_item_usage=True,
        category_11_exact_unchanged_slot=True, both_native_item_consumers=True,
        other_pixels_and_parameters_exact=True, actual_gameplay=False))
    print("124 complete native item renders passed, including 80 Source Item cases.")


def gallery():
    assert not LIVE.exists()
    prepared = base.load(build.PROOF)
    terminal = base.load(play.GALLERY / "terminal.json")
    report = base.load(terminal["report"])
    assert base.digest(terminal["report"]) == terminal["report_sha256"]
    assert report["ROM_sha256"] == prepared["candidate_sha256"] == base.digest(build.ROM)
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    fixture, = report["synthetic_gallery_fixtures"]
    assert not fixture["earned_unlock_verified"] and fixture["manifest_sha256"] == base.digest(fixture["preloaded_save_manifest"])
    image = base.NdsImage.open(build.ROM)
    arm = image.read_file(build.ARM)
    font = GameAsciiFont.from_arm9(arm)
    files = {r["frame"]: r for r in report["frames_captured"]}
    expected = glyph_pixels(font, b"", (), "Source Item", 8, 65)
    category = (8, 64, 96, 76)
    observations = []
    for frame, name in ((2800, "Pumpkin Seeds"), (3000, "Tomato Seedling")):
        capture = files[frame]
        assert base.digest(capture["path"]) == capture["PNG_sha256"]
        with Image.open(capture["path"]) as screen:
            rgb = screen.convert("RGB")
        assert expected == {(x, y) for y in range(category[1], category[3])
                            for x in range(category[0], category[2]) if rgb.getpixel((x, y)) == (230, 230, 230)}
        name_pixels = glyph_pixels(font, b"", (), name, 56, 25)
        assert name_pixels == {(x, y) for y in range(24, 36) for x in range(56, 248)
                               if rgb.getpixel((x, y)) == (230, 230, 230)}
        observations.append(capture | dict(item=name, complete_category_pixels=len(expected)))
    returned = files[3350]
    assert base.digest(returned["path"]) == returned["PNG_sha256"]
    with Image.open(returned["path"]) as final:
        rgb = final.convert("RGB")
    for label, x, y in (("Items", 113, 253), ("Ruins", 113, 273),
                        ("Characters", 98, 293), ("Event Scenes", 92, 313)):
        wanted = glyph_pixels(font, b"", (), label, x, y, advance=6)
        assert wanted == {(u, v) for v in range(y, y + 11) for u in range(92, 164)
                          if rgb.getpixel((u, v)) == (8, 8, 8)}
    assert rgb.getpixel((92, 253)) == (0, 165, 172)
    ROOT.mkdir(exist_ok=True)
    base.save(LIVE, dict(candidate_sha256=report["ROM_sha256"], observed=observations,
        returned=returned, complete_gallery_menu_labels_after_back=True, gallery_unlock_fixture=fixture,
        evidence={terminal["report"]: terminal["report_sha256"],
                  fixture["preloaded_save_manifest"]: fixture["manifest_sha256"]}, hardware=False))
    print("The revised category rendered completely on two actual Gallery items and Back returned to the Gallery menu.")


def startup():
    source = getsource(boot.startup).replace("proof['predecessor_sha256']", "proof['previous_sha256']")
    scope = vars(boot) | {"play": play, "build": build, "STARTUP": STARTUP, "__file__": __file__}
    exec(compile(source, __file__ + "::same-startup-contract", "exec"), scope)
    scope["startup"]()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("native_items", "gallery", "startup"))
    globals()[parser.parse_args().action]()
