"""Replay the revised farewell, private meeting, and reconciliation as exact excerpts."""

from argparse import ArgumentParser

from scripts import replay_north_sea_and_hodram_reconciliation_20261122 as prior
from scripts import replay_trade_house_charles_and_earrings_20261122 as trade
from scripts import stage_hodram_farewells_and_maria_20261122 as stage
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
ROOT = stage.ROOT / "focused_gameplay"
HODRAM_ROOT = ROOT / "route1"
ROM = HODRAM_ROOT / "Hodram_Farewells_And_Maria_FOCUSED_ONLY.nds"
REPORT, LIVE = HODRAM_ROOT / "capture/capture_report.json", HODRAM_ROOT / "verified_gameplay.json"
SAMPLE = (
    *((65, n) for n in (46, 71, 89, 120, 128)),
    *((67, n) for n in (36, 55, 63, 66, 102, 165, 168, 172, 227, 238)),
    *((69, n) for n in (11, 19, 34, 42)),
)
END = 4100 + len(SAMPLE) * 360
CASES = {1: prior.CASES[1] | dict(end=END, sample=SAMPLE)}
scope = prior.hodram_scope | globals()
exec(compile(trade.hodram.replay_source, __file__ + "::Hodram-cold-boot", "exec"), scope)
verify_source = checked_text(prior.hodram_source, {"hodram_B66_gameplay_": "hodram_farewells_maria_gameplay_"})
exec(compile(verify_source, __file__ + "::exact-body-and-nameplate-captures", "exec"), scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("replay", "verify"))
    if cli.parse_args().action == "replay":
        scope["replay"](1)
    else:
        scope["verify"]()
