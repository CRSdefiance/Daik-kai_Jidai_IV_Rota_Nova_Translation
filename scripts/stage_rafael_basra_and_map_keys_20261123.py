"""Apply the source-bound Basra and Map Key manuscript with the native compiler."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import cleanup_hodram_recruitment_and_sails_20261123 as checkpoint
from scripts import pair_rafael_basra_and_map_keys_20261123 as paired
from scripts import stage_rafael_midroute_exchanges_20261122 as prior
from scripts import stage_rafael_palace_and_alliance_20261121 as controls
from scripts.source_locked_derivation_v5118 import checked_text

base, native, established, typed = prior.base, prior.native, prior.established, prior.typed
active = paired.release
parent = SimpleNamespace(ROM=active.ROM, MANIFEST=active.MANIFEST, RELEASE=active.RELEASE,
    STARTUP_CAPTURE=active.STARTUP_CAPTURE, guard_spec=active.scope["guard_spec"],
    bind_registered_story_percent_guard=active.scope["bind_registered_story_percent_guard"])
BATCH = Path(".codex-release-work/rafael_basra_and_map_keys_20261123/final")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Rafael_Basra_And_Map_Keys_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
GUARD_SC0 = paired.OUTPUT.parent / "source25_basra_SC0_qualification.json"
GUARD = paired.OUTPUT.parent / "source25_basra_qualification.json"
MANUSCRIPTS = (Path(__file__).with_name("rafael_basra_and_map_keys_20261123.md"),)
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)

section_source = checked_text(prior.section_source, {
    "                key = int(key) if key.isdecimal() else key":
        "                if len(fields) == 2:\n"
        "                    meaning, note = fields\n"
        "                    fields = [meaning, '', '', note]\n"
        "                assert len(fields) == 4, text\n"
        "                key = int(key) if key.isdecimal() else key",
})
review_source = checked_text(prior.review_source, {
    '            if selector == 254 and change != "retention":\n'
    '                assert (block, ordinal) == (118, 125) and change == "wrap_only"':
        '            if selector == 254:\n                assert change == "retention"',
    'len(records)==275 and len(captions)==5 and len(leads)==21 and sum(r["kind"]=="system" for r in records)==17':
        'len(records)==207 and len(captions)==6 and len(leads)==14 and sum(r["kind"]=="system" for r in records)==2',
    'Reviewed 280 texts in fourteen complete Rafael exchanges.':
        'Reviewed 213 texts across ten Rafael exchanges.',
})
review_scope = prior.review_scope | globals()
for source in (section_source, review_source):
    exec(compile(source, __file__ + "::contextual-review", "exec"), review_scope)

preflight_scope = prior.preflight_scope | globals() | dict(ROOT=BATCH)
preflight_source = checked_text(prior.preflight_source, {'0:"Castor Company"': '0:"Castor Co."'})
exec(compile(preflight_source, __file__ + "::native-preflight", "exec"), preflight_scope)
compiler_scope = prior.compiler_scope | globals()
compiler_scope["compilers"] = FunctionType(established.compilers.__code__, compiler_scope)
guard_source = checked_text(getsource(controls.qualify_format_controls), {
    'group["source"]': 'group["source_block_sha256"]',
    'review.OUTPUT': 'review.REVIEW',
    '        a, z = item["source_offset"] + 5, item["stored_offset"] + 5':
        '        assert item["current"] == item["stored"]\n'
        '        a, z = item["source_offset"] + 5, item["stored_offset"] + 5',
})
guard_scope = vars(controls) | globals()
exec(compile(guard_source, __file__ + "::source-owned-actor-controls", "exec"), guard_scope)
compiler_scope["qualify_format_controls"] = guard_scope["qualify_format_controls"]
stage_source = checked_text(prior.stage_source, {
    'guard = parent.bind_registered_story_percent_guard(parent.guard_spec())(native.files(original), final)':
        'guard = qualify_format_controls(parent.guard_spec(), native.files(original), before, final, groups)',
})
exec(compile(stage_source, __file__ + "::staged-rom", "exec"), compiler_scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "patch", "startup"))
    action = cli.parse_args().action
    if action == "review":
        review_scope["contextual_review"]()
    elif action == "preflight":
        preflight_scope["preflight"]()
    elif action == "stage":
        compiler_scope["stage"]()
    else:
        operation = getattr(established.release_tools, action)
        FunctionType(operation.__code__, operation.__globals__ | globals())()
