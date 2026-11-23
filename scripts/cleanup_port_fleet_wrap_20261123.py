"""Seal the Port Fleet checkpoint after a verified Drive readback."""

from pathlib import Path
from types import FunctionType

from scripts import cleanup_title_reports_label_20261123 as prior
from scripts import register_port_fleet_wrap_20261123 as current


base = current.base
DRIVE = current.ROOT / "drive_latest_build_receipt.json"
RECEIPT = current.ROOT / "checkpoint_cleanup.json"
CLEANUP_PLAN = current.ROOT / "checkpoint_cleanup_plan.json"
OUTPUT = Path("translations/editorial_checkpoints/port_fleet_wrap_20261123")
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
    section = (stub + f"""The Port Fleet captain warning keeps its command together. Gerhard's formal refusal now addresses the admiral directly and fits on one row. The 13-entry review retains eleven other lines with individual reasons. A copied Syracuse save with supplied funds and ability verified Gerhard's refusal and three picker states. The warning passed native formatting and glyph checks offline. Ordinary activation and handheld testing remain open for this batch. [Exact source and display review](../{current.REVIEW.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Cold startup, all 17 focused tests and exact clean-input reconstruction passed. Cleanup removed {len(receipt['removed'])} checked redundant build paths. [Latest testing build]({drive['url']}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(OUTPUT / RECEIPT.name).as_posix()})

All four story archives and the 276 pending shared records match the predecessor. The Captain's Cabin order and Square free-goods confirmation are the next wrap leads. Continue representative ordinary scenes and resolve the remaining shared display paths. [Shared inventory](../{current.REVIEW.as_posix()})

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
