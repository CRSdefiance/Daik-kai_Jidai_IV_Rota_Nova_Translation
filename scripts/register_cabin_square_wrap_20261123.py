"""Register the Auto Move and Square dialogue fixes with both paired replays."""

from pathlib import Path

from scripts import register_port_fleet_wrap_20261123 as parent
from scripts import replay_cabin_warning_wrap_20261123 as cabin
from scripts import stage_cabin_square_wrap_20261123 as stage
from scripts import verify_cabin_square_wrap_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON, routes, audit = stage.ARM, stage.COMMON, parent.routes, parent.audit
PROFILE = "all-routes-cabin-square-wrap-v1-20261123"
ROOT, WORK = stage.ROOT.parent / "registered", stage.ROOT.parent / "registration"
ROM = ROOT / "Translation_DS_Cabin_Square_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_cabin_square_wrap_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_cabin_square_wrap_registered_20261123.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
DISCOVERY = cabin.HISTORY
CHECKPOINT = "Registered clearer dialogue for the Captain's Cabin warning and Square confirmation."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
link_snapshot = parent.link_snapshot
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(parent.parent.prior.parent.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return len(base.load(DISPLAY)["records"])


def observed_count():
    actual = base.load(live.LIVE)
    return actual["revised_holds"] + actual["retained_holds"]


def renamed(source):
    return source.replace("port_fleet_wrap", "cabin_square_wrap")


verify_source = checked_text(parent.verify_source, {
    'played["focused_fixtures"] and played["revised_holds"] == 1 and played["menu_transitions"] == 3':
        'played["focused_fixtures"] and played["revised_holds"] == 3 and played["menu_transitions"] == 2',
    'played["retained_holds"] == 0 and played["revised_offline_only_records"] == [805]':
        'played["retained_holds"] == 2 and not played["revised_offline_only_records"]',
    'stage.prior.prior.parent.stage.observed.prior.shared.paired.prior.entries':
        'stage.prior.parent.stage.observed.prior.shared.paired.prior.entries',
    '''assert all(base.load(replay.ROOT / side / "terminal.json")["history_sha256"] == base.digest(DISCOVERY)
               for side in ("current", "revised"))''':
        '''assert all(base.load(stage.ROOT / f"{side}_cabin" / "terminal.json")["earlier_reference"] == str(DISCOVERY)
               for side in ("old", "new"))''',
    'assert len(rows) == 13': 'assert len(rows) == 40',
    'assert len(matched) == (0 if key in played["revised_offline_only_records"] else 1)':
        'assert len(matched) == (1 if key == 649 else 2)',
    'prior_records_reviewed=13, wording_revisions=2': 'prior_records_reviewed=40, wording_revisions=2',
    'justified_retentions=11, native_display_records=13': 'justified_retentions=38, native_display_records=40',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(renamed(parent.build), {
    'len(batches) == 1093 and len(checks) == 428': 'len(batches) == 1094 and len(checks) == 429',
    'assert len(checks) == 429\n': 'assert len(checks) == 430\n',
    'parent.WORK / "release_stack_with_market_intro_wrap.json"':
        'parent.WORK / "release_stack_with_port_fleet_wrap.json"',
    'verified_market_introduction_predecessor': 'verified_port_fleet_predecessor',
    'source_bound_port_fleet_storage': 'source_bound_cabin_square_storage',
    'previously_localized_records=13, contextual_records_revisited=13, contextual_decisions_reused=11':
        'previously_localized_records=40, contextual_records_revisited=40, contextual_decisions_reused=38',
    'prior_records_reviewed=13, contextual_decisions_reused=11, observed_focused_port_fleet_holds':
        'prior_records_reviewed=40, contextual_decisions_reused=38, observed_focused_cabin_square_holds',
    'justified_retentions=11, name_label_revisions=0, text_display_revisions=2':
        'justified_retentions=38, name_label_revisions=0, text_display_revisions=2',
    'justified_retentions=11, wrap_only_revisions=0': 'justified_retentions=38, wrap_only_revisions=0',
    'focused_port_fleet=True': 'focused_cabin_square=True',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Captain's Cabin and Square testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the reflowed Auto Move warning and giveaway confirmation. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
})
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(renamed(parent.commit), {
    'Preserve the Port Fleet candidate and its predecessor':
        "Preserve the Captain's Cabin and Square candidate and its predecessor",
    old_doc: '''    DOC.write_text(f"""# Captain's Cabin warning and Square confirmation

The Surveyor now gives the room and the order in two complete sentences. The Square confirmation asks whether to give the selected goods away for free and fits on one row. The review records two revisions and 38 individually justified retentions. [Exact source and installed review](../{REVIEW.as_posix()})

Paired emulator runs verified three revised holds, two retained holds and the original returns. The Auto Move replay supplied an empty cabin seat and changed the Surveyor's voice selection, then restored both fields. The Square replay used the Chapel assignment and a supplied voice. Ordinary activation and handheld testing remain open. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})

scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registration", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
