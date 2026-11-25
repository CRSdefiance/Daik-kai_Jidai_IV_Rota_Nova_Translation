"""Stage Rafael's Charlotte and first East Asia exchanges."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import cleanup_hodram_and_lil_followups_20261122 as checkpoint
from scripts import pair_rafael_charlotte_and_maria_20261122 as paired
from scripts import register_hodram_and_lil_followups_20261122 as active
from scripts import stage_hodram_and_lil_followups_20261122 as prior
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established = prior.base, prior.native, prior.established
parent = SimpleNamespace(ROM=active.ROM, MANIFEST=active.MANIFEST, RELEASE=active.RELEASE,
    STARTUP_CAPTURE=active.STARTUP_CAPTURE, guard_spec=active.scope["guard_spec"],
    bind_registered_story_percent_guard=active.scope["bind_registered_story_percent_guard"])
BATCH = Path(".codex-release-work/rafael_charlotte_and_maria_20261122/release")
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Rafael_Charlotte_And_Maria_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)
MANUSCRIPTS = (Path(__file__).with_name("rafael_charlotte_and_maria_20261122.md"),)

review_scope = vars(prior) | globals()
load_sections_source = checked_text(getsource(prior.load_sections), {r"SC([12])": r"SC([0])"})
review_source = checked_text(getsource(prior.contextual_review), {
    '''            if row["native_command_word"] == 0x2100:
                slot, = row["slots"]
                english, meaning, note = CAPTIONS[slot]
                assert (route,block) == (2,133) and english == before
                captions.append(dict(id=ident, slot=slot, Japanese=row["Japanese"], english=english, context=context,
                    source_meaning=meaning, localization_note=note, source_reference=source, current_reference=current,
                    decision="retention",
                    review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
                continue
''': '',
    'assert not sections and len(records)==288 and len(captions)==2 and len(leads)==8':
        'assert not sections and len(records)==134 and not captions and len(leads)==8',
    'ident = f"DK4_MES_B{block}_R{ordinal:04d}"':
        'ident = row["id"]\n            assert ident == f"DK4_MES_B{block}_R{ordinal:04d}"',
    'Reviewed all 288 spoken and system texts and two choice captions.':
        'Reviewed all 134 texts in four complete Rafael exchanges.',
})
for source in (load_sections_source, review_source):
    exec(compile(source, __file__ + "::contextual-review", "exec"), review_scope)

preflight = FunctionType(prior.preflight.__code__, prior.preflight.__globals__ | globals() | dict(ROOT=BATCH))
compiler_scope = prior.compiler_scope | globals()
exec(compile(prior.template.template.renderer_source, __file__ + "::native-layouts", "exec"), compiler_scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "review":
        review_scope["contextual_review"]()
    elif action == "preflight":
        preflight()
    elif action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        compiler_scope[action]()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
