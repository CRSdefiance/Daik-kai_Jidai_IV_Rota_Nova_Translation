"""Sample both menus and the installed sea-battle page turn in the emulator."""

from argparse import ArgumentParser
from struct import pack_into
import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_mediterranean_dialogue_20261121 as original
from scripts import replay_rafael_spain_20261121 as spain
from scripts import stage_rafael_gerhard_tutorial_20261121 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
REPORT = ROOT / "capture/capture_report.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
PATH = stage.PATH
SEQUENCE = (
    89, 93, 137, 147, 160, 167, 179, 197, 201, 206, 218, "3114",
    327, 336, 398, 417, "5298", 511, 515, 523, 527, 535, 539, 542, 545, 549, 552, 556, 560, 566,
)


def make_schedule(commands):
    clock = 4000
    events, requests = [], []
    for command in commands:
        at = command["stored_offset"]
        if command["word"] in stage.compiler.MENU:
            requests.append(dict(type="menu", offset=at, slot=0, holds=[clock - 135, clock - 95, clock - 45]))
            events.append(dict(start=clock, duration=5, buttons=["DOWN"]))
            clock += 300
            requests.append(dict(type="menu", offset=at, slot=1, holds=[clock - 135, clock - 95, clock - 45]))
            events.append(dict(start=clock, duration=5, buttons=["A"]))
            clock += 300
            continue
        plan = command["plan"]
        pages = plan["expected_native_pages"] if plan else 1
        for page in range(1, pages + 1):
            requests.append(dict(type="speech", offset=at, page=page, holds=[clock - 45]))
            events.append(dict(start=clock, duration=5, buttons=["A"]))
            clock += 300
    return events, requests, clock + 420


def replay():
    assert not ROOT.exists()
    proof = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert candidate == proof["candidate_sha256"] and proof["whole_parent_inverse"]
    image = base.NdsImage.open(stage.ROM)
    archive = image.read_file(PATH)
    bank = native.IlnkContainer.parse(archive)
    group, = proof["groups"]
    scene, opening = bank.blocks[84], bank.blocks[44]
    assert native.digest(scene) == group["after"] and opening[:4] == scene[:4] and opening[6:8] == scene[6:8]
    prelude = bytes.fromhex(base.load(spain.OLD_FIXTURE)["original_prelude"])
    assert opening[8:40] == prelude and len(prelude) == 32
    selections = []
    for item in SEQUENCE:
        if isinstance(item, str):
            commands = [row for row in group["commands"] if row["source_offset"] == int(item)]
            assert len(commands) == 1 and commands[0]["word"] in stage.compiler.MENU
        else:
            ident = f"DK4_MES_B84_R{item:04d}"
            commands = [row for row in group["commands"] if row["record_ids"] == [ident]]
            assert len(commands) == (2 if item == 539 else 1)
        selections.extend(commands)
    logical, copied = bytearray(opening[:40]), []
    for command in selections:
        raw = bytes.fromhex(command["stored"])
        at = command["stored_offset"]
        assert scene[at:at + len(raw)] == raw
        copied.append(dict(ids=command["record_ids"], word=command["word"], fixture_offset=len(logical),
                           actual_block_offset=at, hex=raw.hex()))
        logical.extend(raw)
    terminal = group["commands"][-1]
    assert terminal["word"] == 0
    logical.extend(bytes.fromhex(terminal["stored"]))
    pack_into("<H", logical, 4, len(logical) - 8)
    body = bytes(logical) + bytes(-len(logical) % 4)
    inventory, _, _ = native.scoped_inventory()
    parsed, _ = inventory(image.read_file(native.ARM), body)
    indexed = {row["offset"]: row["whole_command_hex"] for row in parsed}
    assert all(indexed[row["fixture_offset"]] == row["hex"] for row in copied)
    bank.blocks[44] = body
    image.replace_file(PATH, bank.to_bytes())
    ROOT.mkdir(parents=True)
    output = ROOT / "Rafael_Gerhard_Tutorial_RESEARCH_ONLY.nds"
    image.save(output)
    inverse = base.NdsImage.open(output)
    inverse.replace_file(PATH, archive)
    assert bytes(inverse.rom.save()) == stage.ROM.read_bytes()
    events, requests, end = make_schedule(selections)
    inputs = ROOT / "inputs.json"
    base.save(inputs, base.load(original.INPUTS) + events)
    base.save(ROOT / "fixture.json", dict(candidate_sha256=candidate, fixture_ROM=str(output),
        fixture_ROM_sha256=base.digest(output), original_prelude=prelude.hex(), copied=copied,
        requested_holds=requests, end=end, exact_candidate_inverse=True, original_story_branches_unexecuted=True,
        sampled_branch_reply_commands_are_sequenced_in_fixture=True, natural_activation=False))
    holds = [f for request in requests for f in request["holds"]] + [end - 1]
    assert holds == sorted(set(holds))
    harness = original.release_checks.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(output), "--out", str(REPORT.parent), "--frames", str(end),
                "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                "--capture-at", *map(str, holds)]
    harness.main()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=("replay", "startup", "patch"))
    check = parser.parse_args().check
    if check == "replay":
        replay()
    else:
        template = original.release_checks.template
        action = template.common.startup if check == "startup" else template.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=stage.native, play=template.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
