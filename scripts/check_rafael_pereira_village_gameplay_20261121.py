"""Compare the focused emulator transcript with installed glyph masks."""

from types import SimpleNamespace

from scripts import check_rafael_mediterranean_gameplay_20261121 as panel
from scripts import replay_rafael_pereira_village_20261121 as replay
from scripts import verify_rafael_pereira_village_20261121 as native_check


stage, base, native, town = replay.stage, replay.base, replay.native, panel.town
PROOF = replay.ROOT / "verified_gameplay.json"


def main():
    assert not PROOF.exists()
    fixture_path, inputs = (replay.ROOT / part for part in ("fixture.json", "inputs.json"))
    fixture, report, proof, review = map(base.load, (fixture_path, replay.REPORT, native_check.PROOF, stage.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == proof["candidate_sha256"] == fixture["candidate_sha256"] == base.digest(stage.ROOT / "clean_rebuilt.nds")
    assert report["ROM_sha256"] == fixture["fixture_ROM_sha256"] == base.digest(fixture["fixture_ROM"])
    assert fixture["exact_candidate_inverse"] and fixture["original_speech_commands_copied_byte_exact"]
    assert fixture["original_scene_branches_unexecuted"] and not fixture["natural_activation"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and report["frames"] == replay.END
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == base.load(inputs)

    image = base.NdsImage.open(stage.ROM)
    bank = native.IlnkContainer.parse(image.read_file(replay.prior.PATH)).blocks
    assert all(bank[x["block"]][x["actual_block_offset"]:][:len(bytes.fromhex(x["hex"]))].hex() == x["hex"]
               for x in fixture["copied"])
    arm, font = (image.read_file(part) for part in (native.ARM, "/GRP/KANJI.FNT"))
    context = SimpleNamespace(image=image, arm=arm)
    paint, system = town.clipped_renderer(context), town.current_fe_painter(context)
    name_font = panel.panel.GameAsciiFont.from_arm9(arm)
    captures = {x["frame"]: x for x in report["frames_captured"] if x["path"].endswith("_cold_boot.png")}
    renders = {r["id"]: r for r in proof["records"]}
    rows = {r["id"]: r for r in review["records"]}
    holds, pictures, absent = [], [], []
    for (block, index), frame in zip(replay.SEQUENCE, replay.FRAMES[:-1], strict=True):
        ident = f"DK4_MES_B{block}_R{index:04d}"
        row, receipt = rows[ident], renders[ident]
        captured, image = town.read_frame(captures, frame)
        is_fe = row["source_selector"] == 254
        if is_fe:
            assert receipt["retained_system_panel"]
            raw = bytes.fromhex(row["current_hex"])[1:]
            plane = system(raw)["physical"]
            assert native.digest(plane) == receipt["panel_mask_sha256"]
        else:
            if row["decision"] == "revision":
                layout = receipt["layouts"][0]
                assert layout["scope"] == "registered default"
                raw = bytes.fromhex(layout["expanded_hex"])
            else:
                raw = bytes.fromhex(row["current_hex"])[1:]
                assert not any(token in raw for token in (b"FI", b"FA", b"FO"))
            rendered = paint(arm, font, raw)
            assert rendered["complete_consumed_bytes"] == len(raw)
            page, = rendered["pages"]
            plane = bytes.fromhex(page["native_plane_hex"])
            if row["decision"] == "revision":
                assert native.digest(plane) == layout["plane_sha256"]
        if not panel.panel.mask_check(plane, 228 if is_fe else 216, image):
            absent.append((ident, frame))
            continue
        if not is_fe:
            panel.panel.complete_mask(name_font, row["speaker"], image, 16, 277, town.INKS[1])
        holds.append(dict(id=ident, block=block, frame=frame, speaker=row["speaker"], decision=row["decision"],
                          system_FE=is_fe, observed=captured))
        pictures.append((ident, image))
    assert not absent, absent
    final, image = town.read_frame(captures, replay.FRAMES[-1])
    pictures.append(("Return after the focused excerpt", image))
    sheets = []
    for i in range(0, len(pictures), 6):
        path = replay.ROOT / f"pereira_village_gameplay_{i // 6 + 1}.png"
        town.sheet(pictures[i:i + 6], path)
        sheets.append(dict(path=str(path), sha256=base.digest(path)))
    observed = {r["id"] for r in holds}
    base.save(PROOF, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_activation=False,
        exact_native_glyph_matches=True, hardware_verified=False, holds=holds, final_hold=final,
        observed_ids=sorted(observed), original_story_branches_unvisited=True,
        offline_only=[r["id"] for r in rows.values() if r["decision"] == "revision" and r["id"] not in observed],
        sheets=sheets, evidence={str(path): base.digest(path) for path in
                                 (fixture_path, replay.REPORT, inputs, native_check.PROOF, fixture["fixture_ROM"])}))
    print(f"Verified {len(holds)} emulator panels, including the 500,000 military-funds notice.")


if __name__ == "__main__":
    main()
