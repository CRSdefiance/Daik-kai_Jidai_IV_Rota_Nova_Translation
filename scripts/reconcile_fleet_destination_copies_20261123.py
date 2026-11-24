"""Check which Fleet Info destination calls only reuse the stored byte."""

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn import UC_ARCH_ARM, UC_MODE_ARM, Uc
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R4
from unicorn.arm_const import UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8

from scripts import reconcile_fleet_destination_writers_20261123 as prior
from scripts import reconcile_genoa_acceptance_20261123 as genoa


OUT = prior.OUT.with_name("fleet_destination_copies_20261123.json")
PREEXISTING_DESTINATION = {
    0x0202EDE4: ("r7", UC_ARM_REG_R7, 1),
    0x0202FC54: ("r5", UC_ARM_REG_R5, 3),
    0x0202FD80: ("r6", UC_ARM_REG_R6, 8),
    0x0202FFBC: ("r6", UC_ARM_REG_R6, 3),
    0x0202FFD4: ("r6", UC_ARM_REG_R6, 8),
    0x020345BC: ("r4", UC_ARM_REG_R4, 8),
    0x02034658: ("r4", UC_ARM_REG_R4, 3),
    0x0203466C: ("r4", UC_ARM_REG_R4, 8),
    0x02035860: ("r5", UC_ARM_REG_R5, 6),
}
STOCK_RECORD_IMPORT = 0x020CDBDC
STOCK_RECORD_LOOKUP = 0x020CDCA0
STOCK_RECORD_BASE = 0x0211C1C0
STOCK_RECORD_SIZE = 0x18
STOCK_CALLS = (0x020CDC7C, 0x020CDC94)
STOCK_RECORDS = 64
WRITER, BASE = prior.WRITER, prior.BASE
FLEET = 0x02300000
RETURN = FLEET + 0x100


def main():
    receipt = genoa.sealed(genoa.PACKAGES[-1], "verification/registered_release_verification.json")
    release, historical = map(prior.read, (receipt, prior.RELEASE))
    assert prior.digest(release["candidate"]) == release["candidate_sha256"]
    assert prior.digest(historical["candidate"]) == historical["candidate_sha256"]
    installed, earlier, clean = [prior.NdsImage.open(p) for p in
                                 (release["candidate"], historical["candidate"], prior.CLEAN)]
    current_arm, earlier_arm, clean_arm = [rom.read_file(prior.ARM) for rom in (installed, earlier, clean)]
    previous_census = prior.read(prior.OUT)["native_reference_census"][str(WRITER)]
    census = prior.references(installed)[WRITER]
    assert census == previous_census and len(census["aligned_ARM_BL"]) == 27
    scoped_calls = set(PREEXISTING_DESTINATION) | set(STOCK_CALLS) | {prior.SCHEDULED_WRITE}
    assert scoped_calls <= {pc for _, pc in census["aligned_ARM_BL"]}
    remaining_calls = sorted(pc for _, pc in census["aligned_ARM_BL"] if pc not in scoped_calls)

    def stable(start, stop):
        code = prior.code_at(current_arm, start, stop)
        assert code == prior.code_at(earlier_arm, start, stop) == prior.code_at(clean_arm, start, stop)
        return code

    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.mem_map(BASE, 0x400000)
    writer = stable(WRITER, WRITER + 12)
    cpu.mem_write(WRITER, writer)
    copies = []
    for address, (name, reg, order) in PREEXISTING_DESTINATION.items():
        start = address - 12
        code = stable(start, address + 4)
        assert [(i.mnemonic, i.op_str) for i in md.disasm(code, start)] == [
            ("ldrb", f"r2, [{name}, #0x3f]"), ("mov", f"r0, {name}"),
            ("mov", f"r1, #{order}"), ("bl", f"#{WRITER:#x}")
        ]
        cpu.mem_write(start, code)
        for value in range(256):
            fleet = bytearray([0x5A] * prior.FLEET_STRIDE)
            fleet[0x3F] = value
            cpu.mem_write(FLEET, bytes(fleet))
            prior.run_fragment(cpu, start, address + 4, ((reg, FLEET),))
            fleet[0x3E] = order
            assert bytes(cpu.mem_read(FLEET, len(fleet))) == fleet, (address, value)
        copies.append(dict(call=address, exact_caller_bytes=code.hex(),
                           order=order, unchanged_destination_byte_cases=256))

    # The initializer can write the destination directly or take its docking byte through the writer.
    init_start, init_stop = 0x020CDB48, STOCK_RECORD_LOOKUP
    initializer = stable(init_start, init_stop)
    imported = stable(STOCK_RECORD_IMPORT, STOCK_RECORD_IMPORT + 16)
    assert [(i.mnemonic, i.op_str) for i in md.disasm(imported, STOCK_RECORD_IMPORT)] == [
        ("ldrb", "r4, [r7, #0x12]"), ("strb", "r4, [r8, #0x3e]"),
        ("ldrb", "r4, [r7, #0x13]"), ("strb", "r4, [r8, #0x3f]")
    ]
    getter = 0x02034674
    lookup = stable(STOCK_RECORD_LOOKUP, STOCK_RECORD_LOOKUP + 20)
    cpu.mem_write(STOCK_RECORD_LOOKUP, lookup)
    cpu.mem_write(init_start, initializer)
    cpu.mem_write(getter, stable(getter, getter + 20))
    table = stable(STOCK_RECORD_BASE, STOCK_RECORD_BASE + STOCK_RECORD_SIZE * STOCK_RECORDS)
    cpu.mem_write(STOCK_RECORD_BASE, table)
    stock_rows = []
    for i in range(STOCK_RECORDS):
        row = table[i * STOCK_RECORD_SIZE:(i + 1) * STOCK_RECORD_SIZE]
        address = STOCK_RECORD_BASE + i * STOCK_RECORD_SIZE
        prior.run_fragment(cpu, STOCK_RECORD_LOOKUP, RETURN, ((UC_ARM_REG_R0, i), (UC_ARM_REG_LR, RETURN)))
        assert cpu.reg_read(UC_ARM_REG_R0) == address
        assert all(value < 90 or value == 115 for value in (row[0x10], row[0x13])), (i, row.hex())
        prior.run_fragment(cpu, 0x020CDBC4, 0x020CDC10, ((UC_ARM_REG_R7, address), (UC_ARM_REG_R8, FLEET)))
        assert bytes(cpu.mem_read(FLEET + 0x3C, 4)) == row[0x10:0x14]
        destination = 115 if row[0x16] & 8 else row[0x10]
        assert cpu.reg_read(UC_ARM_REG_R5) == destination
        if destination != 115:
            for call in STOCK_CALLS:
                prior.run_fragment(cpu, call - 12, call + 4, ((UC_ARM_REG_R8, FLEET),))
                assert bytes(cpu.mem_read(FLEET + 0x3F, 1)) == bytes([destination])
        stock_rows.append(dict(fleet_index=i, exact_record_hex=row.hex(),
                               initial_destination=row[0x13], docking_or_cancel=destination))

    prior.write(OUT, dict(candidate_sha256=release["candidate_sha256"], registered_receipt=prior.reference(receipt),
        earlier_fleet_evidence=prior.reference(prior.OUT), mode="offline native fragments and static byte checks",
        matched_clean_and_earlier_call_bytes=True, original_writer_bytes=writer.hex(),
        writer_census=census, copies=copies, total_native_fragment_cases=256 * len(copies),
        other_writer_calls=remaining_calls, scheduled_call_already_scoped=prior.SCHEDULED_WRITE,
        stock_fleet_initialization=dict(initializer_start=init_start, initializer_sha256=prior.digest_bytes(initializer),
            exact_import_hex=imported.hex(), lookup=STOCK_RECORD_LOOKUP, exact_lookup_hex=lookup.hex(),
            table_address=STOCK_RECORD_BASE, table_sha256=prior.digest_bytes(table), rows=stock_rows,
            derived_calls=list(STOCK_CALLS), no_missionary_slot_from_shipped_rows=True),
        missionary_ordinary_gameplay_reachability_unresolved=True))
    print(f"Verified {len(copies)} destination-copy sites, {STOCK_RECORDS} stock fleet records and their two derived writer calls.")


if __name__ == "__main__":
    main()
