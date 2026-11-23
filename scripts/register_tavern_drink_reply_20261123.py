"""Register Faticia's one-line reply after paired ordinary Istanbul replays."""

from pathlib import Path

from scripts import register_cabin_square_wrap_20261123 as parent
from scripts import stage_tavern_drink_reply_20261123 as stage
from scripts import verify_tavern_drink_reply_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON, routes, audit = stage.ARM, stage.COMMON, parent.routes, parent.audit
PROFILE = "all-routes-tavern-drink-reply-v1-20261123"
ROOT, WORK = stage.ROOT.parent / "registered", stage.ROOT.parent / "registration"
ROM = ROOT / "Translation_DS_Tavern_Drink_Reply_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_tavern_drink_reply_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_tavern_drink_reply_registered_20261123.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
DISCOVERY = stage.BASELINE
CHECKPOINT = "Registered Faticia's one-line reply after the player declines another drink."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
link_snapshot = parent.link_snapshot
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(parent.parent.parent.prior.parent.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return len(base.load(DISPLAY)["records"])


def observed_count():
    actual = base.load(live.LIVE)
    return actual["revised_holds"] + actual["retained_holds"]


def renamed(source):
    return source.replace("cabin_square_wrap", "tavern_drink_reply")


verify_source = checked_text(parent.verify_source, {
    'played["focused_fixtures"] and played["revised_holds"] == 3 and played["menu_transitions"] == 2':
        'played["ordinary_gameplay"] and played["revised_holds"] == 1 and played["menu_transitions"] == 2',
    'played["retained_holds"] == 2 and not played["revised_offline_only_records"]':
        'played["retained_holds"] == 10 and not played["revised_offline_only_records"]',
    'stage.prior.parent.stage.observed.prior.shared.paired.prior.entries':
        'stage.prior.prior.parent.stage.observed.prior.shared.paired.prior.entries',
    '''assert all(base.load(stage.ROOT / f"{side}_cabin" / "terminal.json")["earlier_reference"] == str(DISCOVERY)
               for side in ("old", "new"))''':
        '''assert stored["baseline_trace"] == dict(path=str(DISCOVERY), sha256=base.digest(DISCOVERY))
    assert base.load(DISCOVERY)["ROM_sha256"] == previous["candidate_sha256"]
    assert len(played["Syracuse"]["holds"]) == 2 and not played["Syracuse"]["village_reached"]''',
    'assert len(rows) == 40': 'assert len(rows) == 11',
    'assert len(matched) == (1 if key == 649 else 2)': 'assert len(matched) == 1',
    'prior_records_reviewed=40, wording_revisions=2': 'prior_records_reviewed=11, wording_revisions=1',
    'justified_retentions=38, native_display_records=40': 'justified_retentions=10, native_display_records=11',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(renamed(parent.build), {
    'len(batches) == 1094 and len(checks) == 429': 'len(batches) == 1095 and len(checks) == 430',
    'assert len(checks) == 430\n': 'assert len(checks) == 431\n',
    'parent.WORK / "release_stack_with_port_fleet_wrap.json"':
        'parent.WORK / "release_stack_with_cabin_square_wrap.json"',
    'verified_port_fleet_predecessor': 'verified_cabin_square_predecessor',
    'source_bound_cabin_square_storage': 'source_bound_tavern_drink_reply_storage',
    'previously_localized_records=40, contextual_records_revisited=40, contextual_decisions_reused=38':
        'previously_localized_records=11, contextual_records_revisited=11, contextual_decisions_reused=10',
    'prior_records_reviewed=40, contextual_decisions_reused=38, observed_focused_cabin_square_holds':
        'prior_records_reviewed=11, contextual_decisions_reused=10, observed_ordinary_istanbul_holds',
    'prose_revisions=2, spacing_revisions=0': 'prose_revisions=1, spacing_revisions=0',
    'prose_revisions=2, punctuation_glyph_corrections=0': 'prose_revisions=1, punctuation_glyph_corrections=0',
    'justified_retentions=38, name_label_revisions=0, text_display_revisions=2':
        'justified_retentions=10, name_label_revisions=0, text_display_revisions=1',
    'justified_retentions=38, wrap_only_revisions=0': 'justified_retentions=10, wrap_only_revisions=0',
    'focused_cabin_square=True': 'ordinary_istanbul_tavern=True',
    'live.LIVE, DISCOVERY, routes.OUT': 'live.LIVE, live.REPLAY_DRIVER, DISCOVERY, routes.OUT',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Istanbul Tavern testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes Faticia's revised reply. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
})
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(renamed(parent.commit), {
    "Preserve the Captain's Cabin and Square candidate and its predecessor":
        'Preserve the Istanbul Tavern candidate and its predecessor',
    old_doc: '''    DOC.write_text(f"""# Faticia's reply at the Istanbul Tavern

Faticia now asks “Oh, can't handle another drink?” after the player declines. The one-line reply keeps the light drinking joke. Ten related lines retain their wording, including both first greetings and the toast after accepting. [Exact source and installed review](../{REVIEW.as_posix()})

Paired ordinary saved-game replays verified eleven Tavern panels, the second drink prompt and the return to town. A separate ordinary Syracuse replay verified the sailing estimate and departure notice. It ended at sea. Other village and random outcomes, the two legacy warning callers, and handheld testing remain open. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})

scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registration", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
