"""Register the byte-owned cartridge banner as a cumulative testing release."""

from argparse import ArgumentParser
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from scripts import register_azores_wording_20261123 as previous
from scripts import stage_cartridge_title_20261123 as stage
from scripts.check_cartridge_title_release_inputs_20261123 import PATCH, PATCH_PROOF, REBUILT, STARTUP_CAPTURE
from scripts.reconcile_editorial_acceptance_20261123 import right_bound
from scripts.source_locked_derivation_v5118 import checked_text


base, workflow = previous.base, previous.workflow
mapped, write_update, snapshot_digest = previous.mapped, previous.write_update, previous.snapshot_digest
value, added_field, replace_value, archive = (
    previous.scope[key] for key in ("value", "added_field", "replace_value", "archive")
)
PROFILE = "all-routes-cartridge-title-v1-20261123"
CHECK = "registered_cartridge_title_banner_crc_and_complete_parent_inverse"
PACKAGE = previous.PACKAGE.with_name("all_routes_editorial_20261123_cartridge_title_candidate")
VERIFY = PACKAGE / "verification"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
MANIFEST = stage.ROM.with_suffix(".manifest.json")
REGISTRY_NEXT = stage.WORK / "release_stack_with_cartridge_title.json.gz"
LEDGER_NEXT = stage.WORK / "ledger_after.json.gz"
PLAN = VERIFY / "registration_mutation_plan.json"
STARTUP = stage.EVIDENCE / "own_startup_verification.json"
QA = stage.EVIDENCE / "qa_passed.xml"
DOC = Path("docs/editorial_cartridge_title_registered_20261123.md")
REGISTRY_BEFORE = previous.WORK / "release_stack_with_azores_wording.json.gz"
LEDGER_BEFORE = previous.LEDGER_NEXT
CHECKPOINT = "Registered the English cartridge title and preserved the original Japanese locale field."


def verify(parent, visual_sha):
    review, reconstruction = map(stage.read, (stage.PROOF, PATCH_PROOF))
    assert stage.digest(stage.SHEET) == review["preview"]["sha256"] == visual_sha
    assert review["candidate"]["sha256"] == reconstruction["candidate_sha256"] == stage.digest(stage.ROM)
    assert review["clean"]["sha256"] == reconstruction["clean_sha256"] == parent["clean_input_sha256"] == stage.digest(stage.CLEAN)
    assert review["parent"]["sha256"] == stage.digest(parent["candidate"]) == parent["candidate_sha256"]
    assert reconstruction["byte_exact"] and REBUILT.samefile(stage.ROM)
    assert stage.digest(PATCH) == reconstruction["patch"]["sha256"]
    current, candidate, clean = (Path(p).read_bytes() for p in (parent["candidate"], stage.ROM, stage.CLEAN))
    offset, old = stage.installed_banner(current)
    new_at, new = stage.installed_banner(candidate)
    clean_at, original = stage.installed_banner(clean)
    assert offset == new_at == review["banner_offset"]
    assert (new, review["records"]) == stage.replace_banner(old, original, offset, clean_at)
    assert candidate[:offset] + old + candidate[offset + stage.SIZE:] == current
    rom = stage.NdsImage.open(stage.ROM)
    arm = rom.read_file("/__arm9__.bin")
    assert right_bound(arm, parent["right_bound_configuration"])["matched_repair_spans"] == 8
    assert stage.sha256(arm).hexdigest() == parent["target_ARM9_sha256"]
    for i in range(4):
        assert stage.sha256(rom.read_file(f"/data/SC{i}.DK4")).hexdigest() == parent[f"target_SC{i}_sha256"]
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert [int(suite.get(k, "0")) for k in ("tests", "failures", "errors", "skipped")] == [17, 0, 0, 0]
    scope = previous.startup_scope | dict(STARTUP=STARTUP, STARTUP_CAPTURE=STARTUP_CAPTURE)
    routine = checked_text(previous.startup_source, {
        "compact_azores_payload_exact_and_startup_extent_preserved": "arm9_and_all_runtime_files_match_parent",
    })
    exec(compile(routine, __file__ + "::bound-startup", "exec"), scope)
    scope["startup_proof"](parent, review["candidate"]["sha256"], arm)
    prior = stage.read(previous.REVIEW)
    assert len(prior["shared_consumer_binding"]["records"]) == 276
    assert prior["shared_consumer_binding"]["candidate_sha256"] == parent["candidate_sha256"]
    return review | dict(candidate_sha256=review["candidate"]["sha256"],
        original_banner_sha256=stage.sha256(old).hexdigest(), installed_banner_sha256=stage.sha256(new).hexdigest(),
        shared_consumer_binding=prior["shared_consumer_binding"] | dict(candidate_sha256=review["candidate"]["sha256"]),
        retained_four_route_census_sha256=prior["retained_four_route_census_sha256"],
        retained_editorial_coverage_sha256=prior["retained_editorial_coverage_sha256"],
        visual_review=dict(path=str(stage.SHEET), sha256=visual_sha, all_six_locale_previews_inspected=True),
        physical_firmware_display_verified=False, no_new_dialogue_credit=True, full_editorial_goal_complete=False)


def prepare(visual_sha):
    parent = stage.read(stage.PARENT_RELEASE)
    assert stage.digest(base.REGISTRY) == parent["registry_sha256"] == snapshot_digest(REGISTRY_BEFORE)
    assert stage.digest(base.LEDGER) == snapshot_digest(LEDGER_BEFORE)
    assert stage.digest(parent["manifest"]) == parent["manifest_sha256"]
    assert not PLAN.exists() and not DOC.exists()
    outcome = verify(parent, visual_sha)
    candidate = outcome["candidate_sha256"]
    VERIFY.mkdir(parents=True, exist_ok=True)
    predecessor = {key: parent[key] for key in ("profile", "candidate", "candidate_sha256",
                       "manifest", "manifest_sha256", "registry_sha256")}
    predecessor.update(registry_snapshot=str(REGISTRY_BEFORE), registry_snapshot_format="gzip")
    with mapped(base.REGISTRY) as data:
        assert len(value(data, "accepted_layers", 2)) == 114
        _, start, end, _ = previous.scope["field"](data, "profiles", 2)
        profile = value(data, parent["profile"], 4, start, end)
        assert profile["source25_multiarchive_guard"] == previous.guard_spec()
        successor = profile | dict(verified_azores_wording_predecessor=predecessor, cartridge_title_release=str(REVIEW))
        write_update(data, REGISTRY_NEXT, [added_field(data, PROFILE, successor, 4, 2, start, end)])
    registry_hash = snapshot_digest(REGISTRY_NEXT)
    with mapped(REGISTRY_NEXT) as data:
        assert value(data, PROFILE, 4) == successor and value(data, parent["profile"], 4) == profile
        assert len(value(data, "accepted_layers", 2)) == 114
    stage.write(REVIEW, outcome)
    with mapped(Path(parent["manifest"])) as data:
        assert value(data, "candidate_sha256", 2) == parent["candidate_sha256"]
        assert value(data, "release_stack_sha256", 2) == parent["registry_sha256"]
        batches, checks, paths, records = (value(data, key, 2) for key in ("batches", "checks", "changed_paths", "changed_records"))
        assert len(batches) == 1102 and len(checks) == 437 and all(checks.values())
        assert stage.BANNER not in paths and stage.BANNER not in records and CHECK not in checks
        records[stage.BANNER] = [row["id"] for row in outcome["records"] if row["decision"] == "revision"]
        assert len(records[stage.BANNER]) == 5
        update = dict(profile=PROFILE, candidate_rom=str(stage.ROM), candidate_sha256=candidate,
                      release_stack_sha256=registry_hash, batches=[*batches, str(REVIEW)],
                      checks=checks | {CHECK: True}, changed_paths=sorted([*paths, stage.BANNER]), changed_records=records)
        node = dict(predecessor=predecessor, registered_review=stage.reference(REVIEW),
                    edit_driver=stage.reference(Path(stage.__file__)), registration_driver=stage.reference(Path(__file__)),
                    snapshot_scope=stage.BANNER, exact_complete_parent_inverse=True,
                    banner_release_proof=stage.reference(stage.PROOF), visual_review=outcome["visual_review"])
        write_update(data, MANIFEST, [*(replace_value(data, key, item, 2) for key, item in update.items()),
                                      added_field(data, "cartridge_title_pipeline", node, 2, 2)])
    with mapped(MANIFEST) as data:
        assert all(value(data, key, 2) == item for key, item in update.items())
        assert value(data, "cartridge_title_pipeline", 2) == node
    for path in (PATCH, STARTUP, QA, PATCH_PROOF, stage.SHEET, stage.PROOF):
        target = (PACKAGE if path == PATCH else VERIFY) / path.name
        copyfile(path, target)
        assert stage.digest(path) == stage.digest(target)
    copyfile(REGISTRY_NEXT, PACKAGE / "build_release_stack.json.gz")
    archive(MANIFEST, PACKAGE / "build_manifest.json.gz")
    assert snapshot_digest(PACKAGE / "build_release_stack.json.gz") == registry_hash
    assert snapshot_digest(PACKAGE / "build_manifest.json.gz") == stage.digest(MANIFEST)

    receipt = parent | dict(profile=PROFILE, candidate=str(stage.ROM), candidate_sha256=candidate,
        predecessor=predecessor, registry_sha256=registry_hash, manifest=str(MANIFEST), manifest_sha256=stage.digest(MANIFEST),
        patch=str(PACKAGE / PATCH.name), patch_sha256=stage.digest(PATCH), accepted_layers=114,
        registered_manifest_entries=1103, passing_release_checks=438, changed_components=1, changed_internal_files=[stage.BANNER],
        own_registered_startup=str(VERIFY / STARTUP.name), own_registered_startup_sha256=stage.digest(STARTUP),
        reviewed_UI_labels=5, contextual_records_revisited=0, contextual_decisions_reused=0, previously_localized_records=0,
        new_contextual_records=0, prose_revisions=0, justified_retentions=1, text_display_revisions=5,
        actual_verification_scope=dict(own_startup=True, host_preview_of_all_six_banner_fields=True,
            native_boot_frames=6, protected_getters=24, handheld_firmware_display=False, launcher_GUI_display=False))
    stage.write(RELEASE, receipt)
    stage.write(PACKAGE / "release_manifest.json", receipt | {"user_acceptance_pending": True})
    with mapped(base.LEDGER) as data:
        assert value(data, "records_editorially_completed", 1) == 27700 and not value(data, "full_goal_complete", 1)
        current = value(data, "current_integrated_candidate", 1)
        pending = value(data, "pending_shared_consumer_checkpoint_20261114", 1)
        assert current["sha256"] == pending["candidate_sha256"] == parent["candidate_sha256"]
        current.update(path=str(stage.ROM), sha256=candidate, profile=PROFILE, patch=receipt["patch"],
                       patch_sha256=receipt["patch_sha256"], manifest=str(MANIFEST), manifest_sha256=receipt["manifest_sha256"],
                       registered_release_verification=str(RELEASE))
        pending.update(candidate_sha256=candidate, latest_unchanged_record_binding=str(REVIEW))
        changes = dict(current_integrated_candidate=current, latest_checkpoint=CHECKPOINT,
                       pending_shared_consumer_checkpoint_20261114=pending)
        entry = dict(registered_candidate_sha256=candidate, registered_review=str(REVIEW), registered_release=str(RELEASE),
                     English_launcher_fields=5, original_Japanese_title_retained=True, new_contextual_credit=0)
        write_update(data, LEDGER_NEXT, [*(replace_value(data, k, v, 1) for k, v in changes.items()),
                                         added_field(data, "cartridge_title_20261123", entry, 1, 1)])
    with mapped(LEDGER_NEXT) as data:
        assert all(value(data, key, 1) == item for key, item in changes.items())
        assert value(data, "cartridge_title_20261123", 1) == entry
    stage.write(PLAN, dict(registry_before=parent["registry_sha256"], registry_after=registry_hash,
                          ledger_before=snapshot_digest(LEDGER_BEFORE), ledger_after=snapshot_digest(LEDGER_NEXT),
                          main_sha256=stage.digest(base.PROMOTED), registry_snapshot=str(REGISTRY_NEXT),
                          ledger_snapshot=str(LEDGER_NEXT)))
    (PACKAGE / "README.md").write_text(f"""# Cartridge title testing candidate

The cartridge banner displays **Uncharted Waters IV**, **Rota Nova**, and **KOEI** in the English and four fallback slots. The [clean-input patch](translation.xdelta) reconstructs the testing ROM with SHA-256 `{candidate}`.
""", encoding="utf-8")
    stage.write(PACKAGE / "checksums.json", workflow.package_checksums(PACKAGE))


def finish():
    plan, receipt = map(stage.read, (PLAN, RELEASE))
    assert stage.digest(stage.ROM) == receipt["candidate_sha256"] and stage.digest(MANIFEST) == receipt["manifest_sha256"]
    assert stage.digest(receipt["patch"]) == receipt["patch_sha256"]
    assert stage.read(PACKAGE / "checksums.json") == workflow.package_checksums(PACKAGE)
    files = ((base.REGISTRY, REGISTRY_BEFORE, REGISTRY_NEXT, "registry"), (base.LEDGER, LEDGER_BEFORE, LEDGER_NEXT, "ledger"))
    for live, before, after, key in files:
        assert snapshot_digest(before) == plan[f"{key}_before"] and snapshot_digest(after) == plan[f"{key}_after"]
        assert stage.digest(live) in (plan[f"{key}_before"], plan[f"{key}_after"])
    assert stage.digest(base.PROMOTED) == plan["main_sha256"]
    try:
        for live, _, after, key in files:
            previous.copy_in_place(after, live)
            assert stage.digest(live) == plan[f"{key}_after"]
    except (AssertionError, OSError):
        for live, before, _, key in files:
            previous.copy_in_place(before, live)
            assert stage.digest(live) == plan[f"{key}_before"]
        raise
    pins_path = Path("translations/rom_retention_pins.json")
    pins = stage.read(pins_path)
    path = str(stage.ROM.resolve())
    if all(pin["path"] != path for pin in pins):
        pins.append(dict(path=path, reason=f"Preserve the registered cartridge-title candidate {receipt['candidate_sha256']}"))
        base.replace_checked(pins_path, (previous.scope["dumps"](pins, indent=2, ensure_ascii=False) + "\n").replace("\n", "\r\n").encode())
    DOC.write_text(f"""# Cartridge title localization

The clean DS banner stores the Japanese title and publisher in all six language slots. The English title now reads **Uncharted Waters IV**, **Rota Nova**, and **KOEI**. The French, German, Italian, and Spanish slots also carry the English title for this release. The Japanese slot keeps its original text. The three rows preserve the title, subtitle, and publisher as distinct fields on display. [Exact source and installed references](../{REVIEW.as_posix()})

All six host-rendered previews were inspected. Both banner CRCs, the complete parent inverse, six ordinary game startup frames, 24 protected name getters, and 17 tests passed. The entire ROM outside the banner matches the Azores build. The preview uses host fonts. The actual firmware screen remains unverified. [Preview](../{VERIFY.as_posix()}/cartridge_title_preview.png) · [Clean-input patch](../{PACKAGE.as_posix()}/translation.xdelta)
""", encoding="utf-8")
    prefix = f"# Current editorial checkpoint - 2026-11-23\n\n{CHECKPOINT} [Checkpoint]({DOC.name})\n\n".encode()
    for name in ("editorial_handoff_current.md", "translation_progress.md", "build_continuity_protocol.md"):
        path = DOC.with_name(name)
        content = path.read_bytes()
        if not content.startswith(prefix):
            base.replace_checked(path, prefix + content)
    print(f"Registered {receipt['candidate_sha256']} with 1,103 entries and 438 passing checks.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--visual-sha256")
    parser.add_argument("--finish-only", action="store_true")
    arguments = parser.parse_args()
    if not arguments.finish_only:
        assert arguments.visual_sha256
        prepare(arguments.visual_sha256)
    finish()
