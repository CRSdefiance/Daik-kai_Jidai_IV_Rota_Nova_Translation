"""Verify representative palace, Eirene, Pereira and London panels after cold boot."""

from argparse import ArgumentParser
from types import FunctionType

from scripts import replay_mosque_elysion_mikhail_20261122 as prior
from scripts import stage_palace_eirene_pereira_london_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
RAFAEL_ROOT = ROOT / "rafael"
ROM = RAFAEL_ROOT / "Palace_Eirene_Pereira_FOCUSED_ONLY.nds"
REPORT = RAFAEL_ROOT / "capture/capture_report.json"
RAFAEL_LIVE = RAFAEL_ROOT / "verified_gameplay.json"
SEQUENCE = ((143, 5), (143, 40), (143, 129), (143, 153), (143, 160), (143, 332), (143, 372),
            (145, 47), (145, 157), (145, 203), (145, 212), (152, 54), (152, 128), (152, 217), (152, 221))
INPUT = [(4000 + i * 340, "A") for i in range(len(SEQUENCE))]
END = INPUT[-1][0] + 720
FRAMES = (3900, *(frame + 260 for frame, _ in INPUT[:-1]), END - 1)
rafael_scope = prior.rafael_scope | globals() | dict(ROOT=RAFAEL_ROOT, LIVE=RAFAEL_LIVE, prior=prior.rafael_scope["prior"])
rafael_source = checked_text(prior.rafael_source, {
    'groups[123]["commands"][-1]': 'groups[152]["commands"][-1]',
    prior.ROM.name: ROM.name,
})
exec(compile(rafael_source, __file__ + "::Rafael", "exec"), rafael_scope)
rafael_verify = FunctionType(prior.rafael_verify.__code__,
    prior.rafael_verify.__globals__ | globals() | dict(ROOT=RAFAEL_ROOT, LIVE=RAFAEL_LIVE))

HODRAM_ROOT = ROOT / "route1"
HODRAM_ROM = HODRAM_ROOT / "London_Rescue_FOCUSED_ONLY.nds"
HODRAM_REPORT = HODRAM_ROOT / "capture/capture_report.json"
HODRAM_LIVE = HODRAM_ROOT / "verified_gameplay.json"
SAMPLE = tuple((86, i) for i in (12, 47, 51, 100, 139, 145, 295, 315))
HODRAM_END = 4100 + len(SAMPLE) * 360
CASES = {1: prior.CASES[1] | dict(end=HODRAM_END, sample=SAMPLE)}
hodram_scope = prior.hodram_scope | globals() | dict(ROM=HODRAM_ROM, REPORT=HODRAM_REPORT, LIVE=HODRAM_LIVE, END=HODRAM_END)
exec(compile(prior.prior.hodram.replay_source, __file__ + "::Hodram", "exec"), hodram_scope)
hodram_source = checked_text(prior.hodram_source, {'elysion_and_mikhail_gameplay_': 'london_rescue_gameplay_'})
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
