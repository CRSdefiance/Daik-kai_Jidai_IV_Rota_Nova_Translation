"""Verify revised pages, nameplates, menu captions, and the actual port return."""
from pathlib import Path
from types import SimpleNamespace

from scripts import replay_hodram_alexandria_tutorial_20261121 as replay
from scripts import verify_alexandria_voyage_20261121 as town_replay
from scripts import verify_hodram_alexandria_tutorial_20261121 as display
from scripts import verify_lisbon_seoul_trend_gameplay_20261121 as panel


stage, base, native, town = replay.stage, replay.base, replay.stage.native, panel.town
PROOF = replay.ROOT / "verified_tutorial.json"


def caption_bbox(font, picture, body, y_min, y_max):
    color = (8, 8, 8)
    x_min, x_max = 100, 156
    ink = {(x, y) for y in range(y_min, y_max) for x in range(x_min, x_max) if picture.getpixel((x, y)) == color}
    matches = []
    for y in range(y_min, y_max - 10):
        for x in range(x_min, x_max - 6 * len(body) + 1):
            try:
                count, extent = panel.complete_mask(font, body, picture, x, y, color)
            except ValueError:
                continue
            if len(ink) == count:
                matches.append(extent)
    return matches[0] if len(matches) == 1 else matches


def main():
    assert not PROOF.exists()
    stored, draft, report, before, scope = map(base.load, (
        display.PROOF, stage.review.OUTPUT, replay.REPORT, replay.BASELINE, replay.ROOT / "replay_scope.json"))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == report["ROM_sha256"] == base.digest(stage.ROOT / "clean_rebuilt.nds")
    assert base.digest(replay.BASELINE) == scope["predecessor_report_sha256"]
    prior_coverage = base.load(stage.review.arrival.OUTPUT)
    assert before["ROM_sha256"] == prior_coverage["candidate_sha256"]
    assert draft["source_gameplay_sha256"] == base.digest(stage.review.arrival.OUTPUT)
    donor = base.load(stage.review.arrival.run.ROOT / "source_save.json")
    for run in (before, report):
        town_replay.check_report(run, donor)
    schedule = base.load(replay.ROOT / "inputs.json")
    assert schedule == report["scripted_input_schedule"] and scope["expected_return"] == report["frames"]
    shared = scope["original_inputs_through_menu"]
    assert schedule[:shared] == before["scripted_input_schedule"][:shared]
    assert all(row["buttons"] == ["A"] and row["start"] > replay.MENU for row in schedule[shared:])
    rom = base.NdsImage.open(stage.ROM)
    arm, font = (rom.read_file(path) for path in (native.ARM, "/GRP/KANJI.FNT"))
    paint = town.clipped_renderer(SimpleNamespace(image=rom, arm=arm))
    name_font = panel.GameAsciiFont.from_arm9(arm)
    snapshot = report["read_only_RAM_snapshot"]
    raw = Path(snapshot["path"]).read_bytes()
    assert snapshot["read_only_export"] and native.digest(raw) == snapshot["sha256"]
    cpu, get = town.get_machine(arm, raw)
    assert get(0x7F244) == 1 and get(0xB65E4) == 25
    assert bytes(cpu.mem_read(town.B, 0x400000)) == raw
    captured = {row["frame"]: row for row in report["frames_captured"] if row["path"].endswith("_cold_boot.png")}
    old_frames = {row["frame"]: row for row in before["frames_captured"] if row["path"].endswith("_navigation.png")}
    pictures = {frame: town.read_frame(captured, frame)[1] for frame in captured}
    masks = {frame: bytes(value == town.INKS[0] for value in picture.crop((16, 296, 232, 360)).get_flattened_data())
             for frame, picture in pictures.items()}
    for frame in (8980, 11020):
        old, _ = town.read_frame(old_frames, frame)
        assert old["framebuffer_sha256"] == captured[frame]["framebuffer_sha256"]

    holds, previews = [], []
    rows = {row["id"]: row for row in draft["records"]}
    for row in stored["records"]:
        if row["decision"] != "revision" or row.get("native_caption"):
            continue
        ident = row["id"]
        layout = row["layouts"][0]
        assert layout["scope"] == "registered default"
        body = bytes.fromhex(layout["expanded_hex"])
        pages = paint(arm, font, body)["pages"]
        assert len(pages) == row["native_pages"]
        at = 0
        for index, page in enumerate(pages):
            raster = bytes.fromhex(page["native_plane_hex"])
            assert native.digest(raster) == layout["pages"][index]
            expected = bytes(bool(v) for v in raster)
            for frame, picture in sorted(pictures.items()):
                if frame <= at or masks[frame] != expected:
                    continue
                try:
                    panel.complete_mask(name_font, rows[ident]["speaker"], picture, 16, 277, town.INKS[1])
                except ValueError:
                    continue
                assert panel.mask_check(raster, 216, picture)
                at = frame
                holds.append(dict(id=ident, file_path=row["file_path"], page=index + 1, frame=frame, observed=captured[frame]))
                previews.append((f"{ident} p{index + 1}", picture))
                break
            else:
                raise AssertionError((ident, index + 1, "no exact live page"))

    menu = pictures[replay.MENU]
    choices = {label: caption_bbox(name_font, menu, label, lo, hi)
               for label, lo, hi in (("Listen", 267, 286), ("Skip", 287, 306))}
    assert all(len(r) == 4 and type(r[0]) is int for r in choices.values()), choices
    old_menu, _ = town.read_frame(old_frames, replay.MENU)
    old_last, _ = town.read_frame(old_frames, replay.RETURN)
    end = scope["expected_return"]
    assert captured[end]["framebuffer_sha256"] == old_last["framebuffer_sha256"]
    assert len(holds) == stored["newly_rendered_pages"]
    previews.extend((("Listen and Skip", menu), ("Return to Alexandria Port", pictures[end])))
    sheets = []
    for start in range(0, len(previews), 6):
        p = replay.ROOT / f"hodram_alexandria_gameplay_{start//6+1}.png"
        town.sheet(previews[start:start+6], p)
        sheets.append(dict(path=str(p), sha256=base.digest(p)))
    evidence = (display.PROOF, replay.REPORT, replay.BASELINE, stage.review.arrival.OUTPUT, replay.ROOT / "replay_scope.json")
    base.save(PROOF, dict(candidate_sha256=candidate, exact_native_glyph_matches=True, natural_activation=True,
        hardware_verified=False, holds=holds, sheets=sheets, original_port_transition=True,
        original_port_transition_frame=captured[end], original_port_transition_exact_to_predecessor=True,
        menu=dict(previous=old_menu, revised=captured[replay.MENU], bounds=choices, selected="Listen"),
        unvisited={"path": "Skip", "speech_ids": ["DK4_MES_B167_R0104", "DK4_MES_B167_R0108"]},
        read_only_snapshot=snapshot, evidence={str(p): base.digest(p) for p in evidence}))
    print(f"Matched {len(holds)} revised pages, both exact captions, and the original Alexandria Port return.")


if __name__ == "__main__":
    main()
