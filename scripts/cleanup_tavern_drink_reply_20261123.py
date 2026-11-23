"""Seal the Tavern checkpoint after the new Drive copy passes readback."""

from pathlib import Path
from types import FunctionType

from scripts import cleanup_title_reports_label_20261123 as prior
from scripts import register_tavern_drink_reply_20261123 as current


base = current.base
DRIVE = current.ROOT / "drive_latest_build_receipt.json"
RECEIPT = current.ROOT / "checkpoint_cleanup.json"
CLEANUP_PLAN = current.ROOT / "checkpoint_cleanup_plan.json"
OUTPUT = Path("translations/editorial_checkpoints/tavern_drink_reply_20261123")
cleanup = FunctionType(prior.cleanup.__code__, vars(prior) | dict(
    current=current, stage=current.stage, DRIVE=DRIVE, RECEIPT=RECEIPT, CLEANUP_PLAN=CLEANUP_PLAN))


def handoff():
    release, drive, receipt = map(base.load, (current.RELEASE, DRIVE, RECEIPT))
    candidate = release["candidate_sha256"]
    assert candidate == drive["sha256"] == receipt["candidate_sha256"]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for record in (DRIVE, RECEIPT):
        target = OUTPUT / record.name
        if not target.exists():
            target.write_bytes(record.read_bytes())
        assert base.digest(record) == base.digest(target)
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{current.CHECKPOINT} [Checkpoint]({current.DOC.name})\n\n"
    section = (stub + f"""Faticia's teasing answer now fits on one row. Ordinary Istanbul replays verified the refusal, ten retained Tavern lines, the matching drink prompt and the return to town. The same visits covered accepting the drink, the toast and the Ragusa rumor. An ordinary Syracuse replay verified the sailing estimate and departure notice. That replay ended at sea with the village still unvisited. [Exact source and display review](../{current.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Cold startup, all 17 focused tests and exact clean-input reconstruction passed. Cleanup removed {len(receipt['removed'])} checked redundant build paths. [Latest testing build]({drive['url']}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(OUTPUT / RECEIPT.name).as_posix()})

All four story archives and the 276 pending shared bodies match the predecessor. The fleet-debt and exhibition warning drafts still await a verified display owner. Other town and random variants and handheld testing remain open. [Shared inventory](../{current.REVIEW.as_posix()})

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = current.DOC.with_name(name)
        old = path.read_bytes()
        if not old.startswith(section):
            assert old.startswith(stub.encode())
            base.replace_checked(path, section + old.removeprefix(stub.encode()))
    print(f"Verified {candidate} and cleared {len(receipt['removed'])} redundant build paths.")


if __name__ == "__main__":
    if not RECEIPT.exists():
        cleanup()
    handoff()
