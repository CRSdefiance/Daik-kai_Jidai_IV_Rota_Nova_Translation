"""Check which acceptance evidence carries across the Azores and recruitment releases."""

from pathlib import Path

from scripts import reconcile_elegy_acceptance_20261123 as earlier
from scripts import register_azores_return_20261123 as azores
from scripts import register_recruitment_capacity_20261123 as capacity
from scripts import register_recruitment_shortfall_20261123 as shortfall
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


ARM, COMMON = shortfall.ARM, shortfall.COMMON
OUT = earlier.OUT.with_name("editorial_acceptance_after_recruitment_20261123.json")
DRIVE = OUT.with_name("recruitment_shortfall_drive_20261123.json")


def main():
    accepted = read(earlier.OUT)
    paths = (earlier.RELEASE, azores.RELEASE, capacity.RELEASE, shortfall.RELEASE)
    receipts = [read(path) for path in paths]
    first, last = receipts[0], receipts[-1]
    assert first["candidate_sha256"] == accepted["candidate_sha256"]
    assert digest(CLEAN) == first["clean_input_sha256"] == last["clean_input_sha256"]
    assert digest(REGISTRY) == last["registry_sha256"]
    for parent, child in zip(receipts, receipts[1:]):
        assert child["predecessor"]["candidate_sha256"] == parent["candidate_sha256"]
        assert child["predecessor"]["registry_sha256"] == parent["registry_sha256"]
        assert child["accepted_layers"] == parent["accepted_layers"] == 114
        assert child["whole_parent_inverse_exact"] and child["clean_input_patch_byte_exact"]
    assert [row["passing_release_checks"] for row in receipts] == [442, 443, 444, 445]

    images = []
    for receipt in receipts:
        assert digest(receipt["candidate"]) == receipt["candidate_sha256"]
        assert digest(receipt["patch"]) == receipt["patch_sha256"]
        assert digest(receipt["own_registered_startup"]) == receipt["own_registered_startup_sha256"]
        images.append(NdsImage.open(receipt["candidate"]))
    previous, final = images[0], images[-1]
    assert all(image.read_file(ARM) == images[1].read_file(ARM) for image in images[2:])
    assert previous.read_file(COMMON) == images[1].read_file(COMMON)
    for row, image in zip(receipts, images, strict=True):
        assert sha256(image.read_file(ARM)).hexdigest() == row["target_ARM9_sha256"]
        assert sha256(image.read_file(COMMON)).hexdigest() == row["target_COMMON_sha256"]
    sides = [earlier.common_rows(image.read_file(COMMON), image.read_file(ARM)) for image in images]
    groups = [sorted(a.message_id for a, b in zip(left, right, strict=True) if a != b)
              for left, right in zip(sides, sides[1:])]
    assert groups == [[], list(range(1042, 1049)), [1039, 1041]]
    for name in (ARM, COMMON):
        final.replace_file(name, previous.read_file(name))
    assert bytes(final.rom.save()) == Path(first["candidate"]).read_bytes()
    current = NdsImage.open(last["candidate"])
    story = accepted["credited_story"]
    for name, proof in story["four_route_archives"].items():
        assert sha256(current.read_file(name)).hexdigest() == proof["installed_sha256"]
    shared = accepted["shared_dialogue"]
    pending = shared["inherited_display_evidence"]
    assert digest(pending["path"]) == pending["sha256"]
    rows = read(pending["path"])["records"]
    assert len(rows) == 276 and all(sides[0][r["message_ID"]] == sides[-1][r["message_ID"]] for r in rows)
    assert sha256(current.read_file(earlier.previous.HELP)).hexdigest() == accepted["help_archive"]["installed_sha256"]
    bounds = earlier.previous.right_bound(current.read_file(ARM), last["right_bound_configuration"])
    assert bounds["matched_repair_spans"] == 8
    delivery = read(DRIVE)
    assert delivery["candidate_sha256"] == delivery["downloaded_sha256"] == last["candidate_sha256"]
    assert delivery["streamed_readback_exact"] and delivery["nds_files_in_folder"] == 1
    plan = read(shortfall.PLAN)
    assert plan["main_sha256"] == digest("translations/promoted_build.json")

    write(OUT, dict(candidate_sha256=last["candidate_sha256"], verified_release_chain=[reference(path) for path in paths],
        base_acceptance=reference(earlier.OUT), all_other_ROM_bytes_exact=True, changed_COMMON_records_by_batch=groups,
        preserved_original_positions=story["exact_credited_positions"], preserved_priority_decisions=416,
        exact_retail_event_routes=story["exact_retail_event_routes"], scoped_COMMON_locations_and_bodies_exact=276,
        help_archive=accepted["help_archive"], right_bounds=bounds, drive=reference(DRIVE), main_untouched=True,
        pending_indirect_text_consumers=shared["direct_calls_outside_verified_display_scopes_open"],
        archived_artwork_identity_leads=shared["exact_archived_artwork_identities_open"],
        newly_credited_records=0, full_editorial_goal_complete=False))
    print("Reconciled the three release deltas, all four routes, shared references, Help and exact Drive readback.")


if __name__ == "__main__":
    main()
