"""Remove redundant staging files after the new candidate has been read back from Drive."""

from gzip import open as open_gzip
from hashlib import file_digest
from pathlib import Path
import struct

from scripts import register_ship_room_names_20261122 as release
from scripts.verify_personal_gameplay_v841 import get_machine


base, stage = release.base, release.writer


def main():
    receipt = release.ROOT / "checkpoint_cleanup.json"
    assert not receipt.exists()
    manifest, mutation, drive, visual, items, startup = map(base.load, (
        release.RELEASE, release.VERIFY/"registration_mutation_plan.json",
        release.ROOT/"drive_latest_build_receipt.json", release.EVIDENCE/"visual_review.json",
        release.ITEMS, release.VERIFY/release.STARTUP.name))
    sha = manifest["candidate_sha256"]
    patch_sha = manifest["patch_sha256"]
    assert sha == items["candidate_sha256"] == startup["candidate_sha256"] == drive["sha256"]
    assert drive["sole_nds_in_folder"] and drive["readback_verified"]
    assert base.digest(base.LEDGER) == mutation["ledger_after"]
    assert base.digest(base.REGISTRY) == mutation["registry_after"] == manifest["registry_sha256"]
    assert base.digest(base.PROMOTED) == mutation["main_sha256"]
    assert base.load(release.PACKAGE/"checksums.json") == release.workflow.package_checksums(release.PACKAGE)
    retained = {release.ROM:sha, stage.ROM:sha, release.PATCH:patch_sha,
                release.MANIFEST:manifest["manifest_sha256"], Path(manifest["own_registered_startup"]):
                manifest["own_registered_startup_sha256"]}
    retained.update({Path(p):digest for p,digest in visual.items()})
    item_report = release.EVIDENCE/"item_gameplay/capture/capture_report.json"
    retained[item_report] = items["report_sha256"]
    for shot in [*(row["capture"] for row in items["observed"]), items["observed_return"],
                 *startup["exact_matching_frames"], startup["read_only_snapshot"]]:
        retained[Path(shot["path"])] = shot.get("PNG_sha256",shot.get("sha256"))

    retry = stage.ROOT/"deck_gameplay_retry/capture"
    ram_path = retry/"frame_015300_arm9_ram.bin"
    frame = retry/"frame_015300_navigation.png"
    journal = retry/"navigation_command_journal.json"
    raw = ram_path.read_bytes()
    assert len(raw) == 0x400000
    cpu, get = get_machine(base.NdsImage.open(stage.ROM).read_file(stage.ARM),raw)
    state = list(struct.unpack("<2I",cpu.mem_read(get(0x3F0F8)+8,8)))
    assert state == [0,0]
    identity_root = stage.ROOT/"deck_replay_fleet_identity"
    identity = base.load(identity_root/"fleet_identity.json")
    for path,digest in [(identity_root/"capture_report.json",identity["source_report_sha256"]),
                        (identity_root/"final_arm9_ram.bin",identity["bytes_sha256"]),
                        *((p,base.digest(p)) for p in (ram_path,frame,journal,identity_root/"fleet_identity.json"))]:
        retained[path] = digest
    base.save(release.ROOT/"deck_replay_diagnostic.json",dict(candidate_sha256=sha,frame=15300,
        current_original_mode_fields=state,required_combat_mode_fields=[0,1],
        reason="The cumulative build was still at sea. The historical replay stopped before assigning a crew condition.",
        live_fatigue_dialogue_observed=False,evidence={str(p):retained[p] for p in (ram_path,frame,journal)}))
    assert all(base.digest(p) == digest for p,digest in retained.items())

    for archive,key in ((release.ROOT/"editorial_ledger_before.json.gz","ledger_before"),
                        (release.PACKAGE/"build_release_stack.json.gz","registry_after")):
        with open_gzip(archive,"rb") as source:
            assert file_digest(source,"sha256").hexdigest() == mutation[key]
    discard = {stage.ROOT/"clean_rebuilt.nds":sha, stage.ROOT/"translation.xdelta":patch_sha}
    discard.update({release.ROOT/name:mutation[key] for name,key in (
        ("ledger_before.json","ledger_before"),("ledger_after.json","ledger_after"),
        ("release_stack_with_ship_room_names.json","registry_after"))})
    keep = {path.resolve() for path in retained}
    start = base.load(release.STARTUP_CAPTURE)
    for report in (start,base.load(item_report),base.load(identity_root/"capture_report.json")):
        assert report["ROM_sha256"] == sha
        for shot in report["frames_captured"]:
            candidate = Path(shot["path"])
            if candidate.resolve() not in keep:
                discard[candidate] = shot["PNG_sha256"]
        donor = report["battery_save_preloaded"]
        copy = Path(donor["destination"])
        if copy.exists():
            assert base.digest(donor["source"]) == donor["source_sha256"]
            if base.digest(copy) == donor["source_sha256"]:
                discard[copy] = donor["source_sha256"]
    for state in [*start["read_only_capture_native_states"],start["read_only_native_state"]]:
        assert base.digest(state["path"]) == state["sha256"]
        details = base.load(state["path"])
        for region in details["regions"].values():
            path = Path(region["path"])
            assert path.resolve().parent == Path(state["path"]).resolve().parent
            if path.resolve() not in keep:
                discard[path] = region["sha256"]
    for root in (stage.ROOT/"deck_gameplay/capture",retry):
        for path in root.glob("frame_*.png"):
            if path.resolve() not in keep:
                discard[path] = base.digest(path)
    roots = stage.ROOT.resolve(), release.ROOT.resolve()
    removed = []
    for path,digest in discard.items():
        resolved = path.resolve()
        assert any(resolved.is_relative_to(root) for root in roots)
        assert resolved not in keep and not path.is_symlink() and not path.is_junction()
        assert path.suffix in {".nds",".xdelta",".json",".png",".dsv",".bin"}
        assert base.digest(path) == digest
        removed.append(dict(path=str(path),sha256=digest,bytes=path.stat().st_size))
    for path in discard:
        path.unlink()
    assert all(base.digest(path) == digest for path,digest in retained.items())
    reclaimed = sum(row["bytes"] for row in removed)
    base.save(receipt,dict(removed=removed,reclaimed_bytes=reclaimed,registered_candidate_sha256=sha,
        verified_retained_evidence=len(retained)))
    print(f"Removed {len(removed)} redundant files and reclaimed {reclaimed:,} bytes.",flush=True)


if __name__ == "__main__":
    main()

