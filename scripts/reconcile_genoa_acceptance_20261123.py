"""Carry the known editorial acceptance evidence to the latest Genoa candidate."""

from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from scripts import reconcile_editorial_acceptance_20261123 as acceptance
from scripts import register_cartridge_title_20261123 as registry
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


ROOT = acceptance.OUT.parent
OUT = ROOT / "editorial_acceptance_after_genoa_20261123.json"
STARTING = ROOT / "editorial_acceptance_after_recruitment_20261123.json"
ELEGY = ROOT / "editorial_acceptance_elegy_20261123.json"
ROUTE_CENSUS = ROOT / "current_route_coverage_20261123.json"
GENOA_GAMEPLAY = ROOT / "genoa_copenhagen_current_20261123.json"
ALTERNATE_GAMEPLAY = ROOT / "genoa_alternate_choices_20261123.json"
DRIVE = ROOT / "genoa_alternate_dialogue_drive_20261123.json"
CLEANUP = ROOT / "genoa_alternate_dialogue_cleanup_20261123.json"
WORLDS = tuple(f"/data/SC{i}.DK4" for i in range(4))
STORY = WORLDS[1]
ARM, COMMON, HELP = acceptance.ARM, acceptance.COMMON, acceptance.HELP
PACKAGES = tuple(acceptance.RELEASES / f"all_routes_editorial_20261123_{name}_candidate" for name in (
    "recruitment_shortfall", "price_info_descriptions", "genoa_dialogue", "genoa_alternate_dialogue"))
PRICE_IDS = (143, 166, 203, 208, 216, 225, 226, 227, 233, 234, 236, 245)
GENOA_IDS = {"DK4_MES_B170_R0090", "DK4_MES_B170_R0125", "DK4_MES_B181_R0012"}
ALTERNATE_IDS = {f"DK4_MES_B170_R{n:04d}" for n in (136, 181, 184, 211)}


def sealed(package, name):
    path = package / name
    assert digest(path) == read(package / "checksums.json")[name]
    return path


def blocks(rom, path):
    return IlnkContainer.parse(rom.read_file(path)).blocks


def common_binding(row):
    # Parsing shorter strings creates extra NUL entries and shifts the parse index.
    # The message table still points to the same block offsets.
    return (row.message_id, row.block, row.table_offset, row.block_offset,
            row.copy_end, row.start, row.end, row.text)


def inverse(earlier, candidate, receipt, path):
    previous = receipt["predecessor"]
    restored = NdsImage.open(receipt["candidate"])
    restored.replace_file(path, earlier.read_file(path))
    assert bytes(restored.rom.save()) == Path(previous["candidate"]).read_bytes()
    assert candidate.read_file(path) != earlier.read_file(path)


def story_delta(earlier, current, proof, review, clean, ids):
    old, new = [blocks(rom, STORY) for rom in (earlier, current)]
    source = blocks(clean, STORY)
    touched = {i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b}
    assert touched == {int(i) for i in proof["blocks"]}
    rows = {row["id"]: row for row in review["records"]}
    assert set(review["changed_ids"]) == ids == {row["id"] for row in proof["changed"]}
    inverse = {i: bytearray(new[i]) for i in touched}
    for change in proof["changed"]:
        ident, i, offset = (change[key] for key in ("id", "block", "command_offset"))
        old_bytes, new_bytes = [bytes.fromhex(change[key]) for key in ("before_hex", "after_hex")]
        assert len(old_bytes) == len(new_bytes) and old_bytes[:6] == new_bytes[:6]
        assert b"\0" in new_bytes[6:] and new_bytes.index(0, 6) == old_bytes.index(0, 6)
        assert new[i][offset:offset + len(new_bytes)] == new_bytes
        assert old[i][offset:offset + len(old_bytes)] == old_bytes
        inverse[i][offset:offset + len(old_bytes)] = old_bytes
        row = rows[ident]
        source_ref, registered_ref = (row[key] for key in ("source_reference", "registered_reference"))
        start, source_bytes = source_ref["command_offset"], bytes.fromhex(source_ref["exact_command_hex"])
        assert source[i][start:start + len(source_bytes)] == source_bytes and source_bytes[:6] == new_bytes[:6]
        assert registered_ref["exact_command_hex"] == new_bytes.hex()
        assert registered_ref["command_offset"] == offset and registered_ref["block_sha256"] == sha256(new[i]).hexdigest()
        assert set(row["review"]) == acceptance.GATES and all(row["review"].values())
    assert all(inverse[i] == old[i] for i in touched)
    return dict(story_blocks=sorted(touched), story_records=sorted(ids), exact_owned_body_inverse=True)


def gameplay_scope(current_review):
    old, other = read(GENOA_GAMEPLAY), read(ALTERNATE_GAMEPLAY)
    initial = {row["id"] for row in old["ordinary_gameplay"]["genoa"]["story"]
               if row["block"] == 170 and row["gameplay_observed"]}
    alternate = {row["id"] for branch in other["choice_paths"].values() for row in branch["story"]}
    source_keys = {row["id"] for row in current_review["records"] if row["id"].startswith("DK4_MES_B170_")}
    assert len(initial) == 36 and len(alternate) == 20 and len(initial | alternate) == 48
    assert initial | alternate == source_keys
    labels = {row["id"] for branch in other["choice_paths"].values() for row in branch["choice"]["labels"]}
    assert len(labels) == 4
    assert labels == {row["id"] for row in current_review["records"] if row["id"].startswith("SC1_B170_CHOICE_")}
    return dict(verified_speech_commands_across_builds=len(source_keys), choice_captions=len(labels),
                earlier_input_route=reference(GENOA_GAMEPLAY), two_alternate_input_routes=reference(ALTERNATE_GAMEPLAY))


def main():
    start, earlier, route = map(read, (STARTING, ELEGY, ROUTE_CENSUS))
    receipts = [sealed(pkg, "verification/registered_release_verification.json") for pkg in PACKAGES]
    releases = [read(p) for p in receipts]
    assert start["candidate_sha256"] == releases[0]["candidate_sha256"]
    assert [r["passing_release_checks"] for r in releases] == [445, 446, 447, 448]
    assert len({r["canonical_sha256"] for r in releases}) == 1
    assert all(r["clean_input_patch_byte_exact"] and r["whole_parent_inverse_exact"] for r in releases)
    assert all(r["accepted_layers"] == 114 and r["experimental_not_promoted"] for r in releases)
    for parent, child in zip(releases, releases[1:]):
        assert all(child["predecessor"][k] == parent[k] for k in ("candidate_sha256", "registry_sha256", "manifest_sha256"))
    clean_hash = digest(CLEAN)
    assert all(r["clean_input_sha256"] == clean_hash for r in releases)
    last = releases[-1]
    for release in releases:
        for key, sha in (("candidate", "candidate_sha256"), ("manifest", "manifest_sha256"),
                         ("patch", "patch_sha256"), ("own_registered_startup", "own_registered_startup_sha256")):
            assert digest(release[key]) == release[sha]
    assert digest(REGISTRY) == last["registry_sha256"]
    with registry.mapped(registry.base.LEDGER) as data:
        ledger = registry.value(data, "current_integrated_candidate", 1)
        assert ledger["sha256"] == last["candidate_sha256"] and ledger["profile"] == last["profile"]
        assert registry.value(data, "records_editorially_completed", 1) == 27700
        assert registry.value(data, "full_goal_complete", 1) is False

    clean = NdsImage.open(CLEAN)
    shortfall, price, genoa, current = (NdsImage.open(r["candidate"]) for r in releases)
    images = (shortfall, price, genoa, current)
    for rom, receipt in zip(images, releases, strict=True):
        for i, path in enumerate(WORLDS):
            assert sha256(rom.read_file(path)).hexdigest() == receipt[f"target_SC{i}_sha256"]
        assert sha256(rom.read_file(ARM)).hexdigest() == receipt["target_ARM9_sha256"]
        assert sha256(rom.read_file(COMMON)).hexdigest() == receipt["target_COMMON_sha256"]
    for i, path in enumerate((COMMON, STORY, STORY), 1):
        inverse(images[i - 1], images[i], releases[i], path)
    price_review, genoa_review, current_review = [read(sealed(pkg, "verification/registered_review.json")) for pkg in PACKAGES[1:]]
    after, before = (common_rows(rom.read_file(COMMON), rom.read_file(ARM)) for rom in (price, shortfall))
    assert [a.message_id for a, b in zip(after, before, strict=True)
            if common_binding(a) != common_binding(b)] == list(PRICE_IDS)
    assert sorted(row["message_id"] for row in price_review["records"] if row["decision"] != "retention") == list(PRICE_IDS)
    deltas = [dict(common_records=list(PRICE_IDS), exact_owned_file_inverse=True)]
    for i, review, ids in ((2, genoa_review, GENOA_IDS), (3, current_review, ALTERNATE_IDS)):
        proof = read(sealed(PACKAGES[i], "verification/stored_proof.json"))
        deltas.append(story_delta(images[i - 1], images[i], proof, review, clean, ids))
    assert sha256(current.read_file(HELP)).hexdigest() == start["help_archive"]["installed_sha256"]
    assert current.read_file(HELP) == shortfall.read_file(HELP)
    priorities = acceptance.priority_bindings(
        {path: blocks(clean, path) for path in WORLDS}, {path: blocks(current, path) for path in WORLDS})
    scoped = earlier["shared_dialogue"]["inherited_display_evidence"]
    assert digest(scoped["path"]) == scoped["sha256"]
    shared = read(scoped["path"])
    assert len(shared["records"]) == 276 and not shared["remaining_without_scoped_disposition"]
    assert all(common_binding(after[row["message_ID"]]) == common_binding(before[row["message_ID"]])
               for row in shared["records"])
    assert current.read_file(COMMON) == price.read_file(COMMON)
    assert current.read_file(ARM) == shortfall.read_file(ARM)
    bounds = acceptance.right_bound(current.read_file(ARM), last["right_bound_configuration"])
    assert bounds["matched_repair_spans"] == 8
    assert start["preserved_original_positions"] == route["exact_credited_clean_positions"] == 24092
    assert start["exact_retail_event_routes"] == 1307
    assert all(current.read_file(f"/data/EV{i}.DK4") == clean.read_file(f"/data/EV{i}.DK4") for i in range(4))
    for row in route["routes"].values():
        assert digest(row["source_census"]["path"]) == row["source_census"]["sha256"]
    delivery, cleared = map(read, (DRIVE, CLEANUP))
    assert delivery["candidate_sha256"] == delivery["downloaded_sha256"] == cleared["candidate_sha256"] == last["candidate_sha256"]
    assert delivery["streamed_readback_exact"] and delivery["nds_files_in_folder"] == 1
    assert not any(Path(row["path"]).exists() for row in cleared["removed_exact_duplicates"])
    plan = read(sealed(PACKAGES[-1], "verification/registration_mutation_plan.json"))
    assert plan["main_sha256"] == digest("translations/promoted_build.json")

    write(OUT, dict(candidate_sha256=last["candidate_sha256"], prior_acceptance=reference(STARTING),
        verified_release_chain=[reference(p) for p in receipts], downstream_deltas=deltas,
        registered_story_source_positions=24092, priority_reviews=priorities, historical_editorial_credits=27700,
        scoped_shared_display_records=276, independently_unverified_shared_display_callers=shared["other_direct_display_paths_unverified"],
        separate_archived_artwork_identities=shared["exact_archived_artwork_identities_open"], retail_story_event_bindings=1307,
        approved_help=start["help_archive"], original_gameplay_Genoa=gameplay_scope(current_review),
        inherited_ASCII_right_bound=bounds, drive=reference(DRIVE), cleanup=reference(CLEANUP),
        main_descriptor_preserved=True, full_editorial_goal_complete=False))
    print("Reconciled three successive release deltas, 416 priority decisions and all 48 Genoa recruitment speeches.")


if __name__ == "__main__":
    main()
