"""Archive the current Mediterranean follow-up coverage and verified cleanup."""

from inspect import getsource
from shutil import copyfile

from scripts import cleanup_rafael_ship_lessons_20261123 as prior
from scripts import register_rafael_mediterranean_followups_20261123 as current
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

cleanup_source = getsource(prior.cleanup)
first_attempt = cleanup_source[cleanup_source.index("    first_attempt = "):
                              cleanup_source.index("    if not CLEANUP_PLAN.exists():")]
cleanup_source = checked_text(cleanup_source, {first_attempt: ""})
exec(compile(cleanup_source, __file__ + "::checksum-verified-cleanup", "exec"), globals())


def handoff():
    drive, queue, receipt = map(base.load, (DRIVE, QUEUE, RECEIPT))
    release = base.load(current.RELEASE)
    candidate = release["candidate_sha256"]
    assert candidate == drive["sha256"] == queue["candidate_sha256"] == receipt["candidate_sha256"]
    for proof in (DRIVE, QUEUE, RECEIPT):
        target = CHECKPOINT_DIR / proof.name
        if not target.exists():
            copyfile(proof, target)
        assert base.digest(target) == base.digest(proof)
    open_wraps = sum("reviewed" not in row for row in queue["records"])
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{current.CHECKPOINT} [Checkpoint]({current.DOC.name})\n\n"
    section = (stub + f"""Eight complete Rafael exchanges reconcile 401 exact source/current texts. The ledger carries forward 387 approved decisions and records twelve wording changes and two wrap-only fixes. Thirteen scan leads and Jam's separate “True story” finding are addressed. Fifteen native pages pass, including Rafael's intact full name at default and maximum widths. The 31 retained speakerless commands and 29 names or roles have exact checks. Fresh initialized emulator replays verified 15 holds, including the transition into Eirene's reply. The ordinary triggers and handheld display remain open. [Exact review](../{current.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. The cumulative release passed its cold boot, 17 focused tests and an exact clean-input round trip. Cleanup reclaimed {receipt['reclaimed_bytes']:,} bytes of exact duplicates. [Latest testing build]({drive["url"]}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(CHECKPOINT_DIR / RECEIPT.name).as_posix()})

The refreshed scan has {open_wraps} open wrap leads. Continue the full contextual review, ordinary town and random gameplay coverage, and the 276 shared display leads. Preserve the 27,700 historical credits, separate artwork work and later older-record technical re-audit. [Current wrap queue](../{(CHECKPOINT_DIR / QUEUE.name).as_posix()})

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = current.DOC.with_name(name)
        old = path.read_bytes()
        if not old.startswith(section):
            assert old.startswith(stub.encode())
            base.replace_checked(path, section + old.removeprefix(stub.encode()))
    print(f"Retained {open_wraps} open scan leads. Reclaimed {receipt['reclaimed_bytes']:,} duplicate bytes.")


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        cleanup()
    handoff()
