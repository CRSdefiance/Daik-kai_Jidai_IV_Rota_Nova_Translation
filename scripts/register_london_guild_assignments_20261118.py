"""Register the reviewed London and Malacca assignments with exact clean reconstruction."""

from argparse import ArgumentParser
from collections import Counter
from copy import deepcopy
from pathlib import Path
from shutil import copyfile
from xml.etree import ElementTree

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.script.format_safety_relocated_v2 import bind_registered_story_percent_guard
from scripts import finish_ruin_statue_registration_20261118 as windows
from scripts import replay_london_guild_assignments_20261118 as replay
from scripts import verify_london_guild_assignments_20261118 as display


stage, base, native, parent = display.build, display.base, display.native, display.parent
workflow = parent.workflow
PROFILE = "all-routes-london-malacca-guild-assignments-v1-20261118"
ROOT = Path("out/london_malacca_guild_assignments_registered_20261118_v1")
ROM = ROOT / "Translation_DS_All_Routes_London_Malacca_Guild_Assignments_20261118_candidate.nds"
MANIFEST = ROM.with_suffix(".manifest.json")
PACKAGE = Path("releases/all_routes_editorial_20261118_london_malacca_guild_assignments_candidate")
VERIFY, PATCH = PACKAGE / "verification", PACKAGE / "translation.xdelta"
REVIEW, RELEASE = VERIFY / "registered_review.json", VERIFY / "registered_release_verification.json"
DOC = Path("docs/editorial_london_malacca_guild_assignments_20261118.md")
STARTUP, QA = stage.ROOT / "own_startup_verification.json", stage.ROOT / "supported_qa.xml"
GATES = ["source", "context", "localization", "naturalness", "formatting"]
QUESTION = Path("releases/all_routes_editorial_20261111_story_question_wraps_candidate/verification/registered_review.json")
RAFAEL = Path("releases/all_routes_editorial_20261114_rafael_quest_wraps_candidate/verification/registered_review.json")
LATER_RETENTIONS = {"DK4_MES_B296_R0052": QUESTION, "DK4_MES_B295_R0049": RAFAEL, "DK4_MES_B299_R0077": RAFAEL}


def bind(draft, stored, report, live, target, archives):
    rows = {(row["file_path"], row["id"]): row for row in draft["records"]}
    revised = {(row["file_path"], row["id"]): row for row in report["checked_records"]}
    visited = {row["id"] for row in live["holds"]}
    later = {path: {r["id"]: r for r in base.load(path)["records"]} for path in set(LATER_RETENTIONS.values())}
    history = {}
    for item in draft["records"]:
        path = item["earlier_ledger"]
        if path not in history:
            assert base.digest(path) == item["earlier_ledger_sha256"]
            history[path] = {row["id"]: row for row in base.load(path)["records"]}
    seen, rebound = set(), set()
    for group in stored["groups"]:
        path, n = group["file_path"], group["block"]
        block = native.IlnkContainer.parse(target[path]).blocks[n]
        assert group["after"] == native.digest(block)
        for cmd in group["commands"]:
            if not cmd["record_ids"]:
                continue
            word, start = cmd["word"], cmd["stored_offset"]
            raw = bytes.fromhex(cmd["stored"])
            assert block[start:start + len(raw)] == raw
            values = stage.paired.text_records(raw, word)
            for ident, (relative, selector, body, slots) in zip(cmd["record_ids"], values, strict=True):
                row = rows[path, ident]
                assert (path, ident) not in seen and row["source_selector"] == selector
                assert row["native_slots"] == slots
                payload = bytes([selector]) + body if word == stage.stage.SPEECH else body
                offset = start + relative
                assert block[offset:offset + len(payload)] == payload
                if row["decision"] == "revision":
                    proof = revised[path, ident]
                    expected = bytes([selector]) + body
                    assert expected.hex() == proof.get("stored_hex", proof.get("target_hex"))
                    scope = "Native renderer and direct visual check"
                    receipt = dict(path=str(display.PROOF), sha256=base.digest(display.PROOF), id=ident)
                else:
                    assert payload.hex() == row["current_hex"]
                    if row["historical_layout_matches_current"]:
                        note = history[row["earlier_ledger"]][ident]
                        assert note["planned_integrated_reference"]["exact_stored_hex"] == payload.hex()
                        ref = row["earlier_ledger"]
                    else:
                        ref = LATER_RETENTIONS[ident]
                        note = later[ref][ident]
                        assert note["target_hex"] == note["registered_reference"]["raw_hex"] == payload.hex()
                        rebound.add(ident)
                    assert note["review"]["formatting"]
                    scope = "Byte-identical retention with registered formatting evidence"
                    receipt = dict(path=str(ref), sha256=base.digest(ref), id=ident)
                if ident in visited:
                    scope += " and initialized Rafael replay"
                row["review"]["formatting"] = True
                row["formatting_evidence"] = receipt
                row["display_scope"] = scope
                row["registered_reference"] = dict(candidate_sha256=stored["candidate_sha256"],
                    file_path=path, block=n, offset=offset, command_offset=start, exact_stored_hex=payload.hex(),
                    source_selector=selector, native_command_word=word, slots=slots, archive_sha256=archives[path])
                seen.add((path, ident))
    assert seen == rows.keys() and rebound == LATER_RETENTIONS.keys()
    draft.update(encoder="dialogue-relocatable-v1", review_gates=GATES, formatting_and_registration_pending=False,
        registered=True, candidate_sha256=stored["candidate_sha256"], initialized_rafael=live)
    validate_natural_dialogue_batch(draft)
    return draft


def verify(registry, previous, viewed):
    stored, native_proof, live, startup = map(base.load, (stage.PROOF, display.PROOF, replay.LIVE, STARTUP))
    candidate = base.digest(stage.ROM)
    assert candidate == stored["candidate_sha256"] == native_proof["candidate_sha256"]
    assert candidate == live["candidate_sha256"] == startup["candidate_sha256"]
    assert stored["predecessor_sha256"] == previous["candidate_sha256"]
    assert native_proof["stage_proof_sha256"] == base.digest(stage.PROOF) and stored["whole_parent_inverse"]
    assert startup["cold_boot"] and not startup["savestate"] and startup["complete_deployed_payload_exact"]
    assert len(startup["original_protected_name_getters"]) == 24 and len(startup["exact_matching_frames"]) == 6
    assert all(base.digest(path) == digest for path, digest in startup["evidence"].items())
    assert live["initialized_Rafael"] and live["exact_original_commands"] and live["actual_Castor_and_Rafael_macro_glyphs"]
    assert len(live["holds"]) == 16 and not live["natural_activation"] and not live["hardware"]
    assert all(base.digest(path) == digest for path, digest in live["evidence"].items())
    assert all(base.digest(r["capture"]["path"]) == r["capture"]["PNG_sha256"] for r in live["holds"])
    assert native_proof["revision_count"] == 40 and native_proof["fresh_page_count"] == 18
    assert sum(len(item["pages"]) for r in native_proof["checked_records"] for item in r["layouts"]) == 61
    assert base.digest(native_proof["prior_proof"]["path"]) == native_proof["prior_proof"]["sha256"]
    sheets = native_proof["previous_sheets"] + native_proof["contact_sheets"] + live["sheets"]
    assert {s["path"]: s["sha256"] for s in sheets} == viewed
    assert all(base.digest(path) == sha for path, sha in viewed.items())
    suite, = ElementTree.parse(QA).iter("testsuite")
    assert int(suite.get("tests", 0)) == 32 and all(int(suite.get(k, 0)) == 0 for k in ("failures", "errors", "skipped"))
    assert (stage.ROOT / "clean_rebuilt.nds").read_bytes() == stage.ROM.read_bytes()
    old, new, clean = map(base.NdsImage.open, (parent.ROM, stage.ROM, native.CLEAN))
    assert base.digest(native.CLEAN) == previous["clean_input_sha256"] == stored["clean_sha256"]
    original, result = map(native.files, (old, new))
    assert original.keys() == result.keys()
    changed = stored["changed_blocks"]
    assert {p for p in original if original[p] != result[p]} == changed.keys()
    for path, blocks in changed.items():
        a, b = [native.IlnkContainer.parse(mapping[path]).blocks for mapping in (original, result)]
        assert [i for i, (before, after) in enumerate(zip(a, b, strict=True)) if before != after] == blocks
        new.replace_file(path, original[path])
    assert bytes(new.rom.save()) == parent.ROM.read_bytes()
    guard = registry["profiles"][previous["profile"]]["source25_multiarchive_guard"]
    bound = bind_registered_story_percent_guard(guard)(native.files(clean), result)
    assert bound["total_exact_source_bound_relocated_leading25_count"] == 7
    assert not any(bound["source_bound_new_command_counts"].values())
    archives = {path: native.digest(result[path]) for path in changed}
    assert base.digest(stage.review.OUTPUT) == stored["manuscript_sha256"]
    draft = bind(base.load(stage.review.OUTPUT), stored, native_proof, live, result, archives)
    assert len(draft["records"]) == 151
    assert Counter(r["decision"] for r in draft["records"]) == {"revision": 40, "retention": 111}
    draft.update(approved_source25=bound, direct_visual_review=sheets)
    return stored, native_proof, draft, archives


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--visual-review", type=Path, required=True)
    args = parser.parse_args()
    assert not any(p.exists() for p in (ROOT, PACKAGE, DOC))
    registry_before, ledger_before = base.REGISTRY.read_bytes(), base.LEDGER.read_bytes()
    main_sha = base.digest(base.PROMOTED)
    registry, ledger, previous, manifest = map(base.load, (base.REGISTRY, base.LEDGER, parent.RELEASE, parent.MANIFEST))
    assert native.digest(registry_before) == previous["registry_sha256"] == manifest["release_stack_sha256"]
    assert base.digest(parent.MANIFEST) == previous["manifest_sha256"]
    assert manifest["candidate_sha256"] == base.digest(parent.ROM) == previous["candidate_sha256"]
    assert len(registry["accepted_layers"]) == 114 and PROFILE not in registry["profiles"]
    assert len(manifest["batches"]) == 862 and len(manifest["checks"]) == 197 and all(manifest["checks"].values())
    stored, display_proof, draft, archives = verify(registry, previous, base.load(args.visual_review))
    candidate = draft["candidate_sha256"]
    credited = {(r["file_path"], r["id"]) for r in ledger[base.CONTEXT]["integrated_record_keys"]}
    assert len(credited) == ledger["records_editorially_completed"] == 27700
    assert all((r["file_path"], r["id"]) in credited for r in draft["records"])
    pending = ledger["pending_shared_consumer_checkpoint_20261114"]
    assert pending["remaining_total"] == 276 and pending["candidate_sha256"] == previous["candidate_sha256"]
    assert ledger["current_integrated_candidate"]["sha256"] == previous["candidate_sha256"]
    assert not ledger["full_goal_complete"]

    ROOT.mkdir()
    VERIFY.mkdir(parents=True)
    copyfile(stage.ROOT / "clean_input.xdelta", PATCH)
    copyfile(stage.ROOT / "clean_rebuilt.nds", ROM)
    assert base.digest(ROM) == candidate
    assert base.digest(PATCH) == base.digest(stage.ROOT / "clean_input.xdelta")
    for source in (stage.PROOF, STARTUP, QA, display.PROOF, replay.LIVE, replay.SETUP, args.visual_review):
        dest = VERIFY / source.name
        copyfile(source, dest)
        assert base.digest(source) == base.digest(dest)
    for sheet in display_proof["contact_sheets"] + draft["initialized_rafael"]["sheets"]:
        dest = VERIFY / Path(sheet["path"]).name
        copyfile(sheet["path"], dest)
        assert base.digest(dest) == sheet["sha256"]
    base.save(REVIEW, draft)
    predecessor = {k: previous[k] for k in
                   ("profile", "candidate", "candidate_sha256", "manifest", "manifest_sha256", "registry_sha256")}
    backup = ROOT / "release_stack_before_guild_assignments.json"
    backup.write_bytes(registry_before)
    predecessor["registry"] = str(backup)
    profile = deepcopy(registry["profiles"][previous["profile"]])
    profile.update(verified_forest_expeditions_predecessor=predecessor, london_malacca_guild_assignments_release=str(REVIEW))
    registry["profiles"][PROFILE] = profile
    registry_draft = ROOT / "release_stack_with_guild_assignments.json"
    base.save(registry_draft, registry)
    registry_sha = base.digest(registry_draft)
    manifest.update(profile=PROFILE, candidate_rom=str(ROM), candidate_sha256=candidate, release_stack_sha256=registry_sha)
    manifest["batches"].append(str(REVIEW))
    manifest["checks"]["registered_london_malacca_guild_assignments_and_complete_parent_inverse"] = True
    for row in draft["records"]:
        ids = manifest["changed_records"][row["file_path"]]
        if row["decision"] == "revision" and row["id"] not in ids:
            ids.append(row["id"])
    manifest["london_malacca_guild_assignments_pipeline"] = dict(predecessor=predecessor,
        registered_review=str(REVIEW), registered_review_sha256=base.digest(REVIEW),
        registration_driver_sha256=base.digest(__file__), stored_proof_sha256=base.digest(stage.PROOF),
        native_display_sha256=base.digest(display.PROOF), complete_parent_inverse=True,
        owned_story_blocks=stored["changed_blocks"])
    base.save(MANIFEST, manifest)
    startup = VERIFY / STARTUP.name
    release = previous | dict(profile=PROFILE, candidate=str(ROM), candidate_sha256=candidate, patch=str(PATCH),
        patch_sha256=base.digest(PATCH), manifest=str(MANIFEST), manifest_sha256=base.digest(MANIFEST),
        registry_sha256=registry_sha, predecessor=predecessor, registered_manifest_entries=len(manifest["batches"]),
        passing_release_checks=len(manifest["checks"]), own_registered_startup=str(startup),
        own_registered_startup_sha256=base.digest(startup), changed_internal_files=sorted(archives),
        repository_tests=32, new_contextual_records=0, prose_revisions=40, justified_retentions=111,
        name_label_revisions=0, text_display_revisions=0, final_phrase_refinements_within_revised_prose=6,
        actual_verification_scope=dict(own_startup=True, initialized_Rafael_guild_and_riddle=True,
                                       natural_activation=False, hardware=False),
        **{f"target_SC{i}_sha256": archives[f"/data/SC{i}.DK4"] for i in range(4)})
    base.save(RELEASE, release)
    base.save(PACKAGE / "release_manifest.json", release | {"user_acceptance_pending": True})
    workflow.archive_file(MANIFEST.read_bytes(), PACKAGE / "build_manifest.json.gz")
    workflow.archive_file(registry_draft.read_bytes(), PACKAGE / "build_release_stack.json.gz")
    workflow.archive_file(ledger_before, ROOT / "editorial_ledger_before.json.gz")
    pending["candidate_sha256"] = candidate
    ledger["current_integrated_candidate"].update(path=str(ROM), sha256=candidate, profile=PROFILE,
        patch=str(PATCH), patch_sha256=release["patch_sha256"], manifest=str(MANIFEST),
        manifest_sha256=release["manifest_sha256"], registered_release_verification=str(RELEASE),
        **{f"SC{i}_sha256": release[f"target_SC{i}_sha256"] for i in range(4)})
    checkpoint = "Rafael's ruins investigation and the related London and Malacca guild assignments are reviewed."
    ledger["london_malacca_guild_assignments_20261118"] = dict(registered_candidate_sha256=candidate,
        registered_review=str(REVIEW), registered_release=str(RELEASE), existing_credit=151,
        new_contextual_credit=0, prose_revisions=40, justified_retentions=111)
    ledger["latest_checkpoint"] = checkpoint
    ledger_after = workflow.encode_ledger(ledger)
    base.save(VERIFY / "registration_mutation_plan.json", dict(registry_before=native.digest(registry_before),
        ledger_before=native.digest(ledger_before), registry_after=registry_sha,
        ledger_after=native.digest(ledger_after), main_sha256=main_sha))
    (PACKAGE / "README.md").write_text(f"""# London and Malacca guild assignments test candidate

The [local ROM](../../{ROM.as_posix()}) includes all four reviewed assignments.
The [clean-input patch](translation.xdelta) rebuilds ROM SHA-256 `{candidate}` byte for byte.
Main awaits user acceptance. Natural quest activation and hardware are unverified.
""", encoding="utf-8", newline="\n")
    base.save(PACKAGE / "checksums.json", workflow.package_checksums(PACKAGE))
    assert base.REGISTRY.read_bytes() == registry_before and base.LEDGER.read_bytes() == ledger_before
    assert base.digest(base.PROMOTED) == main_sha
    base.replace_checked(base.REGISTRY, registry_draft.read_bytes())
    try:
        windows.update_ledger_in_place(ledger_before, ledger_after)
    except (OSError, AssertionError):
        base.replace_checked(base.REGISTRY, registry_before)
        raise
    assert base.digest(base.REGISTRY) == registry_sha and base.LEDGER.read_bytes() == ledger_after
    pin_path = Path("translations/rom_retention_pins.json")
    pins = base.load(pin_path)
    candidates = [ROM, stage.ROM, replay.ROM]
    for version in (1, 2, 3):
        folder = stage.ROOT.with_name(f"research_v{version}")
        candidates.append(folder / stage.ROM.name)
        if version >= 2:
            candidates.append(folder / replay.ROOT.name / replay.ROM.name)
    for path in candidates:
        absolute = str(path.resolve())
        if all(pin["path"] != absolute for pin in pins):
            pins.append(dict(path=absolute, reason=f"Preserve guild assignment ROM or replay fixture {base.digest(path)}"))
    pins_payload = (workflow.dumps(pins, ensure_ascii=False, indent=2) + "\n").replace("\n", "\r\n")
    base.replace_checked(pin_path, pins_payload.encode())
    DOC.write_text(f"""# London and Malacca guild assignments

Reviewed 151 records in 19 blocks over the four routes. Rafael's ruins riddle now repeats the same clue throughout his deductions. Hodram's guildmaster sounds wary and familiar while reporting the sea creature. Lil's delivery keeps both the 200 barrels and the two-hold measure. Maria's loan preserves the two handovers, the month-long wait and the 20,000 gold reward. The ledger records 40 revisions and 111 justified retentions. [Exact review ledger](../{REVIEW.as_posix()})

All 40 revised records use one page each, including two speakerless notices. Native checks covered 61 pages with name-width examples. The final visual adjustments removed short overflow pages from the guildmaster's account and the latitude clue. The original speaker controls, aliases, branch destinations and runtime substitutions remain intact. [Final layout pages](../{(VERIFY / 'before_after_1.png').as_posix()})

The initialized Rafael replay matched 16 original dialogue pages, including Castor in the summons, Rafael in the latitude clue, and the change from the quoted riddle to the crew's deduction. The other routes and unvisited alternatives received offline checks. Natural activation and hardware remain unverified. [Rafael replay](../{(VERIFY / 'live_1.png').as_posix()})

The clean-input patch reconstructs the exact candidate. All 114 accepted layers and the ASCII right-bound correction carry forward. Six cold-boot holds, 24 protected name getters and 32 targeted tests passed. The 151 records already had credit, so the total remains 27,700 with 276 shared keys still open. Main awaits acceptance. [Test ROM and patch](../{PACKAGE.as_posix()}/README.md)
""", encoding="utf-8", newline="\n")
    prefix = f"# Current editorial checkpoint - 2026-11-18\n\n{checkpoint} [Checkpoint]({DOC.name})\n\n".encode()
    for name in ("editorial_handoff_current.md", "translation_progress.md", "build_continuity_protocol.md"):
        path = DOC.with_name(name)
        base.replace_checked(path, prefix + path.read_bytes())
    assert base.digest(base.PROMOTED) == main_sha
    print(f"Registered {candidate} with {len(manifest['batches'])} entries, 114 accepted layers and "
          f"{len(manifest['checks'])} passing checks.", flush=True)


if __name__ == "__main__":
    main()
