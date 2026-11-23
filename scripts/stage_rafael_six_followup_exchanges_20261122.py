"""Bind and preflight Rafael's six newly reviewed early-to-midgame exchanges."""

from argparse import ArgumentParser
from pathlib import Path
import re
from types import FunctionType, SimpleNamespace

from scripts import cleanup_rafael_proof_and_financing_20261122 as checkpoint
from scripts import register_rafael_proof_and_financing_20261122 as current
from scripts import stage_rafael_athens_and_maria_crew_20261122 as template
from scripts.source_locked_derivation_v5118 import checked_text


base, native, established = current.base, current.native, template.established
parent = SimpleNamespace(
    ROM=current.ROM, MANIFEST=current.MANIFEST, RELEASE=current.RELEASE, STARTUP_CAPTURE=current.STARTUP_CAPTURE,
    guard_spec=current.scope["guard_spec"], bind_registered_story_percent_guard=current.scope["bind_registered_story_percent_guard"],
)
BATCH = Path("work/analysis/rafael_six_followup_exchanges_20261122/refined")
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROOT = BATCH / "staged"
ROM = ROOT / "Rafael_Six_Followup_Exchanges_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
typed = template.typed
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
draft = SimpleNamespace(ROOT=BATCH, checkpoint=checkpoint)
MANUSCRIPTS = [Path(__file__).with_name(f"rafael_{name}_20261122.md") for name in (
    "lil_farewell_and_lisbon_summons", "sofala_arcadius_pereira_and_scabbard")]
CHOICES = {}
CONTEXT, DECISIONS = {}, {}
for manuscript in MANUSCRIPTS:
    segments = re.split(r"^## SC0 B(\d+)\s*$", manuscript.read_text(encoding="utf-8"), flags=re.M)
    assert not segments[0].strip()
    for number, paragraph in zip(segments[1::2], segments[2::2], strict=True):
        key = 0, int(number)
        assert key not in CONTEXT
        CONTEXT[key], DECISIONS[key] = paragraph.strip().split("\n\n", 1)
assert tuple(number for _, number in CONTEXT) == (50, 52, 55, 57, 61, 62)

review_source = checked_text(template.review_source, {
    'len(checked) == 106 and not choice_proofs and sum(r["source_selector"] == 254 for r in checked) == 4':
        'len(checked) == 129 and not choice_proofs and sum(r["source_selector"] == 254 for r in checked) == 3',
    'in two complete Rafael exchanges.': 'across six complete Rafael exchanges.',
    'assert route == 0 and block == 48 and prior ==': 'assert route == 0 and prior ==',
    'manuscript_sha256=base.digest(MANUSCRIPT)':
        'manuscripts_sha256={str(path):base.digest(path) for path in MANUSCRIPTS}',
})
review_scope = template.review_scope | globals() | dict(ROOT=BATCH, established=template.review_scope["established"])
exec(compile(review_source, __file__ + "::six-source-exchanges", "exec"), review_scope)
preflight = FunctionType(template.preflight.__code__, template.preflight.__globals__ | globals() | dict(ROOT=BATCH))
compiler_scope = template.compiler_scope | globals()
exec(compile(template.renderer_source, __file__ + "::Rafael-native-layouts", "exec"), compiler_scope)


def contextual_review():
    review_scope["contextual_review"](False)
    proof = base.load(REVIEW)
    decisions = {(r["block"], r["current_reference"]["offset"]): r for r in proof["records"]}
    queue = base.load(checkpoint.QUEUE)
    assert queue["candidate_sha256"] == proof["candidate_sha256"]
    leads = [(r["block"], r["offset"]) for r in queue["records"]
             if r["file_path"] == "/data/SC0.DK4" and (0, r["block"]) in CONTEXT and "reviewed" not in r]
    assert len(leads) >= 7
    assert all(decisions[lead]["decision"] == "revision" for lead in leads)
    proof["wrap_leads_covered"] = [decisions[lead]["id"] for lead in leads]
    base.save(REVIEW, proof)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "review":
        contextual_review()
    elif action == "preflight":
        preflight()
    elif action == "stage":
        FunctionType(established.stage.__code__, compiler_scope)()
    elif action == "native_display":
        compiler_scope[action]()
    else:
        inherited = getattr(established.release_tools, action)
        FunctionType(inherited.__code__, inherited.__globals__ | globals())()
