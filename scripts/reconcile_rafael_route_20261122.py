"""Reconcile the sealed Rafael source census and the last contextual packets."""

from collections import Counter
from pathlib import Path

from scripts import pair_rafael_B281_B300_20261122 as first
from scripts import pair_rafael_B301_B342_20261122 as later
from scripts import reconcile_rafael5186_coverage_v1 as census
from scripts import register_rafael_B306_B309_20261122 as latest


base, native = latest.base, latest.native
ARCHIVE = "/data/SC0.DK4"
OUTPUT = Path("work/analysis/rafael_contextual_route_20261122.json")
PACKETS = (
    (first.PAIRED, first.ROOT / "earlier_contextual_decisions_B281_B300.json"),
    *((later.paths(start)[1], later.paths(start)[0] / "earlier_contextual_decisions.json") for start in (301, 321)),
)


def verify_bytes(blocks, group_hashes, number, reference, raw):
    block = blocks[number]
    offset = reference["offset"]
    assert block[offset:offset + len(raw)] == raw, (number, offset)
    if "block_sha256" in reference:
        assert group_hashes[number] == reference["block_sha256"], number


def main():
    assert not OUTPUT.exists()
    source, release, reviewed = map(base.load, (census.OUT, latest.RELEASE, latest.REVIEW))
    assert source["source_ROM_sha256"] == release["clean_input_sha256"] == base.digest(native.CLEAN)
    assert release["candidate_sha256"] == reviewed["candidate_sha256"] == base.digest(latest.ROM)
    assert release["registry_sha256"] == base.digest(base.REGISTRY)
    clean_archive, current_archive = [
        base.NdsImage.open(path).read_file(ARCHIVE) for path in (native.CLEAN, latest.ROM)
    ]
    clean, current = [native.IlnkContainer.parse(raw).blocks for raw in (clean_archive, current_archive)]
    clean_hashes, current_hashes = [[native.digest(block) for block in blocks] for blocks in (clean, current)]
    assert len(clean) == len(current) == 343
    original = {row["id"]: row for row in source["records"]}
    assert len(original) == source["source_objects"] == 6887 and not source["missing"]
    for row in original.values():
        assert row["covered"] and row["exact_credited_source_bindings"] and row["file_path"] == ARCHIVE
        verify_bytes(clean, clean_hashes, row["block"], row["source_reference"], bytes.fromhex(row["source_hex"]))

    mapped, field, value = (latest.scope[name] for name in ("mapped", "field", "value"))
    with mapped(base.LEDGER) as ledger:
        _, start, stop, _ = field(ledger, "contextual_story_natural_dialogue_pass_v1871", 1)
        credited = {(row["file_path"], row["id"]) for row in value(ledger, "integrated_record_keys", 2, start, stop)}
    assert len(credited) == 27700
    assert all((ARCHIVE, binding["id"]) in credited for row in original.values()
               for binding in row["exact_credited_source_bindings"])

    installed = {row["id"]: row for row in reviewed["records"]}
    fresh = {row["id"] for row in reviewed["records"] if "earlier_contextual_decision" not in row}
    assert len(installed) == 61 and len(fresh) == 53
    seen, counts, packet_evidence = set(), Counter(), {}
    for paired_path, carry_path in PACKETS:
        packet, carry = map(base.load, (paired_path, carry_path))
        assert packet["candidate_sha256"] == carry["candidate_sha256"] == release["predecessor"]["candidate_sha256"]
        assert base.digest(paired_path) == carry["source_packet_sha256"]
        carried = {row["id"]: row for row in carry["reused_records"]}
        pending = {row["id"] for row in carry["pending_records"]}
        assert not pending & carried.keys() and pending <= fresh
        for group in packet["groups"]:
            for pair in group["records"]:
                ident, block = pair["id"], pair["block"]
                assert ident not in seen and 281 <= block <= 342
                seen.add(ident)
                assert (ident in pending) != (ident in carried)
                source_ref = pair["source_reference"]
                selector = bytes([pair["selector"]]) if pair["native_command_word"] == 0x4000 else b""
                jp = selector + bytes.fromhex(source_ref["exact_body_hex"])
                assert original[ident]["source_hex"] == jp.hex()
                assert original[ident]["block"] == block and original[ident]["source_reference"]["offset"] == source_ref["offset"]
                verify_bytes(clean, clean_hashes, block, source_ref, jp)
                if ident in carried:
                    prior = carried.pop(ident)
                    assert prior["source_reference"] == source_ref and prior["current_reference"] == pair["current_reference"]
                    assert prior["editorial_decision_carried"] and all(prior["prior_review_gates"].values())
                if ident in installed:
                    final = installed.pop(ident)
                    assert final["source_reference"] == source_ref and all(final["review"].values())
                    ref = final["registered_reference"]
                    assert ref["archive_sha256"] == native.digest(current_archive)
                    body = bytes.fromhex(ref["exact_stored_hex"])
                else:
                    ref = pair["current_reference"]
                    body = selector + bytes.fromhex(ref["exact_body_hex"])
                verify_bytes(current, current_hashes, block, ref, body)
                counts["fresh" if ident in pending else "carried"] += 1
        assert not carried
        packet_evidence.update({str(path): base.digest(path) for path in (paired_path, carry_path)})
    assert not installed and counts == {"carried": 1201, "fresh": 53}
    assert seen == {ident for ident, row in original.items() if 281 <= row["block"] <= 342}
    evidence = {str(path): base.digest(path) for path in (census.OUT, latest.REVIEW, latest.RELEASE, base.LEDGER)}
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], clean_inventory_objects=len(original),
        clean_records_with_existing_credit=len(original), inventory_by_kind=source["object_counts"],
        recent_scope="SC0 B281–342", recent_current_ROM_bytes_checked=len(seen),
        recent_contextual_decisions=dict(counts), evidence=evidence | packet_evidence, new_editorial_credit=0,
        new_gameplay_coverage=False, scoped_to_story_dialogue_style_alternatives_and_choice_captions=True,
        other_Rafael_resources_and_trigger_paths_covered_by_separate_evidence=True, full_editorial_goal_complete=False))
    print("Reconciled 6,887 credited Rafael source objects and 1,254 exact late-route entries on the new ROM.")


if __name__ == "__main__":
    main()
