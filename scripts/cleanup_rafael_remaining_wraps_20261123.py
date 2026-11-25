"""Archive the wrap queue and clean exact duplicates after Drive verification."""

from shutil import copyfile

from scripts import cleanup_rafael_mediterranean_followups_20261123 as prior
from scripts import register_rafael_remaining_wraps_20261123 as current
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

cleanup_source = checked_text(prior.cleanup_source, {
    "    allowed = {stage.ROOT.resolve()}":
        '    prototype = stage.BATCH.parent / "final/staged"\n'
        '    prototype_digest = base.load(prototype / stage.PROOF.name)["candidate_sha256"]\n'
        '    prototype_rom = prototype / stage.ROM.name\n'
        '    assert base.digest(prototype_rom) == prototype_digest != candidate\n'
        '    assert str(prototype_rom.resolve()) in pins\n'
        '    retired += ((prototype / stage.REBUILT.name, prototype_rom, prototype_digest),)\n'
        '    allowed = {stage.ROOT.resolve(), prototype.resolve()}',
})
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
    remaining = [row for row in queue["records"] if "reviewed" not in row]
    assert len(remaining) == 88 and all(row["file_path"] == "/data/SC1.DK4" for row in remaining)
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{current.CHECKPOINT} [Checkpoint]({current.DOC.name})\n\n"
    section = (stub + f"""The clean-Japanese pass reconciles 335 records across seventeen complete Rafael exchanges. The ledger carries forward 316 exact decisions and records eighteen wording changes and one wrap-only fix. All nineteen revised pages, four retained speakerless commands and 24 nameplates passed native checks. A focused emulator replay verified twenty holds, including the book and curse exchange. The ordinary triggers and handheld display remain open. [Exact review](../{current.REVIEW.as_posix()})

The only .nds on Drive matches SHA-256 {candidate}. The cumulative release passed its cold boot, 17 focused tests and a byte-exact clean-input round trip. Cleanup reclaimed {receipt['reclaimed_bytes']:,} bytes of exact duplicates. [Latest testing build]({drive["url"]}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(CHECKPOINT_DIR / RECEIPT.name).as_posix()})

All 88 open scan leads are in Hodram's route. Two separate visual findings remain for Rafael. In B228 R0031, “On Avalon” still crosses a line boundary. In B234 R0035, the adjoining rows split “in the final sea battle.” Keep the full contextual review, ordinary town and random gameplay, the 276 shared display leads, and the 27,700 historical credits in scope. Artwork and the later older-record technical re-audit remain separate. [Current wrap queue](../{(CHECKPOINT_DIR / QUEUE.name).as_posix()})

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = current.DOC.with_name(name)
        old = path.read_bytes()
        if not old.startswith(section):
            assert old.startswith(stub.encode())
            base.replace_checked(path, section + old.removeprefix(stub.encode()))
    print(f"Retained all {len(remaining)} open Hodram scan leads. Reclaimed {receipt['reclaimed_bytes']:,} duplicate bytes.")


if __name__ == "__main__":
    if not QUEUE.exists():
        queue_scope["main"]()
    if not RECEIPT.exists():
        cleanup()
    handoff()
