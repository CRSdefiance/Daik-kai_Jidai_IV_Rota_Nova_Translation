"""Replay complete original blocks behind Rafael's established New Game prelude."""
from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into
from types import FunctionType, SimpleNamespace
import sys

from scripts import replay_rafael_first_market_20261121 as release_checks
from scripts import stage_rafael_mediterranean_dialogue_20261121 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused_gameplay"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
PATH = "/data/SC0.DK4"
CASES = {47: (7997, 7850), 48: (8049, 24500), 49: (8105, 17700), 50: (8154, 12000)}
INPUTS = Path("work/analysis/papal_trade_route_runs_v7625/route0/ordinary_NewGame_inputs.json")


def replay(number):
    prior_version, end = CASES[number]
    target = ROOT / f"B{number}"
    historical = Path(f"work/analysis/Rafael_B{number}_scene_fixtures_v{prior_version}"
                      "/two_complete_source_English_original_Rafael_prelude_fixtures.json")
    reference, = [f for f in base.load(historical)["fixtures"] if f["version"] == "English"]
    proof = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == proof["candidate_sha256"] and proof["whole_parent_inverse"]
    group, = [g for g in proof["groups"] if g["block"] == number]
    candidate = base.NdsImage.open(stage.ROM)
    original = candidate.read_file(PATH)
    archive = native.IlnkContainer.parse(original)
    opening, exchange = (archive.blocks[i] for i in (44, number))
    prelude = bytes.fromhex(reference["original_opening_prelude_hex"])
    assert opening[8:40] == prelude and len(prelude) == 32
    assert (opening[:4], opening[6:8]) == (exchange[:4], exchange[6:8])
    assert native.digest(exchange) == group["after"]
    payload = exchange[8:stage.logical_end(exchange)]
    logical = bytearray(opening[:8] + prelude + payload)
    pack_into("<H", logical, 4, len(logical) - 8)
    fixture = bytes(logical) + bytes(-len(logical) % 4)
    assert fixture[40:len(logical)] == payload
    target.mkdir(parents=True)
    rom = target / f"Rafael_B{number}_RESEARCH_ONLY.nds"
    archive.blocks[44] = fixture
    candidate.replace_file(PATH, archive.to_bytes())
    candidate.save(rom)
    loaded = base.NdsImage.open(rom)
    assert native.IlnkContainer.parse(loaded.read_file(PATH)).blocks[44] == fixture
    loaded.replace_file(PATH, original)
    assert bytes(loaded.rom.save()) == stage.ROM.read_bytes()
    base.save(target / "fixture.json", dict(candidate_sha256=proof["candidate_sha256"], research_ROM=str(rom),
        research_ROM_sha256=base.digest(rom), preserved_block=number, preserved_command_bytes_sha256=native.digest(payload),
        original_prelude=prelude.hex(), original_prelude_evidence=str(historical),
        source_controls_exact_under_constant_shift=True, exact_candidate_inverse=True, natural_activation=False))
    inputs = target / "inputs.json"
    presses = range(4000, end - 210, 240)
    base.save(inputs, base.load(INPUTS) + [dict(start=f, duration=5, buttons=["A"]) for f in presses])
    frames = sorted({3900, end - 1, *[f + 208 for f in presses]})
    harness = release_checks.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(rom), "--out", str(target / "capture"), "--frames", str(end),
                "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                "--capture-at", *map(str, frames)]
    harness.main()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=(*map(str, CASES), "startup", "patch"))
    case = parser.parse_args().case
    if case.isdecimal():
        replay(int(case))
    else:
        template = release_checks.template
        action = template.common.startup if case == "startup" else template.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=stage.native, play=template.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
