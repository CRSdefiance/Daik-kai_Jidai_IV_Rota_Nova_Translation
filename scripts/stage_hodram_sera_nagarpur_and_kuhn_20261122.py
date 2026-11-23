"""Prepare the remaining six Hodram exchanges from exact clean/current evidence."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_hodram_farewells_and_maria_20261122 as current
from scripts import stage_hodram_farewells_and_maria_20261122 as template
from scripts import stage_palace_eirene_pereira_london_20261122 as sections
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established = current.base, current.native, template.established
parent = SimpleNamespace(
    ROM=current.ROM, MANIFEST=current.MANIFEST, RELEASE=current.RELEASE, STARTUP_CAPTURE=current.STARTUP_CAPTURE,
    guard_spec=current.scope["guard_spec"], bind_registered_story_percent_guard=current.scope["bind_registered_story_percent_guard"],
)
BATCH = Path("work/analysis/hodram_sera_nagarpur_and_kuhn_20261122/final")
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
MANUSCRIPT = Path(__file__).with_name("hodram_sera_nagarpur_and_kuhn_20261122.md")
ROOT = BATCH / "staged"
ROM = ROOT / "Hodram_Sera_Nagarpur_And_Kuhn_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=SimpleNamespace(
    QUEUE=current.stage.BATCH / "current_wrap_queue.json"))
CHOICES = {}
HISTORICAL = template.HISTORICAL
BLOCKS = (61, 62, 63, 64, 68, 70)
CONTEXT, DECISIONS = FunctionType(sections.load.__code__, sections.load.__globals__ | globals())()

review_source = checked_text(template.review_source, {
    'len(checked) == 103 and not choice_proofs': 'len(checked) == 108 and not choice_proofs',
    'in three complete exchanges.': 'in six complete exchanges.',
    'assert (route, block) in ((1,65),(1,67)) and prior == " ".join(japanese[1:].decode("cp932").split())':
        'assert route == 1 and block in BLOCKS and prior == " ".join(japanese[1:].decode("cp932").split())',
})
review_scope = template.review_scope | globals() | dict(ROOT=BATCH, established=template.review_scope["established"])
exec(compile(review_source, __file__ + "::source-bound-contextual-review", "exec"), review_scope)
preflight = FunctionType(template.preflight.__code__, template.preflight.__globals__ | globals() | dict(ROOT=BATCH))
compiler_scope = template.compiler_scope | globals()
exec(compile(template.template.template.renderer_source, __file__ + "::bounded-dialogue-layout", "exec"), compiler_scope)


def rebind_historical_differences():
    prior, manuscript = map(base.load, (HISTORICAL, REVIEW))
    previous = base.load(current.RELEASE)["predecessor"]
    assert prior["active_candidate_sha256"] == previous["candidate_sha256"]
    comparisons = {g["block"]: g for g in prior["groups"] if g["block"] in BLOCKS}
    remaining = {r["id"]: r for group in comparisons.values() for r in group["pending_decisions"]}
    assert len(remaining) == 46 and set(comparisons) == set(BLOCKS)
    for group in manuscript["groups"]:
        assert group["current_block_sha256"] == comparisons[group["block"]]["current_block_sha256"]
    for row in manuscript["records"]:
        earlier = remaining.pop(row["id"], None)
        if earlier is None:
            continue
        field = earlier["current_body_reference"]
        assert (row["current_reference"]["offset"], row["current_reference"]["exact_body_hex"]) == (
            field["current_offset"], field["current_body_hex"])
        assert row["Japanese"] == earlier["clean_Japanese"]
        row["earlier_registered_comparison"] = dict(evidence_sha256=base.digest(HISTORICAL),
            earlier_English=earlier["earlier_English"], exact_reference=earlier["historical_installed_reference"])
    assert not remaining
    manuscript["historical_payload_differences_reviewed"] = 46
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
