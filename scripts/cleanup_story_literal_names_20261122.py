"""Remove redundant captures and reconstruction files from the story-name checkpoint."""

from inspect import getsource
from pathlib import Path

from scripts import cleanup_osaka_glass_20261122 as precedent
from scripts import register_story_literal_names_20261122 as release
from scripts import verify_story_literal_names_20261122 as observed
from scripts.source_locked_derivation_v5118 import checked_text


base, stage = release.base, release.stage
DRIVE = release.ROOT / "drive_latest_build_receipt.json"
RECEIPT = release.ROOT / "checkpoint_cleanup.json"
original = getsource(precedent.cleanup)
fixture_branch = original[original.index('    for route, case in focused["cases"].items():'):
    original.index('    assert all(base.digest(p) == h for p, h in retained.items())')]
producer = checked_text(original,{
    "DRIVE, stage.LIVE,": "DRIVE, release.live.LIVE,",
    fixture_branch:'''    retained[release.played.FOCUSED_ROM] = focused["focused_system"]["fixture"]["fixture_sha256"]
    ordinary = focused["ordinary"]
    witness = [side["evidence"] for side in ordinary["confirmation"]]
    witness += ordinary["before_story_holds"] + ordinary["fixed_story_holds"]
    witness += [focused["focused_system"][k] for k in ("screenshot","transition_to_town")]
    for row in witness:
        frame, ram = row["image"], row["read_only_RAM"]
        retained[Path(frame["path"])] = frame["PNG_sha256"]
        retained[Path(ram["path"])] = ram["sha256"]
    shas = (meta["predecessor"]["candidate_sha256"],candidate,focused["focused_system"]["fixture"]["fixture_sha256"])
    for path, sha in zip(observed.REPORTS.values(),shas,strict=True):
        capture_reports.append((path,sha))
        retained[path] = focused["evidence"][str(path)]
    for path, sha in focused["evidence"].items():
        retained[Path(path)] = sha
''',
    "release_stack_with_osaka_glass.json": "release_stack_with_story_literal_names.json",
    '    roots = stage.ROOT.resolve(), release.ROOT.resolve()':'''        for row in report.get("read_only_capture_RAM_snapshots",()):
            child = Path(row["path"])
            assert child.resolve().parent == path.parent.resolve() and row["read_only_export"]
            if child.resolve() not in keep:
                discard[child] = row["sha256"]
    roots = stage.ROOT.resolve(), release.ROOT.resolve()''',
    '{".nds", ".xdelta", ".json", ".png", ".dsv"}': '{".nds", ".xdelta", ".json", ".png", ".dsv", ".bin"}',
})
scope = vars(precedent) | globals()
exec(compile(producer,__file__+"::cleanup", "exec"),scope)


def handoff(result):
    drive = base.load(DRIVE)
    assert drive["sha256"] == result["candidate_sha256"]
    intro=f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

Paired ordinary Hodram New Games reproduced and corrected Charles's surname line in SC1 B42 R0113. The fixed panel shows all four intended lines, then proceeds straight to Hodram's reply. The original Japanese reference, accepted names, five-gate retention and display evidence are bound in the registered review. A focused original SC1 B205 system notice performed the same check for the first name. The third preparation path was checked in the isolated CPU harness. [Exact witness and coverage](../{release.REVIEW.as_posix()})

The sole .nds in the Rota Nova Translation Drive folder matches the registered SHA-256 {drive['sha256']}. The clean-input patch rebuilt the ROM byte for byte. Startup and 17 tests passed. The release carries all 114 accepted layers and the ASCII right-bound correction. Cleanup reclaimed {result['reclaimed_bytes']:,} bytes from {len(result['removed'])} redundant files. [Latest testing ROM]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

Start the next editorial checkpoint with the physical wrap of Hodram's reply in SC1 B42 R0116. The replay shows a short middle line between “Few duties” and “as giving a speech.” Check the entire exchange with the clean Japanese and preserve the original address and transition. Continue the shared and conditional scene coverage and player-facing prose from the current 27,700 credited records and 276 alternate display leads. Artwork and the older-record technical re-audit remain separate.

""".encode("utf-8")
    for name in ("editorial_handoff_current.md","translation_progress.md"):
        path = release.DOC.with_name(name)
        body = path.read_bytes()
        boundary = body.index(b"# Current editorial checkpoint",1)
        base.replace_checked(path,intro+body[boundary:])


if __name__ == "__main__":
    handoff(scope["cleanup"]())
