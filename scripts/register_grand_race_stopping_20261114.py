"""Register the verified Grand Race stopping rule with the cumulative release."""

from copy import deepcopy
from json import dumps
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import stage_grand_race_stopping_20261114 as stage
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.register_lil_ceramics_wrap_20261111 import archive_file, write_pending
from scripts.prepare_all_routes_promotion_20261111 import package_checksums
from scripts.verify_release_baseline import files


base,parent,source=stage.base,stage.parent,stage.review
PROFILE="all-routes-grand-race-stopping-v1-20261114"
CHECK="registered_grand_race_stopping_help_and_complete_parent_inverse"
ROOT=Path("out/grand_race_stopping_registered_20261114_v1")
ROM=ROOT/"Translation_DS_All_Routes_Grand_Race_Help_20261114_candidate.nds"
MANIFEST=ROM.with_suffix(".manifest.json")
PACKAGE=Path("releases/all_routes_editorial_20261114_grand_race_help_candidate")
PATCH,VERIFY=PACKAGE/"translation.xdelta",PACKAGE/"verification"
REVIEW=VERIFY/"registered_review.json"
RELEASE=VERIFY/"registered_release_verification.json"
QA=stage.run.ROOT/"repository_qa.xml"
STARTUP=stage.ROOT/"own_startup_verification.json"
DOC=Path("docs/editorial_grand_race_stopping_registered_20261114.md")
VIEWED="3506911b8228c8638c1f7922960616144c8d93ef7eb2916127efb5e0db071f4c"


def verify(previous, guard):
    editorial, staged, live, startup=map(base.load,(source.OUTPUT,stage.RECEIPT,stage.LIVE,STARTUP))
    assert base.digest(parent.ROM)==previous["candidate_sha256"]==staged["input_ROM_sha256"]
    assert editorial["candidate_sha256"]==previous["candidate_sha256"]
    sha=base.digest(stage.ROM)
    assert sha==staged["research_ROM_sha256"]==live["research_ROM_sha256"]==startup["candidate_sha256"]
    assert live["complete_revised_body_mask"] and len(live["unchanged_framebuffer_controls"])==5
    assert base.digest(live["review_image"])==live["review_image_sha256"]==VIEWED
    assert base.digest(source.OUTPUT)==staged["source_review_sha256"]
    assert startup["cold_boot"] and not startup["savestate"] and startup["complete_deployed_payload_exact"]
    assert len(startup["exact_matching_frames"])==6 and len(startup["original_protected_name_getters"])==24
    for bundle in (live["evidence"],startup["evidence"]):
        assert all(base.digest(path)==digest for path,digest in bundle.items())
    tests=list(ElementTree.parse(QA).iter("testsuite"))
    assert sum(int(item.get("tests",0)) for item in tests)==46
    assert not any(int(item.get(k,0)) for item in tests for k in ("errors","failures","skipped"))
    before,after=map(base.NdsImage.open,(parent.ROM,stage.ROM))
    left,right=files(before),files(after)
    assert left.keys()==right.keys() and {path for path in left if left[path]!=right[path]}=={source.ARM}
    old,new=map(bytes.fromhex,(staged["original_slot_hex"],staged["refined_slot_hex"]))
    at=staged["ARM9_offset"]
    arm=left[source.ARM]
    assert arm[at:at+len(old)]==old and len(old)==len(new)
    assert arm[:at]+new+arm[at+len(old):]==right[source.ARM]
    stage.verify_runtime(right[source.ARM],previous)
    assert source.current.assets.edit.digest(right[source.ARM])==staged["target_ARM9_sha256"]
    clean=base.NdsImage.open(parent.stage.CLEAN)
    format_guard=bind_registered_story_percent_guard(guard)(files(clean),right)
    assert format_guard["total_exact_source_bound_relocated_leading25_count"]==7
    assert not any(format_guard["source_bound_new_command_counts"].values())
    after.replace_file(source.ARM,arm)
    assert bytes(after.rom.save())==parent.ROM.read_bytes()
    rows=[]
    for row in editorial["records"]:
        if row["decision"]=="revision":
            row={k:v for k,v in row.items() if k not in ("offline_automatic_layout_preview","preview_sha256")}
            body=new[:new.index(0)+1]
            row=row | dict(english=stage.DRAFT,proposed_lines=staged["actual_proposed_lines"],
                proposed_hex=body.hex(),proposed_body_bytes=len(body),
                review=row["review"] | {"formatting":True},
                registered_reference=dict(ARM9_offset=at,exact_slot_hex=new.hex(),candidate_sha256=sha),
                actual_revised_page=live)
        else:
            row=row | dict(registered_reference=row["current_reference"] | {"candidate_sha256":sha})
        rows.append(row)
    assert sum(i["decision"]=="revision" for i in rows)==1 and len(rows)==9
    return editorial | dict(records=rows,registered_candidate_sha256=sha,
        direct_revised_page_visual_review=True,registered_format_guard=format_guard)


def main():
    before_registry,before_ledger=base.REGISTRY.read_bytes(),base.LEDGER.read_bytes()
    registry,ledger,manifest,previous=map(base.load,(base.REGISTRY,base.LEDGER,parent.MANIFEST,parent.RELEASE))
    assert base.digest(base.REGISTRY)==previous["registry_sha256"]
    assert base.digest(parent.MANIFEST)==previous["manifest_sha256"]
    assert base.digest(parent.stage.CLEAN)==previous["clean_input_sha256"]
    assert ledger["records_editorially_completed"]==27699 and not ledger["full_goal_complete"]
    assert ledger["current_integrated_candidate"]["sha256"]==previous["candidate_sha256"]
    assert len(manifest["batches"])==808 and len(manifest["checks"])==143 and all(manifest["checks"].values())
    assert len(registry["accepted_layers"])==114 and PROFILE not in registry["profiles"]
    main_sha=base.digest(base.PROMOTED)
    profile=deepcopy(registry["profiles"][previous["profile"]])
    proof=verify(previous,profile["source25_multiarchive_guard"])
    validate_natural_dialogue_batch(proof)
    registry_pending=base.REGISTRY.with_name("release_stack.grand_race_stopping.pending.json")
    ledger_pending=base.LEDGER.with_name("editorial_review_current.grand_race_stopping.pending.json")
    assert not any(path.exists() for path in (ROOT,PACKAGE,DOC,registry_pending,ledger_pending))
    ROOT.mkdir()
    VERIFY.mkdir(parents=True)
    make_xdelta(parent.stage.CLEAN,stage.ROM,PATCH)
    apply_xdelta(parent.stage.CLEAN,PATCH,ROM)
    sha=base.digest(ROM)
    assert sha==proof["registered_candidate_sha256"] and ROM.read_bytes()==stage.ROM.read_bytes()
    for original in (source.OUTPUT,stage.RECEIPT,stage.LIVE,STARTUP,QA):
        copyfile(original,VERIFY/original.name)
        assert base.digest(original)==base.digest(VERIFY/original.name)
    base.save(REVIEW,proof)
    backup=ROOT/"release_stack_before_grand_race_stopping.json"
    backup.write_bytes(before_registry)
    lineage={k:previous[k] for k in ("profile","candidate","candidate_sha256","manifest","manifest_sha256","registry_sha256")}
    lineage["registry"]=str(backup)
    profile.update(verified_alexandria_cooking_predecessor=lineage,
        grand_race_stopping_help_release=str(REVIEW),
        note="Natural wording and verified native display for Grand Race’s stopping rule.")
    registry["profiles"][PROFILE]=profile
    base.save(registry_pending,registry)
    manifest.update(profile=PROFILE,candidate_rom=str(ROM),candidate_sha256=sha,release_stack_sha256=base.digest(registry_pending))
    manifest["batches"].append(str(REVIEW))
    manifest["checks"][CHECK]=True
    assert source.ARM in manifest["changed_paths"]
    ident=next(row["id"] for row in proof["records"] if row["decision"]=="revision")
    owned=manifest["changed_records"][source.ARM]
    if ident not in owned:
        owned.append(ident)
    manifest["grand_race_stopping_registered_successor_pipeline"]=dict(predecessor=lineage,review=str(REVIEW),
        review_sha256=base.digest(REVIEW),producer=stage.__file__,producer_sha256=base.digest(stage.__file__),
        registered_driver=__file__,registered_driver_sha256=base.digest(__file__),
        unchanged_descriptor_and_whole_parent_inverse=True,changed_arm9_body_slot_offset=0x137D7D)
    assert len(manifest["batches"])==809 and len(manifest["checks"])==144
    base.save(MANIFEST,manifest)
    staged=base.load(stage.RECEIPT)
    startup=VERIFY/STARTUP.name
    release=previous | dict(profile=PROFILE,candidate=str(ROM),candidate_sha256=sha,patch=str(PATCH),
        patch_sha256=base.digest(PATCH),manifest=str(MANIFEST),manifest_sha256=base.digest(MANIFEST),
        registry_sha256=base.digest(registry_pending),predecessor=lineage,
        target_ARM9_sha256=staged["target_ARM9_sha256"],registered_manifest_entries=809,
        passing_release_checks=144,repository_tests=46,own_registered_startup=str(startup),
        own_registered_startup_sha256=base.digest(startup),changed_components=[source.ARM],changed_internal_files=[],
        new_contextual_records=0,prose_revisions=1,justified_retentions=8,reviewed_UI_labels=0,
        actual_verification_scope=dict(actual_emulator=True,hardware=False,observed_rules_pages=9,
            revised_page_mask_pass=True,exact_unrelated_and_return_frames=5,wireless_race_started=False))
    base.save(RELEASE,release)
    base.save(PACKAGE/"release_manifest.json",release | {"user_acceptance_pending":True})
    archive_file(MANIFEST.read_bytes(),PACKAGE/"build_manifest.json.gz")
    archive_file(registry_pending.read_bytes(),PACKAGE/"build_release_stack.json.gz")
    archive_file(before_ledger,ROOT/"editorial_ledger_before.json.gz")
    checkpoint="Grand Race rules review and the stopping-page revision are registered."
    ledger["current_integrated_candidate"].update(path=str(ROM),sha256=sha,profile=PROFILE,patch=str(PATCH),
        patch_sha256=release["patch_sha256"],manifest=str(MANIFEST),manifest_sha256=release["manifest_sha256"],
        ARM9_sha256=release["target_ARM9_sha256"],registered_release_verification=str(RELEASE))
    ledger["latest_checkpoint"]=checkpoint
    ledger["grand_race_stopping_rules_20261114"]=dict(review=str(REVIEW),release=str(RELEASE),
        revised_help_pages=1,retained_help_pages=8,new_dialogue_credit=0,exhibition_COMMON_318_consumer_pending=True)
    write_pending(ledger_pending,encode_ledger(ledger))
    change=dict(registry_before=source.current.assets.edit.digest(before_registry),registry_after=base.digest(registry_pending),
        ledger_before=source.current.assets.edit.digest(before_ledger),ledger_after=base.digest(ledger_pending),main_sha256=main_sha)
    base.save(VERIFY/"registration_mutation_plan.json",change)
    (PACKAGE/"README.md").write_text(f"""# Grand Race Help review candidate

The [local ROM](../../{ROM.as_posix()}) contains the revised Stopping a Race page and all prior cumulative work.
The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte.
Hardware testing and acceptance for main remain pending.
""",encoding="utf-8",newline="\n")
    base.save(PACKAGE/"checksums.json",package_checksums(PACKAGE))
    assert base.digest(base.REGISTRY)==change["registry_before"] and base.digest(base.LEDGER)==change["ledger_before"]
    assert base.digest(base.PROMOTED)==main_sha
    registry_pending.replace(base.REGISTRY)
    try:
        ledger_pending.replace(base.LEDGER)
    except OSError:
        base.replace_checked(base.REGISTRY,before_registry)
        raise
    assert base.digest(base.REGISTRY)==change["registry_after"] and base.digest(base.LEDGER)==change["ledger_after"]
    pins=Path("translations/rom_retention_pins.json")
    rows=base.load(pins)
    for path in (ROM,stage.ROM):
        resolved=str(path.resolve())
        assert not any(row["path"]==resolved for row in rows)
        rows.append(dict(path=resolved,reason=f"Preserve Grand Race stopping-page release and verification. SHA256 {sha}"))
    base.replace_checked(pins,(dumps(rows,ensure_ascii=False,indent=2)+"\n").replace("\n","\r\n").encode())
    base.replace_checked(DOC,f"""# Grand Race rules and quit behavior

All nine Grand Race rule pages received a contextual Japanese review and complete current glyph checks. Eight retain their English. **Stopping a Race** now explains that players cannot drop out individually after the race begins and that turning off even one DS ends the race for everyone. The revised page uses the existing ARM9 slot. The live replay found the complete revised glyph mask, and five surrounding frames matched exactly. The cumulative cold boot matched six startup frames and 24 protected name getters. All 46 targeted tests passed.

The original Grand Race help, save selection, Host waiting room and exit were observed using a copy of an ordinary save. No race started. Normal Lisbon **Quit Game** selected COMMON 319. Cancelling restored Functions. The tested Grand Race path requested no COMMON entry. A clean and current native fragment proves the aligned 318 literal at ARM9 offset F57A4 is a graphics table index. The stored exhibition warning still needs a proven caller elsewhere.

The [registered ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers. The ledger remains at 27,699 credited reviews and 277 mapped shared keys to review or classify. The candidate awaits acceptance for main and the full editorial review continues.
""".encode())
    prefix=f"# Current editorial checkpoint - 2026-11-14\n\n{checkpoint} [Checkpoint]({DOC.name})\n\n".encode()
    for name in ("editorial_handoff_current.md","translation_progress.md","build_continuity_protocol.md"):
        path=Path("docs")/name
        base.replace_checked(path,prefix+path.read_bytes())
    assert base.digest(base.PROMOTED)==main_sha
    print(f"Registered {ROM} | SHA-256 {sha} | 809 entries, 114 accepted layers, 144 checks.")


if __name__ == "__main__":
    main()

