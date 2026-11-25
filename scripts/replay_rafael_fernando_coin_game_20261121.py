"""Replay Fernando's dialogue and enter the source coin game in separate focused runs."""
from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace
import sys

from scripts import replay_rafael_refit_sailing_lessons_20261121 as template
from scripts import stage_rafael_fernando_coin_game_20261121 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base, native, earlier = stage.base, stage.native, template.earlier
ROOT = stage.ROOT / "focused_rafael"
REPORT = ROOT / "capture/capture_report.json"
STARTUP_CAPTURE = stage.ROOT / "startup/capture/capture_report.json"
STARTUP_PLAN = stage.ROOT / "startup/identical_inputs.json"
PATH = template.PATH
SAMPLES = {178: (16, 20, 24, 33, 64, 89, 107, 116, 127, 131, 139, 147, 155, 161, 211,
                 218, 231, 234, 237, 240, 257, 265, 275, 283, 336)}
FIRST, END, STEP = 4120, 14300, 360
COIN, COIN_END = stage.ROOT / "coin_ui", 14400
COIN_PLAY = stage.ROOT / "coin_ui_play"
COIN_TOUCH = stage.ROOT / "coin_ui_touch"
COIN_ROUND, ROUND_END = stage.ROOT / "coin_ui_round", 17400
COIN_CENTERS = ((48, 67), (96, 68), (126, 68), (168, 84), (207, 69),
                (48, 99), (55, 131), (87, 131), (118, 132), (176, 120))


dialogue_source = checked_text(getsource(template.replay), {
    '"Rafael_Refit_And_Sails_RESEARCH_ONLY.nds"': '"Rafael_Fernando_Dialogue_RESEARCH_ONLY.nds"',
})
scope = vars(template) | globals()
exec(compile(dialogue_source, __file__, "exec"), scope)


def coin_ui(case):
    proof = base.load(stage.PROOF)
    candidate = base.digest(stage.ROM)
    assert proof["candidate_sha256"] == candidate and proof["whole_parent_inverse"]
    group, = proof["groups"]
    select, = [c for c in group["commands"] if c["word"] == 0xC101]
    assert select["source_offset"] == 388 and select["source"] == select["current"] == select["stored"] == "01c1"
    clean = base.NdsImage.open(native.CLEAN)
    source = native.IlnkContainer.parse(clean.read_file(PATH)).blocks[178]
    assert source[388:390] == b"\x01\xc1"
    image = base.NdsImage.open(stage.ROM)
    before = image.read_file(PATH)
    archive = native.IlnkContainer.parse(before)
    opening, lesson = (archive.blocks[i] for i in (44, 178))
    at = select["stored_offset"]
    assert lesson[at:at+2] == b"\x01\xc1" and opening[26:28] == b"\x00\x49"
    archive.blocks[44] = opening[:26] + lesson[at:at+2] + opening[28:]
    image.replace_file(PATH, archive.to_bytes())
    folder = {"coin": COIN, "coin-play": COIN_PLAY, "coin-touch": COIN_TOUCH, "coin-round": COIN_ROUND}[case]
    folder.mkdir()
    fixture = folder / "Rafael_Original_Coin_UI_RESEARCH_ONLY.nds"
    image.save(fixture)
    inverse = base.NdsImage.open(fixture)
    inverse.replace_file(PATH, before)
    assert bytes(inverse.rom.save()) == stage.ROM.read_bytes()
    base.save(folder / "fixture.json", dict(candidate_sha256=candidate, fixture=str(fixture),
        fixture_sha256=base.digest(fixture), source_opcode="01c1", source_block=178, source_offset=388,
        substituted_opening_block=44, substituted_instruction_offset=26, exact_candidate_inverse=True,
        natural_activation=False, original_recruitment_branch_present=False))
    touches = []
    options = []
    end = COIN_END
    if case == "coin-round":
        end = ROUND_END
        turns = list(range(5000, end - 550, 590))
        moves = [(4300, "A"), (4580, "A")]
        for i, frame in enumerate(turns):
            moves.extend(((frame, "A"), (frame + 125, "A"), (frame + 255, "X")))
            touches.append(dict(start=frame+60, duration=8, buttons=[], touch=list(COIN_CENTERS[i % len(COIN_CENTERS)])))
        extra = {frame + delta for frame in turns for delta in (205, 440, 565)}
        options.append("--touchscreen")
    elif case == "coin-touch":
        turns = list(range(5000, COIN_END - 500, 620))
        moves = [(4300, "A"), (4580, "A")]
        for i, frame in enumerate(turns):
            moves.extend(((frame, "A"), (frame + 210, "X")))
            centers_for_turn = (COIN_CENTERS[i % len(COIN_CENTERS)], COIN_CENTERS[(i+5) % len(COIN_CENTERS)])
            for offset, point in zip((60, 130), centers_for_turn, strict=True):
                touches.append(dict(start=frame+offset, duration=8, buttons=[], touch=list(point)))
        extra = {frame + delta for frame in turns for delta in (180, 415, 555)}
        options.append("--touchscreen")
    elif case == "coin-play":
        turns = list(range(5000, COIN_END - 500, 620))
        moves = [(4300, "A"), (4580, "A")]
        moves.extend((frame + offset, key) for frame in turns for offset, key in ((0, "A"), (145, "X")))
        extra = {frame + delta for frame in turns for delta in (85, 355, 550)}
    else:
        moves = [(i, "A") for i in range(4300, COIN_END - 300, 270)]
        extra = {i + n for i, _ in moves for n in (200, 250)}
    inputs = folder / "inputs.json"
    commands = base.load(earlier.STARTUP_INPUTS) + touches + [dict(start=i, duration=6, buttons=[key]) for i, key in moves]
    base.save(inputs, sorted(commands, key=lambda row: row["start"]))
    frames = sorted({3900, 4140, 4510, 4800, end - 1, *extra})
    harness = earlier.checks.template.games.harness
    sys.argv = [harness.__file__, "--rom", str(fixture), "--out", str(folder / "capture"), "--frames", str(end),
                "--inputs-json", str(inputs), "--press-start", "-1", *options, "--capture-every", "999999",
                "--capture-at", *map(str, frames)]
    harness.main()


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=("focused", "coin", "coin-play", "coin-touch", "coin-round", "startup", "patch"))
    case = parser.parse_args().case
    if case == "focused":
        scope["replay"]()
    elif case in ("coin", "coin-play", "coin-touch", "coin-round"):
        coin_ui(case)
    else:
        prior = earlier.checks.template
        action = prior.common.startup if case == "startup" else prior.common.reconstruct
        runtime = SimpleNamespace(active=stage.parent, PROOF=stage.PROOF, ROOT=stage.ROOT, ROM=stage.ROM,
                                  native=native, play=prior.games)
        FunctionType(action.__code__, action.__globals__ |
                     {"stage": runtime, "STARTUP_CAPTURE": STARTUP_CAPTURE, "PLAN": STARTUP_PLAN})()
