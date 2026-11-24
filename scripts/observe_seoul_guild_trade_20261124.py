"""Replay both buy and sale decisions at the Seoul Guild using the original save."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import register_london_guild_display_20261124 as active
from scripts.observe_setup_save_common_v1 import scoped_observer
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read


ROOT = Path(".codex-release-work/shared_display_20261123/seoul_guild_trade_20261124")
PLAN = Path("work/analysis/guild_transactions_actual_v2237/run_plan.json")
EARLIER = Path("work/analysis/guild_transactions_verification_v2244/current_Guild_full_foreground_state_transitions.json")
CASE = "seoul"


def schedule(case):
    assert case == CASE
    plan = read(PLAN)
    assert digest(PLAN) == read(EARLIER)["source_plan_sha256"] and plan["no_savestate_or_any_synthetic_fixture"]
    history = Path(plan["prior_report"])
    assert digest(history) == plan["prior_report_sha256"]
    inputs = Path(plan["inputs"])
    assert digest(inputs) == plan["inputs_sha256"]
    donor = dict(source=plan["original_genuine_save"], source_sha256=plan["donor_sha256"])
    assert digest(donor["source"]) == donor["source_sha256"]
    return read(inputs), plan["captures"], plan["configured_maximum_frames"], PLAN, donor


def main():
    assert digest(REGISTRY) == read(active.RELEASE)["registry_sha256"]
    ROOT.mkdir(parents=True, exist_ok=True)
    scope = vars(playback) | dict(ROOT=ROOT, parent=active, observer=scoped_observer, get_schedule=schedule,
                                  FOCUS=set(range(3668)), __file__=__file__)
    source = checked_text(getsource(playback.main), {
        "prepared_gallery_save=bool(donor)": "ordinary_cartridge_save=bool(donor)",
    })
    exec(compile(source, __file__ + "::Seoul-Guild-trade", "exec"), scope)
    scope["main"](CASE)


if __name__ == "__main__":
    main()
