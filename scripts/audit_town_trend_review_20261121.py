"""Reconcile the complete reviewed town-trend inventory against the registered ROM."""

from collections import defaultdict
from pathlib import Path

from scripts import register_hangzhou_veracruz_trends_20261121 as registered


base, native = registered.base, registered.native
OUT = registered.batch.OUTPUT.with_name("town_trend_exchange_coverage_20261121_v1.json")
SUFFIXES = (
    "town_trend_exchanges", "genoa_tomatoes", "hamburg_ceramics", "seville_stockholm_trends",
    "sao_jorge_basra_trends", "sofala_malacca_osaka_trends", "havana_calicut_istanbul_trends",
    "hangzhou_veracruz_trends",
)
FOLLOWUP = "story_tag_wraps"


def bound_command(block, reference, body):
    start, offset = reference["command_offset"], reference["offset"]
    assert offset == start + 5 and block[start:start + 2] == b"\x00\x40"
    assert block[offset:offset + len(body) + 1] == body + b"\0"
    if "complete_command_hex" in reference:
        raw = bytes.fromhex(reference["complete_command_hex"])
        assert block[start:start + len(raw)] == raw
    return start


def main():
    assert not OUT.exists()
    current = base.load(base.LEDGER)["current_integrated_candidate"]
    release = base.load(registered.RELEASE)
    assert base.digest(registered.ROM) == current["sha256"] == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"]
    proof_paths = {}
    groups = defaultdict(list)
    for suffix in SUFFIXES:
        path, = Path("releases").glob(f"*{suffix}_candidate/verification/registered_review.json")
        proof_paths[str(path)] = base.digest(path)
        for row in base.load(path)["records"]:
            groups[row["route"], row["block"]].append((path, row))
    followup_path, = Path("releases").glob(f"*{FOLLOWUP}_candidate/verification/registered_review.json")
    proof_paths[str(followup_path)] = base.digest(followup_path)
    followups = {(r["file_path"], r["id"]): r for r in base.load(followup_path)["records"]
                 if r["decision"] == "revision"}
    expected = {(route, index + shift)
                for route, shift in enumerate((39, 31, 27, 0)) for index in range(149, 169)}
    assert groups.keys() == expected
    assert len({(r["file_path"], r["id"]) for rows in groups.values() for _, r in rows}) == 1033
    originals, current_rom = map(base.NdsImage.open, (native.CLEAN, registered.ROM))
    clean_arm, current_arm = [image.read_file(native.ARM) for image in (originals, current_rom)]
    inventory, _, _ = native.scoped_inventory()
    verified = []
    for route in range(4):
        path = f"/data/SC{route}.DK4"
        source, installed = [native.IlnkContainer.parse(image.read_file(path)).blocks
                             for image in (originals, current_rom)]
        for _, index in sorted(key for key in groups if key[0] == route):
            old, new = source[index], installed[index]
            source_cmds, _ = inventory(clean_arm, old)
            installed_cmds, _ = inventory(current_arm, new)
            assert [c["word"] for c in source_cmds] == [c["word"] for c in installed_cmds]
            stored_offsets = {a["offset"]: b["offset"] for a, b in zip(source_cmds, installed_cmds, strict=True)
                              if a["word"] == 0x4000}
            positions = []
            paths = set()
            later, moved = [], []
            for record_path, row in groups[route, index]:
                paths.add(str(record_path))
                update = followups.get((path, row["id"]))
                if update is not None:
                    assert update["source_hex"] == row["source_hex"] and update["block"] == index
                    later.append(dict(id=row["id"], originally_reviewed=str(record_path),
                                      current_review=str(followup_path)))
                    paths.add(str(followup_path))
                    row = update
                source_ref = row["source_reference"]
                target_ref = row["registered_reference"]
                current_start = stored_offsets[source_ref["command_offset"]]
                if current_start != target_ref["command_offset"]:
                    moved.append(dict(id=row["id"], reviewed_offset=target_ref["command_offset"],
                                      installed_offset=current_start))
                    target_ref = target_ref | dict(command_offset=current_start, offset=current_start + 5)
                refs = source_ref, target_ref
                original_body = bytes.fromhex(row["source_hex"])
                final_body = bytes.fromhex(refs[1].get("exact_stored_hex") or refs[1]["raw_hex"])
                assert original_body[0] == final_body[0] == row["source_selector"]
                assert len(row["review"]) == 5 and all(row["review"].values())
                pair = []
                for side, block, ref, body in zip(("source", "installed"), (old, new), refs,
                                                   (original_body, final_body), strict=True):
                    try:
                        pair.append(bound_command(block, ref, body))
                    except AssertionError as error:
                        end = block.index(0, ref["offset"] + 1)
                        raise AssertionError((path, row["id"], side, ref, body,
                                              block[ref["offset"]:end])) from error
                positions.append(tuple(pair))
            assert sorted(positions) == list(stored_offsets.items())
            verified.append(dict(file_path=path, block=index, records=len(positions), original_commands=len(source_cmds),
                                 clean_block_sha256=native.digest(old), current_block_sha256=native.digest(new),
                                 registered_reviews=sorted(paths), later_registered_decisions=later,
                                 migrated_installed_command_offsets=moved))
    assert len(verified) == 80 and sum(g["records"] for g in verified) == 1033
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
                        storylines=4, town_trend_events=20, complete_route_exchanges=80, records=1033, groups=verified,
                        exact_review_receipts=proof_paths, all_five_record_gates_previously_passed=True,
                        audit_scope="Clean-source and installed dialogue commands only. Gameplay scope is in each linked receipt."))
    print("Verified 1,033 source and installed records in all 80 route copies of the 20 mapped town trend exchanges.")


if __name__ == "__main__":
    main()
