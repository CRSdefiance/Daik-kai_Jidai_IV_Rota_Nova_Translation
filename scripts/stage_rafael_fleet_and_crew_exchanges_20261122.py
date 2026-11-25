"""Stage Rafael's six fleet and crew exchanges against the registered candidate."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import cleanup_rafael_charlotte_and_maria_20261122 as checkpoint
from scripts import pair_rafael_fleet_and_crew_exchanges_20261122 as paired
from scripts import register_rafael_charlotte_and_maria_20261122 as active
from scripts import review_current_story_wraps_20261122 as baseline_layout
from scripts import stage_rafael_charlotte_and_maria_20261122 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established = prior.base, prior.native, prior.established
parent = SimpleNamespace(ROM=active.ROM, MANIFEST=active.MANIFEST, RELEASE=active.RELEASE,
    STARTUP_CAPTURE=active.STARTUP_CAPTURE, guard_spec=active.scope["guard_spec"],
    bind_registered_story_percent_guard=active.scope["bind_registered_story_percent_guard"])
BATCH = Path(".codex-release-work/rafael_fleet_and_crew_exchanges_20261122/release")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Rafael_Fleet_And_Crew_Exchanges_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)
MANUSCRIPTS = (Path(__file__).with_name("rafael_fleet_and_crew_exchanges_20261122.md"),)
typed = prior.prior.typed

review_scope = prior.review_scope | globals()
review_source = checked_text(prior.review_source, {
    'len(records)==134 and not captions and len(leads)==8':
        'len(records)==224 and not captions and len(leads)==12 and sum(r["kind"]=="system" for r in records)==4',
    'Reviewed all 134 texts in four complete Rafael exchanges.':
        'Reviewed all 224 texts in six complete Rafael exchanges.',
})
for source in (prior.load_sections_source, review_source):
    exec(compile(source, __file__ + "::contextual-review", "exec"), review_scope)

preflight_source = checked_text(getsource(baseline_layout.preflight), {
    '("FO","FI")': '("FO","FI","FA")',
    '{"FO":default_company[row["route"]],"FI":default_first[row["route"]]}':
        '{"FO":default_company[row["route"]],"FI":default_first[row["route"]],"FA":"Castor"}',
    '{"FO":"W"*20,"FI":"W"*16}': '{"FO":"W"*20,"FI":"W"*16,"FA":"W"*16}',
})
preflight_scope = prior.preflight.__globals__ | globals() | dict(ROOT=BATCH)
exec(compile(preflight_source, __file__ + "::native-preflight", "exec"), preflight_scope)
compiler_scope = prior.compiler_scope | globals()
renderer_source = prior.prior.template.template.renderer_source
exec(compile(renderer_source, __file__ + "::native-layouts", "exec"), compiler_scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "review":
        review_scope["contextual_review"]()
    elif action == "preflight":
        preflight_scope["preflight"]()
    elif action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        compiler_scope[action]()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
