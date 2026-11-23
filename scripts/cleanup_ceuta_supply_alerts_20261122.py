"""Remove verified redundant Ceuta replay artifacts and publish the editorial checkpoint."""

from inspect import getsource

from scripts import cleanup_osaka_glass_20261122 as previous
from scripts import register_ceuta_supply_alerts_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base,stage = release.base,release.stage
DRIVE = release.ROOT/"drive_latest_build_receipt.json"
RECEIPT = release.ROOT/"checkpoint_cleanup.json"

old = getsource(previous.cleanup)
focused = old[old.index('    for route, case in focused["cases"].items():'):old.index('    assert all(base.digest(p) == h for p, h in retained.items())')]
producer = checked_text(old,{
    "DRIVE, stage.LIVE,":"DRIVE, release.playback.LIVE,",
    focused:'''    for row in focused["ordinary_alerts"]:
        for side in ("before","after"):
            proof = row[side]["capture"]
            retained[Path(proof["path"])] = proof["PNG_sha256"]
    for row in focused["matched_control_frames"]:
        retained[Path(row["path"])] = row["PNG_sha256"]
    capture_reports.extend(((release.playback.BASELINE,meta["predecessor"]["candidate_sha256"]),
                            (release.playback.REPORT,candidate)))
    controls = {row["frame"] for row in focused["matched_control_frames"]}
    for path, sha in capture_reports[1:]:
        report = base.load(path)
        assert report["ROM_sha256"]==sha
        snapshot = report["read_only_RAM_snapshot"]
        assert snapshot["read_only_export"]
        retained[Path(snapshot["path"])] = snapshot["sha256"]
        retained[path] = base.digest(path)
        for row in report["frames_captured"]:
            if row["frame"] in controls and row["path"].endswith("_cold_boot.png"):
                retained[Path(row["path"])] = row["PNG_sha256"]
''',
    'release_stack_with_osaka_glass.json':'release_stack_with_ceuta_supply_alerts.json',
    'roots = stage.ROOT.resolve(), release.ROOT.resolve()':'roots = stage.voyage.ROOT.resolve(), release.ROOT.resolve()',
})
scope = vars(previous)|globals()
exec(compile(producer,__file__+"::scoped-checkpoint-duplicates","exec"),scope)


def update_handoff(result):
    drive=base.load(DRIVE)
    assert drive["sha256"]==result["candidate_sha256"]
    section=f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The supply pass revisited 13 records, restored one younger sailor's stammer and justified 12 template retentions. Twelve dialogue templates now receive lowercase water or food in their original substitution slots. The game still uses its title-case resource labels where they are called for. [Exact Japanese and current references](../{release.REVIEW.as_posix()})

The original Ceuta voyage inputs brought up Charles's two shortage alerts naturally. Paired replays checked both complete dialogue bodies, his nameplate and the return to sailing. The other voices and travel cancellation received offline native checks. The older sea-foam encounter did not appear on this replay. [Gameplay and native layouts](../{release.VERIFY.as_posix()})

The sole .nds in the Rota Nova Translation Drive folder matches SHA-256 {drive['sha256']}. The clean-input patch rebuilt it exactly. Startup and 17 focused tests passed, with 114 accepted layers and the ASCII right-bound correction preserved. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

Continue with the remaining practical town and random events, names and unsampled player-facing prose. Keep the 276 alternate display leads, artwork work and the later older-record technical audit in their documented scopes.

""".encode("utf-8")
    for name in ("editorial_handoff_current.md","translation_progress.md"):
        path=release.DOC.with_name(name)
        body=path.read_bytes()
        second=body.index(b"# Current editorial checkpoint",1)
        base.replace_checked(path,section+body[second:])


if __name__=="__main__":
    update_handoff(scope["cleanup"]())

