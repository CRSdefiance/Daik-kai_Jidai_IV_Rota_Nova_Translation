"""Cold-boot a focused excerpt with the original festival picture commands."""

from argparse import ArgumentParser
from struct import pack_into
import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_mediterranean_dialogue_20261121 as original
from scripts import replay_rafael_spain_20261121 as prior
from scripts import stage_rafael_tradehouse_festival_20261121 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
REPORT = ROOT / "capture_extended/capture_report.json"
INPUT_PATH = ROOT / "inputs_extended.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
PATH = "/data/SC0.DK4"
BEFORE = ((65, 17), (65, 46), (66, 31), (67, 118), (67, 126), (67, 194), (67, 202))
FESTIVAL = tuple((69, n) for n in (48, 52, 56, 62, 65, 69, 73, 78, 82, 87, 91, 100))
AFTER = ((69, 143), (69, 162), (69, 176), (69, 254), (70, 29), (70, 121), (70, 157), (70, 174), (70, 214))
SEQUENCE = BEFORE + FESTIVAL + AFTER
INPUT = [(4100 + i * 300, "A") for i in range(len(SEQUENCE) + 3)]
END = INPUT[-1][0] + 720
FRAMES = (4010, *(frame + 272 for frame, _ in INPUT[:-1]), END - 1)


def replay():
    assert not ROOT.exists()
    proof = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert candidate == proof["candidate_sha256"] and proof["whole_parent_inverse"]
    groups = {g["block"]: g for g in proof["groups"]}
    image = base.NdsImage.open(stage.ROM)
    archive = image.read_file(PATH)
    bank = native.IlnkContainer.parse(archive)
    opening = bank.blocks[44]
    prelude = bytes.fromhex(base.load(prior.OLD_FIXTURE)["original_prelude"])
    assert opening[8:40] == prelude and len(prelude) == 32
    for n, group in groups.items():
        scene = bank.blocks[n]
        assert opening[:4] == scene[:4] and opening[6:8] == scene[6:8]
        assert native.digest(scene) == group["after"]
    by_id = {ident: (block, c) for block, group in groups.items() for c in group["commands"] for ident in c["record_ids"]}
    select = lambda keys: [by_id[f"DK4_MES_B{block}_R{index:04d}"] for block, index in keys]
    festive = [(69, c) for c in groups[69]["commands"] if 406 <= c["source_offset"] <= 860]
    assert [r["record_ids"][0] for _, r in festive if r["record_ids"]] == [
        f"DK4_MES_B{block}_R{i:04d}" for block, i in FESTIVAL]
    assert len([c for _, c in festive if not c["record_ids"]]) == 10
    logical = bytearray(opening[:40])
    copied = []
    for block, command in select(BEFORE) + festive + select(AFTER):
        raw = bytes.fromhex(command["stored"])
        at = command["stored_offset"]
        assert bank.blocks[block][at:at + len(raw)] == raw and "target_command_index" not in command
        copied.append(dict(ids=command["record_ids"], block=block, word=command["word"],
                           fixture_offset=len(logical), actual_block_offset=at, hex=raw.hex()))
        logical.extend(raw)
    terminal = groups[70]["commands"][-1]
    assert terminal["word"] == 0
    logical.extend(bytes.fromhex(terminal["stored"]))
    pack_into("<H", logical, 4, len(logical) - 8)
    body = bytes(logical) + bytes(-len(logical) % 4)
    inventory, _, _ = native.scoped_inventory()
    parsed, _ = inventory(image.read_file(native.ARM), body)
    indexed = {r["offset"]: r["whole_command_hex"] for r in parsed}
    assert all(indexed[c["fixture_offset"]] == c["hex"] for c in copied)
    bank.blocks[44] = body
    image.replace_file(PATH, bank.to_bytes())
    ROOT.mkdir(parents=True)
    output = ROOT / "Rafael_Tradehouse_Festival_RESEARCH_ONLY.nds"
    image.save(output)
    inverse = base.NdsImage.open(output)
    inverse.replace_file(PATH, archive)
    assert bytes(inverse.rom.save()) == stage.ROM.read_bytes()
    inputs = ROOT / "inputs.json"
    base.save(inputs, base.load(original.INPUTS) + [dict(start=f, duration=5, buttons=[button]) for f, button in INPUT])
    base.save(ROOT / "fixture.json", dict(candidate_sha256=candidate, fixture_ROM=str(output),
        fixture_ROM_sha256=base.digest(output), original_prelude=prelude.hex(), copied=copied,
        exact_candidate_inverse=True, original_speech_commands_copied_byte_exact=True,
        original_festival_picture_commands_copied_byte_exact=True,
        original_scene_branches_unexecuted=True, natural_activation=False))
    harness = original.release_checks.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(output), "--out", str(REPORT.parent), "--frames", str(END),
                "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                "--capture-at", *map(str, FRAMES)]
    harness.main()


def extended_replay():
    assert not REPORT.exists() and not INPUT_PATH.exists()
    fixture = base.load(ROOT / "fixture.json")
    rom = fixture["fixture_ROM"]
    assert fixture["candidate_sha256"] == base.digest(stage.ROM)
    assert fixture["exact_candidate_inverse"] and base.digest(rom) == fixture["fixture_ROM_sha256"]
    base.save(INPUT_PATH, base.load(original.INPUTS) + [dict(start=f, duration=5, buttons=[b]) for f, b in INPUT])
    harness = original.release_checks.template.games.harness
    sys.argv = [harness.__file__, "--rom", rom, "--out", str(REPORT.parent), "--frames", str(END),
                "--inputs-json", str(INPUT_PATH), "--press-start", "-1", "--capture-every", "999999",
                "--capture-at", *map(str, FRAMES)]
    harness.main()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=("replay", "extended-replay", "startup", "patch"))
    case = parser.parse_args().check
    if case == "replay":
        replay()
    elif case == "extended-replay":
        extended_replay()
    else:
        template = original.release_checks.template
        action = template.common.startup if case == "startup" else template.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=stage.native, play=template.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
