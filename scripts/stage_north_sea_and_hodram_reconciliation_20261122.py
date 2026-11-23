"""Bind, preflight, and stage the North Sea meeting and Hodram’s B66 encounter."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import cleanup_palace_eirene_pereira_london_20261122 as checkpoint
from scripts import register_palace_eirene_pereira_london_20261122 as current
from scripts import stage_palace_eirene_pereira_london_20261122 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established = current.base, current.native, template.established
parent = SimpleNamespace(
    ROM=current.ROM, MANIFEST=current.MANIFEST, RELEASE=current.RELEASE, STARTUP_CAPTURE=current.STARTUP_CAPTURE,
    guard_spec=current.scope["guard_spec"], bind_registered_story_percent_guard=current.scope["bind_registered_story_percent_guard"],
)
BATCH = Path("work/analysis/north_sea_and_hodram_reconciliation_20261122/final")
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
MANUSCRIPT = Path(__file__).with_name("north_sea_and_hodram_reconciliation_20261122.md")
ROOT = BATCH / "staged"
ROM = ROOT / "North_Sea_And_Hodram_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)
CHOICES = {}

CONTEXT, DECISIONS = FunctionType(template.load.__code__, template.load.__globals__ | globals())()
ALIGNED = Path("translations/editorial_checkpoints/palace_and_london_20261122")
HISTORICAL = ALIGNED / "hodram_B61_B70_reconciliation.json"


def reconcile_current_words():
    old = base.load(HISTORICAL)
    assert old["older_rom_reconstructed_and_all_historical_payloads_verified"]
    assert old["candidate_sha256"] == base.digest(parent.ROM)
    earlier = {row["id"]: row for row in old["records"] if row["block"] == 66}
    record = base.load(REVIEW)
    for row in record["records"]:
        if row["route"] != 1:
            continue
        previous = earlier.pop(row["id"])
        assert all(previous["prior_gates"].values())
        assert row["current_reference"]["offset"] == previous["current_body_reference"]["current_offset"]
        assert row["current_reference"]["exact_body_hex"] == previous["current_body_reference"]["current_body_hex"]
        if not previous["exact_payload_match"]:
            row["earlier_registered_comparison"] = dict(
                evidence_sha256=base.digest(HISTORICAL), earlier_English=previous["earlier_English"],
                exact_reference=previous["historical_installed_reference"],
            )
    assert not earlier
    base.save(REVIEW, record)


review_source = checked_text(template.review_source, {
    'len(checked) == 275 and len(choice_proofs) == 1 and sum(r["source_selector"] == 254 for r in checked) == 7':
        'len(checked) == 74 and not choice_proofs and all(r["source_selector"] != 254 for r in checked)',
    'in four complete exchanges.': 'in two complete exchanges.',
})
review_scope = template.review_scope | globals() | dict(ROOT=BATCH, established=template.review_scope["established"])
exec(compile(review_source, __file__ + "::source-paired-review", "exec"), review_scope)
preflight = FunctionType(template.preflight.__code__, template.preflight.__globals__ | globals() | dict(ROOT=BATCH))
compiler_scope = template.compiler_scope | globals()
exec(compile(template.renderer_source, __file__ + "::native-pages", "exec"), compiler_scope)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "review":
        review_scope["contextual_review"](False)
        reconcile_current_words()
    elif action == "preflight":
        preflight()
    elif action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        compiler_scope["native_display"]()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
