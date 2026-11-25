"""Preserve the verified encounter and Osaka draft evidence, then clean the checkpoint."""

from gzip import open as gzip_open
from hashlib import file_digest
from pathlib import Path

from scripts import register_kurushima_surrender_20261122 as release
from scripts import review_osaka_glass_followup_20261122 as osaka
from scripts.verify_seville_square_gameplay_20261121 import Exchange,navigation_state


base,stage,native=release.base,release.stage,release.native
VOYAGE=stage.voyage.ROOT
DRIVE=release.ROOT/"drive_latest_build_receipt.json"
RECEIPT=release.ROOT/"checkpoint_cleanup.json"
FOLLOWUP=osaka.ROOT/"successor_binding.json"


def bind_osaka(candidate):
    assert not FOLLOWUP.exists()
    draft,proof=map(base.load,(osaka.REVIEW,osaka.PROOF))
    assert base.digest(osaka.REVIEW)==proof["manuscript_sha256"]
    assert base.digest(osaka.SHEET)==proof["sheet_sha256"] and len(proof["native_pages"])==2
    assert draft["proposed_changes"]==2 and draft["justified_retentions"]==42
    before,after=map(base.NdsImage.open,(release.parent.ROM,release.ROM))
    for name in (native.ARM,"/GRP/KANJI.FNT","/data/EV3.DK4"):
        assert before.read_file(name)==after.read_file(name)
    blocks={}
    for route,block in enumerate(osaka.BLOCKS):
        name=f"/data/SC{route}.DK4"
        old,now=[native.IlnkContainer.parse(im.read_file(name)).blocks[block] for im in (before,after)]
        assert old==now
        blocks[name]=dict(block=block,exact_current_sha256=native.digest(now))
    report=base.load(release.live.BASELINE)
    witness=report["read_only_RAM_snapshot"]
    raw=Path(witness["path"]).read_bytes()
    assert native.digest(raw)==witness["sha256"]
    state=navigation_state(after.read_file(native.ARM),raw,Exchange(3,59,161,11,Path(osaka.PREVIOUS),{}))
    assert state["town"]!=59
    base.save(FOLLOWUP,dict(candidate_sha256=candidate,retained_earlier_registration=draft["prior_ROM"],
        draft=str(osaka.REVIEW),draft_sha256=base.digest(osaka.REVIEW),stored_and_native_proof=str(osaka.PROOF),
        stored_and_native_proof_sha256=base.digest(osaka.PROOF),visually_reviewed_two_native_previews=True,
        unchanged_osaka_blocks=blocks,current_Font_and_EV3_exact=True,current_ARM9_exact=True,
        ordinary_Nagasaki_departure=True,osaka_arrival_or_event_observed=False,final_native_state=state,
        final_read_only_snapshot=witness,focused_or_ordinary_replay_on_revised_lines_pending=True,
        all_new_Osaka_changes_remain_unregistered=True))
    return witness


def cleanup():
    assert not RECEIPT.exists()
    meta,plan,drive,played,boot,visual=map(base.load,(release.RELEASE,release.VERIFY/"registration_mutation_plan.json",
        DRIVE,release.live.LIVE,release.VERIFY/release.STARTUP.name,release.VISUAL))
    candidate,patch=meta["candidate_sha256"],meta["patch_sha256"]
    assert candidate==drive["sha256"]==played["candidate_sha256"]==boot["candidate_sha256"]
    assert drive["sole_nds_in_folder"] and drive["readback_verified"]
    assert base.digest(base.REGISTRY)==plan["registry_after"]==meta["registry_sha256"]
    assert base.digest(base.LEDGER)==plan["ledger_after"]
    assert base.digest(base.PROMOTED)==plan["main_sha256"]
    assert base.load(release.PACKAGE/"checksums.json")==release.workflow.package_checksums(release.PACKAGE)
    witness=bind_osaka(candidate)
    retained={release.ROM:candidate,stage.ROM:candidate,release.PATCH:patch,release.MANIFEST:meta["manifest_sha256"],
        Path(meta["own_registered_startup"]):meta["own_registered_startup_sha256"],osaka.SHEET:base.digest(osaka.SHEET),
        osaka.REVIEW:base.digest(osaka.REVIEW),osaka.PROOF:base.digest(osaka.PROOF),FOLLOWUP:base.digest(FOLLOWUP)}
    retained.update({Path(p):h for p,h in (played["evidence"]|visual["sheets"]).items()})
    for row in [*boot["exact_matching_frames"],boot["read_only_snapshot"],witness]:
        retained[Path(row["path"])]=row.get("PNG_sha256",row.get("sha256"))
    earlier=base.load(release.live.BASELINE)
    # Keep the opening port, the actual no-route response, and the end of the attempted voyage.
    for row in earlier["frames_captured"]:
        if row["frame"] in (3650,7150,12746) and row["path"].endswith("_navigation.png"):
            retained[Path(row["path"])]=row["PNG_sha256"]
    for row in earlier["read_only_pause_RAM_snapshots"]:
        if row["frame"] in (3650,8550,9020,11620):
            retained[Path(row["path"])]=row["sha256"]
    assert all(base.digest(p)==sha for p,sha in retained.items())
    keep={path.resolve() for path in retained}
    discard={stage.REBUILT:candidate,stage.PATCH:patch}
    for archive,key in ((release.ROOT/"editorial_ledger_before.json.gz","ledger_before"),
                        (release.PACKAGE/"build_release_stack.json.gz","registry_after")):
        with gzip_open(archive,"rb") as source:
            assert file_digest(source,"sha256").hexdigest()==plan[key]
    for filename,key in (("ledger_before.json","ledger_before"),("ledger_after.json","ledger_after"),
                          ("release_stack_with_maria_kurushima_surrender.json","registry_after")):
        discard[release.ROOT/filename]=plan[key]
    for path,sha in ((stage.STARTUP_CAPTURE,candidate),(release.live.REPORT,candidate),
                     (release.live.BASELINE,meta["predecessor"]["candidate_sha256"])):
        report=base.load(path)
        assert report["ROM_sha256"]==sha and report["cold_boot"] and not report["savestate_loaded"]
        for key,field in (("frames_captured","PNG_sha256"),("read_only_pause_RAM_snapshots","sha256")):
            for row in report.get(key,[]):
                child=Path(row["path"])
                assert child.resolve().parent==path.parent.resolve()
                if child.resolve() not in keep:
                    discard[child]=row[field]
        battery=report["battery_save_preloaded"]
        copy=Path(battery["destination"])
        assert copy.resolve().parent==(path.parent/"saves").resolve()
        assert base.digest(battery["source"])==battery["source_sha256"]
        if copy.exists() and base.digest(copy)==battery["source_sha256"]:
            discard[copy]=battery["source_sha256"]
    roots=VOYAGE.resolve(),release.ROOT.resolve()
    removed=[]
    for path,h in discard.items():
        resolved=path.resolve()
        assert any(resolved.is_relative_to(d) for d in roots)
        assert resolved not in keep and not path.is_symlink() and not path.is_junction()
        assert path.suffix in {".nds",".xdelta",".json",".png",".bin",".dsv"} and base.digest(path)==h
        removed.append(dict(path=str(path),sha256=h,bytes=path.stat().st_size))
    for path in discard:
        path.unlink()
    assert all(base.digest(path)==h for path,h in retained.items())
    result=dict(candidate_sha256=candidate,removed=removed,reclaimed_bytes=sum(row["bytes"] for row in removed),
        retained_verified_files=len(retained))
    base.save(RECEIPT,result)
    print(f"Removed {len(removed)} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes.",flush=True)
    return result


def handoff(result):
    drive=base.load(DRIVE)
    assert drive["sha256"]==result["candidate_sha256"]
    section=f"""# Current editorial checkpoint - 2026-11-22

{release.CHECKPOINT} [Checkpoint]({release.DOC.name})

The sole .nds in the Rota Nova Translation Drive folder matches SHA-256 {drive['sha256']}. The clean-input patch reconstructed it exactly. Startup and 17 focused tests passed, preserving 114 accepted layers and the ASCII right-bound correction. Cleanup removed {len(result['removed'])} redundant files and reclaimed {result['reclaimed_bytes']:,} bytes. [Latest testing build]({drive['url']}) | [Clean-input patch](../{release.PATCH.as_posix()}) | [Cleanup receipt](../{RECEIPT.as_posix()})

The ordinary Nagasaki departure displayed Kurushima's incorrect offer and then verified the corrected subject in the successor. The eight complete pages and nameplates, the fleet alert and Sea View transition passed. The corrected speech keeps Maria's name and the full threat. All four offline name widths fit. [Exact contextual decisions](../{release.REVIEW.as_posix()}) | [Emulator comparison](../{(release.VERIFY/release.live.PLAY_SHEET.name).as_posix()})

The Osaka glass pass covers 44 turns across the four storylines with two proposed guildmaster replies and 42 justified retentions. It preserves two later Hodram edits. Both proposed pages pass native and visual checks. Their original Osaka blocks and rendering dependencies match the new registered ROM. The voyage stopped after the natural Kurushima encounter with Osaka still unvisited. Continue with a focused Osaka preview in the original scene and pursue ordinary activation where practical. The 276 alternate display entries, random scenes, conditional names, and other player-facing prose stay in scope. Graphics artwork and the later older-record technical re-audit remain separate. [Exact Osaka review](../{osaka.REVIEW.as_posix()}) | [Stored and native preview](../{osaka.PROOF.as_posix()}) | [Current binding and voyage scope](../{FOLLOWUP.as_posix()})

""".encode("utf-8")
    for name in ("editorial_handoff_current.md","translation_progress.md"):
        path=release.DOC.with_name(name)
        body=path.read_bytes()
        second=body.index(b"# Current editorial checkpoint",1)
        base.replace_checked(path,section+body[second:])


if __name__=="__main__":
    handoff(cleanup())

