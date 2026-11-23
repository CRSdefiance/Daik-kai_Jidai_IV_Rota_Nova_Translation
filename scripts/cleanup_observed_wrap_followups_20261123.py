"""Archive the cross-route wrap checkpoint and remove its verified duplicates."""

from shutil import copyfile

from scripts import cleanup_hodram_late_story_wraps_20261123 as prior
from scripts import cleanup_rafael_mediterranean_followups_20261123 as duplicate_check
from scripts import register_observed_wrap_followups_20261123 as current
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = current.base, current.stage
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = stage.CHECKPOINT
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
    for proof in (DRIVE, QUEUE, RECEIPT):
        target = CHECKPOINT_DIR / proof.name
        if not target.exists():
            copyfile(proof, target)
        assert base.digest(target) == base.digest(proof)
    remaining = [row for row in queue["records"] if "reviewed" not in row]
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{current.CHECKPOINT} [Checkpoint]({current.DOC.name})\n\n"
    section = (stub + f"""Four wrap revisions across Rafael and Hodram reconcile 84 texts in four complete exchanges. The review carries forward 73 individual speech decisions, seven original choice captions and ten names or roles. Five stored native pages passed. Nine focused emulator holds cover the two pages of Cesare's revised trade routes explanation, the return to the following panel, the one-page Zhuge Liang reply, and both Rafael passages. Ordinary activation and handheld testing remain open for these scenes. [Exact review](../{current.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Cold boot, 17 focused tests and byte-exact clean-input patch reconstruction passed. Cleanup reclaimed {receipt['reclaimed_bytes']:,} bytes of exact duplicates. [Latest testing build]({drive['url']}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(CHECKPOINT_DIR / RECEIPT.name).as_posix()})

The refreshed scan has {len(remaining)} open leads. The four gameplay or visual issues listed in the preceding checkpoint are resolved in this candidate. Keep the full contextual review across four routes, practical ordinary town and random scene coverage, the 276 shared display leads and 27,700 historical credits in scope. Graphics artwork and the older-record technical re-audit remain separate. [Current wrap queue](../{(CHECKPOINT_DIR / QUEUE.name).as_posix()})

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = current.DOC.with_name(name)
        contents = path.read_bytes()
        if not contents.startswith(section):
            assert contents.startswith(stub.encode())
            base.replace_checked(path, section + contents.removeprefix(stub.encode()))
    print(f"{len(remaining)} open scan leads. Reclaimed {receipt['reclaimed_bytes']:,} duplicate bytes.")


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        cleanup()
    handoff()
