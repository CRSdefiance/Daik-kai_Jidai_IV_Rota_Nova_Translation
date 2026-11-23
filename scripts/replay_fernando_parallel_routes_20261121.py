"""Replay selected Hodram and Lil commands in the original initialized game."""
from argparse import ArgumentParser
from pathlib import Path
from struct import pack_into
from types import FunctionType, SimpleNamespace
import sys

from scripts import replay_rafael_fernando_coin_game_20261121 as earlier
from scripts import stage_fernando_parallel_routes_20261121 as stage


base, native = stage.base, stage.native
ROOT = stage.ROOT / "focused"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
CASES = {
    1: dict(opening=42, prefix=42, block=169, end=10300,
            input="work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json",
            sample=(16, 20, 24, 33, 70, 81, 89, 108, 111, 114, 117, 132, 136, 149, 157, 208)),
    2: dict(opening=22, prefix=56, block=127, end=11600,
            input="work/analysis/movie_viewport_v303/lil_start_inputs.json",
            sample=(13, 24, 32, 39, 42, 50, 57, 65, 85, 89, 96, 100, 107, 110, 125, 129, 137, 141, 145)),
}


def replay(route):
    case = CASES[route]
    path = f"/data/SC{route}.DK4"
    stored = base.load(stage.PROOF)
    assert stored["candidate_sha256"] == base.digest(stage.ROM) and stored["whole_parent_inverse"]
    group, = [g for g in stored["groups"] if g["route"] == route]
    assert group["file_path"] == path and group["block"] == case["block"]
    image, parent = map(base.NdsImage.open, (stage.ROM, stage.parent.ROM))
    before = image.read_file(path)
    archive = native.IlnkContainer.parse(before)
    init, block = (archive.blocks[i] for i in (case["opening"], case["block"]))
    assert native.digest(block) == group["after"]
    assert native.IlnkContainer.parse(parent.read_file(path)).blocks[case["opening"]] == init
    inventory, _, _ = native.scoped_inventory()
    arm = image.read_file(native.ARM)
    commands, _ = inventory(arm, init)
    first = next(c["offset"] for c in commands if c["word"] == 0x4000)
    assert first == case["prefix"]
    draft = base.load(stage.review.OUTPUT)
    indices = {row["id"]: row["source_record_index"] for row in draft["records"] if row["route"] == route}
    selected = {indices[c["record_ids"][0]]: c for c in group["commands"] if c["record_ids"]}
    body = bytearray(init[:first])
    spans = []
    for index in case["sample"]:
        command = selected[index]
        at = command["stored_offset"]
        raw = bytes.fromhex(command["stored"])
        assert block[at:at+len(raw)] == raw and command["word"] in (0x4000, 0x2100)
        spans.append(dict(ids=command["record_ids"], offset=len(body), original_offset=at,
                            command_sha256=native.digest(raw), block=case["block"]))
        body.extend(raw)
    end = group["commands"][-1]
    assert end["word"] == 0
    body.extend(bytes.fromhex(end["stored"]))
    pack_into("<H", body, 4, len(body) - 8)
    body.extend(bytes(-len(body) % 4))
    check, _ = inventory(arm, bytes(body))
    by_offset = {item["offset"]: item for item in check}
    assert all(native.digest(bytes.fromhex(by_offset[s["offset"]]["whole_command_hex"])) == s["command_sha256"]
               for s in spans)
    archive.blocks[case["opening"]] = bytes(body)
    image.replace_file(path, archive.to_bytes())
    folder = ROOT / f"route{route}"
    folder.mkdir(parents=True)
    research = folder / f"Fernando_SC{route}_RESEARCH_ONLY.nds"
    image.save(research)
    inverse = base.NdsImage.open(research)
    inverse.replace_file(path, before)
    assert bytes(inverse.rom.save()) == stage.ROM.read_bytes()
    base.save(folder / "fixture.json", dict(candidate_sha256=stored["candidate_sha256"], fixture=str(research),
        fixture_sha256=base.digest(research), exact_candidate_inverse=True, copied_native_commands=spans, route=route,
        natural_activation=False, source_block=case["block"], original_opening_block=case["opening"]))
    inputs = folder / "inputs.json"
    moves = list(range(4100, case["end"] - 340, 360))
    source = Path(case["input"])
    base.save(inputs, base.load(source) + [dict(start=i, duration=6, buttons=["A"]) for i in moves])
    frames = sorted({3900, 4050, case["end"] - 1, *[i + n for i in moves for n in (260, 340)]})
    harness = earlier.earlier.checks.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(research), "--out", str(folder / "capture"), "--frames", str(case["end"]),
                "--inputs-json", str(inputs), "--press-start", "-1", "--capture-every", "999999",
                "--capture-at", *map(str, frames)]
    harness.main()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("hodram", "lil", "startup", "patch"))
    case = parser.parse_args().case
    if case in ("hodram", "lil"):
        replay(1 if case == "hodram" else 2)
    else:
        prior = earlier.earlier.checks.template
        action = prior.common.startup if case == "startup" else prior.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=native, play=prior.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
