"""Match Rafael's initialized title-to-dialogue sample against stored records."""
from pathlib import Path
from types import SimpleNamespace

from scripts import replay_parallel_ship_lessons_20261121 as replay
from scripts import verify_hodram_alexandria_tutorial_gameplay_20261121 as alexandria
from scripts import verify_parallel_ship_lessons_20261121 as display


base, native, stage = replay.base, replay.native, replay.stage
panel, town = alexandria.panel, alexandria.town
PROOF = replay.ROOT / "verified_gameplay.json"
FE_ID = "DK4_MES_B177_R0114"
FE_PRIOR = Path("work/analysis/Rafael_B177_B180_ship_body_pixels_v1_20261105/focused_actual_pixels.json")


def foreground(picture, bounds=(16, 296, 232, 360)):
    return bytes(value == town.INKS[0] for value in picture.crop(bounds).get_flattened_data())


def main():
    fixture_path = replay.ROOT / "fixture.json"
    inputs = replay.ROOT / "inputs.json"
    fixture, report, proof, draft = map(base.load, (fixture_path, replay.REPORT, display.PROOF, stage.review.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == fixture["candidate_sha256"] == proof["candidate_sha256"] == base.digest(stage.ROOT / "clean_rebuilt.nds")
    assert fixture["exact_candidate_inverse"] and fixture["original_branch_selection_replaced"]
    assert report["ROM_sha256"] == fixture["fixture_sha256"] == base.digest(fixture["fixture"])
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["frames"] == replay.END and report["scripted_input_schedule"] == base.load(inputs)
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert not report.get("battery_save_preloaded") and not fixture["natural_activation"]
    rom = base.NdsImage.open(stage.ROM)
    arm, font = (rom.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT"))
    paint = town.clipped_renderer(SimpleNamespace(image=rom, arm=arm))
    name_font = panel.GameAsciiFont.from_arm9(arm)
    scope = {row["id"]: row for row in draft["records"] if row["file_path"] == replay.PATH}
    checked = {row["id"]: row for row in proof["records"] if row["file_path"] == replay.PATH}
    captions = [row["id"] for row in checked.values() if row.get("native_caption")]
    captures = {c["frame"]: c for c in report["frames_captured"] if c["path"].endswith("_cold_boot.png")}
    pictures = {frame: town.read_frame(captures, frame)[1] for frame in sorted(captures)}
    masks = {frame: foreground(picture) for frame, picture in pictures.items()}
    holds, previews, breaks, captions_seen = [], [], [], None
    carrier = native.IlnkContainer.parse(rom.read_file(replay.PATH)).blocks[177]
    stored_fe = checked[FE_ID]
    fe_raw = bytes.fromhex(stored_fe["stored_command_hex"])
    assert fe_raw[:6] == b"\x00\x40\xff\xff\x00\xfe"
    old_fe = next(r for r in base.load(FE_PRIOR)["body_pages"] if r["id"] == FE_ID)
    assert fe_raw[6:].split(b"\0", 1)[0].hex() == old_fe["text_hex"]
    fe_cap = old_fe["capture"]
    old_frame = fe_cap["frame"]
    _, old_picture = town.read_frame({old_frame: fe_cap}, old_frame)
    fe_expected = foreground(old_picture)
    last = 3899

    for span in fixture["copied_native_commands"]:
        ident = span["ids"][0]
        record = checked[ident]
        raw = bytes.fromhex(record["stored_command_hex"])
        at = span["original_offset"]
        assert carrier[at:at+len(raw)] == raw and span["command_sha256"] == native.digest(raw)
        if record.get("native_caption"):
            assert span["ids"] == captions
            for frame, picture in pictures.items():
                if frame <= last or picture.getpixel((104, 268)) != (0, 165, 172):
                    continue
                bounds = {name: alexandria.caption_bbox(name_font, picture, name, lo, hi)
                          for name, lo, hi in (("Listen", 267, 286), ("Skip", 287, 306))}
                if all(len(value) == 4 and type(value[0]) is int for value in bounds.values()):
                    captions_seen = dict(ids=captions, selected="Listen", bounds=bounds, observed=captures[frame])
                    previews.append(("Listen / Skip", picture))
                    last = frame
                    break
            assert captions_seen
        elif ident == FE_ID:
            found = next(frame for frame, mask in masks.items() if frame > last and mask == fe_expected)
            assert pictures[found].getpixel((10, 279)) == old_picture.getpixel((10, 279))
            breaks.append(dict(id=ident, observed=captures[found], exact_prior_body_mask=True))
            previews.append(("Extra armor notice", pictures[found]))
            last = found
        elif record["decision"] == "revision":
            first = record["layouts"][0]
            expanded = bytes.fromhex(first["expanded_hex"])
            results = paint(arm, font, expanded)["pages"]
            for page_number, result in enumerate(results, 1):
                pixels = bytes.fromhex(result["native_plane_hex"])
                assert native.digest(pixels) == first["pages"][page_number - 1]
                expected = bytes(bool(value) for value in pixels)
                for frame, mask in masks.items():
                    if frame <= last or mask != expected:
                        continue
                    picture = pictures[frame]
                    assert panel.mask_check(pixels, 216, picture)
                    panel.complete_mask(name_font, scope[ident]["speaker"], picture, 16, 277, town.INKS[1])
                    holds.append(dict(id=ident, page=page_number, file_path=replay.PATH, frame=frame, observed=captures[frame]))
                    previews.append((f"{ident} p{page_number}", picture))
                    last = frame
                    break
                else:
                    raise AssertionError((ident, page_number, "no ordered complete live page"))
    assert len(breaks) == 1 and captions_seen
    assert [h["page"] for h in holds if h["id"] == "DK4_MES_B177_R0180"] == [1, 2]
    sheets = []
    for start in range(0, len(previews), 6):
        path = replay.ROOT / f"rafael_gameplay_{start//6+1}.png"
        town.sheet(previews[start:start+6], path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    seen = {(h["file_path"], h["id"]) for h in holds} | {(replay.PATH, i) for i in captions}
    offline = [(r["file_path"], r["id"]) for r in proof["records"] if r["decision"] == "revision"
               and (r["file_path"], r["id"]) not in seen]
    base.save(PROOF, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_activation=False,
        exact_native_glyph_matches=True, hardware_verified=False, holds=holds, captions=captions_seen,
        extra_armor_notice=breaks[0], sheets=sheets, offline_only=offline,
        evidence={str(p): base.digest(p) for p in (fixture_path, replay.REPORT, inputs, display.PROOF, FE_PRIOR)}))
    print(f"Matched {len(holds)} revised live pages, both captions, and the original extra-armor notice.")


if __name__ == "__main__":
    main()
