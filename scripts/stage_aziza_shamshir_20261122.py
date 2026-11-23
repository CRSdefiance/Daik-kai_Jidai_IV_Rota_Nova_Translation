"""Bind and stage Rafael and Aziza's complete exchange on the registered ROM."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import cleanup_mosque_elysion_mikhail_20261122 as checkpoint
from scripts import register_mosque_elysion_mikhail_20261122 as current
from scripts import stage_mosque_elysion_mikhail_20261122 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established = current.base, current.native, template.established
parent = SimpleNamespace(
    ROM=current.ROM, MANIFEST=current.MANIFEST, RELEASE=current.RELEASE, STARTUP_CAPTURE=current.STARTUP_CAPTURE,
    guard_spec=current.scope["guard_spec"], bind_registered_story_percent_guard=current.scope["bind_registered_story_percent_guard"],
)
BATCH = Path("work/analysis/aziza_shamshir_20261122")
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
MANUSCRIPT = Path(__file__).with_name("rafael_aziza_shamshir_pending_20261122.md")
ROOT = BATCH / "staged"
ROM = ROOT / "Aziza_Shamshir_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)

load = FunctionType(template.binding["load_sections"].__code__, template.binding | globals())
CONTEXT, DECISIONS = load()
review_source = checked_text(template.review_source, {
    'len(checked) == 180 and not choice_proofs and sum(r["source_selector"] == 254 for r in checked) == 7':
        'len(checked) == 78 and not choice_proofs and all(r["source_selector"] != 254 for r in checked)',
    'across three complete scenes.': 'in the complete Aziza exchange.',
})
review_scope = template.scope | globals() | dict(ROOT=BATCH, established=template.binder.established)
exec(compile(review_source, __file__ + "::source-paired-review", "exec"), review_scope)
preflight = FunctionType(template.preflight_scope["preflight"].__code__,
    template.preflight_scope | globals() | dict(ROOT=BATCH))

renderer_source = checked_text(template.renderer_source, {
    'DK4_MES_B123_R0115': 'DK4_MES_B26_R0060',
})
compiler_scope = template.compiler_scope | globals()
exec(compile(renderer_source, __file__ + "::company-substitution", "exec"), compiler_scope)


def confirm_lead():
    observed = base.load(checkpoint.FOLLOWUP)
    assert observed["candidate_sha256"] == base.digest(parent.ROM)
    previous, = observed["records"]
    assert previous["id"] == "DK4_MES_B26_R0060" and "Castor Co.." in previous["offline_name_expansion"]
    revised = base.load(REVIEW)
    assert revised["candidate_sha256"] == observed["candidate_sha256"]
    row, = (r for r in revised["records"] if r["id"] == previous["id"])
    assert row["decision"] == "revision" and "FO," in row["english"]
    for field in ("source_reference", "current_reference"):
        assert row[field]["exact_command_hex"] == previous[field]["exact_command_hex"]


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "review":
        review_scope["contextual_review"](False)
        confirm_lead()
    elif action == "preflight":
        preflight()
    elif action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        compiler_scope["native_display"]()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
