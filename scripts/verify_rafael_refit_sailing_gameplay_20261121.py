"""Bind focused playback to the native text, both choices and the wind explanation."""
from types import SimpleNamespace

from scripts import replay_rafael_refit_sailing_lessons_20261121 as replay
from scripts import verify_rafael_refit_sailing_lessons_20261121 as display
from scripts import verify_parallel_ship_lessons_gameplay_20261121 as earlier


stage, base, native = replay.stage, replay.base, replay.native
panel, town = earlier.panel, earlier.town
PROOF = replay.ROOT / "verified_gameplay.json"
QUESTION = "DK4_MES_B180_R0102"
FOLLOWUPS = {"DK4_MES_B180_R0106", "DK4_MES_B180_R0110"}


def caption_bounds(font, picture, label, top):
    ink = {(x, y) for y in range(top, top + 18) for x in range(12, 244)
           if picture.getpixel((x, y)) == (8, 8, 8)}
    matches = []
    for y in range(top, top + 8):
        for x in range(12, 245 - 6 * len(label)):
            try:
                count, extent = panel.complete_mask(font, label, picture, x, y, (8, 8, 8))
            except ValueError:
                continue
            if count == len(ink):
                matches.append(extent)
    if len(matches) == 1:
        return matches[0]
    return None


def main():
    assert not PROOF.exists()
    fixture_path, inputs = (replay.ROOT / name for name in ("fixture.json", "inputs.json"))
    fixture, report, native_report, manuscript = map(base.load, (fixture_path, replay.REPORT, display.PROOF, stage.review.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == fixture["candidate_sha256"] == native_report["candidate_sha256"] == base.digest(stage.ROOT/"clean_rebuilt.nds")
    assert fixture["exact_candidate_inverse"] and fixture["original_branch_selection_replaced"] and not fixture["natural_activation"]
    assert report["ROM_sha256"] == fixture["fixture_sha256"] == base.digest(fixture["fixture"])
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["frames"] == replay.END and report["scripted_input_schedule"] == base.load(inputs)
    assert not report.get("battery_save_preloaded") and not any(v for k, v in report.items() if k.startswith("synthetic_"))
    rom = base.NdsImage.open(stage.ROM)
    arm, font = (rom.read_file(p) for p in (native.ARM, "/GRP/KANJI.FNT"))
    paint = town.clipped_renderer(SimpleNamespace(image=rom, arm=arm))
    name_font = panel.GameAsciiFont.from_arm9(arm)
    archive = native.IlnkContainer.parse(rom.read_file(replay.PATH))
    rows = {r["id"]: r for r in manuscript["records"]}
    checked = {r["id"]: r for r in native_report["records"]}
    captures = {c["frame"]: c for c in report["frames_captured"] if c["path"].endswith("_cold_boot.png")}
    pictures = {t: town.read_frame(captures, t)[1] for t in sorted(captures)}
    masks = {frame: earlier.foreground(pic) for frame, pic in pictures.items()}
    holds, followups, menus, previews = [], [], [], []
    last = 3899
    for span in fixture["copied_native_commands"]:
        ident = span["ids"][0]
        record = checked[ident]
        block, at = span["block"], span["original_offset"]
        raw = bytes.fromhex(record["stored_command_hex"])
        assert block == record["block"] and archive.blocks[block][at:at+len(raw)] == raw
        assert native.digest(raw) == span["command_sha256"]
        if record.get("native_caption"):
            labels = [rows[i]["english"] for i in span["ids"]]
            for frame, picture in pictures.items():
                if frame <= last or picture.getpixel((107, 270)) != (0, 165, 172):
                    continue
                bounds = [caption_bounds(name_font, picture, label, top) for label, top in zip(labels, (267, 287), strict=True)]
                if all(bounds):
                    menus.append(dict(block=block, ids=span["ids"], labels=labels, bounds=bounds,
                                      selected=0, frame=frame, observed=captures[frame]))
                    previews.append((f"Block {block} choice", picture))
                    last = frame
                    break
            else:
                raise AssertionError((block, "no complete retained lesson menu"))
            continue
        if record["decision"] == "retention" and ident not in FOLLOWUPS:
            continue
        if ident in FOLLOWUPS:
            assert record["decision"] == "retention" and raw[:6] in (b"\x00\x40\xff\xff\x00\x6d", b"\x00\x40\xff\xff\x00\x17")
            expanded = raw[6:raw.index(0, 6)]
        else:
            layout = record["layouts"][0]
            expanded = bytes.fromhex(layout["expanded_hex"])
        page, = paint(arm, font, expanded)["pages"]
        pixels = bytes.fromhex(page["native_plane_hex"])
        if ident not in FOLLOWUPS:
            assert [native.digest(pixels)] == layout["pages"]
        expected = bytes(bool(v) for v in pixels)
        for frame, mask in masks.items():
            if frame <= last or mask != expected:
                continue
            picture = pictures[frame]
            assert panel.mask_check(pixels, 216, picture)
            panel.complete_mask(name_font, rows[ident]["speaker"], picture, 16, 277, town.INKS[1])
            proof = dict(id=ident, file_path=replay.PATH, block=block, page=1, frame=frame, observed=captures[frame])
            (followups if ident in FOLLOWUPS else holds).append(proof)
            previews.append((ident, picture))
            last = frame
            break
        else:
            raise AssertionError((ident, "no complete ordered live panel"))
    question, = [r for r in holds if r["id"] == QUESTION]
    assert tuple(r["id"] for r in followups) == ("DK4_MES_B180_R0106", "DK4_MES_B180_R0110")
    assert question["frame"] < followups[0]["frame"] < followups[1]["frame"]
    assert checked[QUESTION]["native_pages"] == 1
    assert len(holds) == 19 and [m["block"] for m in menus] == [179, 180]
    sheets = []
    for start in range(0, len(previews), 6):
        p = replay.ROOT / f"rafael_tutorials_gameplay_{start // 6 + 1}.png"
        town.sheet(previews[start:start+6], p)
        sheets.append(dict(path=str(p), sha256=base.digest(p)))
    evidence = {str(p): base.digest(p) for p in (fixture_path, inputs, replay.REPORT, display.PROOF)}
    evidence[fixture["fixture"]] = fixture["fixture_sha256"]
    base.save(PROOF, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_activation=False,
        exact_native_glyph_matches=True, hardware_verified=False, holds=holds, captions=menus, sheets=sheets,
        uninterrupted_wind_angle_question=question, unchanged_immediate_followups=followups, evidence=evidence))
    print("Matched 19 revised pages, both lesson menus, and the one-page wind question followed by Manuel's reply.")


if __name__ == "__main__":
    main()
