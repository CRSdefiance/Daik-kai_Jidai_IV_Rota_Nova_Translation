"""Refresh the wrap queue and remove verified duplicate North Sea staging files."""

from pathlib import Path

from scripts import cleanup_mosque_elysion_mikhail_20261122 as cleanup
from scripts import cleanup_palace_eirene_pereira_london_20261122 as prior
from scripts import register_north_sea_and_hodram_reconciliation_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
QUEUE = stage.BATCH / "current_wrap_queue.json"
all_reviews = "(" + ", ".join("current" + ".parent" * i + ".REVIEW" for i in range(10, -1, -1)) + ")"
refresh_source = checked_text(prior.refresh_source, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | {"current": release, "OUTPUT": QUEUE}
exec(compile(refresh_source, __file__ + "::current-wrap-queue", "exec"), queue_scope)
cleanup_source = checked_text(cleanup.cleanup_source, {
    'release_stack_with_mosque_elysion_mikhail.json': 'release_stack_with_north_sea_and_hodram_reconciliation.json',
    'for edition in (stage.BATCH, history, history / "initial_preflight", history / "layout_trial"):':
        'for edition in (stage.BATCH, history, history / "corrected"):',
})
scope = cleanup.scope | globals()
scope["workflow"] = release.parent.scope["workflow"]
exec(compile(cleanup_source, __file__ + "::cleanup", "exec"), scope)


def handoff(result):
    drive, queue = map(base.load, (DRIVE, QUEUE))
    assert drive["sha256"] == queue["candidate_sha256"] == result["candidate_sha256"]
    reviewed = sum("reviewed" in row for row in queue["records"])
    open_wraps = len(queue["records"]) - reviewed
    training = stage.BATCH.parent.parent / "next_contextual_wraps_20261122/rafael_B84_training_contextual_review.json"
    assert len(base.load(training)["records"]) == 131
    section = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The clean-source comparison covers 74 spoken lines. Nine have revised prose and 65 have individual retention reasons. All nine new pages passed the exact game-font and native layout checks. Focused cold-boot replays verified 13 panels and nameplates, including both Port Worker lines and the original question mark. The lesson choice branches and natural story triggers were outside these replays. Earlier ordinary town evidence remains available. [Exact coverage ledger](../{release.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {drive['sha256']}. The clean-input patch reconstructs that ROM byte for byte. Startup and 17 focused repository tests passed. Cleanup removed {len(result['removed'])} duplicate files totaling {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

Six of the 96 earlier Hodram B61–B70 payload differences now have registered decisions. Keep the other 90 in scope. The refreshed scan has {open_wraps} wrap leads awaiting a current decision. Rafael’s B84 training review has 131 exact contextual decisions, nine proposals and 122 justified retentions. It covers the five choice captions and both verified two-page notices. Continue the distinct menu, allocation, native and gameplay checks before integration. All four storylines, shared dialogue, names and roles, practical town and random scenes, and the 276 shared display leads remain active. Preserve the 27,700 historical review credits. Graphics artwork and the later technical re-audit remain separate. [Current wrap queue](../{QUEUE.as_posix()}) · [B84 review](../{training.as_posix()})

""".encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = release.DOC.with_name(name)
        body = path.read_bytes()
        boundary = body.index(b"# Current editorial checkpoint", 1)
        base.replace_checked(path, section + body[boundary:])


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        scope["cleanup"]()
    handoff(base.load(RECEIPT))
