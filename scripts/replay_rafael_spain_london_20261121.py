"""Replay exact sampled speech and the original bullfight and rescue picture switches."""

from argparse import ArgumentParser
from struct import pack_into
import sys
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_mediterranean_dialogue_20261121 as original
from scripts import replay_rafael_spain_20261121 as spain
from scripts import stage_rafael_spain_london_20261121 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
REPORT = ROOT / "capture/capture_report.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
PATH = "/data/SC0.DK4"
HEAD = tuple((81, n) for n in (5, 90, 94, 98, 106, 154))
BEFORE_RESCUE = (
    (81, 163), (81, 198), (81, 206), (81, 209), (81, 224), (81, 228),
    (82, 18), (82, 21), (82, 133), (82, 136), (82, 140), (82, 143), (82, 147),
    (83, 84), (83, 88),
)
AFTER_RESCUE = tuple((83, n) for n in (140, 146, 166, 173, 177, 299))
REFINEMENTS = ((81, 202), (82, 5), (82, 201), (83, 12), (83, 140), (83, 146))


def replay(refinements=False):
    assert not ROOT.exists()
    proof = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert candidate == proof["candidate_sha256"] and proof["whole_parent_inverse"]
    groups = {g["block"]: g for g in proof["groups"]}
    image = base.NdsImage.open(stage.ROM)
    archive = image.read_file(PATH)
    bank = native.IlnkContainer.parse(archive)
    opening = bank.blocks[44]
    prelude = bytes.fromhex(base.load(spain.OLD_FIXTURE)["original_prelude"])
    assert opening[8:40] == prelude and len(prelude) == 32
    for n, group in groups.items():
        scene = bank.blocks[n]
        assert opening[:4] == scene[:4] and opening[6:8] == scene[6:8]
        assert native.digest(scene) == group["after"]
    by_id = {ident: (n, c) for n, group in groups.items() for c in group["commands"] for ident in c["record_ids"]}

    def select(sequence):
        return [by_id[f"DK4_MES_B{block}_R{index:04d}"] for block, index in sequence]

    crowd = [(81, c) for c in groups[81]["commands"] if 1384 <= c["source_offset"] <= 1414]
    rescue = [(83, c) for c in groups[83]["commands"] if 1250 <= c["source_offset"] <= 1676]
    assert [c["record_ids"][0] for _, c in crowd if c["record_ids"]] == ["DK4_MES_B81_R0159"]
    assert [c["record_ids"][0] for _, c in rescue if c["record_ids"]] == [
        f"DK4_MES_B83_R{index:04d}" for index in (92, 96, 101, 104, 107, 111, 114, 117, 120, 123, 127)]
    logical, copied = bytearray(opening[:40]), []
    commands = select(REFINEMENTS) if refinements else select(HEAD) + crowd + select(BEFORE_RESCUE) + rescue + select(AFTER_RESCUE)
    for block, command in commands:
        raw = bytes.fromhex(command["stored"])
        at = command["stored_offset"]
        assert bank.blocks[block][at:at + len(raw)] == raw and "target_command_index" not in command
        copied.append(dict(ids=command["record_ids"], block=block, word=command["word"], fixture_offset=len(logical),
                           actual_block_offset=at, hex=raw.hex()))
        logical.extend(raw)
    terminal = groups[83]["commands"][-1]
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
    output = ROOT / "Rafael_Spain_London_RESEARCH_ONLY.nds"
    image.save(output)
    inverse = base.NdsImage.open(output)
    inverse.replace_file(PATH, archive)
    assert bytes(inverse.rom.save()) == stage.ROM.read_bytes()
    count = sum(bool(row["ids"]) for row in copied)
    presses = [4000 + index * 300 for index in range(count if refinements else count + 5)]
    end = presses[-1] + 720
    holds = [3900, *(frame + 255 for frame in presses), end - 1]
    path = ROOT / "inputs.json"
    base.save(path, base.load(original.INPUTS) + [dict(start=f, duration=5, buttons=["A"]) for f in presses])
    base.save(ROOT / "fixture.json", dict(candidate_sha256=candidate, fixture_ROM=str(output),
        fixture_ROM_sha256=base.digest(output), original_prelude=prelude.hex(), copied=copied,
        scheduled_holds=holds, end=end, exact_candidate_inverse=True, original_picture_and_speech_commands=not refinements,
        final_wrap_refinements=refinements,
        original_scene_branches_unexecuted=True, natural_activation=False))
    harness = original.release_checks.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(output), "--out", str(REPORT.parent), "--frames", str(end),
                "--inputs-json", str(path), "--press-start", "-1", "--capture-every", "999999",
                "--capture-at", *map(str, holds)]
    harness.main()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=("replay", "refinements", "startup", "patch"))
    check = parser.parse_args().check
    if check in ("replay", "refinements"):
        replay(refinements=check == "refinements")
    else:
        template = original.release_checks.template
        action = template.common.startup if check == "startup" else template.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=stage.native, play=template.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
