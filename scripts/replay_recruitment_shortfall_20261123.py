"""Reach Manuel's shortfall prompt through the original Tavern flow."""

import sys
from argparse import ArgumentParser
from inspect import getsource
from io import StringIO
from json import dumps
from types import FunctionType

from scripts import headless_desmume_v193 as harness
from scripts import native_condition_fixture_v520 as fixture_adapter
from scripts import native_recruit_shortfall_fixture_v782 as earlier_fixture
from scripts import replay_recruitment_capacity_20261123 as capacity
from scripts import stage_recruit_crew_20261120 as recruitment
from scripts import stage_recruitment_shortfall_20261123 as stage
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import digest, read, write


ROOT = stage.ROOT
PLAY = ROOT / "focused_qualified"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
PATCH_PROOF = ROOT / "clean_patch_proof.json"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
PAUSE, END = 15900, 18360
FRAMES = (13600, 13880, 15900, 16400, 17240, 17520, 17800, 18080, 18360)
REQUEST = dict(mode="required-crew-shortfall")
CREW = 9


def matches_source(arm, clean, lo, hi):
    if (lo, hi) != (0x57408, 0x576CC):
        return arm[lo:hi] == clean[lo:hi]
    expected = bytearray(clean[lo:hi])
    number = recruitment.number
    for address in recruitment.CALLS:
        at = address - recruitment.BASE - lo
        expected[at:at + 4] = number.assemble(f"bl {number.HELPER}", address)
    return arm[lo:hi] == bytes(expected)


def setup(active_arm_sha):
    source = checked_text(getsource(earlier_fixture.set_condition), {
        "assert arm[lo:hi] == clean[lo:hi]": "assert matches_source(arm, clean, lo, hi)",
        "Exact V780/V782 and declared required-crew-shortfall fixture required": "Exact current ARM9 and declared required-crew-shortfall fixture required",
        'get(0x181B4, (model, 0))': 'get(0x181B4, (model, CREW))',
        'get(0x181BC, (model,)) == 0 and get(0x35048, (fleet,)) == 0':
            'get(0x181BC, (model,)) == CREW and get(0x35048, (fleet,)) == CREW',
        "'crew_after': 0": "'crew_after': CREW",
    })
    scope = vars(earlier_fixture) | dict(ARMS={active_arm_sha}, CREW=CREW, matches_source=matches_source)
    exec(compile(source, __file__ + "::current-crew-halfword-fixture", "exec"), scope)
    return scope["set_condition"]


def replay(side):
    parent, staged = map(read, (stage.parent.RELEASE, stage.PROOF))
    rom, sha = (parent["candidate"], parent["candidate_sha256"]) if side == "current" else (
        staged["candidate"], staged["candidate_sha256"])
    assert digest(rom) == sha and staged["target_ARM9_sha256"] == parent["target_ARM9_sha256"]
    events, _, end, source, donor = capacity.schedule("azores")
    assert end == END and digest(donor["source"]) == donor["source_sha256"]
    folder = PLAY / side
    folder.mkdir(parents=True)
    inputs, commands = folder / "inputs.json", folder / "commands.json"
    nav = [dict(until=END, condition_fixture=REQUEST), dict(stop=True)]
    write(inputs, events)
    write(commands, nav)
    originals = fixture_adapter.set_condition, sys.argv, sys.stdin
    try:
        fixture_adapter.set_condition = setup(parent["target_ARM9_sha256"])
        sys.stdin = StringIO("".join(dumps(row) + "\n" for row in nav))
        sys.argv = [harness.__file__, "--rom", rom, "--out", str(folder / "capture"),
                    "--frames", str(END + 1), "--inputs-json", str(inputs), "--press-start", "-1",
                    "--touchscreen", "--battery-save", donor["source"], "--capture-every", "999999",
                    "--pause-at", str(PAUSE), "--allow-condition-fixtures", "--dump-pause-ram",
                    "--dump-capture-ram", "--capture-at", *map(str, FRAMES)]
        harness.main()
    finally:
        fixture_adapter.set_condition, sys.argv, sys.stdin = originals
    report = read(folder / "capture/capture_report.json")
    assert report["ROM_sha256"] == sha and report["frames"] == END
    assert not report["callback_errors"] and digest(donor["source"]) == donor["source_sha256"]


def check(action):
    scope = vars(capacity) | dict(stage=stage, PATCH=PATCH, REBUILT=REBUILT, PATCH_PROOF=PATCH_PROOF,
                                  STARTUP_CAPTURE=STARTUP_CAPTURE)
    FunctionType(capacity.check.__code__, scope)(action)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("current", "revised", "patch", "startup"))
    action = cli.parse_args().action
    (replay if action in {"current", "revised"} else check)(action)
