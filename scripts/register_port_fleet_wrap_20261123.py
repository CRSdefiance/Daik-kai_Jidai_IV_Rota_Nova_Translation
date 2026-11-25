"""Register two Port Fleet revisions and the current Syracuse replay evidence."""

from pathlib import Path

from scripts import register_market_introduction_wrap_20261123 as parent
from scripts import replay_port_fleet_refusals_20261123 as replay
from scripts import stage_port_fleet_wrap_20261123 as stage
from scripts import verify_port_fleet_wrap_20261123 as live
from scripts.source_locked_derivation_v5118 import checked_text


base, native, workflow = parent.base, parent.native, parent.workflow
ARM, COMMON, routes, audit = stage.ARM, stage.COMMON, parent.routes, parent.audit
PROFILE = "all-routes-port-fleet-wrap-v1-20261123"
ROOT, WORK = stage.ROOT.parent / "registered", stage.ROOT.parent / "registration"
ROM = ROOT / "Translation_DS_Port_Fleet_20261123_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = parent.PACKAGE.with_name("all_routes_editorial_20261123_port_fleet_wrap_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = parent.DOC.with_name("editorial_port_fleet_wrap_registered_20261123.md")
EVIDENCE, DISPLAY = stage.ROOT, stage.PROOF
STARTUP, STARTUP_CAPTURE, QA = EVIDENCE / "own_startup_verification.json", stage.STARTUP_CAPTURE, EVIDENCE / "qa_passed.xml"
VISUAL = EVIDENCE / "visual_review.json"
DISCOVERY = replay.HISTORY
CHECKPOINT = "Registered the reflowed Port Fleet captain warning and Gerhard's reply."
guard_spec = parent.guard_spec
bind_registered_story_percent_guard = parent.bind_registered_story_percent_guard
link_snapshot = parent.link_snapshot
startup_scope = parent.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
exec(compile(parent.prior.parent.startup_source, __file__ + "::startup", "exec"), startup_scope)


def native_count():
    return len(base.load(DISPLAY)["records"])


def observed_count():
    return base.load(live.LIVE)["revised_holds"]


def renamed(source):
    return source.replace("market_intro_wrap", "port_fleet_wrap")


verify_source = checked_text(parent.verify_source, {
    'played["focused_fixtures"] and played["revised_holds"] == 1 and played["menu_transitions"] == 2':
        'played["focused_fixtures"] and played["revised_holds"] == 1 and played["menu_transitions"] == 3',
    'played["retained_holds"] == 2 and not played["revised_offline_only_records"]':
        'played["retained_holds"] == 0 and played["revised_offline_only_records"] == [805]',
    'stage.prior.parent.stage.observed.prior.shared.paired.prior.entries':
        'stage.prior.prior.parent.stage.observed.prior.shared.paired.prior.entries',
    'assert stored["predecessor_sha256"] == base.load(DISCOVERY)["candidate_sha256"]':
        'assert all(base.load(replay.ROOT / side / "terminal.json")["history_sha256"] == base.digest(DISCOVERY)\n'
        '               for side in ("current", "revised"))',
    'assert len(rows) == 11': 'assert len(rows) == 13',
    '''        matched, = [hold for hold in holds if hold["message_ID"] == key]
        row["observed_changed_pages"] = [matched]''':
        '''        matched = [hold for hold in holds if hold["message_ID"] == key]
        assert len(matched) == (0 if key in played["revised_offline_only_records"] else 1)
        row["observed_changed_pages"] = matched''',
    'prior_records_reviewed=11, wording_revisions=1': 'prior_records_reviewed=13, wording_revisions=2',
    'justified_retentions=10, native_display_records=11': 'justified_retentions=11, native_display_records=13',
})
readme = parent.build[parent.build.index('    (PACKAGE / "README.md").write_text'):parent.build.index('    base.save(PACKAGE / "checksums.json"')]
build = checked_text(renamed(parent.build), {
    'len(batches) == 1092 and len(checks) == 427': 'len(batches) == 1093 and len(checks) == 428',
    'assert len(checks) == 428\n': 'assert len(checks) == 429\n',
    'parent.WORK / "release_stack_with_title_reports_label.json"':
        'parent.WORK / "release_stack_with_market_intro_wrap.json"',
    'verified_title_reports_label_predecessor': 'verified_market_introduction_predecessor',
    'source_bound_market_introduction_storage': 'source_bound_port_fleet_storage',
    'previously_localized_records=11, contextual_records_revisited=11, contextual_decisions_reused=10':
        'previously_localized_records=13, contextual_records_revisited=13, contextual_decisions_reused=11',
    'prior_records_reviewed=11, contextual_decisions_reused=10, observed_focused_market_introduction_holds':
        'prior_records_reviewed=13, contextual_decisions_reused=11, observed_focused_port_fleet_holds',
    'prose_revisions=1, spacing_revisions=0': 'prose_revisions=2, spacing_revisions=0',
    'prose_revisions=1, punctuation_glyph_corrections=0': 'prose_revisions=2, punctuation_glyph_corrections=0',
    'justified_retentions=10, name_label_revisions=0, text_display_revisions=1':
        'justified_retentions=11, name_label_revisions=0, text_display_revisions=2',
    'justified_retentions=10, wrap_only_revisions=0': 'justified_retentions=11, wrap_only_revisions=0',
    'focused_market_introduction=True': 'focused_port_fleet=True',
    readme: '''    (PACKAGE / "README.md").write_text(f"""# Port Fleet testing candidate

The [testing ROM](../../{ROM.as_posix()}) includes the reflowed captain warning and Gerhard refusal. The [clean-input patch](translation.xdelta) reconstructs SHA-256 {candidate} byte for byte.
""", encoding="utf-8")
''',
})
old_doc = parent.commit[parent.commit.index("    DOC.write_text"):parent.commit.index("    prefix =")]
commit = checked_text(renamed(parent.commit), {
    'Preserve the Market introduction candidate and its predecessor':
        'Preserve the Port Fleet candidate and its predecessor',
    old_doc: '''    DOC.write_text(f"""# Port Fleet warning and refusal

The port worker's warning keeps “You need to captain a ship!” on one row. Gerhard's reply now reads “No. I will remain your aide.” The review retains eleven crew and resupply lines with individual reasons, including Camille's admiral-name substitution. [Exact source and installed review](../{REVIEW.as_posix()})

The Syracuse replay verified Gerhard's refusal and three original fleet-admiral picker states. The replay used a copied save and supplied funds and Command to reach the selection. The captain warning passed the original native display checks offline. Captain-warning activation, earned fleet formation and handheld testing remain open. [Testing build and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8")
''',
})

scope = parent.scope | globals()
for program in (verify_source, build, commit):
    exec(compile(program, __file__ + "::registration", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
