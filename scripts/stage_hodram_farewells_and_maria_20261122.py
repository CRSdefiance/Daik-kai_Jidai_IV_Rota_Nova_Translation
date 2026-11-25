"""Stage the complete Hodram B65, B67 and B69 contextual reconciliation."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import cleanup_rafael_B84_training_20261122 as checkpoint
from scripts import register_rafael_B84_training_20261122 as current
from scripts import stage_north_sea_and_hodram_reconciliation_20261122 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established = current.base, current.native, template.established
parent = SimpleNamespace(
    ROM=current.ROM, MANIFEST=current.MANIFEST, RELEASE=current.RELEASE, STARTUP_CAPTURE=current.STARTUP_CAPTURE,
    guard_spec=current.guard_spec, bind_registered_story_percent_guard=current.bind_registered_story_percent_guard,
)
BATCH = Path("work/analysis/hodram_farewells_and_maria_20261122/final")
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
MANUSCRIPT = Path(__file__).with_name("hodram_farewells_and_maria_20261122.md")
ROOT = BATCH / "staged"
ROM = ROOT / "Hodram_Farewells_And_Maria_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)
CHOICES = {}
HISTORICAL = Path("translations/editorial_checkpoints/rafael_B84_training_20261122/hodram_remaining_rebound.json")
BLOCKS = (65,67,69)

from scripts.stage_palace_eirene_pereira_london_20261122 import load as load_sections

CONTEXT, DECISIONS = FunctionType(load_sections.__code__, load_sections.__globals__ | globals())()
review_source = checked_text(template.review_source, {
    'len(checked) == 74 and not choice_proofs and all(r["source_selector"] != 254 for r in checked)':
        'len(checked) == 103 and not choice_proofs and all(r["source_selector"] != 254 for r in checked)',
    'in two complete exchanges.': 'in three complete exchanges.',
    'assert (route, block, ordinal) == (1, 168, 96) and prior == "○×△◎▲□×◇!?"':
        'assert (route, block) in ((1,65),(1,67)) and prior == " ".join(japanese[1:].decode("cp932").split())',
})
review_scope = template.review_scope | globals() | dict(ROOT=BATCH, established=template.review_scope["established"])
exec(compile(review_source, __file__ + "::bound-contextual-review", "exec"), review_scope)
preflight = FunctionType(template.preflight.__code__, template.preflight.__globals__ | globals() | dict(ROOT=BATCH))

compiler_scope = template.compiler_scope | globals()
exec(compile(template.template.renderer_source, __file__ + "::original-formatter", "exec"), compiler_scope)


def rebind_historical_differences():
    source = base.load(HISTORICAL)
    comparison = {group["block"]: group for group in source["groups"] if group["block"] in BLOCKS}
    assert source["active_candidate_sha256"] == base.digest(parent.ROM)
    remaining = {r["id"]: r for group in comparison.values() for r in group["pending_decisions"]}
    assert len(remaining) == 44
    manuscript = base.load(REVIEW)
    for group in manuscript["groups"]:
        assert group["current_block_sha256"] == comparison[group["block"]]["current_block_sha256"]
    for row in manuscript["records"]:
        historical = remaining.pop(row["id"], None)
        if historical is None:
            continue
        ref = historical["current_body_reference"]
        assert row["current_reference"]["exact_body_hex"] == ref["current_body_hex"]
        assert row["current_reference"]["offset"] == ref["current_offset"]
        assert row["Japanese"] == historical["clean_Japanese"]
        row["earlier_registered_comparison"] = dict(evidence_sha256=base.digest(HISTORICAL),
            earlier_English=historical["earlier_English"], exact_reference=historical["historical_installed_reference"])
    assert not remaining
    manuscript["historical_payload_differences_reviewed"] = 44
    base.save(REVIEW, manuscript)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "review":
        review_scope["contextual_review"](False)
        rebind_historical_differences()
    elif action == "preflight":
        preflight()
    elif action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        compiler_scope["native_display"]()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
