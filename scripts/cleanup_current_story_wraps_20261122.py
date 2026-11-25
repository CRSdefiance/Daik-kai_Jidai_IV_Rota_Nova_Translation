"""Clear verified scratch copies and retain reproducible evidence for early story wraps."""

from inspect import getsource
from pathlib import Path

from scripts import cleanup_osaka_glass_20261122 as precedent
from scripts import register_current_story_wraps_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
original = getsource(precedent.cleanup)
fixture_branch = original[original.index('    for route, case in focused["cases"].items():'):
                          original.index('    assert all(base.digest(p) == h for p, h in retained.items())')]
producer = checked_text(original, {
    "DRIVE, stage.LIVE,": "DRIVE, release.live.LIVE,",
    "release.PACKAGE / \"checksums.json\") == release.workflow.package_checksums(release.PACKAGE)":
        "release.PACKAGE / \"checksums.json\") == release.parent.workflow.package_checksums(release.PACKAGE)",
    "release.ROM: candidate, stage.ROM: candidate, release.PATCH: patch":
        "release.ROM: candidate, release.PATCH: patch",
    'visual["sheets"].items()': 'visual.items()',
    fixture_branch:'''    setup = base.load(release.live.SETUP)
    fixture = setup["fixture_ROMs"]["after"]
    assert Path(fixture["path"]) == release.live.ROM
    retained[release.live.ROM] = fixture["sha256"]
    retained[release.live.REPORT] = focused["report_sha256"]
    retained.update({Path(r["path"]): r["sha256"] for r in focused["sheets"]})
    retained.update({Path(r["capture"]["path"]): r["capture"]["PNG_sha256"] for r in focused["observations"]})
    retained.update({Path(r["path"]): r["PNG_sha256"] for r in focused["return_frames"].values()})
    capture_reports.append((release.live.REPORT, fixture["sha256"]))
    pins = {Path(r["path"]).resolve() for r in base.load(Path("translations/rom_retention_pins.json"))}
    assert stage.ROM.resolve() not in pins and release.live.ROM.resolve() in pins
''',
    "stage.REBUILT: candidate, stage.PATCH: patch": "stage.REBUILT: candidate, stage.ROM: candidate, stage.PATCH: patch",
    "release_stack_with_osaka_glass.json": "release_stack_with_early_story_wraps.json",
})
scope = vars(precedent) | globals()
exec(compile(producer, __file__ + "::checkpoint-cleanup", "exec"), scope)


def handoff(result):
    drive = base.load(DRIVE)
    assert drive["sha256"] == result["candidate_sha256"]
    section = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The 11 exchanges contain 72 contextual decisions with 59 justified retentions, 11 wrap corrections and two wording revisions. Fifteen native pages passed, including both long-name variants, and six panels played in an initialized Maria scene. Nine revised prompts still have offline evidence only. The scan flagged 423 possible wrap leads across 19,721 ASCII bodies, including the resolved subset. [Exact source and current references](../{release.REVIEW.as_posix()}) · [Triage](../{stage.review.TRIAGE.as_posix()})

The sole .nds in the Drive folder matches SHA-256 {drive['sha256']}. The clean-input patch reconstructs it byte for byte. Startup and 17 regression tests passed. Cleanup reclaimed {result['reclaimed_bytes']:,} bytes from {len(result['removed'])} redundant files. [Latest testing ROM]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

Continue contextual triage on the remaining story leads, shared and conditional scenes, speaker names and player-facing prose. Carry forward the 27,700 credited records and 276 alternate display leads. Keep deferred artwork and the older-record technical re-audit in their established scopes.

""".encode("utf-8")
    for name in ("editorial_handoff_current.md", "translation_progress.md"):
        path = release.DOC.with_name(name)
        body = path.read_bytes()
        boundary = body.index(b"# Current editorial checkpoint", 1)
        base.replace_checked(path, section + body[boundary:])


if __name__ == "__main__":
    handoff(scope["cleanup"]())
