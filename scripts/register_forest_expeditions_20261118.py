"""Register the forest dialogue after native display, visual, replay and release checks."""

from argparse import ArgumentParser
from copy import deepcopy
from pathlib import Path
from shutil import copyfile
from struct import unpack_from
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.dialogue.reviewed_choice_object_v2 import count_and_base, labels
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import check_forest_replay_20261118 as live
from scripts import finish_ruin_statue_registration_20261118 as windows
from scripts import verify_forest_expeditions_20261118 as display


stage, base, native, parent = display.stage, display.base, display.native, display.parent
workflow = parent.workflow
PROFILE = "all-routes-forest-expeditions-v1-20261118"
ROOT = Path("out/forest_expeditions_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_Forest_Expeditions_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_forest_expeditions_candidate")
VERIFY = PACKAGE / "verification"
PATCH = PACKAGE / "translation.xdelta"
REVIEW = VERIFY / "registered_review.json"
RELEASE = VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_forest_expeditions_20261118.md")
STARTUP = stage.ROOT / "own_startup_verification.json"
QA = stage.ROOT / "supported_qa.xml"
HODRAM_WRAP = Path("releases/all_routes_editorial_20261114_hodram_final_wraps_candidate/verification/registered_review.json")


def sheets(native_receipt, replay):
    result = native_receipt["previous_sheets"] + native_receipt["sheets"]
    for entry in native_receipt["menus"]:
        proof = base.load(entry["menu_path"])
        assert base.digest(entry["menu_path"]) == entry["proof_sha256"]
        result += proof.get("review_sheets") or [proof["review_sheet"]]
    return result + [case["review_sheet"] for case in replay["cases"]]


def verify_retention(row, history, later):
    ident = row["id"]
    prior = history[row["earlier_ledger"]][ident]
    assert prior["review"]["formatting"]
    reference = prior["planned_integrated_reference"]
    if ident == "DK4_MES_B290_R0278":
        assert later["review"]["formatting"]
        assert later["registered_reference"]["raw_hex"] == later["target_hex"] == row["current_hex"]
        return dict(path=str(HODRAM_WRAP), sha256=base.digest(HODRAM_WRAP), record_id=ident)
    assert reference["exact_stored_hex"] == row["current_hex"]
    return dict(path=row["earlier_ledger"], sha256=row["earlier_ledger_sha256"], record_id=ident)


def bind_records(draft, stage_proof, banks, candidate, receipt, replay):
    rows = {(row["file_path"], row["id"]): row for row in draft["records"]}
    assert len(rows) == 370
    paths = {row["earlier_ledger"]: row["earlier_ledger_sha256"] for row in rows.values()}
    history = {}
    for path, sha in paths.items():
        assert base.digest(path) == sha
        history[path] = {row["id"]: row for row in base.load(path)["records"]}
    later = next(r for r in base.load(HODRAM_WRAP)["records"] if r["id"] == "DK4_MES_B290_R0278")
    rendered = {(r["file_path"], r["id"]): r for r in receipt["checked_paragraphs"]}
    caption_proofs = {ident: m for m in receipt["menus"] for ident in m["option_ids"]}
    observed = {hold["id"] for case in replay["cases"] for hold in case["body_holds"]}
    observed_menus = {(3, sample["source_command_offset"]) for case in replay["cases"] for sample in case["menu_displays"]}
    bound = set()
    for group in stage_proof["groups"]:
        file, n = group["file_path"], group["block"]
        block = native.IlnkContainer.parse(banks[file]).blocks[n]
        assert native.digest(block) == group["after"]
        for cmd in group["commands"]:
            if not cmd["record_ids"]:
                continue
            at, word = cmd["stored_offset"], cmd["word"]
            raw = bytes.fromhex(cmd["stored"])
            assert block[at:at + len(raw)] == raw
            if word == stage.STYLE:
                offsets, texts = display.unpack(raw)
                entries = [(at + 20 + i, raw[19], texts[i], [j for j, off in enumerate(offsets) if off == i])
                           for i in sorted(texts)]
            elif word in stage.MENU:
                count, header = count_and_base(raw)
                entries = [(at + header + unpack_from("<H", raw, 2 + 2 * i)[0], None, text, [i])
                           for i, text in enumerate(labels(raw))]
                assert count == len(entries)
            else:
                assert word == stage.SPEECH
                entries = [(at + 5, raw[5], raw[5:raw.index(0, 6)], [])]
            for ident, (offset, selector, stored, indices) in zip(cmd["record_ids"], entries, strict=True):
                key = file, ident
                row = rows[key]
                assert key not in bound and block[offset:offset + len(stored)] == stored
                if row["decision"] == "retention":
                    assert stored.hex() == row["current_hex"]
                    row["formatting_evidence"] = verify_retention(row, history, later)
                    row["display_scope"] = "Byte-identical retention with registered formatting evidence"
                else:
                    if word in stage.MENU:
                        proof = caption_proofs[ident]
                        assert proof["candidate_menu_offset"] == at
                        row["formatting_evidence"] = dict(path=proof["menu_path"], sha256=proof["proof_sha256"],
                                                          source_option_index=indices[0])
                    else:
                        proof = rendered[key]
                        body = bytes([selector]) + stored if word == stage.STYLE else stored
                        assert proof["target_hex"] == body.hex()
                        row["formatting_evidence"] = dict(path=str(display.OUTPUT / "native_display.json"),
                                                          record_id=ident)
                    row["display_scope"] = "Native display and direct visual review"
                if ident in observed or (word in stage.MENU and (group["route"], cmd["source_offset"]) in observed_menus):
                    row["display_scope"] += " with initialized Maria emulator evidence"
                row["registered_reference"] = dict(candidate_sha256=candidate, file_path=file, block=n,
                    offset=offset, command_offset=at, exact_stored_hex=stored.hex(),
                    native_command_word=word, source_selector=selector, native_slots=indices,
                    archive_sha256=native.digest(banks[file]))
                row["review"]["formatting"] = True
                bound.add(key)
    assert bound == rows.keys()
    draft.update(encoder="dialogue-relocatable-v1", review_gates=["source", "context", "localization",
        "naturalness", "formatting"], formatting_and_registration_pending=False, registered=True)
    validate_natural_dialogue_batch(draft)
    return draft


def verify(registry, prior, reviewed):
    proof, rendered, replay, startup = map(base.load, (stage.PROOF, display.OUTPUT / "native_display.json",
                                                       live.OUTPUT, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == proof["candidate_sha256"] == rendered["compiled_candidate_sha256"]
    assert candidate == replay["candidate_sha256"] == startup["candidate_sha256"]
    assert startup["cold_boot"] and not startup["savestate"] and startup["complete_deployed_payload_exact"]
    assert len(startup["exact_matching_frames"]) == 6 and len(startup["original_protected_name_getters"]) == 24
    assert all(base.digest(path) == sha for path, sha in startup["evidence"].items())
    assert proof["manuscript_sha256"] == base.digest(stage.review.MANUSCRIPT)
    assert rendered["stage_proof_sha256"] == base.digest(stage.PROOF)
    assert proof["whole_parent_inverse"] and proof["predecessor_sha256"] == prior["candidate_sha256"]
    assert rendered["exact_revised_record_count"] == 87 and rendered["fresh_paragraphs"] == 8
    assert replay["initialized_emulator"] and not replay["hardware"] and not replay["natural_activation"]
    assert replay["cases"][-1]["exact_final_candidate_fixture"]
    assert all(base.digest(case["report"]) == case["report_sha256"] and
               base.digest(case["fixture"]) == case["fixture_sha256"] for case in replay["cases"])
    captures = [item["capture"] for case in replay["cases"] for item in case["menu_displays"] + case["body_holds"]]
    assert all(base.digest(item["path"]) == item["PNG_sha256"] for item in captures)
    visual = sheets(rendered, replay)
    assert len(visual) == 20 and reviewed == {item["path"]: item["sha256"] for item in visual}
    assert all(base.digest(path) == expected for path, expected in reviewed.items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert int(suite.get("tests", 0)) == 32
    assert all(int(suite.get(k, 0)) == 0 for k in ("errors", "failures", "skipped"))

    clean, before, target = map(base.NdsImage.open, (native.CLEAN, parent.ROM, stage.ROM))
    assert proof["source_sha256"] == prior["clean_input_sha256"] == base.digest(native.CLEAN)
    old, new = map(native.files, (before, target))
    assert old.keys() == new.keys()
    paths = {g["file_path"]: g["block"] for g in proof["groups"]}
    assert {p for p in old if old[p] != new[p]} == paths.keys()
    for path, block in paths.items():
        old_bank, new_bank = [native.IlnkContainer.parse(bank[path]).blocks for bank in (old, new)]
        assert [i for i, (a, b) in enumerate(zip(old_bank, new_bank, strict=True)) if a != b] == [block]
        target.replace_file(path, old[path])
    assert bytes(target.rom.save()) == parent.ROM.read_bytes()
    guard = bind_registered_story_percent_guard(registry["profiles"][prior["profile"]]["source25_multiarchive_guard"])
    control = guard(native.files(clean), new)
    assert control["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(control["source_bound_new_command_counts"].values())
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    draft = bind_records(base.load(stage.review.MANUSCRIPT), proof, new, candidate, rendered, replay)
    draft.update(candidate_sha256=candidate, approved_source25=control,
                 visual_review=visual, initialized_emulator_cases=replay["cases"],
                 native_display_sha256=base.digest(display.OUTPUT / "native_display.json"))
    return proof, draft, {p: native.digest(new[p]) for p in paths}


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--visual-review", type=Path, required=True)
    args = parser.parse_args()
    assert not any(p.exists() for p in (ROOT, PACKAGE, DOC))
    registry_before, ledger_before = base.REGISTRY.read_bytes(), base.LEDGER.read_bytes()
    main_digest = base.digest(base.PROMOTED)
    registry, ledger, prior, manifest = map(base.load, (base.REGISTRY, base.LEDGER, parent.RELEASE, parent.MANIFEST))
    assert native.digest(registry_before) == prior["registry_sha256"] == manifest["release_stack_sha256"]
    assert base.digest(parent.MANIFEST) == prior["manifest_sha256"]
    assert manifest["candidate_sha256"] == prior["candidate_sha256"] == base.digest(parent.ROM)
    assert len(registry["accepted_layers"]) == 114 and PROFILE not in registry["profiles"]
    assert len(manifest["batches"]) == 861 and len(manifest["checks"]) == 196 and all(manifest["checks"].values())
    verify_record, draft, archives = verify(registry, prior, base.load(args.visual_review))
    candidate = draft["candidate_sha256"]
    keys = {(r["file_path"], r["id"]) for r in ledger[base.CONTEXT]["integrated_record_keys"]}
    assert len(keys) == ledger["records_editorially_completed"] == 27700
    assert all((row["file_path"], row["id"]) in keys for row in draft["records"])
    pending = ledger["pending_shared_consumer_checkpoint_20261114"]
    assert pending["remaining_total"] == 276 and pending["candidate_sha256"] == prior["candidate_sha256"]
    assert ledger["current_integrated_candidate"]["sha256"] == prior["candidate_sha256"]
    edited = [r for r in draft["records"] if r["decision"] == "revision"]
    assert len(edited) == 87 and not ledger["full_goal_complete"]

    ROOT.mkdir()
    VERIFY.mkdir(parents=True)
    copyfile(stage.ROOT / "clean_input.xdelta", PATCH)
    copyfile(stage.ROOT / "clean_rebuilt.nds", ROM)
    assert base.digest(ROM) == candidate
    assert base.digest(PATCH) == base.digest(stage.ROOT / "clean_input.xdelta")
    for src in (stage.PROOF, STARTUP, QA, live.OUTPUT, live.replay.FIXTURE,
                display.OUTPUT / "native_display.json", args.visual_review):
        dst = VERIFY / src.name
        copyfile(src, dst)
        assert base.digest(src) == base.digest(dst)
    for case in draft["initialized_emulator_cases"]:
        item = case["review_sheet"]
        dst = VERIFY / Path(item["path"]).name
        copyfile(item["path"], dst)
        assert base.digest(dst) == item["sha256"]
    final_sheet, = base.load(display.OUTPUT / "native_display.json")["sheets"]
    copyfile(final_sheet["path"], VERIFY / "final_phrase_wraps.png")
    assert base.digest(VERIFY / "final_phrase_wraps.png") == final_sheet["sha256"]
    base.save(REVIEW, draft)
    predecessor = {k: prior[k] for k in ("profile", "candidate", "candidate_sha256", "manifest", "manifest_sha256",
                                          "registry_sha256")}
    backup = ROOT / "release_stack_before_forest_expeditions.json"
    backup.write_bytes(registry_before)
    predecessor["registry"] = str(backup)
    profile = deepcopy(registry["profiles"][prior["profile"]])
    profile.update(verified_bounty_assignments_predecessor=predecessor, forest_expeditions_release=str(REVIEW))
    registry["profiles"][PROFILE] = profile
    staged_registry = ROOT / "release_stack_with_forest_expeditions.json"
    base.save(staged_registry, registry)
    registry_sha = base.digest(staged_registry)
    manifest.update(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=candidate, release_stack_sha256=registry_sha)
    manifest["batches"].append(str(REVIEW))
    manifest["checks"]["registered_forest_expeditions_and_complete_parent_inverse"] = True
    for row in edited:
        records = manifest["changed_records"][row["file_path"]]
        if row["id"] not in records:
            records.append(row["id"])
    manifest["forest_expeditions_pipeline"] = dict(
        predecessor=predecessor, registered_review=str(REVIEW), registered_review_sha256=base.digest(REVIEW),
        stored_proof_sha256=base.digest(stage.PROOF), native_display_sha256=draft["native_display_sha256"],
        registration_driver_sha256=base.digest(__file__), producer_sha256=base.digest(stage.__file__),
        complete_parent_inverse=True,
        owned_story_blocks={g["file_path"]: [g["block"]] for g in verify_record["groups"]})
    base.save(MANIFEST, manifest)
    archived_startup = VERIFY / STARTUP.name
    release = prior | dict(profile=PROFILE, candidate=str(ROM), candidate_sha256=candidate, patch=str(PATCH),
        patch_sha256=base.digest(PATCH), manifest=str(MANIFEST), manifest_sha256=base.digest(MANIFEST),
        registry_sha256=registry_sha, predecessor=predecessor, registered_manifest_entries=len(manifest["batches"]),
        passing_release_checks=len(manifest["checks"]), own_registered_startup=str(archived_startup),
        own_registered_startup_sha256=base.digest(archived_startup), changed_internal_files=sorted(archives),
        repository_tests=32, new_contextual_records=0, prose_revisions=87, justified_retentions=283,
        name_label_revisions=0, text_display_revisions=0, final_phrase_refinements_within_revised_prose=8,
        actual_verification_scope=dict(own_startup=True, initialized_Maria_forest=True, natural_activation=False, hardware=False),
        **{f"target_SC{i}_sha256": archives[f"/data/SC{i}.DK4"] for i in range(4)})
    base.save(RELEASE, release)
    base.save(PACKAGE / "release_manifest.json", release | {"user_acceptance_pending": True})
    workflow.archive_file(MANIFEST.read_bytes(), PACKAGE / "build_manifest.json.gz")
    workflow.archive_file(staged_registry.read_bytes(), PACKAGE / "build_release_stack.json.gz")
    workflow.archive_file(ledger_before, ROOT / "editorial_ledger_before.json.gz")
    pending["candidate_sha256"] = candidate
    ledger["current_integrated_candidate"].update(path=str(ROM), sha256=candidate, profile=PROFILE,
        patch=str(PATCH), patch_sha256=release["patch_sha256"], manifest=str(MANIFEST),
        manifest_sha256=release["manifest_sha256"], registered_release_verification=str(RELEASE),
        **{f"SC{i}_sha256": release[f"target_SC{i}_sha256"] for i in range(4)})
    checkpoint = "The forest expeditions and bear choices are reviewed across all four routes."
    ledger["forest_expeditions_20261118"] = dict(registered_candidate_sha256=candidate, registered_review=str(REVIEW),
        registered_release=str(RELEASE), existing_credit=370, prose_revisions=87, justified_retentions=283,
        final_phrase_refinements_within_revised_prose=8, new_contextual_credit=0)
    ledger["latest_checkpoint"] = checkpoint
    ledger_after = workflow.encode_ledger(ledger)
    base.save(VERIFY / "registration_mutation_plan.json", dict(registry_before=native.digest(registry_before),
        ledger_before=native.digest(ledger_before), registry_after=registry_sha,
        ledger_after=native.digest(ledger_after), main_sha256=main_digest))
    (PACKAGE / "README.md").write_text(f"""# Forest expeditions test candidate

The [local ROM](../../{ROM.as_posix()}) includes the forest dialogue and the bear menus across all four routes.
The [clean-input patch](translation.xdelta) reconstructs ROM SHA-256 `{candidate}` byte for byte.
Main awaits user acceptance. Hardware and natural activation remain unverified.
""", encoding="utf-8", newline="\n")
    base.save(PACKAGE / "checksums.json", workflow.package_checksums(PACKAGE))
    assert base.REGISTRY.read_bytes() == registry_before and base.LEDGER.read_bytes() == ledger_before
    assert base.digest(base.PROMOTED) == main_digest
    base.replace_checked(base.REGISTRY, staged_registry.read_bytes())
    try:
        windows.update_ledger_in_place(ledger_before, ledger_after)
    except (AssertionError, OSError):
        base.replace_checked(base.REGISTRY, registry_before)
        raise
    assert base.digest(base.REGISTRY) == registry_sha and base.LEDGER.read_bytes() == ledger_after
    pins_path = Path("translations/rom_retention_pins.json")
    pins = base.load(pins_path)
    older = stage.ROOT.with_name("research_v1")
    for path in (ROM, stage.ROM, older / stage.ROM.name, live.replay.ROM,
                 older / live.replay.ROOT.name / live.replay.ROM.name):
        resolved = str(path.resolve())
        if all(entry["path"] != resolved for entry in pins):
            pins.append(dict(path=resolved, reason=f"Preserve forest expedition candidate or emulator fixture {base.digest(path)}"))
    base.replace_checked(pins_path, (workflow.dumps(pins, ensure_ascii=False, indent=2) + "\n")
                         .replace("\n", "\r\n").encode())
    DOC.write_text(f"""# Forest expeditions and bear choices

Reviewed 370 records in SC0 B293, SC1 B290, SC2 B283 and SC3 B252. The ledger records 87 revisions and 283 justified retentions. The wording preserves the different crew voices, deliberate hesitation, and the distinct consequences of standing, hiding, scaring the bear or running. “Try something else” leads to a second menu. The two revised injury notices keep the injuries minor and avoid specifying a count. [Exact review ledger](../{REVIEW.as_posix()})

Native display checks covered 76 progressive pages, two system notices and six menus. Eight pages received fresh checks after a final phrase-wrap adjustment. The 30 revised speech-style objects preserve their native alternatives and aliases. The clean and stored commands preserve all four scenes' original branch destinations. [Final phrase wraps](../{(VERIFY / 'final_phrase_wraps.png').as_posix()})

An initialized DeSmuME replay on the final layout covered both of Maria's bear menus, the scare-off reply, the injury notice and arrival at the ruins. Compatible captures from the first layout also show the run reply and the minor-injury notice after fighting. The other routes and the unvisited outcomes and voice variants were checked offline. Hardware and natural activation remain unverified. [Final replay](../{(VERIFY / 'live_other_scare.png').as_posix()})

The clean-input patch rebuilds the exact ROM with all 114 accepted layers and the registered ASCII right-bound correction. The candidate passed six cold-boot holds, 24 protected name getters and 32 repository tests. The 370 records already had coverage credit, so the totals remain 27,700 credited records and 276 shared keys still open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
    prefix = f"# Current editorial checkpoint - 2026-11-18\n\n{checkpoint} [Checkpoint]({DOC.name})\n\n".encode()
    for name in ("editorial_handoff_current.md", "translation_progress.md", "build_continuity_protocol.md"):
        path = DOC.with_name(name)
        base.replace_checked(path, prefix + path.read_bytes())
    assert base.digest(base.PROMOTED) == main_digest
    print(f"Registered {candidate} with {len(manifest['batches'])} entries, 114 accepted layers and "
          f"{len(manifest['checks'])} passing checks.", flush=True)


if __name__ == "__main__":
    main()
