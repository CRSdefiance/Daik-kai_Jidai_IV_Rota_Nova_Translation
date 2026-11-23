"""Bind the Rafael priorities and all Hodram B61–B70 comparisons to current bytes."""

from collections import Counter
from pathlib import Path

from scripts import register_tavern_nearby_town_wrap_20261123 as current


base, native = current.base, current.native
ROOT = Path("translations/editorial_checkpoints")
HISTORY = ROOT / "palace_and_london_20261122/hodram_B61_B70_reconciliation.json"
OUT = ROOT / "tavern_nearby_town_wrap_20261123/priority_story_reviews.json"
RAFAEL, HODRAM = "/data/SC0.DK4", "/data/SC1.DK4"
NORTH_SEA = "north_sea_and_hodram_reconciliation"
SERA = "hodram_sera_nagarpur_and_kuhn"
FAREWELLS = "hodram_farewells_and_maria"
PACKETS = {
    NORTH_SEA: {(RAFAEL, 49): 61, (HODRAM, 66): 13},
    "rafael_B84_training": {(RAFAEL, 84): 131},
    SERA: {(HODRAM, 61): 12, (HODRAM, 62): 32, (HODRAM, 63): 29,
           (HODRAM, 64): 23, (HODRAM, 68): 8, (HODRAM, 70): 4},
    FAREWELLS: {(HODRAM, 65): 40, (HODRAM, 67): 52, (HODRAM, 69): 11},
}


def bind_record(record, release, clean, current_blocks, candidate):
    path, block = record["file_path"], record["block"]
    original = clean[path][block]
    source, installed = record.get("source_reference"), record["registered_reference"]
    if source is None:
        source = dict(file_path=path, block=block, block_sha256=native.digest(original),
            offset=record["source_offset"], command_offset=record["source_command_offset"],
            exact_command_hex=record["source_command_hex"])
    assert native.digest(original) == source["block_sha256"]
    body_offset = source["offset"]
    if "exact_body_hex" in source:
        expected = bytes.fromhex(source["exact_body_hex"])
        if original[body_offset:body_offset + len(expected)] != expected:
            assert original[body_offset] == record["source_selector"], (path, record["id"], body_offset)
            body_offset += 1
        assert original[body_offset:body_offset + len(expected)] == expected, (path, record["id"], body_offset)
    if "exact_command_hex" in source:
        command = bytes.fromhex(source["exact_command_hex"])
        start = source["command_offset"]
        assert original[start:start + len(command)] == command
    assert set(record["review"]) == set(current.routes.GATES) and all(record["review"].values())
    assert installed["candidate_sha256"] == release["candidate_sha256"]
    active = current_blocks[path][block]
    command = bytes.fromhex(installed["exact_command_hex"])
    offset = installed["command_offset"]
    assert active[offset:offset + len(command)] == command
    assert native.digest(active) == installed["block_sha256"]
    return dict(file_path=path, block=block, id=record["id"], speaker=record["speaker"],
        source_reference=source, verified_source_body_offset=body_offset,
        approved_reference=installed, active_candidate_sha256=candidate,
        english=record["english"], decision=record["decision"], localization_note=record["localization_note"],
        review=record["review"], prior_initialized_excerpt=record.get("observed_in_initialized_excerpt", False))


def main():
    latest = base.load(current.RELEASE)
    assert latest["registry_sha256"] == base.digest(base.REGISTRY)
    candidate = base.digest(current.ROM)
    assert latest["candidate_sha256"] == candidate
    assert base.digest(native.CLEAN) == latest["clean_input_sha256"]
    clean, active = [current.routes.story_blocks(base.NdsImage.open(path)) for path in (native.CLEAN, current.ROM)]
    mapped, value = (current.scope[name] for name in ("mapped", "value"))
    with mapped(current.MANIFEST) as manifest:
        registered = {Path(path) for path in value(manifest, "batches", 2)}
    bound, receipts = {}, {}
    for suffix, allocation in PACKETS.items():
        package = current.PACKAGE.with_name(f"all_routes_editorial_20261122_{suffix}_candidate")
        review = package / "verification/registered_review.json"
        receipt = review.with_name("registered_release_verification.json")
        checksums = base.load(package / "checksums.json")
        assert review in registered
        for path in (review, receipt):
            assert base.digest(path) == checksums[path.relative_to(package).as_posix()]
        decisions, release = map(base.load, (review, receipt))
        assert decisions["candidate_sha256"] == release["candidate_sha256"]
        receipts[str(review)] = base.digest(review)
        actual = Counter()
        for row in decisions["records"]:
            key = row["file_path"], row["block"]
            if key not in allocation:
                continue
            identity = key[0], row["id"]
            assert identity not in bound
            proof = bind_record(row, release, clean, active, candidate)
            bound[identity] = proof | dict(approved_review=str(review))
            actual[key] += 1
        assert actual == allocation

    historical = base.load(HISTORY)
    assert historical["older_rom_reconstructed_and_all_historical_payloads_verified"]
    original_differences = Counter()
    for row in historical["records"]:
        proof = bound[HODRAM, row["id"]]
        assert proof["block"] == row["block"] and proof["source_reference"]["offset"] == row["source"]["offset"]
        comparison = dict(historical_reference=row["historical_installed_reference"],
            earlier_English=row["earlier_English"], baseline_reference=row["current_body_reference"],
            exact_payload_match=row["exact_payload_match"], logical_match=row["logical_match"])
        proof["november_1_comparison"] = comparison
        original_differences["exact_at_intake" if row["exact_payload_match"] else
            "spacing_at_intake" if row["logical_match"] else "logical_difference_at_intake"] += 1
    assert original_differences == {"exact_at_intake": 128, "spacing_at_intake": 1, "logical_difference_at_intake": 95}
    assert len(bound) == 416 and sum(row["file_path"] == HODRAM for row in bound.values()) == 224
    OUT.parent.mkdir(parents=True, exist_ok=True)
    assert not OUT.exists()
    base.save(OUT, dict(candidate_sha256=candidate, clean_sha256=latest["clean_input_sha256"],
        registered_receipts=receipts, historical_intake=dict(path=str(HISTORY), sha256=base.digest(HISTORY)),
        entry_counts=dict(Rafael_B49=61, Rafael_B84=131, Hodram_B61_B70=224),
        historical_difference_counts=dict(original_differences), records=list(bound.values()),
        technical_check_scope="Exact in the current stored story blocks. Reuses the registered contextual and native reviews.",
        new_gameplay_runs=0, new_editorial_credit=0))
    print("Bound 416 priority decisions to the current ROM, including all 96 Hodram historical payload differences.")


if __name__ == "__main__":
    main()
