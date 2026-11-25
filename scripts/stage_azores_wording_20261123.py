"""Stage the observed Azores article, docking phrasing, and address corrections."""

import json
from dataclasses import replace
from hashlib import sha256
from pathlib import Path
from struct import iter_unpack, pack, pack_into, unpack_from

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.main_pool_cache_visibility import POOL, STAGE, cache_plan, wrapper
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts.prepare_azores_wording_20261123 import (
    ARM, BASE, COMMON, DOCK, NAME_CALLS, OUTPUT, RELEASE, digest, owned_entries, read,
)
from scripts.probe_common_display_name_hook import branch_link
from scripts.reconcile_editorial_acceptance_20261123 import reference


ROOT = Path(".codex-release-work/azores_wording_compact_20261123")
ROM = ROOT / "staged/Azores_Wording_STAGED.nds"
PROOF = ROM.parent / "stored_proof.json"
CLEAN = Path("work/clean.nds")
AZORES_VILLAGE = 0x0215AE30
AZORES_TOWN = 0x0215D040
RANK_ID = "ARM9_PROMISED_WORDS_CHIEF_REQUEST"
COMMON_IDS = {f"COMMON_MESSAGE_{key}": key for key in DOCK}
RETIRED_PAYLOAD_SIZE = 123040
RETIRED_CACHE_OFFSET = RETIRED_PAYLOAD_SIZE - 64


def digest_bytes(data):
    return sha256(data).hexdigest()


def common_rows(common, arm):
    return owned_entries(common, arm, digest_bytes(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))


def revise_docking(common, arm, rows):
    blocks = IlnkContainer.parse(common).blocks
    updated = blocks.copy()
    edits = {}
    for key in (69, 70):
        row = rows[key]
        start, end = row.block_offset, row.block_offset + len(row.text)
        assert row.block == 0 and updated[0][start:end] == row.text
        prose = DOCK[key][0].encode("ascii")
        assert prose.count(b"%s") == row.text.count(b"%s") == 1 and len(prose) <= len(row.text)
        # Terminal padding retains the two original native slots. Message 70
        # adjoins 71 in the same record and has no intervening NUL.
        edits[key] = prose.ljust(len(row.text), b" ")
        updated[0] = updated[0][:start] + edits[key] + updated[0][end:]
    result = IlnkContainer(updated).to_bytes()
    assert IlnkContainer.parse(result).blocks == updated
    for before, after in zip(rows, common_rows(result, arm), strict=True):
        assert replace(before, text=edits.get(before.message_id, before.text)) == after
    inverse = updated[0]
    for key in edits:
        row = rows[key]
        start, end = row.block_offset, row.block_offset + len(row.text)
        inverse = inverse[:start] + row.text + inverse[end:]
    assert IlnkContainer([inverse, *updated[1:]]).to_bytes() == common
    return result, edits


def name_wrapper(address):
    # Call the original virtual getter first. Preserve the getter's flags
    # and return its pointer unchanged for all other villages.
    code = pack("<11I",
        0xE92D4070,                  # push {r4, r5, r6, lr}
        0xE12FFF31,                  # blx r1
        0xE10F5000,                  # mrs r5, cpsr
        0xE59F4010,                  # ldr r4, village_pointer
        0xE1500004,                  # cmp r0, r4
        0x059F000C,                  # ldreq r0, sentence_pointer
        0xE128F005,                  # msr cpsr_f, r5
        0xE8BD4070,                  # pop {r4, r5, r6, lr}
        0xE12FFF1E,                  # bx lr
        AZORES_VILLAGE, address + 44,
    )
    return (code + b"the Azores\0").ljust(64, b"\0")


def retired_cache_slot(image, code, arm, payload):
    start, stop = RETIRED_CACHE_OFFSET, RETIRED_PAYLOAD_SIZE
    exact = wrapper(STAGE + start, STAGE + stop, stop, arm)
    assert bytes(payload[start:stop]) == exact
    assert cache_plan(arm)["entry"] == STAGE + len(payload) - 64 > STAGE + stop
    windows = [(address + start, address + stop) for address in (STAGE, POOL)]

    def in_slot(address):
        return any(lo <= address < hi for lo, hi in windows)

    def signed(value, bits):
        return value - (1 << bits) if value >> (bits - 1) else value

    units = [(s.ramAddress, s.data) for s in code.sections]
    units.append((POOL, payload))
    overlays = loadOverlayTable(image.rom.arm9OverlayTable, lambda _, file_id: image.rom.files[file_id])
    units.extend((s.ramAddress, s.data) for s in overlays.values())
    for base, source in units:
        for index, (word,) in enumerate(iter_unpack("<I", source[:len(source) & ~3])):
            pc = base + index * 4
            if in_slot(pc):
                continue
            assert not in_slot(word), (hex(pc), "literal")
            if word >> 25 & 7 == 5:
                target = pc + 8 + signed(word & 0xFFFFFF, 24) * 4
                if word >> 28 == 15:
                    target += (word >> 23) & 2
                assert not in_slot(target), (hex(pc), "ARM branch")
        previous = 0
        for index, (half,) in enumerate(iter_unpack("<H", source[:len(source) & ~1])):
            pc = base + index * 2
            if not in_slot(pc):
                if previous & 0xF800 == 0xF000 and half & 0xF800 in (0xF800, 0xE800):
                    target = pc + 2 + signed(previous & 2047, 11) * 4096 + (half & 2047) * 2
                    if half & 0xF800 == 0xE800:
                        target &= ~3
                    assert not in_slot(target), (hex(pc - 2), "Thumb long branch")
                if half & 0xF800 == 0xE000:
                    assert not in_slot(pc + 4 + signed(half & 2047, 11) * 2), (hex(pc), "Thumb branch")
                if half & 0xF000 == 0xD000 and half >> 8 & 15 < 14:
                    assert not in_slot(pc + 4 + signed(half & 255, 8) * 2), (hex(pc), "Thumb conditional branch")
            previous = half
    return exact


def revise_arm(image, arm, clean, review):
    original = MainCodeFile(arm, BASE)
    code = MainCodeFile(arm, BASE)
    assert bytes(original.save()) == arm
    original_stage = bytes(original.sections[3].data)
    assert original.sections[3].ramAddress == STAGE
    payload = bytearray(original_stage[:-48])
    old_size = len(payload)
    assert cache_plan(arm)["payload_bytes"] == old_size == 123264
    retired = retired_cache_slot(image, original, arm, payload)
    address = POOL + RETIRED_CACHE_OFFSET

    rank, = (row for row in review["records"] if row["id"] == RANK_ID)
    source_text = bytes.fromhex(rank["source_hex"])
    source_at = rank["source_reference"]["text_address"] - BASE
    assert clean[source_at:source_at + len(source_text) + 1] == source_text + b"\0"
    before = bytes.fromhex(rank["installed_hex"]) + b"\0"
    after = before.replace(b"Captain,", b"Admiral,", 1)
    rank_offset = rank["installed_reference"]["pool_offset"]
    assert before.startswith(b"Captain,") and payload[rank_offset:rank_offset + len(before)] == before
    assert after.decode("ascii").rstrip("\0").split() == rank["english"].split()
    payload[rank_offset:rank_offset + len(before)] = after

    helper = name_wrapper(address)
    payload[RETIRED_CACHE_OFFSET:RETIRED_PAYLOAD_SIZE] = helper
    assert len(payload) == old_size
    code.sections[3].data = payload + original_stage[-48:]
    prefix = code.sections[0].data
    assert unpack_from("<I", prefix, 0xE45DC)[0] == POOL + old_size
    for start, call_site, _, end in NAME_CALLS:
        assert arm[start:end] == clean[start:end]
        assert unpack_from("<I", prefix, call_site)[0] == 0xE12FFF31
        pack_into("<I", prefix, call_site, branch_link(BASE + call_site, address))
    assert prefix[AZORES_VILLAGE - BASE:AZORES_VILLAGE - BASE + 8] == b"Azores\0\0"
    assert prefix[AZORES_TOWN - BASE:AZORES_TOWN - BASE + 7] == b"Azores\0"

    result = bytes(code.save())
    loaded = MainCodeFile(result, BASE)
    assert cache_plan(result) == cache_plan(arm)
    mutable_fields = [(call_site, 4) for _, call_site, _, _ in NAME_CALLS]
    for at, length in mutable_fields:
        loaded.sections[0].data[at:at + length] = original.sections[0].data[at:at + length]
    restored = loaded.sections[3].data
    restored[rank_offset:rank_offset + len(before)] = before
    restored[RETIRED_CACHE_OFFSET:RETIRED_PAYLOAD_SIZE] = retired
    assert bytes(restored) == original_stage
    loaded.sections[3].data = restored
    for old, new in zip(original.sections, loaded.sections, strict=True):
        assert (old.ramAddress, old.bssSize, bytes(old.data)) == (new.ramAddress, new.bssSize, bytes(new.data))
    assert bytes(loaded.save()) == arm
    return result, dict(runtime_entry=address, alias_address=address + 44, helper_hex=helper.hex(),
                        native_call_sites=[BASE + field for _, field, _, _ in NAME_CALLS],
                        payload_bytes=old_size, cache_plan=cache_plan(result),
                        retired_cache_slot=dict(pool_offset=RETIRED_CACHE_OFFSET, original_hex=retired.hex(),
                                                zero_external_literal_arm_or_thumb_targets_in_parent=True),
                        rank_pool_offset=rank_offset, rank_body_hex=after[:-1].hex(),
                        owned_static_fields=mutable_fields)


def main():
    assert not PROOF.exists()
    release, review = read(RELEASE), read(OUTPUT)
    parent = Path(release["candidate"])
    assert digest(parent) == review["candidate_sha256"] == release["candidate_sha256"]
    assert digest(CLEAN) == review["clean_sha256"] == release["clean_input_sha256"]
    assert digest("translations/release_stack.json") == release["registry_sha256"]
    image = NdsImage.open(parent)
    arm, common = image.read_file(ARM), image.read_file(COMMON)
    clean_arm = NdsImage.open(CLEAN).read_file(ARM)
    assert digest_bytes(arm) == release["target_ARM9_sha256"]
    assert digest_bytes(common) == release["target_COMMON_sha256"]
    rows = common_rows(common, arm)
    for row in review["records"]:
        assert all(row["review"][gate] is True for gate in ("source", "context", "localization", "naturalness"))
        if row["id"] in COMMON_IDS:
            assert rows[COMMON_IDS[row["id"]]].text.hex() == row["installed_hex"]
        else:
            assert row["id"] == RANK_ID
    target_common, edits = revise_docking(common, arm, rows)
    target_arm, runtime = revise_arm(image, arm, clean_arm, review)
    after = common_rows(target_common, target_arm)
    assert all(row.text == edits.get(row.message_id, rows[row.message_id].text) for row in after)
    image.replace_file(ARM, target_arm)
    image.replace_file(COMMON, target_common)
    candidate = bytes(image.rom.save())
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.read_bytes()
    ROM.parent.mkdir(parents=True, exist_ok=True)
    prefix = ROM.read_bytes() if ROM.is_file() else b""
    assert candidate.startswith(prefix), "Existing stage must be the exact candidate prefix"
    with ROM.open("ab") as out:
        for offset in range(len(prefix), len(candidate), 1 << 20):
            out.write(candidate[offset:offset + (1 << 20)])
    candidate_sha = digest_bytes(candidate)
    assert digest(ROM) == candidate_sha
    PROOF.write_text(json.dumps(dict(
        candidate=reference(ROM), candidate_sha256=candidate_sha, predecessor=reference(parent),
        source_review=reference(OUTPUT), clean_sha256=review["clean_sha256"],
        target_ARM9_sha256=digest_bytes(target_arm), target_COMMON_sha256=digest_bytes(target_common),
        modified_paths=[ARM, COMMON], updated_templates={key: value.hex() for key, value in edits.items()},
        runtime=runtime, whole_parent_inverse=True, display_checks_pending=True,
    ), ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(f"Staged {candidate_sha}. Exact inversion recovered the registered parent.")


if __name__ == "__main__":
    main()
