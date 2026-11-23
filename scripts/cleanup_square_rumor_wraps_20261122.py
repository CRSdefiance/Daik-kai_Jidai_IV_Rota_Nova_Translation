"""Remove redundant checkpoint data after the Square rumor wrap release."""

from inspect import getsource
from pathlib import Path

from scripts import cleanup_osaka_glass_20261122 as precedent
from scripts import register_square_rumor_wraps_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base,stage = release.base,release.stage
DRIVE,RECEIPT = [release.ROOT/name for name in ("drive_latest_build_receipt.json","checkpoint_cleanup.json")]
original=getsource(precedent.cleanup)
fixture_branch=original[original.index('    for route, case in focused["cases"].items():'):
    original.index('    assert all(base.digest(p) == h for p, h in retained.items())')]
producer=checked_text(original,{
    "DRIVE, stage.LIVE,":"DRIVE, release.live.LIVE,",
    fixture_branch:'''    for region, case in focused["cases"].items():
        report = Path(case["report"])
        capture_reports.append((report,candidate))
        retained[report] = base.digest(report)
        earlier = stage.ROOT / f"region{region}" / "capture/capture_report.json"
        if earlier.exists():
            initial = base.load(earlier)
            old_hold, = (row for row in initial["frames_captured"] if row["frame"] == 5900)
            old_ram, = (row for row in initial["read_only_capture_RAM_snapshots"] if row["frame"] == 5900)
            retained[Path(old_hold["path"])] = old_hold["PNG_sha256"]
            retained[Path(old_ram["path"])] = old_ram["sha256"]
            retained[earlier] = base.digest(earlier)
            capture_reports.append((earlier,candidate))
    for path, sha in focused["evidence"].items():
        retained[Path(path)] = sha
    retained.update({Path(p):h for p,h in base.load(stage.PROOF)["sheets"].items()})
''',
    "release_stack_with_osaka_glass.json":"release_stack_with_square_rumor_wraps.json",
    '    roots = stage.ROOT.resolve(), release.ROOT.resolve()':'''        for kind in ("read_only_capture_RAM_snapshots","read_only_pause_RAM_snapshots"):
            for row in report.get(kind,()):
                child=Path(row["path"])
                assert child.resolve().parent==path.parent.resolve() and row["read_only_export"]
                if child.resolve() not in keep:
                    discard[child]=row["sha256"]
        if battery and Path(battery["source"]).name=="disposable_hodram_istanbul.dsv":
            disposable = Path(battery["source"])
            assert disposable.resolve().parent==path.parent.parent.resolve()
            _,_,authored_save = stage.play.history(0)
            assert base.digest(authored_save)==base.digest(disposable)==battery["source_sha256"]
            discard[disposable]=battery["source_sha256"]
    roots = stage.ROOT.resolve(), release.ROOT.resolve()''',
    '{".nds", ".xdelta", ".json", ".png", ".dsv"}':'{".nds", ".xdelta", ".json", ".png", ".dsv", ".bin"}',
})
scope=vars(precedent) | globals()
exec(compile(producer,__file__+"::cleanup","exec"),scope)


def handoff(result):
    drive=base.load(DRIVE)
    assert drive["sha256"]==result["candidate_sha256"]
    intro=f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

COMMON 710 now keeps “Times certainly have changed!” on its own line. COMMON 713 keeps “in the Indian Ocean” together. Both retain their approved dialogue and original portrait. The native formatter comparison kept 51 neighboring controls exact. Two focused Square runs used ordinary menu inputs on a copied Istanbul save with the region and random seed set explicitly. Both full pages and menu returns were verified. The shop list also confirmed the complete Gem Shop caption from the preceding release. [Exact source, current and display evidence](../{release.REVIEW.as_posix()})

The sole Drive .nds matches registered SHA-256 {drive['sha256']}. The clean-input patch rebuilds it byte for byte. Startup and 17 regression tests passed. Cleanup reclaimed {result['reclaimed_bytes']:,} bytes from {len(result['removed'])} redundant files. [Latest testing ROM]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

Continue with remaining shared, random and conditional scenes, speaker names and player-facing prose. Carry forward the existing 27,700 credited records and 276 alternate display leads. Graphics artwork and the older-record technical re-audit remain separate.

""".encode("utf-8")
    for name in ("editorial_handoff_current.md","translation_progress.md"):
        path=release.DOC.with_name(name)
        body=path.read_bytes()
        boundary=body.index(b"# Current editorial checkpoint",1)
        base.replace_checked(path,intro+body[boundary:])


if __name__=="__main__":
    handoff(scope["cleanup"]())
