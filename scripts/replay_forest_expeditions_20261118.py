"""Replay Maria's stored forest choices in the existing initialized emulator entry."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import pack_into
import sys
from types import SimpleNamespace

from scripts import replay_town_quest_exchanges_20261115 as quest
from scripts import stage_forest_expeditions_20261118 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
ROOT = stage.ROOT / "maria_forest_replay"
ROM = ROOT / "Maria_Forest_Initialized_RESEARCH_ONLY.nds"
FILE = "/data/SC3.DK4"
HOST, FOREST = 33, 252
FIXTURE = ROOT / "fixture.json"


def prepare():
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof["candidate_sha256"]
    group = next(row for row in proof["groups"] if row["file_path"] == FILE and row["block"] == FOREST)
    image = base.NdsImage.open(stage.ROM)
    arm, data = (image.read_file(path) for path in (native.ARM, FILE))
    bank = native.IlnkContainer.parse(data)
    entry, forest = bank.blocks[HOST], bank.blocks[FOREST]
    assert native.digest(forest) == group["after"]
    inventory, _, _ = native.scoped_inventory()
    host_commands, host_speech = inventory(arm, entry)
    start = 34
    prefix = [command for command in host_commands if command["offset"] < start]
    cleanup_offset = host_speech[-1]["offset"] + host_speech[-1]["native_extent"]
    cleanup = entry[cleanup_offset:stage.logical_end(entry)]
    assert len(prefix) == 7 and cleanup[:2] == b"\x40\x62" and cleanup[-4:] == b"\0" * 4
    # Start just after the map-inventory gate. Preserve the forest setup,
    # encounter, menus, original predicate operands and all response branches.
    commands = group["commands"]
    first = next(i for i, cmd in enumerate(commands) if cmd["source_offset"] == 320)
    guest = commands[first:-1]
    assert commands[-1]["source"] == commands[-1]["stored"] == "00000080"
    assert all(first <= cmd.get("target_command_index", first) < len(commands) for cmd in guest)
    start_offset = guest[0]["stored_offset"]
    body = bytearray(entry[:start] + forest[start_offset:stage.logical_end(forest) - 4] + cleanup)
    pack_into("<H", body, 4, len(body) - 8)
    inserted = bytes(body) + bytes(-len(body) % 4)
    fixture_commands, _ = inventory(arm, inserted)
    assert all(a["word"] == b["word"] for a, b in zip(prefix, fixture_commands[:len(prefix)], strict=True))
    delta = start - start_offset
    for got, expected in zip(fixture_commands[len(prefix):len(prefix) + len(guest)], guest, strict=True):
        at = expected["stored_offset"] + delta
        raw = bytes.fromhex(expected["stored"])
        assert got["offset"] == at and got["word"] == expected["word"] and inserted[at:at + len(raw)] == raw
    ROOT.mkdir()
    bank.blocks[HOST] = inserted
    image.replace_file(FILE, bank.to_bytes())
    image.save(ROM)
    bank.blocks[HOST] = entry
    assert bank.to_bytes() == data
    image.replace_file(FILE, data)
    assert bytes(image.rom.save()) == stage.ROM.read_bytes()
    unlock_path = ROOT / "existing_system_only_unlock.json"
    precedent = quest.prior.precedent
    unlock = base.load(precedent.HISTORICAL)
    unlock.update(production_ROM=str(ROM), production_ROM_sha256=base.digest(ROM),
                  current_test_scope="Maria forest encounter with initialized setup and the original choice branches.")
    base.save(unlock_path, unlock)
    precedent.validate_fixture(unlock_path)
    base.save(FIXTURE, dict(reference_ROM_sha256=proof["candidate_sha256"], fixture_sha256=base.digest(ROM),
        unlock=str(unlock_path), current_host_sha256=native.digest(entry), forest_sha256=group["after"],
        original_scene_commands_exact=True, whole_source_ROM_inverse=True, natural_unlock=False,
        omitted_map_gate=True, omitted_forest_terminator_replaced_with_host_cleanup=True,
        included_source_offsets=[cmd["source_offset"] for cmd in guest]))


def capture(name, actions, frames):
    root = ROOT / name
    root.mkdir()
    fixture = base.load(FIXTURE)
    assert base.digest(ROM) == fixture["fixture_sha256"]
    precedent = quest.prior.precedent
    unlock = precedent.validate_fixture(fixture["unlock"])
    inputs = base.load(precedent.stage.CAPTURE)["scripted_input_schedule"]
    inputs += [dict(start=frame, duration=16, buttons=[key]) for frame, key in actions]
    schedule = root / "inputs.json"
    base.save(schedule, inputs)
    argv = sys.argv
    try:
        sys.argv = [argv[0], "--rom", str(ROM), "--out", str(root / "capture"),
                    "--frames", str(frames), "--inputs-json", str(schedule), "--touchscreen",
                    "--battery-save", unlock["fixture_save"], "--allow-gallery-fixtures",
                    "--gallery-save-fixture-manifest", fixture["unlock"], "--capture-every", "999999",
                    "--capture-at", *map(str, range(4100, frames, 25))]
        precedent.harness.main()
    finally:
        sys.argv = argv


def startup():
    boot = quest.inherited.boot
    previous = base.load(stage.parent.RELEASE)
    snapshot = base.load(previous["own_registered_startup"])["read_only_snapshot"]["path"]
    prior = Path(snapshot).parent.parent
    context = SimpleNamespace(ROOT=stage.ROOT, ROM=stage.ROM, STORED=stage.PROOF, base=base)
    source = checked_text(getsource(boot.main), {
        'stage.parent.stage.ROOT/"startup_retry"': "PREVIOUS_CAPTURE",
        'stored["previous_sha256"]': 'stored["predecessor_sha256"]',
    })
    env = vars(boot) | dict(stage=context, PREVIOUS_CAPTURE=prior)
    exec(compile(source, __file__ + "::registered-startup", "exec"), env)
    env["main"]()


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("prepare", "discover", "capture", "startup"))
    parser.add_argument("--case")
    parser.add_argument("--frames", type=int, default=8001)
    parser.add_argument("--input", nargs=2, action="append", default=[], metavar=("FRAME", "BUTTON"))
    args = parser.parse_args()
    if args.action == "prepare":
        prepare()
    elif args.action == "startup":
        startup()
    elif args.action == "discover":
        capture("discovery", [(n, "A") for n in range(4200, 7701, 350)], 8051)
    else:
        assert args.case and args.input
        capture(args.case, [(int(n), key) for n, key in args.input], args.frames)


if __name__ == "__main__":
    main()
