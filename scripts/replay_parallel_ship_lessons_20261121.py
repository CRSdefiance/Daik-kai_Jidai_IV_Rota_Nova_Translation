"""Exercise Rafael's refit notice, resized choice and two-page ship lesson."""
from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into
from types import FunctionType, SimpleNamespace
import sys

from scripts import replay_rafael_first_market_20261121 as checks
from scripts import stage_parallel_ship_lessons_20261121 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_rafael"
REPORT = ROOT / "capture/capture_report.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
PATH = "/data/SC0.DK4"
STARTUP_INPUTS = Path("work/analysis/papal_trade_route_runs_v7625/route0/ordinary_NewGame_inputs.json")
PRELUDE = Path("work/analysis/Rafael_B177_B180_actual_fixtures_v1_20261105/ship_buying_and_refit_fixture.json")
SAMPLES = (27, 30, 100, 104, 108, 114, 117, 144, 150, 176, 180, 190, 209, 224)
END = 11500


def replay():
    stored = base.load(stage.PROOF)
    assert stored["candidate_sha256"] == base.digest(stage.ROM) and stored["whole_parent_inverse"]
    group, = [g for g in stored["groups"] if g["file_path"] == PATH]
    assert group["block"] == 177
    rom = base.NdsImage.open(stage.ROM)
    archive_bytes = rom.read_file(PATH)
    archive = native.IlnkContainer.parse(archive_bytes)
    opening, lesson = (archive.blocks[i] for i in (44, 177))
    assert native.digest(lesson) == group["after"]
    prelude = b"".join(bytes.fromhex(c["whole_command_hex"])
                       for c in base.load(PRELUDE)["original_initializers"])
    assert len(prelude) == 32 and opening[8:40] == prelude
    assert (opening[:4], opening[6:8]) == (lesson[:4], lesson[6:8])
    indices = {row["id"]: row["source_record_index"] for row in base.load(stage.review.OUTPUT)["records"]
               if row["file_path"] == PATH}
    commands = {indices[c["record_ids"][0]]: c for c in group["commands"] if c["record_ids"]}
    body = bytearray(opening[:8] + prelude)
    spans = []
    for index in SAMPLES:
        command = commands[index]
        at = command["stored_offset"]
        raw = bytes.fromhex(command["stored"])
        assert lesson[at:at + len(raw)] == raw and command["word"] in (0x4000, 0x2100)
        spans.append(dict(ids=command["record_ids"], offset=len(body), original_offset=at, command_sha256=native.digest(raw)))
        body.extend(raw)
    body.extend(b"\0\0")
    pack_into("<H", body, 4, len(body) - 8)
    body.extend(bytes(-len(body) % 4))
    archive.blocks[44] = bytes(body)
    rom.replace_file(PATH, archive.to_bytes())
    ROOT.mkdir()
    research = ROOT / "Rafael_Alexandria_display_fixture_RESEARCH_ONLY.nds"
    rom.save(research)
    loaded = base.NdsImage.open(research)
    assert native.IlnkContainer.parse(loaded.read_file(PATH)).blocks[44] == body
    loaded.replace_file(PATH, archive_bytes)
    assert bytes(loaded.rom.save()) == stage.ROM.read_bytes()
    base.save(ROOT / "fixture.json", dict(candidate_sha256=stored["candidate_sha256"], fixture=str(research),
        fixture_sha256=base.digest(research), exact_candidate_inverse=True, copied_native_commands=spans,
        original_prelude_evidence=str(PRELUDE), natural_activation=False, original_branch_selection_replaced=True))
    inputs = ROOT / "inputs.json"
    moves = list(range(4120, END - 300, 360))
    base.save(inputs, base.load(STARTUP_INPUTS) + [dict(start=i, duration=6, buttons=["A"]) for i in moves])
    frames = sorted({3900, END - 1, *[i + n for i in moves for n in (260, 340)]})
    harness = checks.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(research), "--out", str(REPORT.parent), "--frames", str(END),
                "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                "--capture-at", *map(str, frames)]
    harness.main()


def route_snapshot(route):
    from scripts import verify_late_trade_exchanges_20261118 as earlier

    source = STARTUP_INPUTS if route == 0 else earlier.build.ROOT / "lil_snapshot_inputs.json"
    target = stage.ROOT / f"route{route}_snapshot"
    target.mkdir(exist_ok=True)
    end = 4000
    inputs = target / "inputs.json"
    assert not inputs.exists() and not (target / "capture").exists()
    base.save(inputs, [r for r in base.load(source) if r["start"] + r.get("duration", 1) <= end])
    harness = checks.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(stage.ROM), "--out", str(target / "capture"),
                "--frames", str(end), "--inputs-json", str(inputs), "--press-start", "-1", "--dump-ram",
                "--capture-every", "999999", "--capture-at", str(end)]
    harness.main()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("focused", "startup", "patch", "route0", "route2"))
    case = parser.parse_args().case
    if case == "focused":
        replay()
    elif case in ("route0", "route2"):
        route_snapshot(int(case[-1]))
    else:
        template = checks.template
        action = template.common.startup if case == "startup" else template.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=native, play=template.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
