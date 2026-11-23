"""Register the checked Rafael wrap follow-ups and their exact patch."""

from inspect import getsource
from pathlib import Path
from types import FunctionType

from scripts import register_rafael_mediterranean_followups_20261123 as parent
from scripts import stage_rafael_remaining_wraps_20261123 as stage
from scripts import verify_rafael_remaining_wraps_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
PROFILE = "all-routes-rafael-remaining-wraps-v1-20261123"
ROOT, WORK = stage.BATCH / "registered", stage.BATCH / "registration"
ROM = ROOT / "Translation_DS_Rafael_Wrap_Followups_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_rafael_remaining_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_remaining_wraps_registered_20261123.md")
DISPLAY, EVIDENCE = stage.NATIVE, stage.ROOT
GLYPHS, FE, ROLES = live.GLYPHS, stage.FE_PROOF, live.ROLES
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Rafael's remaining flagged wrap follow-ups."
RUNS = ("0",)
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
guard_spec = parent.guard_spec
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | globals())
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | globals())

controls_source = checked_text(getsource(parent.retained_controls), {
    'modal["complete_stored_page_count"] == 31': 'modal["complete_stored_page_count"] == 4',
    'len(roles["records"]) == 29': 'len(roles["records"]) == 24',
    "retained_modal_pages=31": "retained_modal_pages=4",
})
exec(compile(controls_source, __file__ + "::retained-source-controls", "exec"), globals())

changed_assertions = parent.verify_source[parent.verify_source.index('    assert sum(r["change_class"]'):
                                          parent.verify_source.index('    result = dict(')]
verify_source = checked_text(parent.verify_source, {
    "observed_count() == 15": "observed_count() == 20",
    "native_count() == 15": "native_count() == 19",
    "len(records) == 401": "len(records) == 335",
    "len(changed) == 14": "len(changed) == 19",
    changed_assertions:'''    assert sum(r["change_class"] == "prose" for r in changed) == 18
    assert sum(r["change_class"] == "wrap_only" for r in changed) == 1
    assert set(manuscript["wrap_leads_covered"]) == {row["id"] for row in changed}
    assert all(row["observed_focused"] and row["observed_focused"]["exact_complete_body_mask"] for row in changed)
    lucia, = [row for row in changed if row["id"] == "DK4_MES_B232_R0065"]
    assert all(not line.endswith("I'm") for line in lucia["display_proof"]["layouts"][0]["lines"])
    clue, = [row for row in changed if row["id"] == "DK4_MES_B336_R0100"]
    assert "A key to the Proof of Conquest" in clue["display_proof"]["layouts"][0]["lines"]
''',
    "wording_revisions=12, wrap_only_revisions=2": "wording_revisions=18, wrap_only_revisions=1",
    "justified_retentions=387": "justified_retentions=316",
})

readme = parent.main[parent.main.index('    (PACKAGE / "README.md").write_text'):parent.main.index('    base.save(PACKAGE / "checksums.json"')]
main = checked_text(parent.main, {
    "len(batches) == 1081 and len(checks) == 416": "len(batches) == 1082 and len(checks) == 417",
    "assert len(checks) == 417": "assert len(checks) == 418",
    "verified_rafael_ship_lessons_predecessor": "verified_rafael_mediterranean_followups_predecessor",
    "previously_localized_records=401, contextual_records_revisited=401, contextual_decisions_reused=387":
        "previously_localized_records=335, contextual_records_revisited=335, contextual_decisions_reused=316",
    "prior_records_reviewed=401, contextual_decisions_reused=387":
        "prior_records_reviewed=335, contextual_decisions_reused=316",
    "justified_retentions=387": "justified_retentions=316",
    "prose_revisions=12": "prose_revisions=18",
    "wrap_only_revisions=2": "wrap_only_revisions=1",
    "default_substitution_panels=1, retained_modal_pages=31":
        "default_substitution_panels=0, retained_modal_pages=4",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael's remaining wrap follow-ups

The [testing ROM](../../{ROM.as_posix()}) incorporates the nineteen remaining Rafael wrap findings from the current scan. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_mediterranean_followups_and_complete_parent_inverse", "rafael_remaining_wraps_and_complete_parent_inverse").replace(
    "rafael_mediterranean_followups_pipeline", "rafael_remaining_wraps_pipeline",
).replace("rafael_mediterranean_followups_release", "rafael_remaining_wraps_release").replace(
    "release_stack_before_rafael_mediterranean_followups", "release_stack_before_rafael_remaining_wraps",
).replace("release_stack_with_rafael_mediterranean_followups", "release_stack_with_rafael_remaining_wraps").replace(
    '"rafael_mediterranean_followups_20261123"', '"rafael_remaining_wraps_20261123"',
)

pins = parent.commit[parent.commit.index("    excerpt_rom = "):parent.commit.index("    research = ")]
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    pins:'''    excerpt_rom = Path(base.load(live.scope["receipt"](0))["rom"])
    prototype_root = stage.BATCH.parent / "final/staged"
    prototype = prototype_root / stage.ROM.name
    assert base.digest(prototype) == base.load(prototype_root / stage.PROOF.name)["candidate_sha256"] != candidate
    earlier = [excerpt_rom, prototype]
    previous_fixture = prototype_root / live.ROOT.name / "route0/fixture.json"
    if previous_fixture.exists():
        evidence = base.load(previous_fixture)
        previous_rom = Path(evidence["rom"])
        assert base.digest(previous_rom) == evidence["rom_sha256"]
        earlier.append(previous_rom)
''',
    "Preserve the Mediterranean follow-ups candidate, predecessor and focused ROMs":
        "Preserve the remaining Rafael wrap candidate, predecessor and focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Rafael's remaining wrap follow-ups

Seventeen complete exchanges reconcile 335 exact source/current texts. The ledger carries forward 316 approved decisions and records eighteen wording revisions and one wrap-only change. These close the nineteen remaining Rafael scan leads in the current candidate. [Exact review](../{REVIEW.as_posix()})

All nineteen revised pages, four byte-identical speakerless commands and 24 names or roles passed native checks. A focused emulator replay verified twenty holds across the changed pages and the retained voice during the book and curse exchange. Ordinary scene activation and handheld display remain unvisited. [Testing build and clean-input patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("release_stack_before_rafael_mediterranean_followups", "release_stack_before_rafael_remaining_wraps").replace(
    "release_stack_with_rafael_mediterranean_followups", "release_stack_with_rafael_remaining_wraps",
)

scope = parent.scope | globals()
for source in (verify_source, main, commit):
    exec(compile(source, __file__ + "::registered-review", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
