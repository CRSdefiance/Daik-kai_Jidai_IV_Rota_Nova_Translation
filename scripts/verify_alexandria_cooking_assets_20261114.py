"""Verify the translated Alexandria text and preserve all original conditional commands."""

from pathlib import Path
from struct import pack, pack_into, unpack_from

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import review_alexandria_cooking_exchange_20261114 as edit
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine


base = edit.base
stage = edit.stage
parent = edit.parent
WORK = edit.ROOT
RECEIPT = WORK / "stored_candidate_assets.json"
REVIEW = edit.OUT.with_name("alexandria_cooking_exchange_reviewed_20261114_v1.json")
VIEWED = (
    "8603ebb668dcf070e27ad62dc80ea1f8678a2b4d9b0ea225d19a378d475d35d5",
    "43011a0a4fcd1977a0a2ce7f98b85a1559523ecf963935601e9eb9dc85ad5abd",
    "ea84da8b97cb9f486d3d503f845312fe091e9b6d22bc6bcd7ef987c0af088d60",
    "50b461f221d4191990069b69d008ad55b478186b4d84c34ab6b3b8427fa27897",
)
SKIP_WORDS = {0x100, 0x200, 0x300, 0x400}
OWNER, STREAM, RESULT, LENGTH = 0x02650000, 0x02660000, 0x02668000, 0x02668100
RESULT_CASES = (0, 1, 2, 3, 0xFFFFFFFF)
GUARD = b"\xA5" * 16


def splice(blob, rows, source_field, at_field, target_field):
    logical = unpack_from("<H", blob, 4)[0] + 8
    assert blob[logical:] == bytes(-logical % 4)
    parts = bytearray(blob[:8])
    start = 8
    offsets = {}
    for row in rows:
        at = row[at_field]
        before = bytes.fromhex(row[source_field])
        after = bytes.fromhex(row[target_field])
        assert (len(after) - len(before)) % 4 == 0
        assert start < at and blob[at:at + len(before)+1] == before + b"\0"
        assert before[0] == after[0] and b"\0" not in after[1:]
        parts.extend(blob[start:at])
        offsets[row["id"]] = len(parts)
        parts.extend(after)
        start = at + len(before)
    parts.extend(blob[start:logical])
    assert len(parts) <= 0x2400 and len(parts) % 4 == logical % 4
    pack_into("<H", parts, 4, len(parts) - 8)
    return bytes(parts) + bytes(-len(parts) % 4), offsets


def compare_commands(arm, old, new, inventory, owned_rows):
    old_commands, old_records = stage.prior.raw_speeches(arm, old, inventory)
    new_commands, new_records = stage.prior.raw_speeches(arm, new, inventory)
    new_logical = unpack_from("<H", new, 4)[0] + 8
    old_logical = unpack_from("<H", old, 4)[0] + 8
    assert len(old_commands) == len(new_commands) == 24
    assert len(old_records) == len(new_records) == 12
    mapping = {a["offset"]: b["offset"] for a, b in zip(old_commands, new_commands, strict=True)}
    mapping[old_logical] = new_logical
    by_current_offset = {row["current_reference"]["offset"]: row for row in owned_rows}
    first_control = next(cmd["offset"] for cmd in old_commands if cmd["word"] == 0x8000)
    assert old[first_control:old_logical] == new[mapping[first_control]:new_logical]
    cases = []
    for a, b in zip(old_commands, new_commands, strict=True):
        assert a["word"] == b["word"] and a["offset"] % 4 == b["offset"] % 4
        if a["word"] == 0x4000:
            continue
        assert a["whole_command_hex"] == b["whole_command_hex"]
        if a["word"] in SKIP_WORDS:
            span = unpack_from("<H", old, a["offset"]+2)[0]
            assert mapping[a["offset"]+4] == b["offset"]+4
            assert mapping[a["offset"]+4+span] == b["offset"]+4+span
            cases.append(dict(word=a["word"], before=a["offset"], after=b["offset"], span=span))
    for a, b in zip(old_records, new_records, strict=True):
        assert a["complete_preamble_hex"] == b["complete_preamble_hex"]
        assert a["record_index"] == b["record_index"]
        assert [mapping[at] for at in a["ancestors"]] == b["ancestors"]
        if a["offset"] in by_current_offset:
            row = by_current_offset[a["offset"]]
            assert b["raw_hex"] == row["requested_relocated_hex"]
            assert b["offset"] == row["proposed_record_offset"]
            row["proposed_stored_reference"] = b
        else:
            assert a["raw_hex"] == b["raw_hex"]
    assert len(cases) == 6
    return mapping, cases


def verify_skips(cpu, old, after, branches):
    hits = []
    baseline = bytes(cpu.mem_read(0x02000000, 0x400000))
    for side, block in (("before", old), ("after", after)):
        cpu.mem_write(STREAM - 16, GUARD + block + GUARD)
        for branch in branches:
            at = branch[side]
            word, span = branch["word"], branch["span"]
            for last in RESULT_CASES:
                owner = GUARD + pack("<4I", 0, STREAM+at, 0, 0) + GUARD
                cpu.mem_write(OWNER - 16, owner)
                cpu.mem_write(RESULT - 16, GUARD + bytes(24) + GUARD)
                cpu.mem_write(LENGTH - 16, GUARD + bytes(4) + GUARD)
                call(cpu, 0x2A510, (RESULT, OWNER, LENGTH, last))
                selected = word == 0x100 or last == {0x200: 0, 0x300: 1, 0x400: 2}.get(word)
                extent = 4 + (span if selected else 0)
                assert unpack_from("<I", cpu.mem_read(LENGTH, 4))[0] == extent
                assert bytes(cpu.mem_read(RESULT - 16, 56)) == GUARD + pack("<6I", 3, 0, 0, 0, 0, 0) + GUARD
                assert bytes(cpu.mem_read(OWNER - 16, len(owner))) == owner
                assert bytes(cpu.mem_read(LENGTH - 16, 36)) == GUARD + pack("<I", extent) + GUARD
                assert bytes(cpu.mem_read(STREAM - 16, len(block)+32)) == GUARD + block + GUARD
                assert bytes(cpu.mem_read(0x02000000, 0x400000)) == baseline
                hits.append(dict(side=side, word=word, last_result=last, command_offset=at, next_offset=at+extent))
    return hits


def main():
    assert not REVIEW.exists() and not RECEIPT.exists()
    draft, preview, release = map(base.load, (edit.OUT, WORK/"native_preview.json", parent.RELEASE))
    assert base.digest(edit.OUT) and base.digest(WORK/"native_preview.json") == draft["checked_native_preview_sha256"]
    assert tuple(base.digest(row["path"]) for row in preview["sheets"]) == tuple(row["sha256"] for row in preview["sheets"]) == VIEWED
    assert preview["checked_individual_pages"] == 26
    assert base.digest(parent.ROM) == release["candidate_sha256"] == draft["candidate_sha256"] == preview["runtime"]["candidate_sha256"]
    current, clean = map(base.NdsImage.open, (parent.ROM, stage.CLEAN))
    arm, original_arm = [rom.read_file(stage.ARM) for rom in (current, clean)]
    assert all(arm[a:b] == original_arm[a:b] for a,b in ((0x2A414,0x2A530),(0x24048,0x24118)))
    inventory, _, _ = stage.prior.scoped_inventory()
    cpu = machine(arm)
    outputs = []
    for group in draft["complete_exchanges"]:
        path, block = group["file_path"], group["block"]
        archive = current.read_file(path)
        clean_archive = clean.read_file(path)
        bank = stage.IlnkContainer.parse(archive)
        old = bank.blocks[block]
        assert edit.digest(old) == group["current_block_sha256"]
        clean_block = stage.IlnkContainer.parse(clean_archive).blocks[block]
        assert edit.digest(clean_block) == group["source_block_sha256"]
        selected = []
        for row in draft["records"]:
            if row["file_path"] != path:
                continue
            if row["decision"] == "reflow":
                assert row["current_hex"] == row["requested_relocated_hex"]
                row["decision"] = "retention"
                row["localization_note"] += " The planner returns the exact stored text. The existing wrap keeps the dissatisfied-customer clause and the catchphrase legible."
            row["current_record_offset"] = row["current_reference"]["offset"]
            if row["decision"] == "revision":
                selected.append(row)
        new, offsets = splice(old, selected, "current_hex", "current_record_offset", "requested_relocated_hex")
        for row in selected:
            row["proposed_record_offset"] = offsets[row["id"]]
        roundtrip, restored_offsets = splice(new, selected, "requested_relocated_hex", "proposed_record_offset", "current_hex")
        assert roundtrip == old
        assert restored_offsets == {row["id"]: row["current_record_offset"] for row in selected}
        mapping, branches = compare_commands(arm, old, new, inventory, selected)
        checks = verify_skips(cpu, old, new, branches)
        bank.blocks[block] = new
        output = bank.to_bytes()
        check = stage.IlnkContainer.parse(output)
        assert len(bank.blocks) == len(check.blocks)
        assert {i for i,(a,b) in enumerate(zip(stage.IlnkContainer.parse(archive).blocks, check.blocks, strict=True)) if a != b} == {block}
        check.blocks[block] = old
        assert check.to_bytes() == archive
        path_on_disk = WORK / Path(path).name
        path_on_disk.write_bytes(output)
        outputs.append(dict(file_path=path, source_archive_sha256=edit.digest(archive),
            proposed_archive_sha256=edit.digest(output), proposed_archive=str(path_on_disk), block=block,
            owned_record_count=len(selected), mapping=mapping, native_relative_decoder_cases=checks,
            proposed_block_sha256=edit.digest(new), signed_size_delta=len(new)-len(old),
            unchanged_conditional_effect_system_panel_and_return_tail=True, exact_archive_inverse=True))
    assert sum(len(item["native_relative_decoder_cases"]) for item in outputs) == 240
    assert sum(item["owned_record_count"] for item in outputs) == 12
    for row in draft["records"]:
        row["review"]["formatting"] = True
        row["display_approval_scope"] = ("Fresh native rendering and directly viewed preview for the proposed stored text."
            if row["decision"] == "revision" else "Exact stored record retained from the current registered candidate.")
    validate_natural_dialogue_batch(draft)
    base.save(RECEIPT, dict(candidate_sha256=release["candidate_sha256"], routes=outputs,
        editorial_draft_sha256=base.digest(edit.OUT), preview_sha256=base.digest(WORK/"native_preview.json"),
        native_tail_skips_checked=240, first_command_entry_same=True,
        target_archive_loader_catalog_and_actual_gameplay_checks_pending=True,
        registration_pending=True))
    base.save(REVIEW, draft | dict(format_gate_pending=False, display_scope="Offline",
        decision_counts=dict(revision=12, retention=36), directly_viewed_sheets=preview["sheets"],
        stored_archive_candidate_receipt=str(RECEIPT), stored_archive_candidate_receipt_sha256=base.digest(RECEIPT)))
    print("Sealed 48 decisions and four reversible archive candidates. 240 native conditional decoder cases passed.")


if __name__ == "__main__":
    main()

