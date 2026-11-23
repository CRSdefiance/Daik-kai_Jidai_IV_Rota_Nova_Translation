"""Remove redundant replay and reconstruction files for the Square rumor checkpoint."""

from inspect import getsource
from pathlib import Path

from scripts import cleanup_osaka_glass_20261122 as precedent
from scripts import register_square_rumor_followup_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE, RECEIPT = [release.ROOT/name for name in ("drive_latest_build_receipt.json","checkpoint_cleanup.json")]
original = getsource(precedent.cleanup)
fixture_branch = original[original.index('    for route, case in focused["cases"].items():'):
    original.index('    assert all(base.digest(p) == h for p, h in retained.items())')]
producer = checked_text(original,{
    "DRIVE, stage.LIVE,": "DRIVE, release.live.LIVE,",
    fixture_branch:'''    for city, holds in focused["observed"].items():
        for hold in holds:
            frame = hold["frame"]
            retained[Path(frame["path"])] = frame["PNG_sha256"]
        for directory in (stage.ROOT,stage.WITNESSES):
            capture = directory / city / "capture/capture_report.json"
            capture_reports.append((capture,candidate))
            retained[capture] = base.digest(capture)
    for path, sha in focused["evidence"].items():
        retained[Path(path)] = sha
    retained.update({Path(p):h for p,h in base.load(stage.PROOF)["sheets"].items()})
''',
    "release_stack_with_osaka_glass.json": "release_stack_with_square_rumor_followup.json",
})
scope = vars(precedent) | globals()
exec(compile(producer,__file__+"::cleanup","exec"),scope)


def handoff(result):
    drive = base.load(DRIVE)
    assert drive["sha256"] == result["candidate_sha256"]
    intro = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The 21-record batch includes all original regional faction and person rumors. Ordinary Valencia and Syracuse visits verified the two revised European rumors, original Shopkeeper labels and return paths. The China rumor passed complete offline native and visual checks. The original prose for 710 and 713 remains justified, with two older line-break leads noted separately in their records. [Exact source and current ledger](../{release.REVIEW.as_posix()})

The sole Drive .nds matches registered SHA-256 {drive['sha256']}. The clean-input patch rebuilds it byte for byte. Startup and 17 regression tests passed. Cleanup reclaimed {result['reclaimed_bytes']:,} bytes from {len(result['removed'])} redundant files. [Latest testing ROM]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

Continue with practical shared and random conversations and remaining player-facing text. Carry forward 27,700 credited records, the 276 alternate display leads, original nameplate decisions and deferred artwork and older-record technical audit.

""".encode("utf-8")
    for name in ("editorial_handoff_current.md","translation_progress.md"):
        path = release.DOC.with_name(name)
        body = path.read_bytes()
        boundary = body.index(b"# Current editorial checkpoint",1)
        base.replace_checked(path,intro+body[boundary:])


if __name__=="__main__":
    handoff(scope["cleanup"]())
