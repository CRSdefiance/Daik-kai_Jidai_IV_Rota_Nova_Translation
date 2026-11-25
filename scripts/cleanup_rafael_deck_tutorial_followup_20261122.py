"""Clear redundant build and replay outputs after the Deck lesson reaches Drive."""

from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path

from scripts import register_rafael_deck_tutorial_followup_20261122 as release


base,stage = release.base,release.stage
RECEIPT = release.ROOT/"checkpoint_cleanup.json"
DRIVE = release.ROOT/"drive_latest_build_receipt.json"


def cleanup():
    assert not RECEIPT.exists()
    release_proof,mutation,drive,live,startup,visual = map(base.load,(
        release.RELEASE,release.VERIFY/"registration_mutation_plan.json",DRIVE,release.live.PROOF,
        release.VERIFY/release.STARTUP.name,stage.ROOT/"visual_review.json"))
    sha,patch_sha = release_proof["candidate_sha256"],release_proof["patch_sha256"]
    assert sha==drive["sha256"]==live["candidate_sha256"]==startup["candidate_sha256"]
    assert drive["sole_nds_in_folder"] and drive["readback_verified"]
    assert base.digest(base.REGISTRY)==mutation["registry_after"]==release_proof["registry_sha256"]
    assert base.digest(base.LEDGER)==mutation["ledger_after"]
    assert base.digest(base.PROMOTED)==mutation["main_sha256"]
    assert base.load(release.PACKAGE/"checksums.json")==release.workflow.package_checksums(release.PACKAGE)
    retained = {release.ROM:sha,stage.ROM:sha,release.PATCH:patch_sha,release.MANIFEST:release_proof["manifest_sha256"],
        Path(release_proof["own_registered_startup"]):release_proof["own_registered_startup_sha256"]}
    retained.update({Path(p):h for p,h in (visual|live["evidence"]).items()})
    for row in [*startup["exact_matching_frames"],startup["read_only_snapshot"]]:
        retained[Path(row["path"])]=row.get("PNG_sha256",row.get("sha256"))
    assert all(base.digest(p)==h for p,h in retained.items())
    keep = {path.resolve() for path in retained}
    for archive,key in ((release.ROOT/"editorial_ledger_before.json.gz","ledger_before"),
                        (release.PACKAGE/"build_release_stack.json.gz","registry_after")):
        with open_gzip(archive,"rb") as src:
            assert file_digest(src,"sha256").hexdigest()==mutation[key]
    discard = {stage.REBUILT:sha,stage.PATCH:patch_sha}
    discard.update({release.ROOT/name:mutation[key] for name,key in (
        ("ledger_before.json","ledger_before"),("ledger_after.json","ledger_after"),
        ("release_stack_with_rafael_deck_tutorial.json","registry_after"))})
    for path in (stage.STARTUP_CAPTURE,release.live.REPORT):
        report = base.load(path)
        assert report["ROM_sha256"]==sha and report["cold_boot"] and not report["savestate_loaded"]
        for row in report["frames_captured"]:
            image = Path(row["path"])
            assert image.resolve().parent==path.parent.resolve()
            if image.resolve() not in keep:
                discard[image]=row["PNG_sha256"]
        save = report["battery_save_preloaded"]
        copy = Path(save["destination"])
        assert copy.resolve().parent==(path.parent/"saves").resolve()
        assert base.digest(save["source"])==save["source_sha256"]
        if copy.exists() and base.digest(copy)==save["source_sha256"]:
            discard[copy]=save["source_sha256"]
    roots = stage.ROOT.resolve(),release.ROOT.resolve()
    removed = []
    for path,h in discard.items():
        resolved=path.resolve()
        assert any(resolved.is_relative_to(root) for root in roots)
        assert resolved not in keep and not path.is_symlink() and not path.is_junction()
        assert path.suffix in {".nds",".xdelta",".json",".png",".dsv"} and base.digest(path)==h
        removed.append(dict(path=str(path),sha256=h,bytes=path.stat().st_size))
    for path in discard:
        path.unlink()
    assert all(base.digest(p)==h for p,h in retained.items())
    result = dict(registered_candidate_sha256=sha,removed=removed,
        reclaimed_bytes=sum(row["bytes"] for row in removed),verified_retained_evidence=len(retained))
    base.save(RECEIPT,result)
    print(f"Removed {len(removed)} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes.",flush=True)
    return result


def handoff(result):
    drive=base.load(DRIVE)
    assert drive["sha256"]==result["registered_candidate_sha256"]
    section=f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The registered ROM is the sole .nds in the Rota Nova Translation Drive folder. Streamed readback matches SHA-256 {drive['sha256']}. Its clean-input patch rebuilds the exact ROM. Startup and 17 focused tests passed. The candidate carries all 114 accepted layers and the ASCII right-bound correction. Checkpoint cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest Drive ROM]({drive['url']}) | [Clean-input patch](../{release.PATCH.as_posix()}) | [Playback and release evidence](../{release.VERIFY.as_posix()}) | [Cleanup receipt](../{RECEIPT.as_posix()})

All twelve panels and eleven Julio nameplates displayed through the original post-Trade event with the established Lisbon save. The normal return to Lisbon matched four reference screens. Six contextual wording revisions and six retentions preserve all sixteen commands and the name substitution. The revised captain speech also passed offline checks at the maximum supported given-name width. [Exact decisions and individual scope](../{release.REVIEW.as_posix()})

Continue with remaining player-visible town and random-event samples and the associated contextual and wrap reviews. Carry forward the current character setup and 207 default name decisions. The 276 alternate display entries, conditional and custom names, and other player-facing text remain in scope. The older-record technical re-audit and graphics artwork stay separate. [Setup and name ledger](../translations/editorial_checkpoints/SharedText_20261110_v1/early_setup_current_20261122_v1.json) | [Shared leads](../translations/editorial_checkpoints/SharedText_20261110_v1/shared_display_worklist_20261121_v3.json)

""".encode("utf-8")
    for name in ("editorial_handoff_current.md","translation_progress.md"):
        path=release.DOC.with_name(name)
        body=path.read_bytes()
        second=body.index(b"# Current editorial checkpoint",1)
        base.replace_checked(path,section+body[second:])


if __name__=="__main__":
    handoff(cleanup())

