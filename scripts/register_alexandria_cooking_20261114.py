"""Register the source-bound Alexandria exchange as a verified cumulative successor."""

from copy import deepcopy
from json import dumps
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import verify_alexandria_cooking_guards_20261114 as checked
from scripts import replay_alexandria_cooking_20261114 as replay
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.prepare_all_routes_promotion_20261111 import package_checksums
from scripts.register_lil_ceramics_wrap_20261111 import archive_file, write_pending
from scripts.verify_release_baseline import files


loader, base, parent, stage = checked.loader, checked.base, checked.parent, checked.stage
assets = loader.assets
PROFILE = "all-routes-alexandria-cooking-v1-20261114"
CHECK = "registered_alexandria_cooking_complete_parent_inverse"
ROOT = Path("out/alexandria_cooking_registered_20261114_v1")
ROM = ROOT / "Translation_DS_All_Routes_Alexandria_Cooking_20261114_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261114_alexandria_cooking_candidate")
PATCH, VERIFICATION = PACKAGE / "translation.xdelta", PACKAGE / "verification"
REVIEW = VERIFICATION / "registered_review.json"
RELEASE = VERIFICATION / "registered_release_verification.json"
DOC = Path("docs/editorial_alexandria_cooking_registered_20261114.md")
STARTUP = loader.ROOT / "own_startup_verification.json"
VISUAL = replay.ROOT / "visual_review.json"
QA = assets.WORK / "repository_qa_verified.xml"


def stable_id(row):
    return "DK4_MES_B" + row["id"].split("_B")[1]


def verify_reconstruction(old, proof, draft):
    original = base.NdsImage.open(parent.ROM)
    before = files(original)
    assert base.digest(stage.CLEAN) == old["clean_input_sha256"]
    assert base.digest(parent.MANIFEST) == old["manifest_sha256"]
    assert base.digest(parent.ROM) == old["candidate_sha256"] == proof["candidate_sha256"]
    for archive in proof["routes"]:
        path = archive["file_path"]
        assert assets.edit.digest(before[path]) == archive["source_archive_sha256"]
        bank = stage.IlnkContainer.parse(before[path])
        block = archive["block"]
        owned = [row for row in draft["records"] if row["file_path"] == path and row["decision"] == "revision"]
        rebuilt, positions = assets.splice(bank.blocks[block], owned, "current_hex", "current_record_offset", "requested_relocated_hex")
        assert all(positions[row["id"]] == row["proposed_record_offset"] for row in owned)
        bank.blocks[block] = rebuilt
        raw = bank.to_bytes()
        assert assets.edit.digest(raw) == archive["proposed_archive_sha256"]
        assert raw == Path(archive["proposed_archive"]).read_bytes()
        original.replace_file(path, raw)
    after = files(original)
    changed = {row["file_path"] for row in proof["routes"]}
    assert before.keys() == after.keys() and {path for path in before if before[path] != after[path]} == changed
    assert assets.edit.digest(after["/_pxl/personinfo.pxl"]) == old["target_PersonInfo_PXL_sha256"]
    checked.verify_runtime(after[stage.ARM], old)
    assert bytes(original.rom.save()) == loader.ROM.read_bytes()
    for path in changed:
        original.replace_file(path, before[path])
    assert bytes(original.rom.save()) == parent.ROM.read_bytes()
    return sorted(changed)


def main():
    registry_pending = base.REGISTRY.with_name("release_stack.alexandria_cooking.pending.json")
    ledger_pending = base.LEDGER.with_name("editorial_review_current.alexandria_cooking.pending.json")
    assert not any(path.exists() for path in (ROOT, PACKAGE, DOC, registry_pending, ledger_pending))
    old, draft, assets_proof, load_proof, safety, startup, live, visual = map(base.load,
        (parent.RELEASE, assets.REVIEW, assets.RECEIPT, loader.RECEIPT, checked.PROOF, STARTUP, replay.LIVE, VISUAL))
    changed = verify_reconstruction(old, assets_proof, draft)
    sha = base.digest(loader.ROM)
    assert sha == load_proof["proposed_ROM_sha256"] == startup["candidate_sha256"] == safety["candidate_sha256"]
    assert assets_proof["native_tail_skips_checked"] == 240 and load_proof["complete_native_loads"] == 1307
    assert load_proof["parent_modes"] == 2614 and len(safety["revised_catalogue_miss_cases"]) == 12
    assert len(startup["exact_matching_frames"]) == 6 and len(startup["original_protected_name_getters"]) == 24
    assert startup["cold_boot"] and not startup["savestate"] and startup["complete_deployed_payload_exact"]
    assert len(live["actual_progressive_panels"]) == 11 and visual["reported_complete_scene_pages"] == 12
    assert visual["replay_sha256"] == base.digest(replay.LIVE)
    assert base.digest(assets.REVIEW) == load_proof["evidence"][str(assets.REVIEW)]
    assert base.digest(assets.RECEIPT) == base.load(replay.SETUP)["archive_receipt_sha256"]
    assert base.digest(live["capture_report"]) == live["capture_report_sha256"]
    for evidence in (startup["evidence"], load_proof["evidence"], visual["reviewed_sheets"]):
        assert all(base.digest(path) == expected for path, expected in evidence.items())
    for panel in live["actual_progressive_panels"]:
        assert base.digest(panel["observed"]["path"]) == panel["observed"]["PNG_sha256"]
    suites = list(ElementTree.parse(QA).iter("testsuite"))
    assert sum(int(row.get("tests",0)) for row in suites) == 56
    assert not any(int(row.get(key,0)) for row in suites for key in ("errors","failures","skipped"))
    spec = safety["source25_multiarchive_guard"]
    rebound = checked.checked_receipt(spec)
    assert rebound["all_existing_exact_source_offsets_target_offsets_controls_and_bytes_verified"]

    before_registry, before_ledger = base.REGISTRY.read_bytes(), base.LEDGER.read_bytes()
    assert stage.sha(before_registry) == old["registry_sha256"]
    registry, ledger, manifest = map(base.load, (base.REGISTRY, base.LEDGER, parent.MANIFEST))
    assert PROFILE not in registry["profiles"] and len(registry["accepted_layers"]) == 114
    assert len(manifest["batches"]) == 807 and len(manifest["checks"]) == 142 and all(manifest["checks"].values())
    assert ledger["current_integrated_candidate"]["sha256"] == old["candidate_sha256"]
    assert ledger["records_editorially_completed"] == 27697 and not ledger["full_goal_complete"]
    credits = {(r["file_path"], r["id"]) for r in ledger[base.CONTEXT]["integrated_record_keys"]}
    assert all((row["file_path"],stable_id(row)) in credits for row in draft["records"])
    main_sha = base.digest(base.PROMOTED)
    ROOT.mkdir()
    VERIFICATION.mkdir(parents=True)
    make_xdelta(stage.CLEAN, loader.ROM, PATCH)
    apply_xdelta(stage.CLEAN, PATCH, ROM)
    assert ROM.read_bytes() == loader.ROM.read_bytes() and base.digest(ROM) == sha

    paths = (assets.RECEIPT, loader.RECEIPT, checked.PROOF, STARTUP, replay.LIVE, VISUAL, QA, Path(spec["path"]))
    for path in paths:
        copyfile(path, VERIFICATION / path.name)
        assert base.digest(VERIFICATION / path.name) == base.digest(path)
    records, retained = [], []
    current = base.NdsImage.open(ROM)
    arm = current.read_file(stage.ARM)
    inventory, _, _ = stage.prior.scoped_inventory()
    for archive in assets_proof["routes"]:
        path = archive["file_path"]
        block = archive["block"]
        raw = stage.IlnkContainer.parse(current.read_file(path)).blocks[block]
        _, current_rows = stage.prior.raw_speeches(arm, raw, inventory)
        rows = [row for row in draft["records"] if row["file_path"] == path]
        for row, stored in zip(rows, current_rows, strict=True):
            revised = row["decision"] == "revision"
            target = row["requested_relocated_hex"] if revised else row["current_hex"]
            assert stored["raw_hex"] == target and stored["complete_preamble_hex"] == row["source_reference"]["complete_preamble_hex"]
            item = row | dict(id=stable_id(row), registered_reference=stored | dict(
                block=block, file_path=path, candidate_sha256=sha, block_sha256=stage.sha(raw)))
            (records if revised else retained).append(item)
    assert (len(records),len(retained)) == (12,36)
    review = draft | dict(records=records, unchanged_leads=retained, registered_candidate_sha256=sha,
        registered_release_applied=True, gameplay_scope=str(VERIFICATION / VISUAL.name))
    validate_natural_dialogue_batch(review)
    validate_natural_dialogue_batch(review | {"records": retained})
    base.save(REVIEW, review)

    previous = ROOT / "release_stack_before_alexandria_cooking.json"
    previous.write_bytes(before_registry)
    archive_file(before_ledger, ROOT / "editorial_ledger_before.json.gz")
    predecessor = {key: old[key] for key in ("profile","candidate","candidate_sha256","manifest","manifest_sha256","registry_sha256")}
    predecessor["registry"] = str(previous)
    profile = deepcopy(registry["profiles"][old["profile"]])
    source25 = VERIFICATION / Path(spec["path"]).name
    profile.update(verified_maria_final_wraps_predecessor=predecessor, alexandria_cooking_release=str(REVIEW),
        source25_multiarchive_guard=dict(path=str(source25), sha256=base.digest(source25)),
        note="Contextual review of the Alexandria cooking exchange across all four routes.")
    registry["profiles"][PROFILE] = profile
    base.save(registry_pending, registry)
    manifest.update(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=sha,
        release_stack_sha256=base.digest(registry_pending))
    manifest["batches"].append(str(REVIEW))
    manifest["checks"][CHECK] = True
    for row in records:
        owned = manifest["changed_records"][row["file_path"]]
        if row["id"] not in owned:
            owned.append(row["id"])
    manifest["alexandria_cooking_registered_successor_pipeline"] = dict(predecessor=predecessor,
        driver=__file__, driver_sha256=base.digest(__file__), review=str(REVIEW), review_sha256=base.digest(REVIEW),
        guard_checks=str(VERIFICATION/checked.PROOF.name), original_branches_and_complete_parent_inverse=True,
        four_archive_changes=[dict(file_path=x["file_path"],block=x["block"],sha256=x["proposed_archive_sha256"])
            for x in assets_proof["routes"]])
    assert len(manifest["batches"]) == 808 and len(manifest["checks"]) == 143
    base.save(MANIFEST, manifest)
    start = VERIFICATION / STARTUP.name
    release = old | dict(profile=PROFILE,candidate=str(ROM),candidate_sha256=sha,patch=str(PATCH),patch_sha256=base.digest(PATCH),
        manifest=str(MANIFEST),manifest_sha256=base.digest(MANIFEST),registry_sha256=base.digest(registry_pending),
        predecessor=predecessor,registered_manifest_entries=808,passing_release_checks=143,repository_tests=56,
        own_registered_startup=str(start),own_registered_startup_sha256=base.digest(start),changed_components=[],
        changed_internal_files=changed,new_contextual_records=0,prose_revisions=12,justified_retentions=36,reviewed_UI_labels=0,
        actual_verification_scope=dict(actual_emulator=True,hardware=False,checked_representative_progressive_panels=11,
            checked_unchanged_market_panel=1,observable_following_onboarding=True,initialized_Maria_entry=True))
    base.save(RELEASE, release)
    base.save(PACKAGE / "release_manifest.json", release | {"user_acceptance_pending":True})
    archive_file(MANIFEST.read_bytes(), PACKAGE / "build_manifest.json.gz")
    archive_file(registry_pending.read_bytes(), PACKAGE / "build_release_stack.json.gz")

    checkpoint = "The Alexandria cooking exchange is registered across all four routes."
    ledger["current_integrated_candidate"].update(path=str(ROM),sha256=sha,profile=PROFILE,patch=str(PATCH),
        patch_sha256=release["patch_sha256"],manifest=str(MANIFEST),manifest_sha256=release["manifest_sha256"],
        registered_release_verification=str(RELEASE))
    ledger["latest_checkpoint"] = checkpoint
    ledger["alexandria_cooking_retrospective_20261114"] = dict(review=str(REVIEW),release=str(RELEASE),
        new_dialogue_credit=0,prior_credits_preserved=48,prose_revisions=12,exact_retentions=36)
    write_pending(ledger_pending, encode_ledger(ledger))
    mutation = dict(registry_before=stage.sha(before_registry),registry_after=base.digest(registry_pending),
        ledger_before=stage.sha(before_ledger),ledger_after=base.digest(ledger_pending),main_sha256=main_sha)
    base.save(VERIFICATION / "registration_mutation_plan.json", mutation)
    (PACKAGE/"README.md").write_text(f"""# Alexandria cooking review candidate

The [local ROM](../../{ROM.as_posix()}) carries the Alexandria cooking review and the full preceding release.
The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` from Japanese SHA-256
`{old['clean_input_sha256']}`. The exact cumulative ROM passed emulator startup and native entry checks.
Hardware testing and acceptance for main remain pending.
""",encoding="utf-8",newline="\n")
    base.save(PACKAGE / "checksums.json", package_checksums(PACKAGE))
    assert base.digest(base.REGISTRY) == mutation["registry_before"] and base.digest(base.LEDGER) == mutation["ledger_before"]
    assert base.digest(base.PROMOTED) == main_sha
    registry_pending.replace(base.REGISTRY)
    try:
        ledger_pending.replace(base.LEDGER)
    except OSError:
        base.replace_checked(base.REGISTRY, before_registry)
        raise
    assert base.digest(base.REGISTRY) == mutation["registry_after"]
    assert base.digest(base.LEDGER) == mutation["ledger_after"]
    pins_path = Path("translations/rom_retention_pins.json")
    pins = base.load(pins_path)
    for path in (ROM, loader.ROM, Path(base.load(replay.SETUP)["fixture_ROMs"]["after"]["path"])):
        exact = str(path.resolve())
        assert not any(row["path"] == exact for row in pins)
        pins.append(dict(path=exact,reason=f"Preserve Alexandria release and verification. SHA256 {base.digest(path)}"))
    base.replace_checked(pins_path,(dumps(pins,ensure_ascii=False,indent=2)+"\n").replace("\n","\r\n").encode())
    base.replace_checked(DOC,f"""# Alexandria cooking exchange

The [registered review](../{REVIEW.as_posix()}) records 12 revisions and 36 retentions across the four copies of the scene. The owner repeats her “sweet” catchphrase, asserts her judgment and leaves the method to the cook. His repeated “yeah, yeah” shows his impatience without changing their relationship. All 48 existing dialogue credits are preserved.

All 26 preview pages received visual review. The complete parent inverse, 240 conditional decoder checks, 1,307 whole-block loads, 2,614 native interpreter entries and 56 targeted tests passed. An initialized Maria replay observed all 11 speeches, both speaker labels, the original forecast, and its dismissal back to Hangzhou’s opening sequence. Natural Alexandria activation and hardware stay unvisited. A separate cumulative cold boot matched six frames and 24 protected name getters.

Only the four Alexandria story blocks changed. The original event controls and impersonal forecast are byte-exact. The stale SC3 B38 format receipt was refreshed after proving its two relocated source selectors, exact records and offsets still match. All seven relocated selectors and four negative controls pass the unchanged detector. The cumulative [ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers, the Market and ASCII right-bound fixes, and the Sailor Info correction.

The full editorial goal remains active. Continue shared consumer review, names and other UI text, and representative town and random-scene coverage. Keep deferred artwork and the older-record technical re-audit separate.
""".encode())
    lead=f"# Current editorial checkpoint - 2026-11-14\n\n{checkpoint} [Checkpoint]({DOC.name})\n\n".encode()
    for filename in ("editorial_handoff_current.md","translation_progress.md","build_continuity_protocol.md"):
        path=Path("docs")/filename
        base.replace_checked(path,lead+path.read_bytes())
    assert base.digest(base.PROMOTED) == main_sha
    print(f"Registered {ROM} | SHA-256 {sha} | 808 entries, 114 accepted layers, 143 checks.")


if __name__ == "__main__":
    main()

