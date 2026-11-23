"""Remove redundant editor replay files while retaining both defects' witnesses."""

from inspect import getsource

from scripts import cleanup_osaka_glass_20261122 as previous
from scripts import register_captain_name_delete_20261122 as release
from scripts.source_locked_derivation_v5118 import checked_text


base,stage=release.base,release.stage
DRIVE=release.ROOT/"drive_latest_build_receipt.json"
RECEIPT=release.ROOT/"checkpoint_cleanup.json"
old=getsource(previous.cleanup)
focused=old[old.index('    for route, case in focused["cases"].items():'):old.index('    assert all(base.digest(p) == h for p, h in retained.items())')]
producer=checked_text(old,{
    "DRIVE, stage.LIVE,":"DRIVE, release.live.LIVE,",
    focused:'''    defect=base.load(release.DISPLAY)
    assert defect["candidate_sha256"]==meta["predecessor"]["candidate_sha256"]
    witnessed=[side["evidence"] for row in focused["editable_results"] for side in (row["before"],row["after"])]
    witnessed += [row["evidence"] for row in focused["confirmation"]]
    witnessed += [defect[name] for name in ("first_page","incorrect_extra_page","correct_literal_nameplate")]
    for witness in witnessed:
        frame = witness["image"]
        snapshot = witness["read_only_RAM"]
        retained[Path(frame["path"])] = frame["PNG_sha256"]
        retained[Path(snapshot["path"])] = snapshot["sha256"]
    first = stage.BASELINE
    replay = release.played.replay.REPORT
    capture_reports.extend(((first,defect["candidate_sha256"]),(replay,candidate)))
    for path, sha in capture_reports[1:]:
        report = base.load(path)
        assert report["ROM_sha256"]==sha
        retained[path]=base.digest(path)
        for row in report.get("frames_captured",()):
            if row["frame"] in (2050,2790,15220,28520):
                retained[Path(row["path"])]=row["PNG_sha256"]
        if raw:=report.get("read_only_RAM_snapshot"):
            assert raw["read_only_export"]
            retained[Path(raw["path"])]=raw["sha256"]
''',
    'release_stack_with_osaka_glass.json':'release_stack_with_captain_name_delete.json',
    '    roots = stage.ROOT.resolve(), release.ROOT.resolve()':'''        for key in ("read_only_pause_RAM_snapshots","read_only_capture_RAM_snapshots"):
            for row in report.get(key,()):
                child=Path(row["path"])
                assert child.resolve().parent==path.parent.resolve() and row["read_only_export"]
                if child.resolve() not in keep:
                    discard[child]=row["sha256"]
    roots = stage.run.ROOT.resolve(), release.ROOT.resolve()''',
    '{".nds", ".xdelta", ".json", ".png", ".dsv"}':'{".nds", ".xdelta", ".json", ".png", ".dsv", ".bin"}',
})
scope=vars(previous)|globals()
exec(compile(producer,__file__+"::scoped-duplicates","exec"),scope)


def update_handoff(result):
    drive=base.load(DRIVE)
    assert drive["sha256"]==result["candidate_sha256"]
    n=release.native_count()
    top=f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

An ordinary Hodram New Game reached the 16-letter first-name limit, rejected an extra key, reproduced the two-letter deletion and verified the one-character correction. The replay accepted all four customized fields. The isolated matrix checked {n} character-width and cursor cases, with the village and other keyboard providers matching stock behavior. [Editor comparison](../{(release.VERIFY / release.played.SHEET.name).as_posix()})

The ordinary opening exposed a separate defect in SC1 B42 R0113. Charles's original line passes a custom surname through FA. The first expansion is exact, but the visible panel substitutes the literal FI, FA and FO sequences inside that surname, adding an unwanted page. Hodram's own nameplate spells the same custom name correctly. Start the next display correction from the exact held body and original voice and transition. The source-bound progressive path first expands at ARM9 020242C8, presents the resulting buffer at 020242F0, and reaches the separate portrait preparation call at 02054160. Qualify the affected caller before changing any shared consumer. [Exact surname defect, original source and captured name fields](../{(release.VERIFY / release.DISPLAY.name).as_posix()})

The sole Drive .nds matches registered SHA-256 {drive['sha256']}. The clean-input patch rebuilt it exactly. Startup and 17 regressions passed, preserving all 114 accepted layers and the ASCII right-bound correction. Cleanup removed {len(result['removed'])} files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) · [Patch](../{release.PATCH.as_posix()}) · [Cleanup receipt](../{RECEIPT.as_posix()})

The remaining shared town and random encounters, conditional name and role paths, other player-facing prose and 276 alternate display leads stay in scope. Deferred graphics and the older-record technical re-audit retain their separate work.

""".encode("utf-8")
    for name in ("editorial_handoff_current.md","translation_progress.md"):
        path=release.DOC.with_name(name)
        body=path.read_bytes()
        second=body.index(b"# Current editorial checkpoint",1)
        base.replace_checked(path,top+body[second:])


if __name__=="__main__":
    update_handoff(scope["cleanup"]())

