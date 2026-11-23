"""Refresh the Hodram wrap queue and clear verified duplicate artifacts."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_observed_wrap_followups_20261123 as prior
from scripts import cleanup_rafael_mediterranean_followups_20261123 as duplicate_check
from scripts import register_hodram_b221_b260_wrap_fixes_20261123 as current
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = current.base, current.stage
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = Path("translations/editorial_checkpoints/hodram_b221_b260_wrap_fixes_20261123")
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


def handoff():
    release, drive, queue, receipt = map(base.load, (current.RELEASE, DRIVE, QUEUE, RECEIPT))
    candidate = release["candidate_sha256"]
    assert candidate == drive["sha256"] == queue["candidate_sha256"] == receipt["candidate_sha256"]
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)
    for proof in (DRIVE, QUEUE, RECEIPT):
        target = CHECKPOINT_DIR / proof.name
        if not target.exists():
            copyfile(proof, target)
        assert base.digest(target) == base.digest(proof)
    remaining = [row for row in queue["records"] if "reviewed" not in row]
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{current.CHECKPOINT} [Checkpoint]({current.DOC.name})\n\n"
    section = (stub + f"""Twenty-two complete exchanges in Hodram B221–B260 reconcile 358 exact texts. The ledger records 29 revisions, 281 justified dialogue or panel retentions, 11 retained choice captions and 37 retained personality variants. Thirty native display cases passed, including both widths of Hatra's greeting. Focused emulation verified 34 holds, including the original Leave it response, the speakerless notices and the return to port. Ordinary activation, remaining choices and handheld display are unvisited in this batch. [Exact review](../{current.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Startup, 17 focused tests and exact clean-input patch reconstruction passed. Cleanup reclaimed {receipt['reclaimed_bytes']:,} bytes of build intermediates. [Latest testing build]({drive['url']}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(CHECKPOINT_DIR / RECEIPT.name).as_posix()})

The refreshed scan has {len(remaining)} open leads. The next Hodram packet covers B261–B310, with 305 exact texts in 14 complete exchanges. Its original packet references the registered predecessor. Rebind the unchanged blocks to the active candidate for the next batch. Keep the full four-route contextual review, ordinary town and random gameplay, 276 shared display leads and 27,700 historical credits in scope. Graphics artwork and the older-record technical re-audit remain separate. [Current wrap queue](../{(CHECKPOINT_DIR / QUEUE.name).as_posix()}) · [Paired source](../{stage.paired.OUTPUT.as_posix()})

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = current.DOC.with_name(name)
        old = path.read_bytes()
        if not old.startswith(section):
            assert old.startswith(stub.encode())
            base.replace_checked(path, section + old.removeprefix(stub.encode()))
    print(f"{len(remaining)} open scan leads. Reclaimed {receipt['reclaimed_bytes']:,} duplicate bytes.")


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        cleanup()
    handoff()
