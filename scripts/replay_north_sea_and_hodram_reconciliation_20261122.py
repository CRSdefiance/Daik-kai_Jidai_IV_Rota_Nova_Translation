"""Verify the revised North Sea and SC1 B66 panels in focused emulator replays."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_palace_eirene_pereira_london_20261122 as prior
from scripts import stage_north_sea_and_hodram_reconciliation_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
RAFAEL_ROOT = ROOT / "rafael"
ROM = RAFAEL_ROOT / "North_Sea_FOCUSED_ONLY.nds"
REPORT = RAFAEL_ROOT / "capture/capture_report.json"
RAFAEL_LIVE = RAFAEL_ROOT / "verified_gameplay.json"
SEQUENCE = tuple((49, i) for i in (90, 126, 213, 266, 271, 328, 367))
INPUT = [(4000 + i * 340, "A") for i in range(len(SEQUENCE))]
END = INPUT[-1][0] + 720
FRAMES = (3900, *(frame + 260 for frame, _ in INPUT[:-1]), END - 1)
rafael_scope = prior.rafael_scope | globals() | dict(ROOT=RAFAEL_ROOT, LIVE=RAFAEL_LIVE, prior=prior.rafael_scope["prior"])
rafael_source = checked_text(prior.rafael_source, {
    'groups[152]["commands"][-1]': 'groups[49]["commands"][-1]',
    prior.ROM.name: ROM.name,
})
exec(compile(rafael_source, __file__ + "::Rafael", "exec"), rafael_scope)
rafael_verify = FunctionType(prior.rafael_verify.__code__,
    prior.rafael_verify.__globals__ | globals() | dict(ROOT=RAFAEL_ROOT, LIVE=RAFAEL_LIVE))

HODRAM_ROOT = ROOT / "route1"
HODRAM_ROM = HODRAM_ROOT / "Hodram_B66_FOCUSED_ONLY.nds"
HODRAM_REPORT = HODRAM_ROOT / "capture/capture_report.json"
HODRAM_LIVE = HODRAM_ROOT / "verified_gameplay.json"
SAMPLE = tuple((66, i) for i in (6, 26, 45, 56, 68, 72))
HODRAM_END = 4100 + len(SAMPLE) * 360
CASES = {1: prior.CASES[1] | dict(end=HODRAM_END, sample=SAMPLE)}
hodram_scope = prior.hodram_scope | globals() | dict(ROM=HODRAM_ROM, REPORT=HODRAM_REPORT, LIVE=HODRAM_LIVE, END=HODRAM_END)
exec(compile(prior.prior.prior.hodram.replay_source, __file__ + "::Hodram", "exec"), hodram_scope)
hodram_source = checked_text(prior.hodram_source, {'london_rescue_gameplay_': 'hodram_B66_gameplay_'})
exec(compile(hodram_source, __file__ + "::Hodram-body-and-labels", "exec"), hodram_scope)
combine = FunctionType(prior.combine.__code__, prior.combine.__globals__ | globals())


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("rafael_replay", "rafael_verify", "hodram_replay", "hodram_verify", "combine"))
    action = cli.parse_args().action
    if action == "rafael_replay":
        rafael_scope["replay"]()
    elif action == "rafael_verify":
        rafael_verify()
    elif action == "hodram_replay":
        hodram_scope["replay"](1)
    elif action == "hodram_verify":
        hodram_scope["verify"]()
    else:
        combine()
