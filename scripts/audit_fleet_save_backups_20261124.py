"""Inventory the Fleet Info fields in the existing DS battery-save backups."""

from collections import Counter
from pathlib import Path
from struct import unpack_from

from dk4tool.rom.nds import NdsImage
from scripts.stage_cartridge_title_20261123 import CLEAN, digest, read, reference, sha256, write


ROOT = Path("translations/editorial_checkpoints/shared_display_20261123")
INPUT = ROOT / "fleet_battery_fields_20261124.json"
OUT = ROOT / "fleet_save_backup_audit_20261124.json"
SAVES = Path("E:/Rota Nova translations/Saves")
RELEASE = Path("releases/all_routes_editorial_20261124_yard_numerals_candidate/verification/registered_release_verification.json")
ARM, BASE = "/__arm9__.bin", 0x02000000
SLOT_BYTES, SLOT_COUNT = 0xA000, 6
COUNTS = {"docking": 63, "destination": 63, "headquarters": 20}
ORDINARY_OR_NO_TARGET = {*range(90), 115}


def fields_from_observed_reads(proof):
    cases = proof["ordinary_restores"]
    assert {row["case"] for row in cases} == {"copenhagen", "nagasaki"}
    maps = []
    for case in cases:
        rows = case["all_read_fields"]
        offsets = {(r["field"], r["index"]): r["serialized_offset"] for r in rows}
        expected = {(field, index) for field, count in COUNTS.items() for index in range(count)}
        assert offsets.keys() == expected and len(rows) == len(set(offsets.values())) == len(expected)
        assert all(8 <= offset < SLOT_BYTES for offset in offsets.values())
        donor = case["pristine_donor"]
        raw = Path(donor["path"]).read_bytes()
        assert sha256(raw).hexdigest() == donor["sha256"]
        start = case["verified_slot_index"] * SLOT_BYTES
        slot = raw[start:start + SLOT_BYTES]
        assert sha256(slot).hexdigest() == case["slot_sha256"]
        assert all(slot[row["serialized_offset"]] == row["saved"] for row in rows)
        maps.append(offsets)
    assert maps[0] == maps[1]
    return {field: [maps[0][field, i] for i in range(count)] for field, count in COUNTS.items()}


def backup_slots(path, offsets):
    raw = path.read_bytes()
    assert len(raw) == 262266 and raw.endswith(b"|-DESMUME SAVE-|")
    slots = []
    for index in range(SLOT_COUNT):
        start = index * SLOT_BYTES
        slot = raw[start:start + SLOT_BYTES]
        ref = dict(slot_index=index, offset=start, sha256=sha256(slot).hexdigest())
        if slot == b"\xff" * SLOT_BYTES:
            slots.append(ref | {"status": "empty"})
            continue
        if slot[:4] != b"DK4R":
            slots.append(ref | {"status": "unrecognized_header", "header": slot[:4].hex()})
            continue
        checksum, = unpack_from("<I", slot, 4)
        signed_sum = sum(value if value < 128 else value - 256 for value in slot[8:]) & 0xFFFFFFFF
        if checksum != signed_sum:
            slots.append(ref | dict(status="bad_checksum", stored_checksum=checksum, computed_checksum=signed_sum))
            continue
        fields = {field: bytes(slot[at] for at in positions).hex() for field, positions in offsets.items()}
        slots.append(ref | dict(status="valid", checksum=checksum, fields_hex_by_index=fields))
    return dict(path=path.as_posix(), sha256=sha256(raw).hexdigest(), slots=slots)


def main():
    release, observed = map(read, (RELEASE, INPUT))
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(release["candidate"]) == release["candidate_sha256"]
    clean, current = (NdsImage.open(path).read_file(ARM) for path in (CLEAN, release["candidate"]))
    assert sha256(current).hexdigest() == release["target_ARM9_sha256"]
    spans = observed["original_restore_source"]["spans"]
    for row in spans:
        start, end = row["start"] - BASE, row["end"] - BASE
        assert clean[start:end] == current[start:end] and sha256(current[start:end]).hexdigest() == row["exact_sha256"]

    offsets = fields_from_observed_reads(observed)
    backups = [backup_slots(path, offsets) for path in sorted(SAVES.glob("*.dsv"))]
    assert backups and {row["pristine_donor"]["sha256"] for row in observed["ordinary_restores"]} <= {row["sha256"] for row in backups}
    states = Counter(slot["status"] for backup in backups for slot in backup["slots"])
    assert sum(states.values()) == len(backups) * SLOT_COUNT
    assert states["valid"] > 0
    field_values = {field: Counter() for field in COUNTS}
    unique_slots, unique_vectors = set(), set()
    special = []
    for backup in backups:
        for slot in backup["slots"]:
            if slot["status"] != "valid":
                continue
            unique_slots.add(slot["sha256"])
            fields = slot["fields_hex_by_index"]
            unique_vectors.add(tuple(fields.values()))
            for field, serialized in fields.items():
                values = bytes.fromhex(serialized)
                assert len(values) == COUNTS[field]
                field_values[field].update(values)
                special.extend(dict(path=backup["path"], slot_index=slot["slot_index"], field=field, index=index, value=value)
                               for index, value in enumerate(values) if value not in ORDINARY_OR_NO_TARGET)

    write(OUT, dict(candidate_sha256=release["candidate_sha256"], exact_source_and_current_restore_spans=spans,
                    save_root=SAVES.as_posix(), backup_count=len(backups), slot_states=dict(states),
                    distinct_valid_slots=len(unique_slots), distinct_field_vectors=len(unique_vectors),
                    serialized_offsets_by_field_and_index=offsets, field_value_counts={k: dict(sorted(v.items())) for k, v in field_values.items()},
                    field_bytes_checked=sum(sum(counts.values()) for counts in field_values.values()),
                    special_inputs=special, backups=backups, proof_sources=list(map(reference, (RELEASE, INPUT))),
                    scope="Offline census of existing checksum-valid slots using offsets from earlier ordinary loads. Covers bytes at save ingress. Other backups and later runtime writes are outside this census.",
                    ordinary_gameplay_added=False, ROM_changed=False, new_editorial_credit=0))
    print(f"Checked {states['valid']} checksum-valid slots in {len(backups)} backups, including {len(unique_slots)} distinct slots. "
          f"Found {len(special)} values beyond the ordinary ports and sentinel 115.")


if __name__ == "__main__":
    main()
