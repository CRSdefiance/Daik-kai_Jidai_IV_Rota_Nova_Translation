"""Compare selected emulator pages and nameplates with exact native glyph masks."""

from types import SimpleNamespace

from scripts import check_rafael_mediterranean_gameplay_20261121 as panel
from scripts import replay_rafael_east_asia_followup_20261121 as replay
from scripts import verify_rafael_east_asia_followup_20261121 as native_check


stage, base, native, town = replay.stage, replay.base, replay.native, panel.town
PROOF = replay.ROOT / "verified_gameplay.json"
REPLAY_STAGE = stage.ROOT.with_name("staged_v1")
REPLAY_ROOT = REPLAY_STAGE / "focused_gameplay"
REPORT = REPLAY_ROOT / "capture/capture_report.json"
REFERENCE_STAGE = stage.ROOT.with_name("staged_v3")
REFERENCE_GAMEPLAY = REFERENCE_STAGE / "focused_gameplay/verified_gameplay.json"


def qualify_fixture(fixture, image, candidate):
    latest = base.load(stage.PROOF)
    assert latest["candidate_sha256"] == candidate
    final = native.IlnkContainer.parse(image.read_file(replay.prior.PATH)).blocks
    groups = latest["groups"]
    by_source = {(g["block"], c["source_offset"]): c for g in groups for c in g["commands"]}
    assert fixture["candidate_sha256"] == candidate
    by_position = {(g["block"], c["stored_offset"]): c for g in groups for c in g["commands"]}
    for copy in fixture["copied"]:
        block = copy["block"]
        original = by_position[block, copy["actual_block_offset"]]
        target = by_source[block, original["source_offset"]]
        offset, raw = target["stored_offset"], bytes.fromhex(copy["hex"])
        assert original["stored"] == target["stored"] == copy["hex"]
        assert final[block][offset:offset + len(raw)] == raw
    assert final[44][8:40].hex() == fixture["original_prelude"]


def check_excerpt(report_path, inputs, sequence, scheduled_frames, end, stem, proof, rows, image, candidate):
    fixture_path = report_path.parent.parent / "fixture.json"
    fixture, report = map(base.load, (fixture_path, report_path))
    assert report["ROM_sha256"] == fixture["fixture_ROM_sha256"] == base.digest(fixture["fixture_ROM"])
    assert fixture["exact_candidate_inverse"] and fixture["original_speech_commands_copied_byte_exact"]
    assert fixture["original_scene_branches_unexecuted"] and not fixture["natural_activation"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not report.get("battery_save_preloaded") and report["frames"] == end
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert report["scripted_input_schedule"] == base.load(inputs)
    qualify_fixture(fixture, image, candidate)

    arm, font = (image.read_file(part) for part in (native.ARM, "/GRP/KANJI.FNT"))
    paint = town.clipped_renderer(SimpleNamespace(image=image, arm=arm))
    name_font = panel.panel.GameAsciiFont.from_arm9(arm)
    captures = {x["frame"]: x for x in report["frames_captured"] if x["path"].endswith("_cold_boot.png")}
    renders = {r["id"]: r for r in proof["records"]}
    frames = iter(scheduled_frames)
    holds, pictures = [], []
    for block, index in sequence:
        ident = f"DK4_MES_B{block}_R{index:04d}"
        row, receipt = rows[ident], renders[ident]
        assert row["source_selector"] < 207
        if row["decision"] == "revision":
            layout = receipt["layouts"][0]
            assert layout["scope"] == "registered default"
            raw = bytes.fromhex(layout["expanded_hex"])
        else:
            encoded = bytes.fromhex(row["current_hex"])[1:].decode("ascii")
            raw = stage.review.TOKEN.sub(lambda m: proof["default_names"][m[0]], encoded).encode("ascii")
        rendered = paint(arm, font, raw)
        assert rendered["complete_consumed_bytes"] == len(raw)
        for number, page in enumerate(rendered["pages"], 1):
            frame = next(frames)
            captured, shown = town.read_frame(captures, frame)
            plane = bytes.fromhex(page["native_plane_hex"])
            if row["decision"] == "revision":
                assert native.digest(plane) == layout["page_sha256"][number - 1]
            assert panel.panel.mask_check(plane, 216, shown), (ident, frame, number)
            panel.panel.complete_mask(name_font, row["speaker"], shown, 16, 277, town.INKS[1])
            holds.append(dict(id=ident, frame=frame, page=number, speaker=row["speaker"], decision=row["decision"],
                              block=block, system_FE=False, observed=captured))
            pictures.append((ident + (f" page {number}" if len(rendered["pages"]) > 1 else ""), shown))
    remaining = list(frames)
    final = holds[-1]["observed"]
    if remaining:
        assert remaining == [scheduled_frames[-1]]
        final, shown = town.read_frame(captures, remaining[0])
        pictures.append(("Return after the focused excerpt", shown))

    replay.ROOT.mkdir(exist_ok=True)
    sheets = []
    for index in range(0, len(pictures), 6):
        target = replay.ROOT / f"{stem}_{index // 6 + 1}.png"
        town.sheet(pictures[index:index + 6], target)
        sheets.append(dict(path=str(target), sha256=base.digest(target)))
    files = (fixture_path, report_path, inputs, fixture["fixture_ROM"])
    return holds, sheets, final, bool(remaining), {str(path): base.digest(path) for path in files}


def qualify_observed_pages(image, candidate, proof, refresh_ids):
    earlier, previous, latest, native_receipt = map(base.load, (REFERENCE_GAMEPLAY,
        REFERENCE_STAGE / stage.PROOF.name, stage.PROOF, native_check.REFERENCE_DISPLAY))
    rom = REFERENCE_STAGE / stage.ROM.name
    assert previous["candidate_sha256"] == earlier["candidate_sha256"] == native_receipt["candidate_sha256"] == base.digest(rom)
    assert latest["candidate_sha256"] == candidate
    prior = base.NdsImage.open(rom)
    arm = native_check.display.ASSETS
    assert all(prior.read_file(asset) == image.read_file(asset) for asset in arm)
    path = replay.prior.PATH
    bank = native.IlnkContainer.parse(image.read_file(path)).blocks
    assert native.IlnkContainer.parse(prior.read_file(path)).blocks[44] == bank[44]
    assert previous["groups"][-1]["commands"][-1]["stored"] == latest["groups"][-1]["commands"][-1]["stored"]
    native_rows = [{row["id"]: row for row in report["records"]} for report in (native_receipt, proof)]
    kept, replaced = [], set()
    for hold in earlier["holds"]:
        ident = hold["id"]
        old, current = [by_id[ident] for by_id in native_rows]
        if old["stored_command_hex"] != current["stored_command_hex"]:
            replaced.add(ident)
            continue
        offset, raw = current["stored_offset"], bytes.fromhex(current["stored_command_hex"])
        assert bank[hold["block"]][offset:offset + len(raw)] == raw
        assert old.get("layouts") == current.get("layouts") and old["decision"] == current["decision"]
        assert base.digest(hold["observed"]["path"]) == hold["observed"]["PNG_sha256"]
        kept.append(hold)
    assert replaced == refresh_ids & set(earlier["observed_ids"])
    assert earlier["single_press_page_turn_reclaimed"]
    assert all(any(h["id"] == ident for h in kept) for ident in ("DK4_MES_B78_R0005", "DK4_MES_B78_R0009"))
    assert all(base.digest(s["path"]) == s["sha256"] for s in earlier["sheets"])
    return earlier, kept, sorted(replaced)


def main():
    assert not PROOF.exists()
    proof, draft = map(base.load, (native_check.PROOF, stage.OUTPUT))
    candidate = base.digest(stage.ROM)
    assert candidate == proof["candidate_sha256"] == base.digest(stage.ROOT / "clean_rebuilt.nds")
    image = base.NdsImage.open(stage.ROM)
    rows = {r["id"]: r for r in draft["records"]}
    plan = replay.company_settings(replay.FINAL_SEQUENCE)
    current = (replay.FOCUS_REPORT, replay.FOCUS / "inputs.json", plan["SEQUENCE"], plan["FRAMES"], plan["END"], "visual_refinements")
    focused, more_sheets, returned, focused_return, new_files = check_excerpt(*current, proof, rows, image, candidate)
    assert focused_return
    earlier, prior, replaced = qualify_observed_pages(image, candidate, proof, {row["id"] for row in focused})
    assert [p["page"] for p in prior if p["id"] == "DK4_MES_B75_R0238"] == [1, 2]
    holds = prior + focused
    observed = {r["id"] for r in holds}
    assert len(observed) == 32 and len(holds) == 33
    evidence = earlier["evidence"] | new_files | {
        str(path): base.digest(path) for path in (native_check.PROOF, REFERENCE_GAMEPLAY, REFERENCE_STAGE / stage.PROOF.name)}
    base.save(PROOF, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_activation=False,
        exact_native_glyph_matches=True, hardware_verified=False, holds=holds, final_hold=returned,
        company_final_hold=earlier["company_final_hold"], observed_ids=sorted(observed), original_story_branches_unvisited=True,
        offline_only=[r["id"] for r in rows.values() if r["decision"] == "revision" and r["id"] not in observed],
        single_press_page_turn_reclaimed=True, refreshed_earlier_ids=replaced,
        sheets=earlier["sheets"] + more_sheets, evidence=evidence))
    print(f"Verified {len(holds)} emulator pages across {len(observed)} speech records.")


if __name__ == "__main__":
    main()
