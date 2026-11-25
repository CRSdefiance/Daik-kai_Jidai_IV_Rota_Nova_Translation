"""Replay representative changed lines with original portraits and names."""

from argparse import ArgumentParser
from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import replay_rafael_confrontations_and_maria_wraps_20261122 as rafael
from scripts import replay_tavern_and_proof_exchanges_20261122 as hodram
from scripts import stage_trade_house_charles_and_earrings_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = stage.ROOT / "focused_gameplay"
LIVE = ROOT / "verified_gameplay.json"
RAFAEL_ROOT = ROOT / "rafael"
ROM = RAFAEL_ROOT / "Rafael_Trade_And_Charles_FOCUSED_ONLY.nds"
REPORT = RAFAEL_ROOT / "capture/capture_report.json"
RAFAEL_LIVE = RAFAEL_ROOT / "verified_gameplay.json"
SEQUENCE = ((65, 17), (65, 26), (65, 54), (73, 6), (73, 15), (73, 18),
            (86, 21), (86, 36), (86, 55), (86, 133))
INPUT = [(4000 + i * 340, "A") for i in range(len(SEQUENCE))]
END = INPUT[-1][0] + 720
FRAMES = (3900, *(frame + 260 for frame, _ in INPUT[:-1]), END - 1)
rafael_scope = rafael.rafael_scope | globals() | dict(ROOT=RAFAEL_ROOT, LIVE=RAFAEL_LIVE)
rafael_source = checked_text(rafael.rafael_source, {
    'groups[82]["commands"][-1]': 'groups[86]["commands"][-1]',
    rafael.ROM.name: ROM.name,
})
exec(compile(rafael_source, __file__ + "::Rafael-cold-boot", "exec"), rafael_scope)
rafael_verify = FunctionType(rafael.rafael_verify.__code__,
    rafael.rafael_verify.__globals__ | globals() | dict(ROOT=RAFAEL_ROOT, LIVE=RAFAEL_LIVE))

HODRAM_ROOT = ROOT / "route1"
HODRAM_ROM = HODRAM_ROOT / "Hodram_Earrings_FOCUSED_ONLY.nds"
HODRAM_REPORT = HODRAM_ROOT / "capture/capture_report.json"
HODRAM_LIVE = HODRAM_ROOT / "verified_gameplay.json"
SAMPLE = tuple((210, i) for i in (5, 9, 70, 73, 77, 99, 114))
HODRAM_END = 4100 + len(SAMPLE) * 360
CASES = {1: hodram.CASES[1] | dict(end=HODRAM_END, sample=SAMPLE)}
hodram_scope = hodram.scope | globals() | dict(ROM=HODRAM_ROM, REPORT=HODRAM_REPORT,
    LIVE=HODRAM_LIVE, END=HODRAM_END, stage=SimpleNamespace(**(vars(stage) | {"CHOICES_AND_PAGES": stage.CHOICE_PROOF})))
exec(compile(hodram.replay_source, __file__ + "::Hodram-cold-boot", "exec"), hodram_scope)
hodram_source = checked_text(getsource(hodram.verify), {
    'tavern_and_proofs_gameplay_': 'earrings_gameplay_',
})
exec(compile(hodram_source, __file__ + "::Hodram-labels-and-planes", "exec"), hodram_scope)


def combine():
    assert not LIVE.exists()
    each = ((0, base.load(RAFAEL_LIVE)), (1, base.load(HODRAM_LIVE)))
    observations, sheets, reports, exits = [], [], {}, {}
    candidate = base.digest(stage.ROM)
    for route, proof in each:
        assert proof["candidate_sha256"] == candidate and proof["initialized_excerpts"]
        assert not proof["natural_story_triggers_claimed"]
        observations.extend(row | dict(file_path=f"/data/SC{route}.DK4") for row in proof["observations"])
        sheets.extend(proof["sheets"])
        reports[route] = proof["report_sha256"]
        exits[route] = proof["return_frame"]
    assert len(observations) == len(SEQUENCE) + len(SAMPLE)
    base.save(LIVE, dict(candidate_sha256=candidate, initialized_excerpts=True, natural_story_triggers_claimed=False,
        observed_speech_pages=len(observations), observations=observations, sheets=sheets,
        rafael_report_sha256=reports[0], hodram_report_sha256=reports[1],
        rafael_return=exits[0], hodram_return=exits[1], hardware=False))


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
