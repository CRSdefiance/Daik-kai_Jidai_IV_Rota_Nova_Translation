"""Clean redundant Istanbul checkpoint intermediates and record retained evidence."""

from inspect import getsource

from scripts import cleanup_osaka_glass_20261122 as previous
from scripts import register_istanbul_tobacco_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
old_focus = getsource(previous.cleanup)
producer = checked_text(old_focus, {
    "focused, boot, visual = map(base.load,": "focused, boot, visual, normal = map(base.load,",
    "DRIVE, stage.LIVE,": "DRIVE, release.replay.LIVE,",
    "release.STARTUP.name, release.VISUAL))": "release.STARTUP.name, release.VISUAL, release.replay.NORMAL))",
    'folder = stage.ROOT / f"route{route}"': 'folder = release.replay.ROOT / f"route{route}"',
    '    assert all(base.digest(p) == h for p, h in retained.items())\n    keep =': '''    capture_reports.append((stage.VOYAGE/"capture/capture_report.json",normal["candidate_sha256"]))
    for row in [*(s["observed"] for s in normal["exact_complete_panels"]),normal["exit"]]:
        retained[Path(row["path"])] = row["PNG_sha256"]
    for row in normal["moments"].values():
        retained[Path(row["path"])] = row["sha256"]
    initial = stage.VOYAGE / "editorial"
    original_proof = base.load(initial / "stored_proof.json")
    original_rom = initial / "Istanbul_Tobacco_Lil_STAGED.nds"
    retained[original_rom] = original_proof["candidate_sha256"]
    for path, sha in (
        (initial / "startup/capture/capture_report.json", original_proof["candidate_sha256"]),
        (initial / "focused/route2/capture/capture_report.json",
         base.load(initial / "focused/route2/fixture.json")["sha256"]),
    ):
        report = base.load(path)
        assert report["ROM_sha256"] == sha
        capture_reports.append((path,sha))
        receipt = report["frames_captured"][-1]
        retained[Path(receipt["path"])] = receipt["PNG_sha256"]
        if entry := report.get("read_only_RAM_snapshot"):
            retained[Path(entry["path"])] = entry["sha256"]
    assert all(base.digest(p) == h for p, h in retained.items())
    keep =''',
    'discard = {stage.REBUILT: candidate, stage.PATCH: patch}': '''discard = {stage.REBUILT: candidate, stage.PATCH: patch,
        initial/"clean_rebuilt.nds": original_proof["candidate_sha256"]}''',
    'release_stack_with_osaka_glass.json': 'release_stack_with_istanbul_tobacco.json',
    '    roots = stage.ROOT.resolve(), release.ROOT.resolve()': '''        for row in report.get("read_only_pause_RAM_snapshots", ()):
            child = Path(row["path"])
            assert child.resolve().parent == path.parent.resolve() and row["read_only_export"]
            if child.resolve() not in keep:
                discard[child] = row["sha256"]
    roots = stage.VOYAGE.resolve(), release.ROOT.resolve()''',
    '{".nds", ".xdelta", ".json", ".png", ".dsv"}': '{".nds", ".xdelta", ".json", ".png", ".dsv", ".bin"}',
})
scope = vars(previous) | globals()
exec(compile(producer,__file__+"::scoped-duplicates","exec"),scope)


def handoff(result):
    drive = base.load(DRIVE)
    assert drive["sha256"] == result["candidate_sha256"]
    head = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The Istanbul pass revisited 32 clean Japanese and installed English pairs. Two Lil replies now sound more conversational and keep the full expression of interest together. The other 30 turns retain their wording with individual reasons. [Exact decisions and coverage](../{release.REVIEW.as_posix()})

The original event triggered on August 12 after normal Inn stays, showing all eight Hodram panels and their return to the Square. Hodram's archive is byte-identical in the successor. The initialized Lil replay verified all eight panels with the revised lines. Natural activation on Lil's route and hardware remain unvisited. [Emulator and native evidence](../{release.VERIFY.as_posix()})

The Drive folder's sole .nds matched the registered SHA-256 {drive['sha256']}. The clean-input patch reconstructed it exactly. Startup, 17 tests and the original speaker-control checks passed with all 114 accepted layers and the ASCII right-bound correction. Cleanup removed {len(result['removed'])} files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

Continue with remaining practical town and random events, conditional role and custom names, and the remaining player-facing prose. The 276 alternate display entries retain their earlier evidence. Deferred graphics and the later older-record technical audit remain separate.

""".encode("utf-8")
    for name in ("editorial_handoff_current.md","translation_progress.md"):
        path = release.DOC.with_name(name)
        body = path.read_bytes()
        second = body.index(b"# Current editorial checkpoint", 1)
        base.replace_checked(path,head+body[second:])


if __name__ == "__main__":
    handoff(scope["cleanup"]())

