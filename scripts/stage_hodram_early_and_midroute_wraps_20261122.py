"""Stage eighteen complete Hodram exchanges over the registered candidate."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import cleanup_rafael_fleet_and_crew_exchanges_20261122 as checkpoint
from scripts import pair_hodram_early_and_midroute_wraps_20261122 as paired
from scripts import register_rafael_fleet_and_crew_exchanges_20261122 as active
from scripts import stage_rafael_fleet_and_crew_exchanges_20261122 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established = prior.base, prior.native, prior.established
parent = SimpleNamespace(ROM=active.ROM, MANIFEST=active.MANIFEST, RELEASE=active.RELEASE,
    STARTUP_CAPTURE=active.STARTUP_CAPTURE, guard_spec=active.scope["guard_spec"],
    bind_registered_story_percent_guard=active.scope["bind_registered_story_percent_guard"])
BATCH = Path(".codex-release-work/hodram_early_and_midroute_wraps_20261122/final")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Hodram_Early_And_Midroute_Wraps_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
FE_PROOF, CHOICE_PROOF = ROOT / "unchanged_FE_pages.json", ROOT / "unchanged_choice.json"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)
MANUSCRIPTS = (Path(__file__).with_name("hodram_early_and_midroute_wraps_20261122.md"),)
typed = prior.typed

section_source = checked_text(prior.prior.load_sections_source, {
    r"SC([0])": r"SC([1])",
    "                assert int(key) not in rows\n                rows[int(key)] = fields":
        "                key = int(key) if key.isdecimal() else key\n"
        "                assert key not in rows\n                rows[key] = fields",
})
review_source = checked_text(prior.review_source, {
    '            assert ident == f"DK4_MES_B{block}_R{ordinal:04d}"':
        '            if ordinal is not None:\n                assert ident == f"DK4_MES_B{block}_R{ordinal:04d}"',
    '            assert row["native_command_word"] == 0x4000 and selector <= 254':
        '''            if row["native_command_word"] == 0x2100:
                slot, = row["slots"]
                meaning, replacement, protection, note = decisions.pop(f"C{slot}")
                assert ordinal is None and selector is None and not replacement and not protection
                captions.append(dict(id=ident, slot=slot, Japanese=row["Japanese"], english=before, context=context,
                    source_meaning=meaning, localization_note=note, source_reference=source, current_reference=current,
                    decision="retention",
                    review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
                continue
            assert row["native_command_word"] == 0x4000 and selector <= 254''',
    'len(records)==224 and not captions and len(leads)==12 and sum(r["kind"]=="system" for r in records)==4':
        'len(records)==278 and len(captions)==4 and len(leads)==24 and sum(r["kind"]=="system" for r in records)==20',
    'Reviewed all 224 texts in six complete Rafael exchanges.':
        'Reviewed all 282 texts in eighteen complete Hodram exchanges.',
})
review_scope = prior.review_scope | globals()
for source in (section_source, review_source):
    exec(compile(source, __file__ + "::contextual-review", "exec"), review_scope)

preflight_scope = prior.preflight_scope | globals() | dict(ROOT=BATCH)
exec(compile(prior.preflight_source, __file__ + "::native-preflight", "exec"), preflight_scope)
compiler_scope = prior.compiler_scope | globals()
exec(compile(getsource(established.native_display), __file__ + "::native-layouts", "exec"), compiler_scope)


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
