"""Stage the complete Rafael recruitment and ship lesson batch."""

from argparse import ArgumentParser
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import preflight_rafael_refitting_and_sailing_20261123 as prototype
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent = prototype.packet.base, prototype.packet.native, prototype.parent
established, typed = prototype.prior.established, prototype.prior.typed
BATCH = prototype.STAGED.parent / "final"
ROOT = BATCH / "staged"
REVIEW, PREFLIGHT = BATCH / "contextual_review.json", BATCH / "native_preflight.json"
ROM = ROOT / "Rafael_Recruitment_And_Ship_Lessons_STAGED.nds"
PROOF, NATIVE = ROOT / "stored_proof.json", ROOT / "native_display.json"
PATCH, REBUILT = ROOT / "translation.xdelta", ROOT / "clean_rebuilt.nds"
FE_PROOF = ROOT / "unchanged_FE_pages.json"
STARTUP_CAPTURE = ROOT / "startup/capture/capture_report.json"
MANUSCRIPTS = (*prototype.MANUSCRIPTS, Path(__file__).with_name("rafael_jam_and_fernando_20261123.md"))
LATEEN = prototype.STAGED.parent / "lateen_refinement/preflight.json"
LATEEN_ID = "DK4_MES_B180_R0082"
review = SimpleNamespace(REVIEW=REVIEW, PREFLIGHT=PREFLIGHT)
paired, checkpoint = prototype.paired, prototype.checkpoint


section_scope = prototype.review_scope | dict(MANUSCRIPTS=MANUSCRIPTS)
original_sections = FunctionType(prototype.review_scope["load_sections"].__code__, section_scope)


def load_sections():
    sections = original_sections()
    previous = base.load(prototype.REVIEW)
    refinement = base.load(LATEEN)
    row, = [item for item in previous["records"] if item["id"] == LATEEN_ID]
    assert refinement["id"] == LATEEN_ID and refinement["candidate_sha256"] == previous["candidate_sha256"]
    assert refinement["source"] == row["source_reference"] and refinement["current"] == row["current_reference"]
    assert not refinement["installed_or_observed"] and refinement["native_page"]["native_independent_plane_equal"]
    meaning, earlier, _, _ = sections[0, 180][1][82]
    assert earlier == row["english"]
    sections[0, 180][1][82] = (
        meaning, refinement["english"], ";".join(refinement["protected_phrases"]),
        "The headwind setup, downwind speed and instructor's check-in each have a clear beat. The angle phrase fits on one row.",
    )
    return sections


def carry_forward_plans(draft):
    original, receipt = map(base.load, (prototype.REVIEW, prototype.PREFLIGHT))
    assert draft["candidate_sha256"] == original["candidate_sha256"] == receipt["candidate_sha256"]
    assert receipt["draft_sha256"] == base.digest(prototype.REVIEW) and not receipt["pending"]
    current = {row["id"]: row for row in draft["records"]}
    unchanged = {}
    for row in original["records"]:
        if row["decision"] == "revision" and row["id"] != LATEEN_ID:
            assert current[row["id"]] == row
            key = f'{row["route"]}/{row["id"]}'
            unchanged[key] = receipt["plans"][key]
    assert len(unchanged) == len(receipt["plans"]) - 1 == 12
    assert all(base.digest(sheet["path"]) == sheet["sha256"] for sheet in receipt["sheets"])
    return unchanged


review_source = checked_text(prototype.prior.review_source, {
    'len(records)==207 and len(captions)==6 and len(leads)==14 and sum(r["kind"]=="system" for r in records)==2':
        'len(records)==209 and len(captions)==8 and len(leads)==11 and sum(r["kind"]=="system" for r in records)==1',
    'manuscripts_sha256={str(path):base.digest(path) for path in MANUSCRIPTS},':
        'manuscripts_sha256={str(path):base.digest(path) for path in MANUSCRIPTS},\n'
        '        lateen_refinement_preflight={str(LATEEN):base.digest(LATEEN)},',
    'Reviewed 213 texts across ten Rafael exchanges.':
        'Reviewed 217 texts across the five Rafael recruitment and lesson exchanges.',
})
review_scope = prototype.review_scope | globals()
exec(compile(review_source, __file__ + "::contextual-review", "exec"), review_scope)

preflight_source = checked_text(prototype.prior.preflight_source, {
    "    plans,pictures,open_cases={},[],[]": "    plans,pictures,open_cases=carry_forward_plans(draft),[],[]",
    '        key=f\'{row["route"]}/{row["id"]}\'':
        '        key=f\'{row["route"]}/{row["id"]}\'\n'
        '        if key in plans:\n'
        '            continue',
    'plans=plans,pending=open_cases,sheets=sheets,offline_native_only=True,':
        'plans=plans,pending=open_cases,sheets=sheets,offline_native_only=True,\n'
        '        reused_preflight={str(prototype.PREFLIGHT):base.digest(prototype.PREFLIGHT)},',
})
preflight_scope = prototype.preflight_scope | globals() | dict(ROOT=BATCH)
exec(compile(preflight_source, __file__ + "::native-preflight", "exec"), preflight_scope)

compiler_scope = prototype.compiler_scope | globals()
compiler_scope["compilers"] = FunctionType(established.compilers.__code__, compiler_scope)
exec(compile(prototype.stage_source, __file__ + "::stage", "exec"), compiler_scope)
compiler_scope["native_display"] = FunctionType(
    prototype.compiler_scope["native_display"].__code__, compiler_scope,
)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("review", "preflight", "stage", "native_display", "patch", "startup"))
    action = cli.parse_args().action
    if action == "review":
        review_scope["contextual_review"]()
    elif action == "preflight":
        preflight_scope["preflight"]()
    elif action in ("stage", "native_display"):
        compiler_scope[action]()
    else:
        operation = getattr(established.release_tools, action)
        FunctionType(operation.__code__, operation.__globals__ | globals())()
