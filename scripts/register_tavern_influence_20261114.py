"""Register the verified Tavern rumor and reconstruct it from clean Japanese."""

from copy import deepcopy
from json import dumps
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import stage_tavern_influence_20261114 as stage
from scripts import verify_tavern_influence_20261114 as live
from scripts.checkpoint_current_town_replays_20261114 import OUTPUT as TOWNS
from scripts.editorial_ledger_storage_v1 import encode_ledger
from scripts.prepare_all_routes_promotion_20261111 import package_checksums, verify_runtime
from scripts.register_lil_ceramics_wrap_20261111 import archive_file, write_pending
from scripts.verify_release_baseline import files

base, parent = stage.base, stage.parent
PROFILE = "all-routes-tavern-influence-v1-20261114"
ROOT = Path("out/tavern_influence_registered_20261114_v1")
ROM = ROOT/"Translation_DS_All_Routes_Tavern_Influence_20261114_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261114_tavern_influence_candidate")
PATCH, VERIFY = PACKAGE/"translation.xdelta", PACKAGE/"verification"
REVIEW = VERIFY/"registered_review.json"
RELEASE = VERIFY/"registered_release_verification.json"
DOC = Path("docs/editorial_tavern_influence_registered_20261114.md")
STARTUP, QA = stage.ROOT/"own_startup_verification.json", stage.ROOT/"repository_qa.xml"
VIEWED = "81e3e04dffb124a62d48ecb4b992d1318b7b532ecfb9026e7936fa407d0678d5"


def verify(prior, guard):
    storage, review, boot, towns = map(base.load,(stage.STORED,live.OUT,STARTUP,TOWNS))
    assert base.digest(stage.ROM) == storage["candidate_sha256"] == review["candidate_sha256"] == boot["candidate_sha256"]
    assert base.digest(parent.ROM) == prior["candidate_sha256"] == storage["previous_sha256"] == towns["candidate_sha256"]
    assert base.digest(stage.CLEAN) == prior["clean_input_sha256"]
    assert storage["whole_parent_inverse"] and storage["preserved_entries"]==3667 and storage["preserved_blocks"]==40
    assert review["native_layout"]["distinct_tested_cases"] == 17
    assert base.digest(review["native_layout"]["sheet"]) == review["native_layout"]["sheet_sha256"] == VIEWED
    assert len(review["observed_gameplay"]["unmodified_holds"]) == 13
    assert sum(len(row["cases"]) for row in towns["current_town_observations"].values()) == 16
    assert boot["cold_boot"] and not boot["savestate"] and boot["complete_deployed_payload_exact"]
    assert len(boot["exact_matching_frames"]) == 6 and len(boot["original_protected_name_getters"]) == 24
    for group in (review["observed_gameplay"]["evidence"],boot["evidence"]):
        assert all(base.digest(path)==digest for path,digest in group.items())
    tests, = ElementTree.parse(QA).iter("testsuite")
    assert tuple(int(tests.get(key,0)) for key in ("tests","failures","errors","skipped")) == (28,0,0,2)
    previous, revised = map(base.NdsImage.open,(parent.ROM,stage.ROM))
    a,b = files(previous),files(revised)
    assert a.keys() == b.keys() and {p for p in a if a[p]!=b[p]} == {stage.COMMON}
    verify_runtime(b[stage.ARM],prior)
    digest = parent.source.current.assets.edit.digest
    assert digest(b[stage.COMMON]) == storage["target_COMMON_sha256"]
    checked = bind_registered_story_percent_guard(guard)(files(base.NdsImage.open(stage.CLEAN)),b)
    assert checked["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(checked["source_bound_new_command_counts"].values())
    revised.replace_file(stage.COMMON,a[stage.COMMON])
    assert bytes(revised.rom.save()) == parent.ROM.read_bytes()
    row, = review["records"]
    row["registered_reference"] = row["staged_reference"] | dict(exact_stored_hex=row["staged_hex"],candidate_sha256=storage["candidate_sha256"])
    return storage, review | dict(checked_story_format_guard=checked, direct_visual_review_complete=True,
        current_town_receipt=str(TOWNS),current_town_receipt_sha256=base.digest(TOWNS))


def main():
    before_registry, before_ledger = base.REGISTRY.read_bytes(),base.LEDGER.read_bytes()
    registry, ledger, manifest, prior = map(base.load,(base.REGISTRY,base.LEDGER,parent.MANIFEST,parent.RELEASE))
    assert base.digest(base.REGISTRY) == prior["registry_sha256"] and base.digest(parent.MANIFEST) == prior["manifest_sha256"]
    assert ledger["current_integrated_candidate"]["sha256"] == prior["candidate_sha256"]
    assert ledger["records_editorially_completed"] == 27699 and not ledger["full_goal_complete"]
    assert len(registry["accepted_layers"]) == 114 and PROFILE not in registry["profiles"]
    assert len(manifest["batches"]) == 810 and len(manifest["checks"]) == 145 and all(manifest["checks"].values())
    main_sha = base.digest(base.PROMOTED)
    profile = deepcopy(registry["profiles"][prior["profile"]])
    staged, review = verify(prior,profile["source25_multiarchive_guard"])
    reg_tmp = base.REGISTRY.with_name("release_stack.tavern_influence.pending.json")
    ledger_tmp = base.LEDGER.with_name("editorial_review_current.tavern_influence.pending.json")
    assert not any(p.exists() for p in (ROOT,PACKAGE,DOC,reg_tmp,ledger_tmp))
    ROOT.mkdir()
    VERIFY.mkdir(parents=True)
    make_xdelta(stage.CLEAN,stage.ROM,PATCH)
    apply_xdelta(stage.CLEAN,PATCH,ROM)
    sha = base.digest(ROM)
    assert sha == review["candidate_sha256"] and ROM.read_bytes() == stage.ROM.read_bytes()
    for p in (stage.STORED,live.OUT,STARTUP,QA,TOWNS):
        copyfile(p,VERIFY/p.name)
        assert base.digest(p) == base.digest(VERIFY/p.name)
    base.save(REVIEW,review)
    backup = ROOT/"release_stack_before_tavern_influence.json"
    backup.write_bytes(before_registry)
    lineage = {k:prior[k] for k in ("profile","candidate","candidate_sha256","manifest","manifest_sha256","registry_sha256")}
    lineage["registry"] = str(backup)
    profile.update(verified_about_extras_predecessor=lineage, tavern_influence_release=str(REVIEW),
        note="Natural barkeep wording and verified native display for COMMON 821.")
    registry["profiles"][PROFILE] = profile
    base.save(reg_tmp,registry)
    manifest.update(profile=PROFILE,candidate_rom=str(ROM),candidate_sha256=sha,release_stack_sha256=base.digest(reg_tmp))
    manifest["batches"].append(str(REVIEW))
    manifest["checks"]["registered_tavern_influence_and_complete_parent_inverse"] = True
    assert stage.COMMON in manifest["changed_paths"]
    ids = manifest["changed_records"][stage.COMMON]
    if "COMMON_MESSAGE_821" not in ids:
        ids.append("COMMON_MESSAGE_821")
    manifest["tavern_influence_registered_successor_pipeline"] = dict(predecessor=lineage,review=str(REVIEW),
        review_sha256=base.digest(REVIEW),producer=stage.__file__,producer_sha256=base.digest(stage.__file__),
        registered_driver=__file__,registered_driver_sha256=base.digest(__file__),
        complete_parent_inverse=True, native_allocation=staged["byte_allocation"])
    base.save(MANIFEST,manifest)
    startup = VERIFY/STARTUP.name
    release = prior | dict(profile=PROFILE,candidate=str(ROM),candidate_sha256=sha,patch=str(PATCH),
        patch_sha256=base.digest(PATCH),manifest=str(MANIFEST),manifest_sha256=base.digest(MANIFEST),
        registry_sha256=base.digest(reg_tmp),predecessor=lineage,target_COMMON_sha256=staged["target_COMMON_sha256"],
        registered_manifest_entries=811,passing_release_checks=146,repository_tests=26,legacy_fixture_tests_skipped=2,
        own_registered_startup=str(startup),own_registered_startup_sha256=base.digest(startup),
        changed_components=[],changed_internal_files=[stage.COMMON],new_contextual_records=0,
        prose_revisions=1,justified_retentions=11,reviewed_UI_labels=0,actual_verification_scope=dict(
            actual_emulator=True,hardware=False,observed_revised_rumors=1,retained_observed_holds=13,
            offline_role_and_name_variants=17))
    base.save(RELEASE,release)
    base.save(PACKAGE/"release_manifest.json",release | {"user_acceptance_pending":True})
    archive_file(MANIFEST.read_bytes(),PACKAGE/"build_manifest.json.gz")
    archive_file(reg_tmp.read_bytes(),PACKAGE/"build_release_stack.json.gz")
    archive_file(before_ledger,ROOT/"editorial_ledger_before.json.gz")
    checkpoint = "The Istanbul barkeep’s influence rumor is registered, with current coverage in three towns."
    ledger["current_integrated_candidate"].update(path=str(ROM),sha256=sha,profile=PROFILE,patch=str(PATCH),
        patch_sha256=release["patch_sha256"],manifest=str(MANIFEST),manifest_sha256=release["manifest_sha256"],
        MESFILE_sha256=release["target_COMMON_sha256"],registered_release_verification=str(RELEASE))
    ledger["latest_checkpoint"] = checkpoint
    ledger["tavern_influence_review_20261114"] = dict(review=str(REVIEW),release=str(RELEASE),town_coverage=str(TOWNS),
        revised_existing_key=821,new_dialogue_credit=0,followup_key=827,known_pending_counts_unchanged=True)
    write_pending(ledger_tmp,encode_ledger(ledger))
    digest = parent.source.current.assets.edit.digest
    planned = dict(registry_before=digest(before_registry),registry_after=base.digest(reg_tmp),
        ledger_before=digest(before_ledger),ledger_after=base.digest(ledger_tmp),main_sha256=main_sha)
    base.save(VERIFY/"registration_mutation_plan.json",planned)
    (PACKAGE/"README.md").write_text(f"""# Tavern Influence test candidate

The [local ROM](../../{ROM.as_posix()}) includes the revised Istanbul Tavern rumor.
The [clean-input patch](translation.xdelta) reconstructs SHA-256 `{sha}` byte for byte. It awaits hardware testing and acceptance for main.
""",encoding="utf-8",newline="\n")
    base.save(PACKAGE/"checksums.json",package_checksums(PACKAGE))
    assert base.digest(base.REGISTRY) == planned["registry_before"] and base.digest(base.LEDGER) == planned["ledger_before"]
    assert base.digest(base.PROMOTED) == main_sha
    reg_tmp.replace(base.REGISTRY)
    try:
        ledger_tmp.replace(base.LEDGER)
    except OSError:
        base.replace_checked(base.REGISTRY,before_registry)
        raise
    assert base.digest(base.REGISTRY) == planned["registry_after"] and base.digest(base.LEDGER) == planned["ledger_after"]
    pins = Path("translations/rom_retention_pins.json")
    existing = base.load(pins)
    for path in (ROM,stage.ROM):
        resolved = str(path.resolve())
        assert not any(r["path"]==resolved for r in existing)
        existing.append(dict(path=resolved,reason=f"Preserve Tavern rumor release and verified replay. SHA256 {sha}"))
    base.replace_checked(pins,(dumps(existing,ensure_ascii=False,indent=2)+"\n").replace("\n","\r\n").encode())
    base.replace_checked(DOC,f"""# Istanbul Tavern and current town replay coverage

The barkeep's influence rumor, COMMON 821, now reads “Hayreddin from Alexandria is a pirate with real pull here” in the observed exchange. The revised wording preserves the source's local influence and casual tone, distinct from the neighboring formal reputation report. All three substitutions stay in their original order. The complete clean and prior English records are preserved in the [registered review](../{REVIEW.as_posix()}).

The current replay verifies the entire revised two-line panel and thirteen identical surrounding holds. Seventeen controlled native layout and glyph pages include all four role values and the shortest and longest supplied names and towns. These layouts are offline. The cumulative cold boot verifies six startup frames and 24 protected getters using the existing system-only unlock fixture. Twenty-six targeted tests passed. Two older tests skipped because their V99 and V101 fixtures were unavailable.

Three ordinary replays supply sixteen complete dialogue holds across the Nagasaki Tavern and Inn, the Istanbul Tavern and the Amsterdam Market. The [observed-town ledger](../{TOWNS.as_posix()}) includes exact source/current references, individual retentions and an open follow-up for COMMON 827. Its toast currently calls the relationship a new friendship. The Japanese toasts the introduction. These runs add representative regional coverage without new dialogue credit. Amsterdam Square and additional conditional town conversations remain unvisited in these replays.

The [registered test ROM and exact clean-input patch](../{PACKAGE.as_posix()}/README.md) preserve all 114 accepted layers and the ASCII right bound. The ledger still credits 27,699 reviews. There are 277 mapped shared keys left to review or classify. Hardware testing remains open.
""".encode())
    prefix = f"# Current editorial checkpoint - 2026-11-14\n\n{checkpoint} [Checkpoint]({DOC.name})\n\n".encode()
    for name in ("editorial_handoff_current.md","translation_progress.md","build_continuity_protocol.md"):
        path = Path("docs")/name
        base.replace_checked(path,prefix+path.read_bytes())
    assert base.digest(base.PROMOTED) == main_sha
    print(f"Registered {ROM} SHA-256 {sha}. 811 entries, 114 accepted layers, 146 checks.")


if __name__ == "__main__":
    main()
