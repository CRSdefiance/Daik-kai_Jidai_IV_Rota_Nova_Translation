"""Replay both choices through the complete original Miracle Bullet Charm event."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into
from sys import executable
from subprocess import run

from scripts import stage_hodram_B91_B110_20261122 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "branch_gameplay"
ROM, FIXTURE = ROOT / "Hodram_B91_COMPLETE_RESEARCH_ONLY.nds", ROOT / "fixture.json"
HISTORICAL = Path("work/emulation_v193")
SCHEDULES = {"accept": "Hodram_B91_B110_20261101_B91", "decline": "Hodram_B91_B110_20261101_B91_decline"}
ENTRY = 42


def prepare():
    ROOT.mkdir()
    report = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert candidate == report["candidate_sha256"] and report["whole_parent_inverse"]
    image = base.NdsImage.open(stage.ROM)
    arm = image.read_file(native.ARM)
    archive = image.read_file(stage.scope["ARCHIVE"])
    bank = native.IlnkContainer.parse(archive)
    inventory, _, _ = native.scoped_inventory()
    initial = bank.blocks[ENTRY]
    initial_commands, initial_speech = inventory(arm, initial)
    first = initial_speech[0]["offset"]
    prelude = initial[8:first]
    prefix = [c for c in initial_commands if c["offset"] < first]
    assert first == 42 and len(prelude) == 34 and len(prefix) == 8
    clean = base.NdsImage.open(native.CLEAN)
    assert native.IlnkContainer.parse(clean.read_file(stage.scope["ARCHIVE"])).blocks[ENTRY][8:first] == prelude
    selected = bank.blocks[91]
    group, = [g for g in report["groups"] if g["block"] == 91]
    assert native.digest(selected) == group["after"]
    limit = stage.logical_end(selected)
    assert selected[:4] == initial[:4] and selected[6:8] == initial[6:8] and not any(selected[limit:])
    body = bytearray(initial[:8] + prelude + selected[8:limit])
    pack_into("<H", body, 4, len(body) - 8)
    body.extend(bytes(-len(body) % 4))
    shifted, _ = inventory(arm, bytes(body))
    source_commands, _ = inventory(arm, selected)
    assert len(shifted) == len(prefix) + len(source_commands) and len(body) < 0x2400
    for old, new in zip(source_commands, shifted[len(prefix):], strict=True):
        assert new["offset"] == old["offset"] + 34 and new["whole_command_hex"] == old["whole_command_hex"]
        assert new["ancestor_0100_offsets"] == [n + 34 for n in old["ancestor_0100_offsets"]]
    bank.blocks[ENTRY] = bytes(body)
    image.replace_file(stage.scope["ARCHIVE"], bank.to_bytes())
    image.save(ROM)
    restored = base.NdsImage.open(ROM)
    restored.replace_file(stage.scope["ARCHIVE"], archive)
    assert bytes(restored.rom.save()) == stage.ROM.read_bytes()
    base.save(FIXTURE, dict(candidate_sha256=candidate, fixture_sha256=base.digest(ROM),
        staged_group_sha256=group["after"], full_command_count=len(source_commands),
        original_initializers=prefix, unchanged_source_commands_and_relative_branches=True,
        exact_whole_candidate_inverse=True, initialized_complete_script=True, natural_activation=False))


def replay(mode):
    assert base.digest(ROM) == base.load(FIXTURE)["fixture_sha256"]
    historical_file = HISTORICAL / SCHEDULES[mode] / "capture_report.json"
    historical = base.load(historical_file)
    assert historical["cold_boot"] and not historical["savestate_loaded"] and not historical.get("battery_save_preloaded")
    dest = ROOT / mode
    dest.mkdir()
    inputs = dest / "inputs.json"
    base.save(inputs, historical["scripted_input_schedule"])
    frames = historical["frames"]
    captures = sorted({4560, 4680, frames - 1} | set(range(4800, min(frames, 10000), 120)))
    run([executable, "-m", "scripts.headless_desmume_v193", "--rom", str(ROM), "--out", str(dest / "capture"),
         "--frames", str(frames), "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
         "--capture-at", *map(str, captures)], check=True)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", *SCHEDULES))
    action = parser.parse_args().action
    prepare() if action == "prepare" else replay(action)
