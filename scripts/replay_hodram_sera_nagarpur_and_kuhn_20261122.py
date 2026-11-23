"""Replay Sera's memories, Nagarpur's taunt and the Indian Ocean legend."""

from argparse import ArgumentParser

from scripts import replay_hodram_farewells_and_maria_20261122 as prior
from scripts import stage_hodram_sera_nagarpur_and_kuhn_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = stage.ROOT / "focused_gameplay"
HODRAM_ROOT = ROOT / "route1"
ROM = HODRAM_ROOT / "Hodram_Sera_Nagarpur_And_Kuhn_FOCUSED_ONLY.nds"
REPORT = HODRAM_ROOT / "capture/capture_report.json"
LIVE = HODRAM_ROOT / "verified_gameplay.json"
SAMPLE = (
    *((61, number) for number in (28, 32, 44)),
    *((62, number) for number in (76, 83)),
    *((63, number) for number in (96, 100, 140)),
    *((64, number) for number in (11, 55, 63, 66)),
)
END = 4100 + len(SAMPLE) * 360
CASES = {1: prior.CASES[1] | dict(end=END, sample=SAMPLE)}
scope = prior.scope | globals()
exec(compile(prior.trade.hodram.replay_source, __file__ + "::Hodram-replay", "exec"), scope)
verify_source = checked_text(prior.verify_source, {
    "hodram_farewells_maria_gameplay_": "hodram_sera_nagarpur_kuhn_gameplay_",
})
exec(compile(verify_source, __file__ + "::body-and-speaker-verification", "exec"), scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "verify"))
    if cli.parse_args().action == "replay":
        scope["replay"](1)
    else:
        scope["verify"]()
