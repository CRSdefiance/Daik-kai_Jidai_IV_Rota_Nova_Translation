"""Verify the Market introduction, its small-town instructions and the return."""

from inspect import getsource
from types import FunctionType, SimpleNamespace

from scripts import stage_market_introduction_wrap_20261123 as stage
from scripts import verify_square_and_market_reward_wraps_20261123 as earlier
from scripts.source_locked_derivation_v5118 import checked_text


base = stage.base
LIVE = stage.ROOT / "focused_dialogue.json"


def main():
    assert not LIVE.exists()
    stored = base.load(stage.PROOF)
    assert base.digest(stage.ROM) == stored["candidate_sha256"]
    previous = base.load(stage.parent.RELEASE)
    assert base.digest(stage.parent.ROM) == previous["candidate_sha256"] == stored["predecessor_sha256"]
    ctx = stage.town.RegisteredRuntime(stage.parent.RELEASE, previous["own_registered_startup"], captain=3)
    cpu, _, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    rom = base.NdsImage.open(stage.ROM)
    arm, kanji = (rom.read_file(path) for path in (stage.ARM, "/GRP/KANJI.FNT"))
    assert arm == ctx.arm
    raster, _, _ = stage.town.font_tools(rom)
    displays = {}
    for row in stored["records"]:
        key = row["message_ID"]
        if key not in stage.CHAIN:
            continue
        old, _ = stage.display(ctx, bytes.fromhex(row["current_hex"]), key, cpu)
        new = bytes.fromhex(row["display_hex"])
        old_plane, new_plane = (stage.town.render_portrait(raster, arm, kanji, data)[0] for data in (old, new))
        assert stage.native.digest(new_plane) == row["native_plane_sha256"]
        displays[key] = (old.hex(), new.hex(), old_plane, new_plane)
    read_run = checked_text(getsource(earlier.market.read_run), {
        "[2, 16, 1, 2]": f"[2, {stage.BRANCH_INPUT}, 1, 2]",
        "assert report['frames'] == plan['frames'] == 12001":
            "assert report['frames'] == plan['frames'] == 12001\n"
            "    assert plan['synthetic_qualification2_quantity12_and_bonus1_inputs_at_original_BBCA4']",
    })
    scope = vars(earlier.market) | {"CHAIN": stage.CHAIN}
    exec(compile(read_run, __file__ + "::read_introduction", "exec"), scope)
    market = SimpleNamespace(**(vars(earlier.market) | {"CHAIN": stage.CHAIN, "read_run": scope["read_run"]}))
    derived = vars(earlier) | {"stage": stage, "market": market}
    for name in ("display_hold", "render_sheet", "market_holds"):
        derived[name] = FunctionType(derived[name].__code__, derived)
    evidence = {str(stage.PROOF): base.digest(stage.PROOF)}
    holds, returns, sheets = derived["market_holds"](stored, displays, evidence)
    assert [row["message_ID"] for row in holds] == stage.CHAIN
    base.save(LIVE, dict(candidate_sha256=stored["candidate_sha256"], predecessor_sha256=stored["predecessor_sha256"],
        original_reward_sequence=stage.CHAIN, observed=dict(market=holds), revised_holds=1, retained_holds=2,
        menu_transitions=len(returns), revised_offline_only_records=[], ordinary_gameplay=False,
        focused_fixtures=True, naturally_earned_reward=False, hardware=False, returns=returns,
        evidence=evidence, sheets=sheets))
    print("Verified the revised offer, both retained panels and the matching return frames.")


if __name__ == "__main__":
    main()
