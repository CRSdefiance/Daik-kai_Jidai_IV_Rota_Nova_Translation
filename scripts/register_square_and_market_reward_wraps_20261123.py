"""Register the two shared dialogue revisions and their native replay evidence."""

from inspect import getsource
from pathlib import Path

from scripts import register_tavern_nearby_town_wrap_20261123 as parent
from scripts import stage_square_and_market_reward_wraps_20261123 as stage
from scripts import verify_square_and_market_reward_wraps_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON, routes, audit = stage.ARM, stage.COMMON, parent.routes, parent.audit
PROFILE = "all-routes-square-and-market-reward-wraps-v1-20261123"
ROOT, WORK = stage.ROOT.parent / "registered", stage.ROOT.parent / "registration"
ROM = ROOT / "Translation_DS_Square_Market_Reward_Wraps_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_square_market_reward_wraps_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_square_and_market_reward_wraps_registered_20261123.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
DISCOVERY = Path("translations/editorial_checkpoints/shared_display_20261123/additional_voyages_20261123.json")
CHECKPOINT = "Registered clearer dialogue for the Square sample pitch and the Market recommendation."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
link_snapshot = parent.link_snapshot
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(parent.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return len(base.load(DISPLAY)["records"])


def observed_count():
    report = base.load(live.LIVE)
    return report["revised_holds"] + report["retained_holds"]


verify_source = checked_text(getsource(parent.verify), {
    '{str(stage.KEY)}': '{str(key) for key in stage.EDITS}',
    'stored["allocations"][str(stage.KEY)]["new_null_fields"] == 0':
        'all(slot["new_null_fields"] == 0 for slot in stored["allocations"].values())',
    'played["ordinary_battery_save_gameplay"] and played["revised_holds"] == 2 and played["menu_transitions"] == 4':
        'played["focused_fixtures"] and played["revised_holds"] == 2 and played["menu_transitions"] == 3',
    'played["retained_holds"] == 8': 'played["retained_holds"] == 5',
    'stage.observed.prior.shared.paired.prior.entries': 'parent.stage.observed.prior.shared.paired.prior.entries',
    '== {stage.KEY}': '== set(stage.EDITS)',
    'assert base.load(audit.OUT)["candidate_sha256"] == previous["candidate_sha256"]':
        'assert base.digest(audit.OUT) == prior_review["retained_editorial_coverage_sha256"]',
    'assert stored["inherited_observations_sha256"] == base.digest(DISCOVERY)':
        'assert stored["predecessor_sha256"] == base.load(DISCOVERY)["candidate_sha256"]',
    'assert len(rows) == 9': 'assert len(rows) == 27',
    '''    revised, = [row for row in rows if row["decision"] == "revision"]
    assert revised["message_ID"] == stage.KEY and revised["installed_hex"] == installed[stage.KEY].text.hex()
    assert all(case["complete_native_body"] for case in stored["native_town_cases"])
    assert len({case["town"] for case in stored["native_town_cases"]}) == 90
    revised["observed_changed_pages"] = [row for row in played["observed"]["tunis"] if row["message_ID"] == stage.KEY]''':
        '''    revised = {row["message_ID"]: row for row in rows if row["decision"] == "revision"}
    assert revised.keys() == stage.EDITS.keys()
    holds = [row for group in played["observed"].values() for row in group]
    for key, row in revised.items():
        assert row["installed_hex"] == installed[key].text.hex()
        matched, = [hold for hold in holds if hold["message_ID"] == key]
        row["observed_changed_pages"] = [matched]
    assert all(row["installed_hex"] == installed[row["message_ID"]].text.hex() for row in rows)''',
    'ordinary_tavern_dialogue=played, visual_review=viewed, prior_records_reviewed=9, wording_revisions=1':
        'focused_dialogue=played, visual_review=viewed, prior_records_reviewed=27, wording_revisions=2',
    'justified_retentions=8, native_town_variants=90': 'justified_retentions=25, native_display_records=27',
})


def renamed(source):
    return source.replace("tavern_nearby_town_wrap", "square_and_market_reward_wraps")


readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(renamed(parent.build), {
    'len(batches) == 1089 and len(checks) == 424': 'len(batches) == 1090 and len(checks) == 425',
    'assert len(checks) == 425\n': 'assert len(checks) == 426\n',
    'parent.WORK / "release_stack_with_regional_rumor_wrap_followups.json"':
        'parent.WORK / "release_stack_with_tavern_nearby_town_wrap.json"',
    'verified_regional_rumor_wrap_followups_predecessor': 'verified_tavern_nearby_town_wrap_predecessor',
    'source_bound_tavern_storage': 'source_bound_square_and_market_storage',
    'previously_localized_records=9, contextual_records_revisited=9, contextual_decisions_reused=8':
        'previously_localized_records=27, contextual_records_revisited=27, contextual_decisions_reused=25',
    'prior_records_reviewed=9, contextual_decisions_reused=8, observed_ordinary_tavern_holds':
        'prior_records_reviewed=27, contextual_decisions_reused=25, observed_focused_square_and_market_holds',
    'prose_revisions=1, spacing_revisions=0': 'prose_revisions=2, spacing_revisions=0',
    'prose_revisions=1, punctuation_glyph_corrections=0': 'prose_revisions=2, punctuation_glyph_corrections=0',
    'justified_retentions=8, name_label_revisions=0, text_display_revisions=1':
        'justified_retentions=25, name_label_revisions=0, text_display_revisions=2',
    'justified_retentions=8, wrap_only_revisions=0': 'justified_retentions=25, wrap_only_revisions=0',
    'ordinary_Tunis_and_Syracuse=True': 'focused_square_and_market=True',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Square and Market dialogue testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the reflowed sample pitch and recommendation. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
})

old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(renamed(parent.commit), {
    'Preserve the Tavern candidate and its predecessor': 'Preserve the Square and Market candidate and its predecessor',
    old_doc: '''    DOC.write_text(f"""# Square sample pitch and Market recommendation

The Square's alternate giveaway voice now fits “Try a sample! It's free right now!” on one row. The recommendation puts the offer and the thank-you on complete rows. The review records two revisions and 25 individually justified retentions. [Exact source and installed review](../{REVIEW.as_posix()})

Paired emulator runs verified both revised pages, five retained holds and three transition frames. A four-byte Chapel, assignment and voice fixture selected the original Square branch. The Market run supplied merchandise, share and reward prerequisites. Ordinary activation and hardware testing remain open. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})

scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registration", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
