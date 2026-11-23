"""Record the Drive readback and remove verified build intermediates."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_rafael_mediterranean_followups_20261123 as prior
from scripts import register_square_and_market_reward_wraps_20261123 as current
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = current.base, current.stage
DRIVE = current.ROOT / "drive_latest_build_receipt.json"
RECEIPT = current.ROOT / "checkpoint_cleanup.json"
CLEANUP_PLAN = current.ROOT / "checkpoint_cleanup_plan.json"
OUTPUT = Path("translations/editorial_checkpoints/square_and_market_reward_wraps_20261123")

source = checked_text(prior.cleanup_source, {
    'reclaimed_bytes=sum(row["bytes"] for row in removed)':
        'removed_entry_bytes=sum(row["bytes"] for row in removed), accounting="Logical sizes include a hardlinked ROM."',
})
exec(compile(source, __file__ + "::cleanup", "exec"), globals())


def handoff():
    release, drive, receipt = map(base.load, (current.RELEASE, DRIVE, RECEIPT))
    candidate = release["candidate_sha256"]
    assert candidate == drive["sha256"] == receipt["candidate_sha256"]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for record in (DRIVE, RECEIPT):
        target = OUTPUT / record.name
        if not target.exists():
            copyfile(record, target)
        assert base.digest(record) == base.digest(target)
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{current.CHECKPOINT} [Checkpoint]({current.DOC.name})\n\n"
    section = (stub + f"""The Square pitch now fits on one row, and the Market recommendation puts the letter and the thank-you on separate complete rows. The source review reconciles 27 shared records and records 25 individually justified retentions. Native formatting and paired emulator fixtures verified both revised pages, five retained holds and three transition frames. Ordinary activation and handheld testing remain open for these branches. [Exact review](../{current.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Cold startup, 17 focused tests and exact clean-input reconstruction passed. Cleanup removed {len(receipt['removed'])} verified redundant build paths. [Latest testing build]({drive['url']}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(OUTPUT / RECEIPT.name).as_posix()})

The four story archives and all 276 pending shared bodies match the predecessor. Continue verifying the remaining display owners and representative shared encounters. The fleet-debt and exhibition-warning drafts still await a verified caller. [Shared inventory](../{current.REVIEW.as_posix()})

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = current.DOC.with_name(name)
        old = path.read_bytes()
        if not old.startswith(section):
            assert old.startswith(stub.encode())
            base.replace_checked(path, section + old.removeprefix(stub.encode()))
    print(f"Sealed {candidate} and removed {len(receipt['removed'])} verified redundant build paths.")


if __name__ == "__main__":
    if not RECEIPT.exists():
        cleanup()
    handoff()
