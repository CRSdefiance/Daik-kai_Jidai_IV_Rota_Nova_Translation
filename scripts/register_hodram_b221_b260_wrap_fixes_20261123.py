"""Register the tested B221–B260 Hodram dialogue and clean-input patch."""

from inspect import getsource
from os import link
from pathlib import Path
from types import FunctionType

from scripts import register_observed_wrap_followups_20261123 as parent
from scripts import stage_hodram_b221_b260_wrap_fixes_20261123 as stage
from scripts import verify_hodram_b221_b260_wrap_fixes_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native = stage.base, stage.native
PROFILE = "all-routes-hodram-b221-b260-wrap-fixes-v1-20261123"
ROOT, WORK = stage.BATCH / "registered", stage.BATCH / "registration"
ROM = ROOT / "Translation_DS_Hodram_B221_B260_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_hodram_b221_b260_wrap_fixes_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_hodram_b221_b260_wrap_fixes_registered_20261123.md")
DISPLAY, EVIDENCE, FE = stage.NATIVE, stage.ROOT, stage.FE_PROOF
GLYPHS, CHOICE, ROLES, STYLES = live.GLYPHS, live.CHOICES, live.ROLES, live.STYLES
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_focused.xml"
VISUAL = EVIDENCE / "visual_review.json"
CHECKPOINT = "Registered Hodram's historical rumors, ruins dialogue and figurehead follow-ups."
RUNS = ("route1", *live.RUNS)
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
startup_scope["startup_proof"] = FunctionType(parent.startup_scope["startup_proof"].__code__, startup_scope)
native_count = FunctionType(parent.native_count.__code__, parent.native_count.__globals__ | globals())
observed_count = FunctionType(parent.observed_count.__code__, parent.observed_count.__globals__ | globals())


def link_snapshot(source, destination, expected):
    archive = Path(".codex-release-work").resolve(strict=True)
    assert source.resolve(strict=True).is_relative_to(archive)
    assert destination.parent.resolve(strict=True).is_relative_to(archive)
    assert not source.is_symlink() and not destination.exists()
    assert base.digest(source) == expected
    link(source, destination)
    assert source.samefile(destination) and base.digest(destination) == expected


controls_source = checked_text(getsource(parent.parent.retained_controls), {
    'complete_stored_page_count"] == 17': 'complete_stored_page_count"] == 16',
    'len(choice["choices"]) == 22 and len(played["original_menu_choices"]) == 3':
        'len(choice["choices"]) == 11 and len(played["original_menu_choices"]) == 1',
    'if block == 216 and label["command_word"] == 0x2200:':
        'if block == 243 and label["command_word"] == 0x2100 and label["slot"] == 1:',
    'len(styles["records"]) == 7': 'len(styles["records"]) == 37',
    'retained_modal_pages=17': 'retained_modal_pages=16',
})
scene_checks = parent.verify_source[parent.verify_source.index('    cesare, ='):parent.verify_source.index('    result = dict(')]
verify_source = checked_text(parent.verify_source, {
    'observed_count() == 9': 'observed_count() == 34',
    'native_count() == 5': 'native_count() == 30',
    'archives = {"/data/SC0.DK4", "/data/SC1.DK4"}': 'archives = {stage.ARCHIVE}',
    'len(records) == 77': 'len(records) == 310',
    'len(changed) == 4': 'len(changed) == 29',
    'for r in changed) == 4': 'for r in changed) == 29',
    'assert not manuscript["wrap_leads_covered"]':
        'assert set(manuscript["wrap_leads_covered"]) == {row["id"] for row in changed}',
    scene_checks:'''    hatra, = [row for row in changed if row["id"] == "DK4_MES_B247_R0006"]
    default, maximum = hatra["display_proof"]["layouts"]
    assert default["lines"][0] == "Welcome, Hodram."
    assert maximum["lines"][0].startswith("Welcome, W") and maximum["lines"][0].endswith(".")
    assert default["lines"][-1].strip() == maximum["lines"][-1].strip() == "Another lovely day, isn't it?"
''',
    'observed_findings_preflight_sha256=base.digest(stage.PLAN_PROOF)':
        'heuristic_triage_sha256=base.digest(stage.paired.QUEUE)',
    'wording_revisions=4': 'wording_revisions=29',
    'justified_retentions=73, choice_label_retentions=7': 'justified_retentions=281, choice_label_retentions=11',
})

readme = parent.main[parent.main.index('    (PACKAGE / "README.md").write_text'):parent.main.index('    base.save(PACKAGE / "checksums.json"')]
main = checked_text(parent.main, {
    'len(batches) == 1085 and len(checks) == 420': 'len(batches) == 1086 and len(checks) == 421',
    'assert len(checks) == 421': 'assert len(checks) == 422',
    'verified_hodram_late_story_wraps_predecessor': 'verified_active_predecessor',
    '        copyfile(base.REGISTRY, registry_backup)\n    copyfile(base.LEDGER, ledger_backup)':
        '        link_snapshot(parent.WORK / "release_stack_with_active_predecessor.json", registry_backup, snapshot["registry_before"])\n'
        '    link_snapshot(parent.WORK / "ledger_after.json", ledger_backup, snapshot["ledger_before"])',
    'previously_localized_records=84, contextual_records_revisited=84, contextual_decisions_reused=80':
        'previously_localized_records=358, contextual_records_revisited=358, contextual_decisions_reused=329',
    'prior_records_reviewed=84, contextual_decisions_reused=80':
        'prior_records_reviewed=358, contextual_decisions_reused=329',
    'justified_retentions=73, retained_choice_labels=7, retained_style_variants=0':
        'justified_retentions=281, retained_choice_labels=11, retained_style_variants=37',
    'prose_revisions=4': 'prose_revisions=29',
    'focused_initialized_Hodram=True, focused_initialized_Rafael=True, default_substitution_panels=0, retained_modal_pages=0, revised_modal_pages=0, native_choice_outcomes=2':
        'focused_initialized_Hodram=True, default_substitution_panels=1, retained_modal_pages=16, revised_modal_pages=0, native_choice_outcomes=1',
    'stage.PLAN_PROOF': 'STYLES',
    readme:'''    (PACKAGE / "README.md").write_text(f"""# Hodram B221–B260 dialogue review

The [testing ROM](../../{ROM.as_posix()}) incorporates 29 revised passages in Hodram's historical rumors, ruins, and figurehead scenes. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""",encoding="utf-8")
''',
}).replace("observed_wrap_followups", "hodram_b221_b260_wrap_fixes").replace(
    "verified_active_predecessor", "verified_observed_wrap_followups_predecessor").replace(
    "release_stack_with_active_predecessor", "release_stack_with_observed_wrap_followups")

pins = parent.commit[parent.commit.index("    earlier = "):parent.commit.index("    research = ")]
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(parent.commit, {
    pins:'''    _, fixture, receipt = live.choice_paths(243)
    assert base.digest(fixture) == base.load(receipt)["rom_sha256"]
    earlier = [live.route_rom(1), fixture]
''',
    'Preserve the observed-wrap candidate, predecessor and focused ROMs':
        'Preserve the Hodram B221–B260 candidate, predecessor and focused ROMs',
    old_doc:'''    DOC.write_text(f"""# Hodram B221–B260 dialogue review

Twenty-two complete exchanges reconcile 358 previously localized texts. The ledger records 29 wording and wrap revisions, 281 justified dialogue or notice retentions, 11 original choice captions, and 37 retained personality variants. [Exact review](../{REVIEW.as_posix()})

All 30 revised display cases passed native glyph and layout checks, including Hatra's greeting at two name widths. Sixteen speakerless commands and 25 names or roles passed native verification. Focused emulator replays verified 34 holds, including Hatra's default greeting and the original Leave it outcome in the figurehead scene. Ordinary activation, other choices and handheld display remain open for these scenes. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""",encoding="utf-8")
''',
}).replace("observed_wrap_followups", "hodram_b221_b260_wrap_fixes")

scope = parent.scope | globals()
for source in (controls_source, verify_source, main, commit):
    exec(compile(source, __file__ + "::registered-review", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
