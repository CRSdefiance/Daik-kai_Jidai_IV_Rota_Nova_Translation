"""Reconcile exact credited route positions against the latest cumulative candidate."""

from collections import Counter
from pathlib import Path

from scripts import pair_hodram_opening_20261122 as hodram
from scripts import register_hodram_B311_B324_20261122 as build

base, native = build.base, build.native
OUT = Path("work/analysis/route_coverage_at_hodram_B324_20261122.json")
CENSUSES = (
    Path("work/story_source_coverage_20261109_SC0_v1/coverage.json"),
    hodram.CENSUS,
    Path("work/story_source_coverage_20261110_SC2_v8/coverage.json"),
    Path("work/story_source_coverage_20261110_SC3_v17/coverage.json"),
)
SHARED = Path("translations/editorial_checkpoints/SharedText_20261110_v1/shared_display_worklist_20261121_v3.json")


def main():
    assert not OUT.exists()
    release, shared, review = map(base.load, (build.RELEASE, SHARED, build.REVIEW))
    assert release["candidate_sha256"] == base.digest(build.ROM) == review["candidate_sha256"]
    assert release["clean_input_sha256"] == base.digest(native.CLEAN)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    old_proof = base.load(build.parent.RELEASE)
    assert old_proof["candidate_sha256"] == release["predecessor"]["candidate_sha256"] == base.digest(build.parent.ROM)
    clean, current, previous = [base.NdsImage.open(path) for path in (native.CLEAN, build.ROM, build.parent.ROM)]
    assert current.read_file("/COMMON/MESFILE.DK4") == previous.read_file("/COMMON/MESFILE.DK4")
    assert shared["candidate_sha256"] != release["candidate_sha256"] and len(shared["records"]) == 276
    mapped, field, value = (build.scope[name] for name in ("mapped", "field", "value"))
    with mapped(base.LEDGER) as ledger:
        _, start, stop, _ = field(ledger, "contextual_story_natural_dialogue_pass_v1871", 1)
        credited = {(row["file_path"], row["id"]) for row in value(ledger, "integrated_record_keys", 2, start, stop)}
    assert len(credited) == 27700
    rows = {}
    for route, path in enumerate(CENSUSES):
        census = base.load(path)
        archive = f"/data/SC{route}.DK4"
        clean_archive, active_archive, prior_archive = [image.read_file(archive) for image in (clean, current, previous)]
        blocks = native.IlnkContainer.parse(clean_archive).blocks
        assert census["source_ROM_sha256"] == release["clean_input_sha256"]
        assert native.digest(clean_archive) == census["source_archive_sha256"]
        assert not census["missing"] and not census["inventory_failures"] and not census["legacy_source_bindings_not_exact"]
        expected = (6887, 5356, 6720, 5129)[route]
        originals = census["records"]
        assert expected == len(originals)
        checked = set()
        for original in originals:
            assert original["covered"] and original["file_path"] == archive
            block, offset = original["block"], original["source_reference"]["offset"]
            source = bytes.fromhex(original["source_hex"])
            assert source and blocks[block][offset:offset + len(source)] == source
            key = block, offset
            assert key not in checked
            checked.add(key)
            references = original["exact_credited_source_bindings"]
            assert references and all((archive, ref["id"]) in credited for ref in references)
        if route == 1:
            installed = native.IlnkContainer.parse(active_archive).blocks
            assert len(review["records"]) == 590
            for record in review["records"]:
                ref = record["registered_reference"]
                block = installed[record["block"]]
                size = bytes.fromhex(ref["exact_stored_hex"])
                assert ref["archive_sha256"] == native.digest(active_archive)
                assert block[ref["offset"]:ref["offset"] + len(size)] == size and all(record["review"].values())
        else:
            assert active_archive == prior_archive
        rows[archive] = dict(
            exact_credited_clean_positions=len(checked),
            counts_by_kind=dict(Counter(record["kind"] for record in originals)),
            census=str(path), census_sha256=base.digest(path), installed_archive_sha256=native.digest(active_archive),
            same_archive_as_previous_candidate=active_archive==prior_archive,
            latest_registered_records_rechecked=590 if route==1 else 0,
        )
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], registry_sha256=release["registry_sha256"],
        ledger_sha256=base.digest(base.LEDGER), total_integrated_ledger_credits=len(credited), routes=rows,
        open_shared_stored_records=len(shared["records"]), shared_display_worklist=str(SHARED),
        shared_display_worklist_sha256=base.digest(SHARED), new_play_coverage=False,
        new_editorial_credit=0, full_goal_complete=False))
    print({archive: row["exact_credited_clean_positions"] for archive, row in rows.items()})


if __name__ == "__main__":
    main()

