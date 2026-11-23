"""Record the Tavern release, Drive readback and verified duplicate cleanup."""

from pathlib import Path
from shutil import copyfile

from scripts import cleanup_rafael_mediterranean_followups_20261123 as prior
from scripts import register_tavern_nearby_town_wrap_20261123 as current
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = current.base, current.stage
DRIVE = current.ROOT / "drive_latest_build_receipt.json"
RECEIPT = current.ROOT / "checkpoint_cleanup.json"
CLEANUP_PLAN = current.ROOT / "checkpoint_cleanup_plan.json"
OUTPUT = Path("translations/editorial_checkpoints/tavern_nearby_town_wrap_20261123")

cleanup_source = checked_text(prior.cleanup_source, {
    '    if not CLEANUP_PLAN.exists():': '''    for name in ("attempt_before_space_recovery", "attempt_with_hardlinked_rom"):
        interrupted = (stage.ROOT.parent / name).resolve()
        if not interrupted.is_dir():
            continue
        old_rom = interrupted / current.ROOT.name / current.ROM.name
        old_patch = interrupted / current.PACKAGE.name / current.PATCH.name
        retired += ((old_rom, current.ROM, candidate), (old_patch, current.PATCH, patch))
        for source in (old_rom, old_patch):
            assert source.parent.resolve().is_relative_to(interrupted)
            allowed.add(source.parent.resolve())
    if not CLEANUP_PLAN.exists():''',
    'reclaimed_bytes=sum(row["bytes"] for row in removed)':
        'removed_entry_bytes=sum(row["bytes"] for row in removed), accounting="Logical file sizes include hardlinked ROM paths."',
})
exec(compile(cleanup_source, __file__ + "::cleanup", "exec"), globals())


def handoff():
    release, drive, receipt = map(base.load, (current.RELEASE, DRIVE, RECEIPT))
    candidate = release["candidate_sha256"]
    assert candidate == drive["sha256"] == receipt["candidate_sha256"]
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for source in (DRIVE, RECEIPT):
        target = OUTPUT / source.name
        if not target.exists():
            copyfile(source, target)
        assert base.digest(source) == base.digest(target)
    stub = f"# Current editorial checkpoint - 2026-11-23\n\n{current.CHECKPOINT} [Checkpoint]({current.DOC.name})\n\n"
    section = (stub + f"""The barkeep’s nearby-town question now keeps the town and question mark together on the second row. The native check exercises all 90 stock towns. Two ordinary Tunis holds verified the revision. Eight other holds and four drink-menu transitions passed in Tunis and Syracuse. The review records eight individually justified retentions. [Exact review](../{current.REVIEW.as_posix()})

Four saved-game replays on the predecessor verified 17 ordinary shared panels and eight story panels from Maria’s encounter with Kurushima after Nagasaki. They also reached the rat warning and the empty shore search. Other random outcomes and conditional variants remain open. [Gameplay evidence](../{current.DISCOVERY.as_posix()})

The sole .nds on Drive matches SHA-256 {candidate}. Startup, 17 focused tests and exact clean-input reconstruction passed. Cleanup removed {len(receipt['removed'])} verified redundant paths. [Latest testing build]({drive['url']}) · [Clean-input patch](../{current.PATCH.as_posix()}) · [Cleanup receipt](../{(OUTPUT / RECEIPT.name).as_posix()})

The inventory audit binds 27,700 credited texts, including 24,092 story positions, 3,392 COMMON records, 202 Help topics and 14 ARM9 entries. It also rechecked 414 default-name getter cases and the current Julio, Trade Goods Info and Deck regression dependencies. This COMMON-only revision leaves those components and the 276 pending shared entries byte-identical. Continue the shared ownership work and representative gameplay, starting with the 35 unresolved legacy messages and scene labels. Graphics artwork and the older-record technical re-audit remain separate. [Inventory and dependency audit](../{current.audit.OUT.as_posix()})

""").encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = current.DOC.with_name(name)
        old = path.read_bytes()
        if not old.startswith(section):
            assert old.startswith(stub.encode())
            base.replace_checked(path, section + old.removeprefix(stub.encode()))
    print(f"Sealed {candidate} and removed {len(receipt['removed'])} verified redundant paths.")


if __name__ == "__main__":
    if not RECEIPT.exists():
        cleanup()
    handoff()
