"""Stage the Hodram exchanges with separate speech, modal, and retained typed objects."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import cleanup_rafael_midroute_exchanges_20261122 as checkpoint
from scripts import pair_hodram_midroute_followups_20261123 as paired
from scripts import register_rafael_midroute_exchanges_20261122 as active
from scripts import stage_hodram_early_and_midroute_wraps_20261122 as hodram
from scripts import stage_rafael_midroute_exchanges_20261122 as precedent
from scripts.source_locked_derivation_v5118 import checked_text

base, native, established, typed = precedent.base, precedent.native, precedent.established, precedent.typed
parent = SimpleNamespace(ROM=active.ROM, MANIFEST=active.MANIFEST, RELEASE=active.RELEASE,
    STARTUP_CAPTURE=active.STARTUP_CAPTURE, guard_spec=active.scope["guard_spec"],
    bind_registered_story_percent_guard=active.scope["bind_registered_story_percent_guard"])
BATCH = Path(".codex-release-work/hodram_midroute_followups_20261123/release")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Hodram_Midroute_Followups_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF = ROOT / "modal_native_display.json"
MANUSCRIPTS = (Path(__file__).with_name("hodram_midroute_followups_20261123.md"),)
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)

section_source = checked_text(hodram.section_source, {
    "                key = int(key) if key.isdecimal() else key":
        "                if len(fields) == 2:\n"
        "                    meaning, note = fields\n"
        "                    fields = [meaning, '', '', note]\n"
        "                assert len(fields) == 4, text\n"
        "                key = int(key) if key.isdecimal() else key",
})
review_source = checked_text(precedent.review_source, {
    '    for group in packet["groups"]:': '    styles = []\n    for group in packet["groups"]:',
    '            if row["native_command_word"] in (0x2100, 0x2200):':
        '            if row["native_command_word"] == 0x4100:\n'
        '                meaning, replacement, protection, note = decisions.pop(ident)\n'
        '                assert ordinal is None and selector == 208 and not replacement and not protection\n'
        '                styles.append(dict(id=ident, slots=row["slots"], Japanese=row["Japanese"], english=before,\n'
        '                    speaker=row["speaker"], source_meaning=meaning, localization_note=note,\n'
        '                    source_reference=source, current_reference=current, context=context, decision="retention",\n'
        '                    review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))\n'
        '                continue\n'
        '            if row["native_command_word"] in (0x2100, 0x2200):',
    'assert (block, ordinal) == (118, 125) and change == "wrap_only"':
        'assert (block, ordinal) in ((135, 35), (136, 38)) and change == "prose"',
    'names[selector] if selector != 254 else "System"':
        'names[selector] if selector < 207 else row["speaker"]',
    'len(records)==275 and len(captions)==5 and len(leads)==21 and sum(r["kind"]=="system" for r in records)==17':
        'len(records)==293 and len(captions)==8 and len(styles)==5 and len(leads)==17 and sum(r["kind"]=="system" for r in records)==10',
    'retained_choice_labels=captions, counts=counts,': 'retained_choice_labels=captions, retained_style_variants=styles, counts=counts,',
    'Reviewed 280 texts in fourteen complete Rafael exchanges.': 'Reviewed 306 texts in thirteen full Hodram exchanges.',
})
review_scope = precedent.review_scope | globals()
for source in (section_source, review_source):
    exec(compile(source, __file__ + "::contextual-review", "exec"), review_scope)

preflight_scope = precedent.preflight_scope | globals() | dict(ROOT=BATCH)
exec(compile(precedent.preflight_source, __file__ + "::native-preflight", "exec"), preflight_scope)
compiler_scope = precedent.compiler_scope | globals()
compiler_scope["compilers"] = FunctionType(established.compilers.__code__, compiler_scope)
exec(compile(precedent.stage_source, __file__ + "::staged-rom", "exec"), compiler_scope)


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("review", "preflight", "stage", "patch", "startup"))
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
