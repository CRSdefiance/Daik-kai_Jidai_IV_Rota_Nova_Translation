"""Clear redundant staging artifacts after the registered Rafael checkpoint."""

from inspect import getsource

from scripts import cleanup_current_story_wraps_20261122 as previous
from scripts import refresh_story_wrap_queue_20261122 as queue
from scripts import register_rafael_diplomacy_and_friends_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
source = checked_text(previous.producer, {
    'release.parent.workflow.package_checksums(release.PACKAGE)': 'workflow.package_checksums(release.PACKAGE)',
    'setup = base.load(release.live.SETUP)\n    fixture = setup["fixture_ROMs"]["after"]\n    assert Path(fixture["path"]) == release.live.ROM\n    retained[release.live.ROM] = fixture["sha256"]':
        'fixture = base.load(release.live.ROOT / "fixture.json")\n    assert Path(fixture["fixture_ROM"]) == release.live.ROM\n    retained[release.live.ROM] = fixture["fixture_ROM_sha256"]',
    'retained.update({Path(r["path"]): r["PNG_sha256"] for r in focused["return_frames"].values()})':
        'exit = focused["return_frame"]\n    retained[Path(exit["path"])] = exit["PNG_sha256"]',
    'capture_reports.append((release.live.REPORT, fixture["sha256"]))':
        'capture_reports.append((release.live.REPORT, fixture["fixture_ROM_sha256"]))',
    'release_stack_with_early_story_wraps.json': 'release_stack_with_rafael_diplomacy_and_friends.json',
})
handoff_source = checked_text(getsource(previous.handoff), {
    '    section = f"""': '''    current_queue = base.load(queue.OUTPUT)
    assert current_queue["candidate_sha256"] == drive["sha256"]
    leads = len(current_queue["records"])
    reviewed = sum("reviewed" in lead for lead in current_queue["records"])
    section = f"""''',
    'The 11 exchanges contain 72 contextual decisions with 59 justified retentions, 11 wrap corrections and two wording revisions. Fifteen native pages passed, including both long-name variants, and six panels played in an initialized Maria scene. Nine revised prompts still have offline evidence only. The scan flagged 423 possible wrap leads across 19,721 ASCII bodies, including the resolved subset. [Exact source and current references](../{release.REVIEW.as_posix()}) · [Triage](../{stage.review.TRIAGE.as_posix()})':
        'The Pereira negotiations, Eirene conversation and Charlotte village scenes account for 268 retrospective decisions. Thirteen lines have new wording, 15 have wrap fixes and 240 have justified retentions. All 28 changed panels passed native visual checks, and five changed panels and five retained panels played with intact speaker labels in a focused Rafael replay. The other 23 changed panels have offline display evidence. [Exact source and current references](../{release.REVIEW.as_posix()})',
    'Continue contextual triage on the remaining story leads, shared and conditional scenes, speaker names and player-facing prose. Carry forward the 27,700 credited records and 276 alternate display leads. Keep deferred artwork and the older-record technical re-audit in their established scopes.':
        'The refreshed wrap queue has {leads} heuristic leads, including {reviewed} with current source-based decisions. Continue with the unreviewed clusters and practical town and random scenes. Carry forward 27,700 credited records and the separate 276-entry shared display worklist. [Current wrap queue](../{queue.OUTPUT.as_posix()})',
})
scope = previous.scope | globals()
scope["workflow"] = release.parent.scope["workflow"]
for program in (source, handoff_source):
    exec(compile(program, __file__ + "::cleanup", "exec"), scope)


if __name__ == "__main__":
    scope["handoff"](scope["cleanup"]())
