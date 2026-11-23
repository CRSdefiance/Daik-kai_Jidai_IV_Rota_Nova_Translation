"""Prepare all fourteen Rafael midroute exchanges through their exact native consumers."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import cleanup_hodram_early_and_midroute_wraps_20261122 as checkpoint
from scripts import pair_rafael_midroute_exchanges_20261122 as paired
from scripts import register_hodram_early_and_midroute_wraps_20261122 as active
from scripts import stage_hodram_early_and_midroute_wraps_20261122 as prior
from scripts.stage_rafael_fleet_and_crew_exchanges_20261122 import preflight_source as progressive_preflight_source
from scripts import stage_forest_expeditions_20261118 as forest
from scripts.stage_hamburg_ceramics_cross_route_20261120 import current_fe_painter
from scripts.source_locked_derivation_v5118 import checked_text

base, native, established, typed = prior.base, prior.native, prior.established, prior.typed
parent = SimpleNamespace(ROM=active.ROM, MANIFEST=active.MANIFEST, RELEASE=active.RELEASE,
    STARTUP_CAPTURE=active.STARTUP_CAPTURE, guard_spec=active.scope["guard_spec"],
    bind_registered_story_percent_guard=active.scope["bind_registered_story_percent_guard"])
BATCH = Path(".codex-release-work/rafael_midroute_exchanges_20261122/release")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Rafael_Midroute_Exchanges_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF = ROOT / "modal_native_display.json"
MANUSCRIPTS = (Path(__file__).with_name("rafael_midroute_exchanges_20261122.md"),)
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)

section_source = checked_text(prior.section_source, {r"SC([1])": r"SC([0])"})
review_source = checked_text(prior.review_source, {
    'if row["native_command_word"] == 0x2100:': 'if row["native_command_word"] in (0x2100, 0x2200):',
    'decisions.pop(f"C{slot}")': 'decisions.pop(f\'{row["source_command_offset"]}.{slot}\')',
    '            if selector == 254:\n                assert change == "retention"':
        '            if selector == 254 and change != "retention":\n'
        '                assert (block, ordinal) == (118, 125) and change == "wrap_only"',
    'len(records)==278 and len(captions)==4 and len(leads)==24 and sum(r["kind"]=="system" for r in records)==20':
        'len(records)==275 and len(captions)==5 and len(leads)==21 and sum(r["kind"]=="system" for r in records)==17',
    'Reviewed all 282 texts in eighteen complete Hodram exchanges.':
        'Reviewed 280 texts in fourteen complete Rafael exchanges.',
})
review_scope = prior.review_scope | globals()
for source in (section_source, review_source):
    exec(compile(source, __file__ + "::contextual-review", "exec"), review_scope)


def modal_painter():
    release = base.load(parent.RELEASE)
    ctx = native.RegisteredRuntime(parent.RELEASE, release["own_registered_startup"], captain=3)
    return current_fe_painter(ctx)


def plan_fe(row, painter):
    logical = row["english"]
    protection = row["protected_phrases"]
    for _, lines, compiled in forest.system.candidate_rows(logical, protection):
        try:
            page = painter(compiled[1:])
            membership = forest.system.check_FE_rows(compiled[1:], page)
            assert page["complete_consumed_bytes"] == len(compiled) - 1
            plane = page["physical"]
            assert all(not any(plane[y*228+216:(y+1)*228]) for y in range(64))
        except AssertionError:
            continue
        return compiled[1:], dict(lines=list(lines), expected_native_pages=1, encoded_hex=compiled.hex(),
                                  row_membership=membership, physical_plane_sha256=native.digest(plane))
    raise AssertionError(f"No verified modal layout for {row['id']}")


preflight_source = checked_text(progressive_preflight_source, {
    '            body,plan = layout.plan_progressive(row,old[0],old[1:],new[1:])':
        '            if old[0] == 254:\n'
        '                body,plan = plan_fe(row,modal_painter())\n'
        '                plans[key] = dict(plan=plan, consumer="original_FE")\n'
        '                continue\n'
        '            body,plan = layout.plan_progressive(row,old[0],old[1:],new[1:])',
})
preflight_scope = prior.preflight_scope | globals() | dict(ROOT=BATCH)
exec(compile(preflight_source, __file__ + "::native-preflight", "exec"), preflight_scope)

rebuild_tools = vars(established.exact).copy()
rebuild_tools["stage"] = SimpleNamespace(**(vars(forest) | {"plan_fe": plan_fe}))
rebuild_tools["rebuild_function"] = FunctionType(established.exact.rebuild_function.__code__, rebuild_tools)
exact = SimpleNamespace(**rebuild_tools)
compiler_scope = prior.compiler_scope | globals()
compiler_scope["compilers"] = FunctionType(established.compilers.__code__, compiler_scope)
stage_source = checked_text(getsource(established.stage), {
    '                    assert planned["lines"] == planned_rows': '                    assert planned["lines"] == planned_rows, (ident, planned["lines"], planned_rows)',
    '    rebuild, in_place = compilers()': '    rebuild, in_place = compilers()\n    paint_fe = modal_painter()',
    'new, commands, plans = rebuild(rows, clean, old, inventory, clean_arm, arm, None)':
        'new, commands, plans = rebuild(rows, clean, old, inventory, clean_arm, arm, paint_fe)',
})
exec(compile(stage_source, __file__ + "::staged-rom", "exec"), compiler_scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("review","preflight","stage","patch","startup"))
    action = parser.parse_args().action
    if action == "review":
        review_scope["contextual_review"]()
    elif action == "preflight":
        preflight_scope[action]()
    elif action == "stage":
        compiler_scope[action]()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
