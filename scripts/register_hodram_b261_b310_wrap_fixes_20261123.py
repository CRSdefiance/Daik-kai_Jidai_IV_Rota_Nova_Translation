"""Register the final Hodram wrap batch and its clean-input patch."""

from types import FunctionType

from scripts import register_hodram_b221_b260_wrap_fixes_20261123 as parent
from scripts import stage_hodram_b261_b310_wrap_fixes_20261123 as stage
from scripts import verify_hodram_b261_b310_wrap_fixes_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
PROFILE = "all-routes-hodram-b261-b310-wrap-fixes-v1-20261123"
ROOT, WORK = stage.BATCH / "registered", stage.BATCH / "registration"
ROM = ROOT / "Translation_DS_Hodram_B261_B310_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_hodram_b261_b310_wrap_fixes_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_b261_b310_wrap_fixes_registered_20261123.md")
DISPLAY, EVIDENCE, FE = stage.NATIVE, stage.ROOT, stage.FE_PROOF
GLYPHS, CHOICE, ROLES, STYLES = live.GLYPHS, live.CHOICES, live.ROLES, live.STYLES
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Hodram's final queued wrap fixes, including the Proofs, bounty and expedition scenes."
RUNS = ("route1",)
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
link_snapshot = parent.link_snapshot
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | globals())
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | globals())

old_choices = parent.controls_source[
    parent.controls_source.index("        if block == 243"):parent.controls_source.index('        assert row["english"]')]
controls_source = checked_text(parent.controls_source, {
    'complete_stored_page_count"] == 16': 'complete_stored_page_count"] == 15',
    'len(choice["choices"]) == 11 and len(played["original_menu_choices"]) == 1':
        'len(choice["choices"]) == 7 and not played["original_menu_choices"]',
    old_choices: "",
    'len(styles["records"]) == 37': 'len(styles["records"]) == 115',
    'retained_modal_pages=16': 'retained_modal_pages=15',
    'retained_supporting_roles=25': 'retained_supporting_roles=12',
})
scene_checks = parent.verify_source[parent.verify_source.index('    hatra, ='):parent.verify_source.index('    result = dict(')]
verify_source = checked_text(parent.verify_source, {
    'observed_count() == 34': 'observed_count() == 20',
    'native_count() == 30': 'native_count() == 19',
    'len(records) == 310': 'len(records) == 183',
    'len(changed) == 29': 'len(changed) == 18',
    'for r in changed) == 29': 'for r in changed) == 14',
    'for r in changed) == 0': 'for r in changed) == 4',
    'assert set(manuscript["wrap_leads_covered"]) == {row["id"] for row in changed}':
        'assert len(manuscript["wrap_leads_covered"]) == 17\n'
        '    assert set(manuscript["wrap_leads_covered"]) < {row["id"] for row in changed}',
    scene_checks:'''    address, = [row for row in changed if row["id"] == "DK4_MES_B286_R0005"]
    default, maximum = address["display_proof"]["layouts"]
    assert default["lines"][0] == "At last, Mr. Bergstrom!"
    assert maximum["lines"][0] == f"At last, Mr. {'W' * 16}!"
    assert [line.strip() for line in default["lines"][1:]] == [line.strip() for line in maximum["lines"][1:]]
''',
    'heuristic_triage_sha256=base.digest(stage.paired.QUEUE), wording_revisions=29, wrap_only_revisions=0':
        'heuristic_triage_sha256=base.digest(stage.bound.QUEUE), exact_rebinding_sha256=base.digest(stage.bound.OUTPUT), wording_revisions=14, wrap_only_revisions=4',
    'justified_retentions=281, choice_label_retentions=11': 'justified_retentions=165, choice_label_retentions=7',
})
readme = parent.main[parent.main.index('    (PACKAGE / "README.md").write_text'):parent.main.index('    base.save(PACKAGE / "checksums.json"')]
main = checked_text(parent.main, {
    'len(batches) == 1086 and len(checks) == 421': 'len(batches) == 1087 and len(checks) == 422',
    'assert len(checks) == 422': 'assert len(checks) == 423',
    'verified_observed_wrap_followups_predecessor': 'verified_active_predecessor',
    '"release_stack_with_observed_wrap_followups.json"': '"release_stack_with_active_predecessor.json"',
    'previously_localized_records=358, contextual_records_revisited=358, contextual_decisions_reused=329':
        'previously_localized_records=305, contextual_records_revisited=305, contextual_decisions_reused=287',
    'prior_records_reviewed=358, contextual_decisions_reused=329':
        'prior_records_reviewed=305, contextual_decisions_reused=287',
    'justified_retentions=281, retained_choice_labels=11, retained_style_variants=37':
        'justified_retentions=165, retained_choice_labels=7, retained_style_variants=115',
    'prose_revisions=29': 'prose_revisions=14',
    'wrap_only_revisions=0': 'wrap_only_revisions=4',
    'retained_modal_pages=16, revised_modal_pages=0, native_choice_outcomes=1':
        'retained_modal_pages=15, revised_modal_pages=0, native_choice_outcomes=0',
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Hodram B261–B310 dialogue review

The [testing ROM](../../{ROM.as_posix()}) incorporates 18 revised passages in Hodram's bounty, Proofs of Conquest, and expedition scenes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("hodram_b221_b260_wrap_fixes", "hodram_b261_b310_wrap_fixes").replace(
    "verified_active_predecessor", "verified_hodram_b221_b260_wrap_fixes_predecessor").replace(
    "release_stack_with_active_predecessor", "release_stack_with_hodram_b221_b260_wrap_fixes")

pins = parent.commit[parent.commit.index("    _, fixture, receipt"):parent.commit.index("    research = ")]
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    pins: '    earlier = [live.route_rom(1)]\n',
    'Preserve the Hodram B221–B260 candidate, predecessor and focused ROMs':
        'Preserve the Hodram B261–B310 candidate, predecessor and focused ROM',
    old_doc:'''    DOC.write_text(f"""# Hodram B261–B310 dialogue review

Fourteen complete exchanges reconcile 305 previously localized texts. Fourteen wording revisions and four wrap-only fixes resolve 17 queued leads and a nearby awkward phrase. The ledger records 165 justified dialogue or panel retentions, seven original choice captions and 115 retained personality variants. [Exact review](../{REVIEW.as_posix()})

All 19 revised display cases passed native glyph and layout checks, including the guildmaster's greeting at two surname widths. Fifteen speakerless commands and 12 names or roles passed native verification. Twenty focused emulator holds cover each revision, a reward notice, a substituted injury notice and the return to port. Ordinary event triggers, conditional outcomes and handheld display remain unvisited in this batch. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("hodram_b221_b260_wrap_fixes", "hodram_b261_b310_wrap_fixes")

scope = parent.scope | globals()
for source in (controls_source, verify_source, main, commit):
    exec(compile(source, __file__ + "::registered-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
