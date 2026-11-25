"""Archive Rafael's fleet and crew checkpoint and clear verified duplicates."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_rafael_charlotte_and_maria_20261122 as prior
from scripts import register_rafael_fleet_and_crew_exchanges_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage, live = release.base, release.stage, release.live
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = stage.paired.OUTPUT.parent
all_reviews = "(" + ", ".join("current" + ".parent" * n + ".REVIEW" for n in range(19, -1, -1)) + ")"
refresh_source = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=release, OUTPUT=QUEUE)
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)

cleanup_source = checked_text(prior.cleanup_source, {
    "release_stack_with_rafael_charlotte_and_maria.json": "release_stack_with_rafael_fleet_and_crew_exchanges.json",
    'history / "staging"': 'history / "preflight"',
})
scope = prior.scope | globals()
exec(compile(cleanup_source, __file__ + "::checksum-bound-cleanup", "exec"), scope)


def handoff(result):
    drive, queue = map(base.load, (DRIVE, QUEUE))
    candidate = base.load(release.RELEASE)["candidate_sha256"]
    assert drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"] == candidate
    for evidence in (DRIVE, QUEUE, RECEIPT):
        archived = CHECKPOINT_DIR / evidence.name
        if not archived.exists():
            copyfile(evidence, archived)
        assert base.digest(evidence) == base.digest(archived)
    open_wraps = sum("reviewed" not in row for row in queue["records"])
    queue_ref = (CHECKPOINT_DIR / QUEUE.name).as_posix()
    cleanup_ref = (CHECKPOINT_DIR / RECEIPT.name).as_posix()
    stub = f"# Current editorial checkpoint - 2026-11-22\n\n{release.CHECKPOINT} [Checkpoint]({release.DOC.name})\n\n"
    section = (stub + f"""Six complete exchanges add 224 decisions. Twelve passages changed to address the flagged wraps, and 212 have individual retention reasons. Fifteen revised display cases passed exact glyph checks across default and maximum name widths. All four original system panels and nine supporting role labels passed their native checks. Focused gameplay verified 25 holds and the return to port. Natural story activation and handheld verification remain open for this batch. [Exact review](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Startup and 17 targeted tests passed, and the clean-input patch reconstructs the ROM byte for byte. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Clean-input patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{cleanup_ref})

The current scan has {open_wraps} wrap leads awaiting a decision. The next Hodram packet covers 282 texts in 18 complete early and midroute exchanges, including 24 flagged wraps and four original choice labels. Continue Rafael's remaining story leads, the other storylines, ordinary town and random scenes, names, and remaining player-facing prose. Preserve the 276 shared display leads, 27,700 historical credits, deferred artwork, and later older-record technical re-audit. [Current wrap queue](../{queue_ref}) · [Next Hodram packet](../translations/editorial_checkpoints/hodram_early_and_midroute_wraps_20261122/paired_source.json)

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = release.DOC.with_name(name)
        body = path.read_bytes()
        if not body.startswith(section):
            base.replace_checked(path, section + body.removeprefix(stub.encode("utf-8")))


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        scope["cleanup"]()
    handoff(base.load(RECEIPT))
