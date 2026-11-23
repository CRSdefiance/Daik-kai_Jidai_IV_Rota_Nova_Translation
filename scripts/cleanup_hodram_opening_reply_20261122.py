"""Clear verified redundant files after the Hodram dialogue checkpoint."""

from inspect import getsource
from pathlib import Path

from scripts import cleanup_osaka_glass_20261122 as precedent
from scripts import register_hodram_opening_reply_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE, RECEIPT = [release.ROOT/name for name in ("drive_latest_build_receipt.json","checkpoint_cleanup.json")]
original = getsource(precedent.cleanup)
fixture_branch = original[original.index('    for route, case in focused["cases"].items():'):
    original.index('    assert all(base.digest(p) == h for p, h in retained.items())')]
producer = checked_text(original,{
    "DRIVE, stage.LIVE,": "DRIVE, release.live.LIVE,",
    fixture_branch:'''    for hold in focused["observed"]:
        frame = hold["frame"]
        retained[Path(frame["path"])] = frame["PNG_sha256"]
    capture_reports.append((stage.REPORT,candidate))
    for path, sha in focused["evidence"].items():
        retained[Path(path)] = sha
    native = base.load(release.DISPLAY)
    retained.update({Path(p):h for p,h in native["sheets"].items()})
''',
    "release_stack_with_osaka_glass.json": "release_stack_with_hodram_opening_reply.json",
})
scope = vars(precedent) | globals()
exec(compile(producer,__file__+"::cleanup","exec"),scope)


def handoff(result):
    drive = base.load(DRIVE)
    assert drive["sha256"] == result["candidate_sha256"]
    intro = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The registered review has all 15 clean Japanese, prior English and installed references. Hodram's reply keeps his wording and the comparison now reads on one line. The brief “Anyway...” marks his turn to the reward policy. Two prose revisions clarify how the state pays naval rewards and restore the urgency of investigating the reported Hanseatic incursion. The three revised pages passed offline native checks and matched the full body masks during a normal Hodram New Game. The replay also shows the intact custom surname in Charles's lead-in. [Coverage ledger](../{release.REVIEW.as_posix()}) · [Ordinary replay](../{(release.VERIFY / release.display.SHEET.name).as_posix()})

The sole Drive .nds matches registered SHA-256 {drive['sha256']}. The clean-input patch reconstructs it byte for byte. Startup and 17 regression tests passed. Cleanup reclaimed {result['reclaimed_bytes']:,} bytes from {len(result['removed'])} redundant files. [Latest testing ROM]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

Carry the 27,700 credited records forward and continue with practical shared and conditional scenes, speaker names and remaining player-facing text. Keep the 276 alternate display paths in scope and preserve the separate artwork and older-record technical audit work.

""".encode("utf-8")
    for name in ("editorial_handoff_current.md","translation_progress.md"):
        path = release.DOC.with_name(name)
        body = path.read_bytes()
        boundary = body.index(b"# Current editorial checkpoint",1)
        base.replace_checked(path,intro+body[boundary:])


if __name__=="__main__":
    handoff(scope["cleanup"]())
