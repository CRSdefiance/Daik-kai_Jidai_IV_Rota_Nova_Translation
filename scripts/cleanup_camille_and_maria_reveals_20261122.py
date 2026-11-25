"""Carry forward current wrap leads and clear the verified staging duplicates."""

from scripts import cleanup_lil_lessons_and_maria_scenes_20261122 as precedent
from scripts import register_camille_and_maria_reveals_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.draft.ROOT / "current_wrap_queue.json"
FOLLOWUP = stage.draft.ROOT / "observed_phrase_breaks.json"
refresh_source = checked_text(precedent.refresh_source, {
    '(current.parent.parent.parent.REVIEW, current.parent.parent.REVIEW, current.parent.REVIEW, current.REVIEW)':
        '(current.parent.parent.parent.parent.REVIEW, current.parent.parent.parent.REVIEW, current.parent.parent.REVIEW, current.parent.REVIEW, current.REVIEW)',
})
queue_scope = precedent.queue_scope | {"current": release, "OUTPUT": QUEUE}
exec(compile(refresh_source, __file__ + "::wrap-queue", "exec"), queue_scope)

cleanup_source = checked_text(precedent.cleanup_source, {
    'release_stack_with_lil_lessons_and_maria_scenes.json': 'release_stack_with_camille_and_maria_reveals.json',
})
handoff_source = checked_text(precedent.handoff_source, {
    'The review covers 224 spoken turns, three speakerless panels and six choice labels. Eight lines have revised wording, nine have improved wraps and 210 main records have individual retentions. Focused Lil and Maria replays verified 25 panels, including the Basra Shopkeeper’s quip. Lil’s scene host returned to port, and Maria’s advanced to its original Xien Yan joining notice. All changes passed native and visual checks, including the longest allowed name in Camille’s line. The three choice objects and three original speakerless commands are byte-exact.':
        'The review covers 191 spoken turns and an intact Osaka Glass forecast. Two lines have new wording, ten have improved wraps and 180 have justified retentions, including 14 decisions from the previous review. Focused Lil and Maria playback verified 22 panels and their speaker labels. All 12 changed panels passed offline native and visual checks.',
    'The focused Maria replay also revealed two neighboring wrap leads. Lil’s reference to the people of Southeast Asia and Maria’s “for all you’re worth” can be tested as whole phrases in the next batch. [Exact records and emulator holds](../{FOLLOWUP.as_posix()})':
        'The two earlier Maria findings are closed. Lil’s reference to the people of Southeast Asia and Maria’s “for all you’re worth” both appeared as intact phrases. The same replay exposed two neighboring breaks in “tell you the truth” and “making things up.” [Exact observed references](../{FOLLOWUP.as_posix()})',
})
scope = precedent.scope | globals()
scope["workflow"] = release.parent.scope["workflow"]
for program in (cleanup_source, handoff_source):
    exec(compile(program, __file__ + "::cleanup", "exec"), scope)


def log_observed_neighbors():
    report = base.load(release.REVIEW)
    assert report["candidate_sha256"] == base.digest(release.ROM)
    phrases = {"DK4_MES_B36_R0034": ("tell you the truth.", "tell"),
               "DK4_MES_B36_R0049": ("making things up!", "making things")}
    rows = []
    for row in report["records"]:
        key = row["id"]
        if row["file_path"] != "/data/SC3.DK4" or key not in phrases:
            continue
        phrase, expected_tail = phrases[key]
        hold = row["observed_focused"]["capture"]
        exact = row["registered_reference"]
        text = bytes.fromhex(exact["exact_body_hex"]).decode("ascii")
        assert any(line.strip().endswith(expected_tail) for line in text.splitlines())
        assert phrase in row["english"] and phrase not in text
        assert base.digest(hold["path"]) == hold["PNG_sha256"]
        rows.append(dict(id=key, source_reference=row["source_reference"], current_reference=exact,
                         wording=row["english"], protected_phrase_to_check=phrase, focused_replay_hold=hold))
    assert len(rows) == 2
    base.save(FOLLOWUP, dict(candidate_sha256=report["candidate_sha256"], rows=rows,
                            formatting_check_pending=True, original_trigger_observed=False))


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not FOLLOWUP.exists():
        log_observed_neighbors()
    scope["handoff"](scope["cleanup"]())
