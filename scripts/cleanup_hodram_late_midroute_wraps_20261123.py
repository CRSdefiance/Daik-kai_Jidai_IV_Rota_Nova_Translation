"""Advance the Hodram checkpoint after Drive readback and verified duplicate cleanup."""

from shutil import copyfile

from scripts import cleanup_rafael_remaining_wraps_20261123 as prior
from scripts import register_hodram_late_midroute_wraps_20261123 as current
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = current.base, current.stage
QUEUE = stage.BATCH / "current_wrap_queue.json"
CHECKPOINT_DIR = stage.paired.OUTPUT.parent
DRIVE = current.ROOT / "drive_latest_build_receipt.json"
RECEIPT = current.ROOT / "checkpoint_cleanup.json"
CLEANUP_PLAN = current.ROOT / "checkpoint_cleanup_plan.json"
REVIEW_COUNT = prior.REVIEW_COUNT + 1
all_reviews = "(" + ", ".join("current" + ".parent" * depth + ".REVIEW"
                             for depth in range(REVIEW_COUNT - 1, -1, -1)) + ")"
contents = checked_text(prior.contents, {prior.all_reviews: all_reviews})
queue_scope = prior.queue_scope | dict(current=current, OUTPUT=QUEUE)
exec(compile(contents, __file__ + "::current-wrap-queue", "exec"), queue_scope)
exec(compile(prior.prior.cleanup_source, __file__ + "::checksum-verified-cleanup", "exec"), globals())


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
    section = (stub + f"""The clean-Japanese pass covered 496 records in 15 Hodram exchanges. It produced 24 wording revisions, one wrap-only revision, 469 justified speech or panel retentions, and two retained choice captions. Native checks verified 25 revised pages, 50 speakerless commands and 24 names or roles. Focused emulator runs verified 39 holds, both choices in Cesare's ship lesson and the two-page buying explanation. Ordinary activation and handheld testing remain open for these scenes. [Exact review](../{current.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Cold boot, 17 focused tests and byte-exact clean-input patch reconstruction passed. Cleanup reclaimed {receipt['reclaimed_bytes']:,} bytes of exact duplicates. [Latest testing build]({drive["url"]}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(CHECKPOINT_DIR / RECEIPT.name).as_posix()})

The refreshed scan has {len(remaining)} open leads. Cesare's B167 R0122 wrap is a separate gameplay finding. The first page has four lines with spare width, including successive breaks after “deals” and “towns.” Retain the rule about early trade routes, the one-percent share and the one-to-five-unit limit while reflowing it. Carry forward Rafael's B228 R0031 “On Avalon” and B234 R0035 “in the final sea battle” visual leads. Keep the contextual review, ordinary town and random gameplay, 276 shared display leads and 27,700 historical credits in scope. Artwork and the older-record technical re-audit remain separate. [Current wrap queue](../{(CHECKPOINT_DIR / QUEUE.name).as_posix()}) · [Cesare's two-page capture](../{(current.VERIFY / 'hodram_late_midroute_menus_1.png').as_posix()})

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
