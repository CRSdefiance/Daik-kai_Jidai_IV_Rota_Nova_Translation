"""Register the Mediterranean follow-up release after the required verification."""

from pathlib import Path
from types import FunctionType

from scripts import register_rafael_ship_lessons_20261123 as parent
from scripts import stage_rafael_mediterranean_followups_20261123 as stage
from scripts import verify_rafael_mediterranean_followups_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
PROFILE = "all-routes-rafael-mediterranean-followups-v1-20261123"
ROOT, WORK = stage.BATCH / "registered", stage.BATCH / "registration"
ROM = ROOT / "Translation_DS_Rafael_Mediterranean_Followups_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_rafael_mediterranean_followups_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_rafael_mediterranean_followups_registered_20261123.md")
DISPLAY, EVIDENCE = stage.NATIVE, stage.ROOT
GLYPHS, FE, ROLES = live.GLYPHS, stage.FE_PROOF, live.ROLES
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Rafael's Mediterranean follow-ups and Jam's wrap correction."
RUNS = ("0",)
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
guard_spec = parent.guard_spec
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | globals())
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | globals())


def retained_controls(records, played, banks, candidate):
    modal, roles = map(base.load, (FE, ROLES))
    assert modal["candidate_sha256"] == roles["candidate_sha256"] == candidate
    assert modal["original_modal_consumer"] and modal["complete_stored_page_count"] == 31
    owners = {row["id"]: row for row in records if row["source_selector"] == 254}
    assert owners.keys() == {panel["id"] for panel in modal["records"]}
    for panel in modal["records"]:
        row = owners[panel["id"]]
        installed = row["registered_reference"]
        assert row["decision"] == "retention" and not panel["second_page"]
        assert installed["exact_command_hex"] == panel["exact_command_hex"] == row["current_reference"]["exact_command_hex"]
        assert installed["command_offset"] == panel["stored_offset"]
    assert owners[live.MODAL_SAMPLE]["observed_focused"]
    assert roles["offline_native_getters_only"] and roles["new_editorial_credit"] == 0
    assert {row["actor_ID"] for row in roles["records"]} == {r["source_selector"] for r in records} - {254}
    assert len(roles["records"]) == 29 and all(all(row["review"].values()) for row in roles["records"])
    assert not base.load(stage.REVIEW)["retained_choice_labels"]
    return dict(modal_proof_sha256=base.digest(FE), retained_modal_pages=31, revised_modal_pages=0,
        retained_choice_labels=[], role_proof_sha256=base.digest(ROLES), retained_roles=len(roles["records"]))


changed_assertions = parent.verify_source[parent.verify_source.index('    assert sum(r["change_class"]'):
                                          parent.verify_source.index('    result = dict(')]
verify_source = checked_text(parent.verify_source, {
    'observed_count() == 32 and played["reused_count"] == 17': 'observed_count() == 15',
    "native_count() == 20": "native_count() == 15",
    "len(records) == 209": "len(records) == 401",
    "len(changed) == 20": "len(changed) == 14",
    changed_assertions:'''    assert sum(r["change_class"] == "prose" for r in changed) == 12
    assert sum(r["change_class"] == "wrap_only" for r in changed) == 2
    jam, = [r for r in changed if r["id"] == "DK4_MES_B176_R0040"]
    assert jam["english"] == jam["previous_English"] and jam["observed_focused"]
    assert any("True story." in line for line in jam["display_proof"]["layouts"][0]["lines"])
    introduction, = [r for r in changed if r["id"] == "DK4_MES_B168_R0050"]
    default, maximum = introduction["display_proof"]["layouts"]
    assert "Rafael Castor." in default["lines"] and "W" * 16 + " " + "W" * 16 + "." in maximum["lines"]
    assert introduction["observed_focused"]["default_substitutions"] == {"FI": "Rafael", "FA": "Castor"}
''',
    "wording_revisions=16, wrap_only_revisions=4": "wording_revisions=12, wrap_only_revisions=2",
    "justified_retentions=189, choice_label_retentions=8": "justified_retentions=387, choice_label_retentions=0",
    "target_locale=\"en-US\", visual_review=viewed,":
        'target_locale="en-US", prior_exact_review_references=manuscript["exact_prior_registered_reviews"], visual_review=viewed,',
})

readme = parent.main[parent.main.index('    (PACKAGE / "README.md").write_text'):parent.main.index('    base.save(PACKAGE / "checksums.json"')]
main = checked_text(parent.main, {
    "len(batches) == 1080 and len(checks) == 415": "len(batches) == 1081 and len(checks) == 416",
    "assert len(checks) == 416": "assert len(checks) == 417",
    "verified_rafael_basra_and_map_keys_predecessor": "verified_rafael_ship_lessons_predecessor",
    "previously_localized_records=217, contextual_records_revisited=217, contextual_decisions_reused=117":
        "previously_localized_records=401, contextual_records_revisited=401, contextual_decisions_reused=387",
    "prior_records_reviewed=217, contextual_decisions_reused=117": "prior_records_reviewed=401, contextual_decisions_reused=387",
    "justified_retentions=189, retained_choice_labels=8": "justified_retentions=387, retained_choice_labels=0",
    "prose_revisions=16": "prose_revisions=12",
    "wrap_only_revisions=4": "wrap_only_revisions=2",
    "default_substitution_panels=0, retained_modal_pages=1, revised_modal_pages=0, native_choice_outcomes=2":
        "default_substitution_panels=1, retained_modal_pages=31, revised_modal_pages=0, native_choice_outcomes=0",
    "FE, CHOICE, ROLES, stage.LATEEN": "FE, ROLES",
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Rafael's Mediterranean follow-ups

The [testing ROM](../../{ROM.as_posix()}) updates Rafael's Mediterranean scenes and keeps Jam's “True story” on a single line. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("rafael_ship_lessons_and_complete_parent_inverse", "rafael_mediterranean_followups_and_complete_parent_inverse").replace(
    "rafael_ship_lessons_pipeline", "rafael_mediterranean_followups_pipeline",
).replace("rafael_ship_lessons_release", "rafael_mediterranean_followups_release").replace(
    "release_stack_before_rafael_ship_lessons", "release_stack_before_rafael_mediterranean_followups",
).replace("release_stack_with_rafael_ship_lessons", "release_stack_with_rafael_mediterranean_followups").replace(
    '"rafael_ship_lessons_20261123"', '"rafael_mediterranean_followups_20261123"',
)

pins = parent.commit[parent.commit.index("    excerpt_rom = "):parent.commit.index("    research = ")]
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    pins:'''    excerpt_rom = Path(base.load(live.scope["receipt"](0))["rom"])
    prototype = stage.BATCH.parent / "staged" / stage.ROM.name
    prototype_proof = stage.BATCH.parent / "staged" / stage.PROOF.name
    assert base.digest(prototype) == base.load(prototype_proof)["candidate_sha256"] != candidate
    earlier = [excerpt_rom, prototype]
''',
    "Preserve the Rafael ship lessons candidate, predecessor and focused ROMs":
        "Preserve the Mediterranean follow-ups candidate, predecessor and focused ROMs",
    old_doc:'''    DOC.write_text(f"""# Rafael's Mediterranean follow-ups

Eight complete exchanges were reconciled against the clean Japanese and their earlier registered proofs. The ledger carries forward 387 exact decisions and records twelve wording changes and two wrap-only fixes. The revisions cover the Mediterranean relic, the royal audience and the recruits Al, Angelo, Carlo, Samwell and Jam. [Exact review](../{REVIEW.as_posix()})

Native checks verified 15 revised pages across default and maximum name widths, 31 retained speakerless commands and 29 names or roles. Fifteen focused emulator holds include Rafael's full-name introduction, Jam's repaired line and the transition from Claudio's portrait to Eirene's speakerless reply. Natural story activation and handheld display remain unvisited. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("release_stack_before_rafael_ship_lessons", "release_stack_before_rafael_mediterranean_followups").replace(
    "release_stack_with_rafael_ship_lessons", "release_stack_with_rafael_mediterranean_followups",
)

scope = parent.scope | globals()
for source in (verify_source, main, commit):
    exec(compile(source, __file__ + "::registered-review", "exec"), scope)

if __name__ == "__main__":
    scope["main"]()
