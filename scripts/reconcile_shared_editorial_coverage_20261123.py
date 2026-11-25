"""Join the cumulative shared display checkpoints against the installed COMMON inventory."""

from pathlib import Path

from scripts.reconcile_legacy_fleet_and_quit_paths_20261123 import (
    WORKLIST, base, current, native, common_message_entries, owned_entries, stored_record,
    DIRECTORY_OFFSET, TABLE_OFFSET,
)
from scripts.reconcile_story_artwork_inventory_20261123 import OUT as ARTWORK


OUT = ARTWORK.with_name("shared_editorial_coverage_20261123.json")
STAGES = (
    ("gallery_caption_display_dispositions", "shared_visible_content_dispositions", "needing_distinct_editorial_disposition"),
    ("chooser_and_online_dispositions", "confirmed_visible_aliases", "remaining_needing_distinct_disposition"),
    ("story_still_label_dispositions", "story_label_dispositions", "remaining_needing_distinct_disposition"),
    ("opening_label_dispositions", "label_dispositions", "remaining_needing_distinct_disposition"),
    ("legacy_save_dispositions", "label_dispositions", "remaining_needing_distinct_disposition"),
    ("promotional_display_paths", "promotion_records", "remaining_outside_checked_title_content"),
    ("legacy_setup_and_recruitment", "reviewed_entries", "remaining_without_scoped_disposition"),
    ("legacy_fleet_and_quit_paths", "reviewed_entries", "remaining_without_scoped_disposition"),
    ("cartridge_header_check", "reviewed_entries", "remaining_without_scoped_disposition"),
    ("title_variant_display", "reviewed_entries", "remaining_without_scoped_disposition"),
    ("lisbon_new_save", "reviewed_entries", "remaining_without_scoped_disposition"),
    ("ds_save_space", "reviewed_entries", "remaining_without_scoped_disposition"),
    ("market_exit_current", "reviewed_entries", "remaining_without_scoped_disposition"),
    ("final_shared_artwork_leads", "records", "remaining_without_scoped_disposition"),
    ("story_artwork_inventory", "archived_story_labels", "remaining_without_scoped_disposition"),
)


def check_storage(row, verified):
    assert row["file_path"] == verified["file_path"]
    clean_ref = row.get("source_reference", row.get("clean_reference"))
    assert clean_ref == verified["source_reference"]
    assert row["installed_reference"] == verified["installed_reference"]
    both = row.get("exact_COMMON_hex", row.get("exact_stored_hex"))
    clean = row.get("source_hex", row.get("clean_hex", both))
    installed = row.get("installed_hex", both)
    assert (clean, installed) == (verified["source_hex"], verified["installed_hex"])


def main():
    release, review, worklist = map(base.load, (current.RELEASE, current.REVIEW, WORKLIST))
    assert base.digest(current.ROM) == release["candidate_sha256"] == review["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    clean, target = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    ja, en = (image.read_file(current.ARM) for image in (clean, target))
    common = target.read_file(current.COMMON)
    assert native.digest(en) == release["target_ARM9_sha256"] and native.digest(common) == release["target_COMMON_sha256"]
    source = common_message_entries(clean.read_file(current.COMMON), ja)
    active = owned_entries(common, en, native.digest(en[DIRECTORY_OFFSET:TABLE_OFFSET]))
    assert len(source) == len(active) == 3668
    inventory = {row["message_ID"]: row for row in worklist["records"]}
    binding = {row["message_ID"]: row for row in review["shared_consumer_binding"]["records"]}
    assert inventory.keys() == binding.keys() and len(inventory) == 276
    remaining, results, checkpoints = set(inventory), [], []
    for name, records_field, remaining_field in STAGES:
        path = ARTWORK.with_name(f"{name}_20261123.json")
        data = base.load(path)
        waiting = set(data[remaining_field])
        rows = {r["message_ID"]: r for r in data[records_field]}
        assert len(rows) == len(data[records_field])
        if name == "final_shared_artwork_leads":
            assert rows.keys() & waiting == {3401, 3490}
            rows = {key: row for key, row in rows.items() if key not in waiting}
        assert rows.keys() <= remaining and remaining - rows.keys() == waiting, path
        digest = base.digest(path)
        for key, record in rows.items():
            bound = stored_record(key, source, active, inventory, binding)
            check_storage(record, bound)
            results.append(bound | dict(scoped_display_evidence=str(path), scoped_display_evidence_sha256=digest))
        checkpoints.append(dict(path=str(path), sha256=digest, newly_evidenced=len(rows), remaining=len(waiting)))
        remaining = waiting
    assert not remaining and {row["message_ID"] for row in results} == inventory.keys()
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], verified_installed_COMMON_sha256=native.digest(common),
        mapped_COMMON=3668, previously_credited_COMMON=3392, scoped_shared_display_findings=len(results),
        new_editorial_credit=0, remaining_without_scoped_disposition=[], other_direct_display_paths_unverified=True,
        exact_archived_artwork_identities_open=base.load(ARTWORK)["exact_archived_artwork_identities_open"],
        records=sorted(results, key=lambda row: row["message_ID"]), subdivision_evidence=checkpoints,
        evidence={str(p): base.digest(p) for p in (WORKLIST, current.RELEASE, current.REVIEW, Path(__file__))},
        full_editorial_goal_complete=False))
    print(f"Verified {len(results)} non-overlapping shared dispositions and all exact current storage references.")


if __name__ == "__main__":
    main()
