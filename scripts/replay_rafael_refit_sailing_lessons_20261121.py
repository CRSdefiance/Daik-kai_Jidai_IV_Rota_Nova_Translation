"""Run a focused emulator excerpt of both lessons and the exact release checks."""
from argparse import ArgumentParser
from struct import pack_into
from types import FunctionType, SimpleNamespace
import sys

from scripts import replay_parallel_ship_lessons_20261121 as earlier
from scripts import stage_rafael_refit_sailing_lessons_20261121 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_rafael"
REPORT = ROOT / "capture/capture_report.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
PATH = earlier.PATH
SAMPLES = {179: (27, 59, 62, 80, 87, 93, 102, 106, 110, 114, 118, 122, 128),
           180: (5, 13, 19, 72, 76, 93, 99, 102, 106, 110, 113, 116, 139)}
FIRST, END, STEP = 4120, 14700, 360


def replay():
    stored = base.load(stage.PROOF)
    assert stored["candidate_sha256"] == base.digest(stage.ROM) and stored["whole_parent_inverse"]
    rom = base.NdsImage.open(stage.ROM)
    archive_bytes = rom.read_file(PATH)
    archive = native.IlnkContainer.parse(archive_bytes)
    opening = archive.blocks[44]
    prelude = b"".join(bytes.fromhex(c["whole_command_hex"])
                       for c in base.load(earlier.PRELUDE)["original_initializers"])
    assert len(prelude) == 32 and opening[8:40] == prelude
    indices = {row["id"]: row["source_record_index"] for row in base.load(stage.review.OUTPUT)["records"]}
    body = bytearray(opening[:8] + prelude)
    spans = []
    for group in stored["groups"]:
        block = group["block"]
        lesson = archive.blocks[block]
        assert native.digest(lesson) == group["after"]
        assert (opening[:4], opening[6:8]) == (lesson[:4], lesson[6:8])
        commands = {indices[c["record_ids"][0]]: c for c in group["commands"] if c["record_ids"]}
        for index in SAMPLES[block]:
            command = commands[index]
            at = command["stored_offset"]
            raw = bytes.fromhex(command["stored"])
            assert lesson[at:at + len(raw)] == raw and command["word"] in (0x4000, 0x2100)
            spans.append(dict(block=block, ids=command["record_ids"], offset=len(body), original_offset=at,
                              command_sha256=native.digest(raw)))
            body.extend(raw)
    body.extend(b"\0\0")
    pack_into("<H", body, 4, len(body) - 8)
    body.extend(bytes(-len(body) % 4))
    archive.blocks[44] = bytes(body)
    rom.replace_file(PATH, archive.to_bytes())
    ROOT.mkdir()
    research = ROOT / "Rafael_Refit_And_Sails_RESEARCH_ONLY.nds"
    rom.save(research)
    loaded = base.NdsImage.open(research)
    assert native.IlnkContainer.parse(loaded.read_file(PATH)).blocks[44] == body
    loaded.replace_file(PATH, archive_bytes)
    assert bytes(loaded.rom.save()) == stage.ROM.read_bytes()
    base.save(ROOT / "fixture.json", dict(candidate_sha256=stored["candidate_sha256"], fixture=str(research),
        fixture_sha256=base.digest(research), exact_candidate_inverse=True, copied_native_commands=spans,
        original_prelude_evidence=str(earlier.PRELUDE), natural_activation=False, original_branch_selection_replaced=True))
    inputs = ROOT / "inputs.json"
    moves = list(range(FIRST, END - 350, STEP))
    base.save(inputs, base.load(earlier.STARTUP_INPUTS) + [dict(start=i, duration=6, buttons=["A"]) for i in moves])
    frames = sorted({3900, END - 1, *[i + n for i in moves for n in (260, 340)]})
    harness = earlier.checks.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(research), "--out", str(REPORT.parent), "--frames", str(END),
                "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                "--capture-at", *map(str, frames)]
    harness.main()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("focused", "startup", "patch"))
    case = parser.parse_args().case
    if case == "focused":
        replay()
    else:
        template = earlier.checks.template
        action = template.common.startup if case == "startup" else template.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=native, play=template.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
