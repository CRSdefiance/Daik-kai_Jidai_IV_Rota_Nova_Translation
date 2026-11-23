"""Register Market introduction wording and its original reward-branch evidence."""

from pathlib import Path

from scripts import register_title_reports_label_20261123 as parent
from scripts import stage_market_introduction_wrap_20261123 as stage
from scripts import verify_market_introduction_wrap_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


prior = parent.parent
base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON, routes, audit = stage.ARM, stage.COMMON, parent.routes, parent.audit
PROFILE = "all-routes-market-intro-wrap-v1-20261123"
ROOT, WORK = stage.ROOT.parent / "registered", stage.ROOT.parent / "registration"
ROM = ROOT / "Translation_DS_Market_Introduction_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = prior.PACKAGE.with_name("all_routes_editorial_20261123_market_introduction_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = prior.DOC.with_name("editorial_market_introduction_wrap_registered_20261123.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
DISCOVERY = Path("translations/editorial_checkpoints/shared_display_20261123/bounded_calls_current_20261123.json")
CHECKPOINT = "Registered the Market letter-of-introduction dialogue on two complete rows."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
link_snapshot = parent.link_snapshot
startup_scope = prior.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(prior.parent.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return len(base.load(DISPLAY)["records"])


def observed_count():
    played = base.load(live.LIVE)
    return played["revised_holds"] + played["retained_holds"]


def renamed(source):
    return source.replace("square_and_market_reward_wraps", "market_intro_wrap")


verify_source = checked_text(prior.verify_source, {
    'played["focused_fixtures"] and played["revised_holds"] == 2 and played["menu_transitions"] == 3':
        'played["focused_fixtures"] and played["revised_holds"] == 1 and played["menu_transitions"] == 2',
    'played["retained_holds"] == 5': 'played["retained_holds"] == 2',
    'parent.stage.observed.prior.shared.paired.prior.entries':
        'stage.prior.parent.stage.observed.prior.shared.paired.prior.entries',
    'assert len(rows) == 27': 'assert len(rows) == 11',
    'prior_records_reviewed=27, wording_revisions=2': 'prior_records_reviewed=11, wording_revisions=1',
    'justified_retentions=25, native_display_records=27': 'justified_retentions=10, native_display_records=11',
})
readme = prior.build[prior.build.index('    (PACKAGE / "README.md").write_text'):prior.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(renamed(prior.build), {
    'len(batches) == 1090 and len(checks) == 425': 'len(batches) == 1092 and len(checks) == 427',
    'assert len(checks) == 426\n': 'assert len(checks) == 428\n',
    'parent.WORK / "release_stack_with_tavern_nearby_town_wrap.json"':
        'parent.WORK / "release_stack_with_title_reports_label.json"',
    'verified_tavern_nearby_town_wrap_predecessor': 'verified_title_reports_label_predecessor',
    'source_bound_square_and_market_storage': 'source_bound_market_introduction_storage',
    'previously_localized_records=27, contextual_records_revisited=27, contextual_decisions_reused=25':
        'previously_localized_records=11, contextual_records_revisited=11, contextual_decisions_reused=10',
    'prior_records_reviewed=27, contextual_decisions_reused=25, observed_focused_square_and_market_holds':
        'prior_records_reviewed=11, contextual_decisions_reused=10, observed_focused_market_introduction_holds',
    'prose_revisions=2, spacing_revisions=0': 'prose_revisions=1, spacing_revisions=0',
    'prose_revisions=2, punctuation_glyph_corrections=0': 'prose_revisions=1, punctuation_glyph_corrections=0',
    'justified_retentions=25, name_label_revisions=0, text_display_revisions=2':
        'justified_retentions=10, name_label_revisions=0, text_display_revisions=1',
    'justified_retentions=25, wrap_only_revisions=0': 'justified_retentions=10, wrap_only_revisions=0',
    'focused_square_and_market=True': 'focused_market_introduction=True',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Market introduction testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the reflowed letter-of-introduction offer. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
})
old_doc = prior.commit[prior.commit.index("    DOC.write_text"):prior.commit.index("    prefix =")]
commit = checked_text(renamed(prior.commit), {
    'Preserve the Square and Market candidate and its predecessor':
        'Preserve the Market introduction candidate and its predecessor',
    old_doc: '''    DOC.write_text(f"""# Market letter of introduction

The Market trader now offers the letter and thanks the player on two complete rows. The clean Japanese links the offer to the sale of popular goods. The next panel still explains where to use the introduction, and the review retains ten related records with individual reasons. [Exact source and installed review](../{REVIEW.as_posix()})

Paired emulator runs verified the revised offer, the small-town instructions, the farewell and the return. The runs supplied stock, share and reward conditions to reach the original introduction branch. Earned reward activation and handheld display remain untested. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})

scope = prior.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registration", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
