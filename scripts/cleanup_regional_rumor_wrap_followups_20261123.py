"""Seal the regional rumor checkpoint after verifying the Drive readback."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_rafael_mediterranean_followups_20261123 as prior
from scripts import register_regional_rumor_wrap_followups_20261123 as current


base, stage = current.base, current.stage
DRIVE = current.ROOT / "drive_latest_build_receipt.json"
RECEIPT = current.ROOT / "checkpoint_cleanup.json"
CLEANUP_PLAN = current.ROOT / "checkpoint_cleanup_plan.json"
OUTPUT = Path("translations/editorial_checkpoints/regional_rumor_wrap_followups_20261123")
exec(compile(prior.cleanup_source, __file__ + "::checkpoint-cleanup", "exec"), globals())


def handoff():
    release, review, drive, receipt = map(base.load, (current.RELEASE, current.REVIEW, DRIVE, RECEIPT))
    candidate = release["candidate_sha256"]
    assert candidate == review["candidate_sha256"] == drive["sha256"] == receipt["candidate_sha256"]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for source in (DRIVE, RECEIPT):
        target = OUTPUT / source.name
        if not target.exists():
            copyfile(source, target)
        assert base.digest(source) == base.digest(target)
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{current.CHECKPOINT} [Checkpoint]({current.DOC.name})\n\n"
    section = (stub + f"""Ordinary visits to Tunis, Valencia and Syracuse verified 19 dialogue holds across nine COMMON records. The Seoul visit naturally triggered Yifa's recruitment and verified Yukihisa's “Taoist arts?” panel. The repeated Delicacy Shop rows in Tunis also appear in the clean Japanese build. The Valencia and Syracuse rumor revisions passed fresh ordinary gameplay, including the Shopkeeper nameplates and return to the Square. The other 19 regional rumors retain their wording with individual reasons. [Ordinary visit evidence](../{current.DISCOVERY.as_posix()}) · [Installed review](../{current.REVIEW.as_posix()})

The only .nds on Drive matches SHA-256 {candidate}. Startup, all 17 focused tests and byte-exact clean-input reconstruction passed. Cleanup reclaimed {receipt['reclaimed_bytes']:,} bytes of verified intermediates. [Latest testing build]({drive['url']}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(OUTPUT / RECEIPT.name).as_posix()})

The current four-route census binds 24,092 credited clean-source positions through 51 registered updates. This release preserves all four verified story archives, so the zero-open storyline wrap scan still applies. The 276 pending shared bodies also match exactly. Continue display ownership, representative ordinary town and random gameplay, and final inventory reconciliation. The first shared follow-ups remain the 27 legacy entries and eight scene labels without an association. Graphics artwork and the older-record technical re-audit remain separate. [Route audit](../{current.routes.OUT.as_posix()}) · [Shared priority list](../translations/editorial_checkpoints/shared_display_20261123/binding_after_hodram_20261123.json)

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = current.DOC.with_name(name)
        old = path.read_bytes()
        if not old.startswith(section):
            assert old.startswith(stub.encode())
            base.replace_checked(path, section + old.removeprefix(stub.encode()))
    print(f"Sealed {candidate} and reclaimed {receipt['reclaimed_bytes']:,} bytes.")


if __name__ == "__main__":
    if not RECEIPT.exists():
        cleanup()
    handoff()
