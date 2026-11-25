"""Replay both menu objects and the two-page Valdes instruction after cold boot."""

from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into
import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_mediterranean_dialogue_20261121 as prior
from scripts import stage_rafael_spain_20261121 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
REPORT = ROOT / "capture/capture_report.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
PATH = "/data/SC0.DK4"
SEQUENCE = (71, 75, "SC0_B60_CHOICE_768_0", 177, 182, "SC0_B60_CHOICE_1852_0", 474, 486, 489)
INPUT = [(4000, "A"), (4240, "A"), (4460, "DOWN"), (4580, "UP"), (4720, "A"), (4960, "A"),
         (5200, "A"), (5400, "DOWN"), (5680, "A"), (6000, "A"), (6300, "A"), (6600, "A"), (6920, "A")]
FRAMES = (3900, 4208, 4380, 4550, 4680, 4940, 5170, 5360, 5560, 5950, 6230, 6530, 6830, 7399)
END = 7400
OLD_FIXTURE = Path("work/rafael_mediterranean_dialogue_20261121/staged_v2/focused_gameplay/B47/fixture.json")


def replay():
    assert not ROOT.exists()
    proof = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert candidate == proof["candidate_sha256"] and proof["whole_parent_inverse"]
    group, = proof["groups"]
    rom = base.NdsImage.open(stage.ROM)
    archive = rom.read_file(PATH)
    bank = native.IlnkContainer.parse(archive)
    opening, scene = (bank.blocks[i] for i in (44, 60))
    prelude = bytes.fromhex(base.load(OLD_FIXTURE)["original_prelude"])
    assert opening[8:40] == prelude and len(prelude) == 32
    assert opening[:4] == scene[:4] and opening[6:8] == scene[6:8]
    assert native.digest(scene) == group["after"]
    commands = {ident: cmd for cmd in group["commands"] for ident in cmd["record_ids"]}
    logical = bytearray(opening[:40])
    copied = []
    for item in SEQUENCE:
        ident = item if isinstance(item, str) else f"DK4_MES_B60_R{item:04d}"
        command = commands[ident]
        raw = bytes.fromhex(command["stored"])
        at = command["stored_offset"]
        assert scene[at:at + len(raw)] == raw
        assert command["word"] == (0x2100 if isinstance(item, str) else 0x4000)
        copied.append(dict(ids=command["record_ids"], word=command["word"], fixture_offset=len(logical),
                           actual_block_offset=at, hex=raw.hex()))
        logical.extend(raw)
    terminal = group["commands"][-1]
    assert terminal["word"] == 0
    logical.extend(bytes.fromhex(terminal["stored"]))
    pack_into("<H", logical, 4, len(logical) - 8)
    fixture = bytes(logical) + bytes(-len(logical) % 4)
    inventory, _, _ = native.scoped_inventory()
    original, _ = inventory(rom.read_file(native.ARM), fixture)
    indexed = {cmd["offset"]: cmd["whole_command_hex"] for cmd in original}
    assert all(indexed[cmd["fixture_offset"]] == cmd["hex"] for cmd in copied)
    bank.blocks[44] = fixture
    rom.replace_file(PATH, bank.to_bytes())
    ROOT.mkdir(parents=True)
    output = ROOT / "Rafael_Spain_Choices_RESEARCH_ONLY.nds"
    rom.save(output)
    inverse = base.NdsImage.open(output)
    inverse.replace_file(PATH, archive)
    assert bytes(inverse.rom.save()) == stage.ROM.read_bytes()
    inputs = ROOT / "inputs.json"
    base.save(inputs, base.load(prior.INPUTS) + [dict(start=f, duration=5, buttons=[button]) for f, button in INPUT])
    base.save(ROOT / "fixture.json", dict(candidate_sha256=candidate, fixture_ROM=str(output),
        fixture_ROM_sha256=base.digest(output), original_prelude=prelude.hex(), copied=copied,
        exact_candidate_inverse=True, original_menu_objects_copied_byte_exact=True,
        original_relationship_and_choice_branches_unexecuted=True, natural_activation=False))
    harness = prior.release_checks.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(output), "--out", str(REPORT.parent), "--frames", str(END),
                "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                "--capture-at", *map(str, FRAMES)]
    harness.main()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=("replay", "startup", "patch"))
    case = parser.parse_args().check
    if case == "replay":
        replay()
    else:
        template = prior.release_checks.template
        action = template.common.startup if case == "startup" else template.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=native, play=template.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
