"""Clear redundant files after verifying the Square shop name checkpoint."""

from inspect import getsource
from pathlib import Path

from scripts import cleanup_osaka_glass_20261122 as precedent
from scripts import register_square_shop_names_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base,stage = release.base,release.stage
DRIVE,RECEIPT = [release.ROOT/name for name in ("drive_latest_build_receipt.json","checkpoint_cleanup.json")]
original = getsource(precedent.cleanup)
fixture_branch = original[original.index('    for route, case in focused["cases"].items():'):
    original.index('    assert all(base.digest(p) == h for p, h in retained.items())')]
producer = checked_text(original,{
    "DRIVE, stage.LIVE,": "DRIVE, release.live.LIVE,",
    fixture_branch:'''    for city, observation in focused["observed"].items():
        for frame in observation["retained_frames"]:
            retained[Path(frame["path"])] = frame["PNG_sha256"]
        capture = stage.ROOT / city / "capture/capture_report.json"
        capture_reports.append((capture,candidate))
        retained[capture] = base.digest(capture)
    for path, sha in focused["evidence"].items():
        retained[Path(path)] = sha
    retained.update({Path(p):h for p,h in base.load(stage.PROOF)["sheets"].items()})
''',
    "release_stack_with_osaka_glass.json": "release_stack_with_square_shop_names.json",
})
scope = vars(precedent) | globals()
exec(compile(producer,__file__+"::cleanup","exec"),scope)


def handoff(result):
    drive = base.load(DRIVE)
    assert drive["sha256"]==result["candidate_sha256"]
    intro = f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The complete 18-caption review matches the Japanese categories and the goods each shop sells. Spice Shop and Craft Shop were observed during ordinary Syracuse and Lisbon visits. Scent Shop, Gem Shop and Dye Shop passed the same native formatter and full glyph checks offline. The original commodity category terms passed 144 independent getter comparisons. [Exact source and installed decisions](../{release.REVIEW.as_posix()})

The sole Drive .nds matches registered SHA-256 {drive['sha256']}. The clean-input patch rebuilds it byte for byte. Startup and 17 regression tests passed. Cleanup reclaimed {result['reclaimed_bytes']:,} bytes from {len(result['removed'])} redundant files. [Latest testing ROM]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

Carry forward 27,700 credited editorial records. The prior Square rumor pass leaves two known phrase breaks at COMMON 710 and 713. The current regional formatter reflows existing line feeds, so qualify a wording-preserving layout against that consumer before changing storage. Other shared and random scenes, names and remaining player-facing prose stay in scope, along with the 276 alternate display leads. Artwork and the older-record technical audit remain separate. [Exact rumor references](../{release.parent.REVIEW.as_posix()})

""".encode("utf-8")
    for name in ("editorial_handoff_current.md","translation_progress.md"):
        path = release.DOC.with_name(name)
        body = path.read_bytes()
        boundary = body.index(b"# Current editorial checkpoint",1)
        base.replace_checked(path,intro+body[boundary:])


if __name__=="__main__":
    handoff(scope["cleanup"]())
