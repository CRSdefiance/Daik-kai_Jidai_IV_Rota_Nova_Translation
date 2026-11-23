"""Archive the final Hodram wrap checkpoint and clear verified intermediates."""

from inspect import getsource

from scripts import cleanup_hodram_b221_b260_wrap_fixes_20261123 as prior
from scripts import cleanup_rafael_mediterranean_followups_20261123 as duplicate_check
from scripts import register_hodram_b261_b310_wrap_fixes_20261123 as current
from scripts.source_locked_derivation_v5118 import checked_text


base, stage, Path, copyfile = current.base, current.stage, prior.Path, prior.copyfile
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = prior.CHECKPOINT_DIR.with_name("hodram_b261_b310_wrap_fixes_20261123")
DRIVE = current.ROOT / "drive_latest_build_receipt.json"
RECEIPT = current.ROOT / "checkpoint_cleanup.json"
CLEANUP_PLAN = current.ROOT / "checkpoint_cleanup_plan.json"
REVIEW_COUNT = prior.REVIEW_COUNT + 1
all_reviews = "(" + ", ".join("current" + ".parent" * depth + ".REVIEW"
                             for depth in range(REVIEW_COUNT - 1, -1, -1)) + ")"
contents = checked_text(prior.contents, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=current, OUTPUT=QUEUE)
exec(compile(contents, __file__ + "::current-wrap-queue", "exec"), queue_scope)
exec(compile(duplicate_check.cleanup_source, __file__ + "::checksum-verified-cleanup", "exec"), globals())

old_handoff = getsource(prior.handoff)
first = old_handoff.index('    section = (stub + f"""')
last = old_handoff.index('""").encode("utf-8")', first)
handoff_source = checked_text(old_handoff, {
    old_handoff[first:last]: '''    section = (stub + f"""Fourteen complete Hodram exchanges in B261–B310 reconcile 305 exact texts. There are 14 wording revisions, four wrap-only fixes, 165 justified dialogue or panel retentions, seven original choice captions and 115 retained personality variants. Native checks cover 19 revised display cases and the focused emulator run verifies 20 holds. Ordinary event triggers, conditional outcomes and handheld checks remain open for these scenes. [Exact review](../{current.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Startup, 17 focused tests and exact clean-input patch reconstruction passed. Cleanup reclaimed {receipt['reclaimed_bytes']:,} bytes of build intermediates. [Latest testing build]({drive['url']}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(CHECKPOINT_DIR / RECEIPT.name).as_posix()})

The current storyline wrap scan has {len(remaining)} unresolved heuristic leads. Continue shared display ownership and contextual decisions for the 276 pending records, practical ordinary town and random scene coverage, and final inventory reconciliation across all four routes. Preserve 27,700 historical review credits. Graphics artwork and the older-record technical re-audit remain separate. [Current wrap queue](../{(CHECKPOINT_DIR / QUEUE.name).as_posix()}) · [Shared display worklist](../translations/editorial_checkpoints/shared_display_20261123/paired_worklist.json)

''',
})
exec(compile(handoff_source, __file__ + "::checkpoint-handoff", "exec"), globals())


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        cleanup()
    handoff()
