"""Replay the complete revised kitchen scene at an initialized game entry."""

import argparse
import sys
from pathlib import Path
from struct import pack_into, unpack_from

from scripts import replay_maria_opening_wraps_20261114 as precedent
from scripts import verify_alexandria_cooking_assets_20261114 as verified
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime


edit, stage, base, parent = verified.edit, verified.stage, verified.base, verified.parent
ROOT = edit.ROOT / "gameplay"
INPUTS = ROOT / "inputs.json"
SETUP = ROOT / "fixture_receipt.json"
LIVE = ROOT / "live_receipt.json"
FRAME_COUNT = 10501
RETURN_FRAMES = (3900, 9250, 10250)
FILE = "/data/SC3.DK4"
TOOL = precedent.precedent.verify.__globals__["previous"].previous.prior


def prepare():
    assert not ROOT.exists()
    release = base.load(parent.RELEASE)
    receipt, review = map(base.load, (verified.RECEIPT, verified.REVIEW))
    assert receipt["candidate_sha256"] == review["candidate_sha256"] == release["candidate_sha256"]
    assert base.digest(parent.ROM) == release["candidate_sha256"]
    ctx = RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    arm = ctx.arm
    inventory, _, _ = stage.prior.scoped_inventory()
    image = base.NdsImage.open(parent.ROM)
    original = image.read_file(FILE)
    active = next(row for row in receipt["routes"] if row["file_path"] == FILE)
    assert edit.digest(original) == active["source_archive_sha256"]
    staged = Path(active["proposed_archive"]).read_bytes()
    assert edit.digest(staged) == active["proposed_archive_sha256"]
    bank = stage.IlnkContainer.parse(staged)
    host, guest = bank.blocks[33], bank.blocks[159]
    host_commands, host_speech = inventory(arm, host)
    host_end = host_speech[-1]["offset"] + host_speech[-1]["native_extent"]
    cleanup = [cmd["whole_command_hex"] for cmd in host_commands if cmd["offset"] >= host_end]
    assert len([cmd for cmd in host_commands if cmd["offset"] < 34]) == 7
    assert cleanup[0] == "4062" and cleanup[-1] == "00000000"

    guest_logical_end = 8 + unpack_from("<H", guest, 4)[0]
    assert guest[guest_logical_end-6:guest_logical_end] == bytes.fromhex("00c200000000")
    guest_commands, guest_speeches = inventory(arm, guest)
    assert len(guest_commands) == 24 and len(guest_speeches) == 12
    body = bytearray(host[:34] + guest[8:guest_logical_end-4] + bytes.fromhex("".join(cleanup)))
    pack_into("<H", body, 4, len(body) - 8)
    replacement = bytes(body) + bytes(-len(body) % 4)
    commands, speeches = inventory(arm, replacement)
    assert [row["whole_command_hex"] for row in commands[7:7+23]] == [row["whole_command_hex"] for row in guest_commands[:-1]]
    assert [row["whole_command_hex"] for row in speeches] == [row["whole_command_hex"] for row in guest_speeches]
    assert [row["whole_command_hex"] for row in commands[-len(cleanup):]] == cleanup

    bank.blocks[33] = replacement
    image.replace_file(FILE, bank.to_bytes())
    ROOT.mkdir(parents=True)
    target = ROOT / "Maria_Alexandria_cooking_RESEARCH_ONLY.nds"
    image.save(target)
    bank.blocks[33] = host
    assert bank.to_bytes() == staged
    image.replace_file(FILE, original)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    manifest = ROOT / "existing_system_only_unlock.json"
    unlock = base.load(precedent.HISTORICAL)
    unlock.update(production_ROM=str(target), production_ROM_sha256=base.digest(target),
                  current_test_scope="Complete Alexandria cooking scene at initialized Maria entry with existing system-only unlock.")
    base.save(manifest, unlock)
    precedent.validate_fixture(manifest)
    setup = base.load(precedent.stage.CAPTURE)
    schedule = setup["scripted_input_schedule"] + [
        dict(start=frame, duration=16, buttons=["A"]) for frame in range(4200, 8501, 325)]
    base.save(INPUTS, schedule)
    _, painter = stage.prior.precedent.planners(arm)
    font = ctx.image.read_file("/GRP/KANJI.FNT")
    planes = []
    _, raw_records = stage.prior.raw_speeches(arm, guest, inventory)
    for record in raw_records:
        raw = bytes.fromhex(record["raw_hex"])
        if raw[0] == 254:
            continue
        page, = painter(arm, font, raw[1:])["pages"]
        planes.append(dict(record_index=record["record_index"], selector=raw[0], plane=page["native_plane_hex"]))
    base.save(SETUP, dict(candidate_sha256=release["candidate_sha256"], archive_receipt_sha256=base.digest(verified.RECEIPT),
        fixture_ROMs=dict(after=dict(path=str(target), sha256=base.digest(target), unlock=str(manifest), unlock_sha256=base.digest(manifest))),
        original_scene_commands_in_fixture=[row["whole_command_hex"] for row in guest_commands[:-1]],
        original_fixture_host_cleanup=cleanup, whole_checked_ROM_inverse_exact=True,
        progressive_targets=planes, market_notice_exact_hex=raw_records[-1]["raw_hex"]))


def capture():
    fixture = base.load(SETUP)["fixture_ROMs"]["after"]
    assert base.digest(fixture["path"]) == fixture["sha256"]
    unlock = precedent.validate_fixture(fixture["unlock"])
    original = sys.argv
    output = ROOT / "after_verified"
    assert not output.exists()
    try:
        sys.argv = [original[0], "--rom", fixture["path"], "--out", str(output), "--frames", str(FRAME_COUNT),
            "--inputs-json", str(INPUTS), "--battery-save", unlock["fixture_save"], "--allow-gallery-fixtures",
            "--gallery-save-fixture-manifest", fixture["unlock"], "--touchscreen", "--capture-every", "999999",
            "--capture-at", *map(str, sorted(set(RETURN_FRAMES) | set(range(4350, 8251, 25))))]
        precedent.harness.main()
    finally:
        sys.argv = original


def verify():
    receipt = base.load(SETUP)
    report_path = ROOT / "after_verified/capture_report.json"
    report = base.load(report_path)
    precedent.validate_capture(report)
    assert report["ROM_sha256"] == receipt["fixture_ROMs"]["after"]["sha256"]
    assert report["frames"] == FRAME_COUNT and report["scripted_input_schedule"] == base.load(INPUTS)
    photos = TOOL.photos(report)
    candidates = [(frame, item, TOOL.body_masks(image)) for frame,(item,image) in sorted(photos.items())
                  if 4350 <= frame <= 8250]
    cursor = 4350
    shown = []
    for row in receipt["progressive_targets"]:
        expected = TOOL.prior.masks(bytes.fromhex(row["plane"]))
        matches = [(frame, item) for frame, item, masks in candidates if frame > cursor and masks == expected]
        assert matches, (row["record_index"], cursor)
        cursor, observed = matches[0]
        shown.append(row | dict(frame=cursor, observed=observed))
    assert len(shown) == 11 and cursor < 8250
    base.save(LIVE, dict(research_fixture_ROM_sha256=report["ROM_sha256"], frames=FRAME_COUNT,
        actual_progressive_panels=shown, sampled_followup_frames={frame: photos[frame][0] for frame in RETURN_FRAMES},
        capture_report=str(report_path), capture_report_sha256=base.digest(report_path),
        initialized_Maria_entry=True, natural_Alexandria_event_trigger_or_hardware_observed=False,
        market_panel_and_return_visual_review_pending=True))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "capture", "verify"))
    globals()[parser.parse_args().action]()

