"""Bind the current Madeira confirmation and its cancel action to native text."""

from pathlib import Path
from struct import unpack_from

from PIL import Image, ImageDraw

from scripts import replay_battle_dialogue_followup_20261119 as play
from scripts import stage_battle_dialogue_followup_20261119 as build
from scripts.audit_fleet_encounter_dialogue_20261119 import page, snapshot
from scripts.verify_london_stockholm_dialogue_20261115 import native_hold

base = build.base
PROOF = build.ROOT / "verified_madeira_confirmation.json"
SHEET = build.ROOT / "madeira_confirmation_replay.png"
FRAMES = (6520, 6620, 6740)


def main():
    assert not PROOF.exists() and not SHEET.exists()
    stored = base.load(build.PROOF)
    candidate = base.digest(build.ROM)
    assert candidate == stored["candidate_sha256"]
    root = play.ROOT / "first_mate"
    terminal_path, trace_path = root / "terminal.json", root / "requests.json"
    report_path = root / "capture/capture_report.json"
    terminal, trace, report = map(base.load, (terminal_path, trace_path, report_path))
    assert terminal["ROM_sha256"] == report["ROM_sha256"] == candidate
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert report["scripted_input_schedule"] == play.schedule("first_mate")[0]
    assert report["frames"] == 6940 and report["battery_save_preloaded"]["copied_byte_exact_before_cold_boot"]
    donor = report["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert {k for k, v in report.items() if k.startswith("synthetic_") and v} == {"synthetic_battle_recovery_proximity_fixtures"}
    calls = trace["source_requests"]
    assert not {300, 304}.intersection(r["message_ID"] for r in calls)
    selected = [r for r in calls if r["message_ID"] == 2129]
    assert [r["PC"] for r in selected] == [0x0205528C, 0x020534F4]
    assert selected[0]["frame"] == selected[1]["frame"] and 6520 < selected[0]["frame"] < 6620
    assert selected[0]["caller_LR"] == selected[1]["caller_LR"] == 0x02053D10
    fixture, = report["synthetic_battle_recovery_proximity_fixtures"]
    assert fixture == terminal["location_fixture"]
    assert fixture["frame"] == 5000 and fixture["town_ID"] == 30
    arm_ram = {f["frame"]: f for f in report["read_only_capture_RAM_snapshots"]}
    original = snapshot(arm_ram[5000])
    after_position = bytearray(original)
    for address, data in fixture["declared_fields"].items():
        at = int(address) - 0x02000000
        body = bytes.fromhex(data)
        after_position[at:at+len(body)] = body
    image = base.NdsImage.open(build.ROM)
    arm = image.read_file(build.ARM)
    modified, assignment = play.assign_first_mate(arm, bytes(after_position))
    assert assignment == fixture["first_mate_fixture"]
    assert build.native.digest(modified) == fixture["after_RAM_sha256"]
    visible = snapshot(arm_ram[6620])
    plain, display = (unpack_from("<I", arm, p)[0]-0x02000000 for p in (0x5444C, 0x54450))
    expected, = [r for r in stored["records"] if r["message_ID"] == 2129]
    sample, = [r for r in expected["native_displays"] if r["visible_lines"] == ["May we strike Madeira?"]]
    assert visible[display:display+256].split(b"\0", 1)[0].hex() == sample["display_hex"]
    assert visible[plain:plain+256].split(b"\0", 1)[0].hex() == sample["expansion_hex"]
    cpu, get = play.earlier.get_machine(arm, visible)
    assert get(0x82478, get(0xCB1A8)+0x2090, 1) == 23
    actor = get(0xCB184)+4+23*32
    assert get(0x53F4C, actor, 0x02117D20) == 2129

    cancelled = snapshot(arm_ram[6740])
    cpu, get = play.earlier.get_machine(arm, cancelled)
    state = list(unpack_from("<3I", cpu.mem_read(get(0x3F0F8)+8, 12)))
    pending_town = unpack_from("<I", cpu.mem_read(get(0xCB19C)+0x1360, 4))[0]
    assert state == [0, 0, 0] and pending_town == 115, (state, pending_town)

    frames = {f["frame"]: f for f in report["frames_captured"] if f["path"].endswith("_cold_boot.png")}
    tile = page(image, frames[6620])
    painter, _, _ = build.workflow.font_tools(image)
    plane, glyphs = build.render_portrait(painter, arm, image.read_file("/GRP/KANJI.FNT"),
                                         bytes.fromhex(sample["display_hex"]))
    assert build.native.digest(plane) == sample["ink_sha256"] and len(glyphs) == sample["glyph_count"]
    ink = native_hold(tile, plane)
    sheet = Image.new("RGB", (3*256, 408), "#263238")
    label = ImageDraw.Draw(sheet)
    for i, (frame, caption) in enumerate(zip(FRAMES, ("Select Madeira", "Manuel's confirmation", "Cancel and return"), strict=True)):
        label.text((i*256+4, 4), caption, fill="white")
        sheet.paste(page(image, frames[frame]), (i*256, 21))
    sheet.save(SHEET)
    paths = [build.PROOF, terminal_path, trace_path, report_path, SHEET, Path(__file__)]
    evidence = {str(path): base.digest(path) for path in paths}
    evidence.update({frames[f]["path"]: frames[f]["PNG_sha256"] for f in FRAMES})
    evidence.update({arm_ram[f]["path"]: arm_ram[f]["sha256"] for f in (5000, 6620, 6740)})
    base.save(PROOF, dict(candidate_sha256=candidate, original_sequences_initialized=True,
        natural_random_selection_verified=False, hardware=False, original_cancel_state=state, original_cancelled_town=pending_town,
        legacy_keys_300_and_304_requested=False, sheets=[dict(path=str(SHEET), sha256=base.digest(SHEET))],
        outcomes=[dict(event="madeira_cancel", observed=[dict(message_ID=2129, frame=6620, complete_ink_pixels=ink,
                                                              native_requests=selected, capture=frames[6620])],
                       fixture=fixture, original_cancel_transition=True)], evidence=evidence))
    print("Verified the revised First Mate's panel and original cancel transition.")


if __name__ == "__main__":
    main()
