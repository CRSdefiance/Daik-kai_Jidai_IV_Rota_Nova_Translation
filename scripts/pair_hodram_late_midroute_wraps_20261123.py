"""Pair Hodram's next wrap leads with their previously reviewed full exchanges."""

from collections import Counter
from pathlib import Path

from scripts import pair_hodram_midroute_followups_20261123 as prior


base, native, ARCHIVE = prior.base, prior.native, prior.ARCHIVE
PARENT = Path("releases/all_routes_editorial_20261123_rafael_remaining_wraps_candidate/release_manifest.json")
QUEUE = Path("translations/editorial_checkpoints/rafael_remaining_wraps_20261123/current_wrap_queue.json")
OUTPUT = Path("translations/editorial_checkpoints/hodram_late_midroute_wraps_20261123/paired_source.json")
INTERVALS = {
    "B131_B150": (141, 142, 145, 147, 148, 150),
    "B151_B160": (156, 160),
    "B161_B170": (166, 167),
    "B171_B180": (175, 176, 177, 178, 179),
}


def main():
    release, queue = map(base.load, (PARENT, QUEUE))
    rom = Path(release["candidate"])
    candidate = base.digest(rom)
    clean = base.digest(native.CLEAN)
    assert candidate == release["candidate_sha256"] == queue["candidate_sha256"]
    assert clean == release["clean_input_sha256"]
    verification = PARENT.with_name("verification") / "registered_release_verification.json"
    assert base.digest(verification) == queue["exact_release_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]

    images = [base.NdsImage.open(path) for path in (native.CLEAN, rom)]
    arms = [image.read_file(native.ARM) for image in images]
    archives = [image.read_file(ARCHIVE) for image in images]
    hashes = [native.digest(archive) for archive in archives]
    assert hashes[1] == release["target_SC1_sha256"]
    banks = [native.IlnkContainer.parse(archive).blocks for archive in archives]

    groups, reviews = [], {}
    for interval, blocks in INTERVALS.items():
        package = Path(f"releases/all_routes_editorial_20261122_hodram_{interval}_candidate")
        reference = package / "verification/registered_review.json"
        reviews[reference.as_posix()] = base.digest(reference)
        assert reviews[reference.as_posix()] == base.load(package / "checksums.json")["verification/registered_review.json"]
        rows = base.load(reference)["records"]
        for block in blocks:
            records = [row for row in rows if row["block"] == block and row["file_path"] == ARCHIVE]
            leads = {row["offset"]: row for row in queue["records"] if row["file_path"] == ARCHIVE
                     and row["block"] == block and "reviewed" not in row}
            assert records and leads, block
            assert all(all(row["review"].values()) for row in records), block
            try:
                group = prior.binding["bind_block"](block, records, [bank[block] for bank in banks], hashes, arms, leads)
            except (AssertionError, KeyError, StopIteration) as error:
                raise ValueError(f"Could not rebind Hodram B{block} to {reference.as_posix()}") from error
            for row, original in zip(group["records"], sorted(records, key=lambda item: item["source_reference"]["offset"]), strict=True):
                assert row["id"] == original["id"]
                row.update(prior_registered_review=reference.as_posix(), prior_context=original["context"],
                           prior_source_meaning=original["source_meaning"], prior_localization_note=original["localization_note"])
            groups.append(group)

    counts = Counter(row["native_command_word"] for group in groups for row in group["records"])
    wraps = sum(len(group["open_wrap_leads"]) for group in groups)
    assert len(groups) == 15 and wraps == 20
    assert not OUTPUT.exists()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=clean, groups=groups,
                           earlier_reviews=reviews, contextual_review_pending=True, new_review_credit=0))
    print(f"Bound {sum(counts.values())} texts across {len(groups)} complete Hodram exchanges, including {wraps} wrap leads.")


if __name__ == "__main__":
    main()
