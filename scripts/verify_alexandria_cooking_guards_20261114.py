"""Verify effective catalogue ownership, placeholder safety, and wrap-queue continuity."""

from copy import deepcopy
from pathlib import Path

from dk4tool.script.format_safety_relocated_v2 import checked_receipt, reject_with_receipt
from scripts import verify_alexandria_cooking_loader_20261114 as loader
from scripts import prove_lil_shrines_temples_controls_v3168c as catalogue
from scripts import scan_current_progressive_wrap_leads_20261111 as wrap
from scripts import verify_historical_story_wraps_storage_20261111 as precedent
from scripts.prepare_all_routes_promotion_20261111 import verify_runtime
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_release_baseline import files


base, parent, stage = loader.base, loader.parent, loader.stage
ROOT = loader.ROOT
PROOF = ROOT / "current_guard_checks.json"



def rebind_source25(spec, clean, before, after):
    historical = checked_receipt(spec)
    revised = deepcopy(historical)
    route, = revised["additional_routes"]
    path = route["file_path"]
    assert path == "/data/SC3.DK4"
    source_bank, parent_bank, target_bank = [stage.IlnkContainer.parse(fileset[path]).blocks
                                             for fileset in (clean, before, after)]
    refreshed = []
    for row in route["relocated_source25_records"]:
        block = row["block"]
        assert block == 38 and parent_bank[block] == target_bank[block]
        assert stage.sha(source_bank[block]) == row["clean_block_sha256"]
        fresh_hash = stage.sha(target_bank[block])
        assert fresh_hash != row["target_block_sha256"]
        refreshed.append(dict(id=row["id"], block=block, old_hash=row["target_block_sha256"], new_hash=fresh_hash))
        row["target_block_sha256"] = fresh_hash
    assert len(refreshed) == 2
    parent_report = reject_with_receipt(clean, before, revised)
    target_report = reject_with_receipt(clean, after, revised)
    for result in (parent_report, target_report):
        assert result["total_exact_source_bound_relocated_leading25_count"] == 7
        assert result["all_four_final_story_archives_checked"]
        assert not any(result["source_bound_new_command_counts"].values())

    negatives = []
    for case in ("wrong-clean-selector-offset", "wrong-stored-preamble", "wrong-target-index", "injected-printf"):
        wrong, target = deepcopy(revised), after.copy()
        entry = wrong["additional_routes"][0]["relocated_source25_records"][0]
        if case == "wrong-clean-selector-offset":
            entry["source_offset"] += 2
        elif case == "wrong-stored-preamble":
            entry["complete_preamble_hex"] = "0040ffff0024"
        elif case == "wrong-target-index":
            entry["target_index"] += 1
        else:
            bank = stage.IlnkContainer.parse(after[path])
            blob = bank.blocks[159]
            assert blob.count(b"Hmm...") == 1
            bank.blocks[159] = blob.replace(b"Hmm...", b"%s ABC")
            target[path] = bank.to_bytes()
        try:
            reject_with_receipt(clean, target, wrong)
        except (AssertionError, ValueError) as error:
            if case == "injected-printf":
                assert isinstance(error, ValueError) and "%s" in str(error)
            negatives.append(dict(case=case, rejected=True, failure=type(error).__name__))
        else:
            raise AssertionError(case)
    revised.update(positive=target_report, parent_positive=parent_report, negative_cases=negatives,
        source25_predecessor_receipt=spec, rebound_archive_hashes=refreshed,
        all_existing_exact_source_offsets_target_offsets_controls_and_bytes_verified=True)
    revised["evidence"] = historical["evidence"] | {str(p): base.digest(p)
        for p in (Path(spec["path"]), parent.RELEASE, loader.RECEIPT, Path(__file__))}
    return revised


def main():
    release = base.load(parent.RELEASE)
    receipt = base.load(loader.RECEIPT)
    review = base.load(loader.assets.REVIEW)
    assert base.digest(loader.ROM) == receipt["proposed_ROM_sha256"]
    assert base.digest(parent.ROM) == release["candidate_sha256"] == receipt["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(parent.MANIFEST) == release["manifest_sha256"]
    before, after, clean = map(base.NdsImage.open, (parent.ROM, loader.ROM, stage.CLEAN))
    active = base.load(base.REGISTRY)["profiles"][release["profile"]]
    rebound = rebind_source25(active["source25_multiarchive_guard"], files(clean), files(before), files(after))
    guard_path = ROOT / "source25_current_qualification.json"
    base.save(guard_path, rebound)
    checked = rebound["positive"]
    arm = after.read_file(stage.ARM)
    assert arm == before.read_file(stage.ARM)
    verify_runtime(arm, release)

    adapter = base.load(precedent.HISTORICAL)["source_owned_dispatch_adapters"]["bind_current_catalog"]
    adapter = checked_text(adapter,{
        "2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a":stage.sha(arm),
        "read(Path(image.path).with_suffix('.manifest.json')) if hasattr(image,'path') else read(Path(read(SOURCE)['current_ROM']).with_suffix('.manifest.json'))":
            "read(MANIFEST)",
        "read(SOURCE)['current_ROM'].replace('.nds','.manifest.json')": "str(MANIFEST)",
    })
    selected = [row for row in review["records"] if row["decision"] == "revision"]
    misses, contexts, scans = [], [], []
    for path in receipt["verified_archives"]:
        route = int(path.split("SC")[1][0])
        env = vars(catalogue) | dict(MANIFEST=parent.MANIFEST,route=route,route_mask=1 << route)
        exec(compile(adapter,__file__+"::same-registered-native-catalogue-adapter","exec"),env)
        lookup, current_catalogue_receipt = env["bind_current_catalog"](before)
        revised_lookup, target_catalogue_receipt = env["bind_current_catalog"](after)
        assert revised_lookup == lookup
        del current_catalogue_receipt["records"], target_catalogue_receipt["records"]
        contexts.append(dict(route=route,before=current_catalogue_receipt,after=target_catalogue_receipt))
        rows = [row for row in selected if row["file_path"] == path]
        assert rows
        for row in rows:
            old, new = map(bytes.fromhex,(row["current_hex"],row["requested_relocated_hex"]))
            assert old[1:] not in lookup and new[1:] not in revised_lookup
            misses.append(dict(id=row["id"], before=old.hex(), after=new.hex()))
        _, leads_before = wrap.scan(path,before.read_file(path))
        _, leads_after = wrap.scan(path,after.read_file(path))
        def identity(item):
            return item["block"], item["source_selector"], item["stored_body_hex"], item["rows"], item["findings"]
        # This batch may rebase existing command offsets. No new wrap lead may be introduced.
        assert sorted(map(identity,leads_before),key=repr) == sorted(map(identity,leads_after),key=repr)
        scans.append(dict(file_path=path, heuristic_leads_preserved=len(leads_after), no_new_leads=True,
            candidate_archive_sha256=stage.sha(after.read_file(path))))
    assert len(misses) == 12
    base.save(PROOF,dict(candidate_sha256=receipt["proposed_ROM_sha256"], registered_parent_sha256=release["candidate_sha256"],
        guarded_story_percent_check=checked,
        source25_multiarchive_guard=dict(path=str(guard_path), sha256=base.digest(guard_path)), original_market_and_ASCII_right_bound_verified=True,
        revised_catalogue_miss_cases=misses, catalogue_receipts=contexts, wrap_leads=scans,
        earlier_queue=str(parent.TRIAGE), earlier_queue_sha256=base.digest(parent.TRIAGE)))
    print("Existing registered format and runtime guards passed. 12 catalogue misses and no new wrap leads.")


if __name__ == "__main__":
    main()

