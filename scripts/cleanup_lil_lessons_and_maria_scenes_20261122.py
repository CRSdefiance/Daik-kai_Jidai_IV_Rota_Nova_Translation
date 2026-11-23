"""Refresh wrap leads and clear redundant files from the Lil and Maria checkpoint."""

from scripts import cleanup_tavern_and_proof_exchanges_20261122 as precedent
from scripts import register_lil_lessons_and_maria_scenes_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.draft.ROOT / "current_wrap_queue.json"
FOLLOWUP = stage.draft.ROOT / "observed_maria_wrap_followup.json"
refresh_source = checked_text(precedent.refresh_source, {
    '(current.parent.parent.REVIEW, current.parent.REVIEW, current.REVIEW)':
        '(current.parent.parent.parent.REVIEW, current.parent.parent.REVIEW, current.parent.REVIEW, current.REVIEW)',
    '            assert key not in reviewed\n': '',
})
queue_scope = precedent.queue_scope | {"current": release, "OUTPUT": QUEUE}
exec(compile(refresh_source, __file__ + "::wrap-queue", "exec"), queue_scope)

cleanup_source = checked_text(precedent.cleanup_source, {
    '    retained[release.live.REPORT] = focused["report_sha256"]':
        '''    retained[release.live.REPORT] = focused["lil_report_sha256"]
    maria = base.load(release.live.MARIA_ROOT / "fixture_receipt.json")["fixture_ROMs"]["after"]
    assert Path(maria["path"]) == release.live.MARIA_ROM
    retained[release.live.MARIA_ROM] = maria["sha256"]
    retained[release.live.MARIA_REPORT] = focused["maria_report_sha256"]''',
    '    exit = focused["return_frame"]\n    retained[Path(exit["path"])] = exit["PNG_sha256"]':
        '    for exit in [focused["lil_return"], *focused["maria_returns"]]:\n        retained[Path(exit["path"])] = exit["PNG_sha256"]',
    '    capture_reports.append((release.live.REPORT, fixture["fixture_sha256"]))':
        '''    capture_reports.append((release.live.REPORT, fixture["fixture_sha256"]))
    capture_reports.append((release.live.MARIA_REPORT, maria["sha256"]))''',
    'and release.live.ROM.resolve() in pins': 'and {release.live.ROM.resolve(), release.live.MARIA_ROM.resolve()} <= pins',
    'release_stack_with_tavern_and_proof_exchanges.json': 'release_stack_with_lil_lessons_and_maria_scenes.json',
})
handoff_source = checked_text(precedent.handoff_source, {
    'The review covers 203 spoken turns and eight choice labels. Fourteen lines have revised wording, 18 have improved wraps and 171 have justified retentions. Seven changed and eight retained panels played with intact speaker labels in a focused Hodram replay. Mikhail’s joke went from two pages to one and advanced directly to Hodram’s reply. The other 25 changed turns, including Maria’s lines, have offline display evidence.':
        'The review covers 224 spoken turns, three speakerless panels and six choice labels. Eight lines have revised wording, nine have improved wraps and 210 main records have individual retentions. Focused Lil and Maria replays verified 25 panels, including the Basra Shopkeeper’s quip. Lil’s scene host returned to port, and Maria’s advanced to its original Xien Yan joining notice. All changes passed native and visual checks, including the longest allowed name in Camille’s line. The three choice objects and three original speakerless commands are byte-exact.',
    '[Current wrap queue](../{QUEUE.as_posix()})':
        '[Current wrap queue](../{QUEUE.as_posix()})\n\nThe focused Maria replay also revealed two neighboring wrap leads. Lil’s reference to the people of Southeast Asia and Maria’s “for all you’re worth” can be tested as whole phrases in the next batch. [Exact records and emulator holds](../{FOLLOWUP.as_posix()})',
})
scope = precedent.scope | globals()
scope["workflow"] = release.parent.scope["workflow"]
for program in (cleanup_source, handoff_source):
    exec(compile(program, __file__ + "::cleanup", "exec"), scope)


def observed_wrap_followup():
    registered, played = map(base.load, (release.REVIEW, release.live.LIVE))
    assert registered["candidate_sha256"] == played["candidate_sha256"] == base.digest(release.ROM)
    phrases = {
        "DK4_MES_B36_R0037": ("the people of Southeast Asia.", "The focused panel puts of Southeast Asia on a separate row. Keep the people and the place together."),
        "DK4_MES_B36_R0045": ("for all you're worth,", "The focused panel splits the complete idiom after all. Preserve it and the warning in the next trial."),
    }
    rows = []
    for row in (r for r in registered["records"] if r["id"] in phrases and r["file_path"] == "/data/SC3.DK4"):
        hold = row["observed_focused"]["capture"]
        assert row["decision"] == "retention" and base.digest(hold["path"]) == hold["PNG_sha256"]
        phrase, reason = phrases[row["id"]]
        assert phrase in row["english"]
        rows.append(dict(id=row["id"], source_reference=row["source_reference"], current_reference=row["registered_reference"],
                         wording=row["english"], proposed_protected_phrase=phrase, reason=reason, initialized_replay_hold=hold))
    assert len(rows) == 2
    base.save(FOLLOWUP, dict(candidate_sha256=registered["candidate_sha256"], rows=rows, source_words_still_approved=True,
                            formatting_proposal_pending=True, natural_activation_observed=False))


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not FOLLOWUP.exists():
        observed_wrap_followup()
    scope["handoff"](scope["cleanup"]())
