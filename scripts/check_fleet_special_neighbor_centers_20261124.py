"""Check original neighbor lookups for the Missionary and no-target slots."""

from struct import pack, unpack

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from scripts import reconcile_fleet_docking_inputs_20261124 as docking
from scripts import register_nagasaki_contract_wrap_20261124 as current
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


trace, lists = docking.trace, docking.lists
OUT = docking.OUT.with_name("fleet_special_neighbor_centers_20261124.json")
PORTS = 0x020CB178
NEIGHBOR_GETTER = 0x02089DB8
SLOTS = {114: bytes.fromhex("00009e05000000"), 115: bytes.fromhex("00000003000004")}
SPANS = ((NEIGHBOR_GETTER, 0x02089DF4), (0x020B1864, 0x020B19D8), (0x020B2AC8, 0x020B2B48),
         (0x0203ADF4, 0x0203AE80), (0x0203593C, 0x02035A30), (0x020B5600, 0x020B5630))


def dependencies(original, arm, raw):
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    ops, spans = {}, []
    for lo, hi in SPANS:
        part = trace.code_at(arm, lo, hi)
        assert part == trace.code_at(original, lo, hi) == trace.code_at(raw, lo, hi)
        spans.append(dict(start=lo, end=hi, sha256=sha256(part).hexdigest()))
        ops.update({i.address: f"{i.mnemonic} {i.op_str}" for i in md.disasm(part, lo)})
    evidence = {
        0x02089DBC: "mov r0, #7", 0x02089DC4: "ldrb r0, [r3, #6]", 0x02089DD8: "str r0, [r2, r1, lsl #2]",
        0x020B2B24: "strne r5, [sb, r7, lsl #2]", 0x020B1998: "ldr r1, [fp, r6, lsl #2]",
        0x020B19B4: "ldr r0, [fp, r6, lsl #2]", 0x020B19B8: "str r0, [sl, r7, lsl #2]",
        0x020B18BC: "add r6, r6, #1", 0x020B18C0: "strne r0, [sl, r7, lsl #2]",
        0x020B1930: "ldrgt r0, [fp, r6, lsl #2]", 0x020B1938: "strgt r0, [sl, r7, lsl #2]",
        0x0203AE14: "cmp r0, #0", 0x0203AE18: "ble #0x203ae38", 0x0203AE20: "ldr r3, [r8, r0, lsl #2]",
        0x0203AE60: "cmp r0, #0", 0x0203AE64: "ble #0x203ae80", 0x0203AE6C: "ldr r3, [r8, r0, lsl #2]",
        0x02035970: "ldrb r2, [r4, #0x3c]", 0x02035980: "cmp r0, #0",
        0x02035998: "ldr r2, [r1, r2, lsl #2]", 0x020359E4: "ldrb r2, [r4, #0x3c]",
        0x020359F4: "cmp r0, #0", 0x02035A0C: "ldr r2, [r1, r2, lsl #2]",
    }
    assert all(ops[at] == expected for at, expected in evidence.items())
    for at, entry in ((0x020B2AD4, 0x020B5600), (0x020B2AE4, NEIGHBOR_GETTER), (0x020B1978, 0x020B2AC8),
                      (0x020B1880, 0x020B1954), (0x020B18F8, 0x020B1954), (0x0203AE10, 0x020B18DC),
                      (0x0203AE5C, 0x020B1864), (0x0203597C, 0x020B1954), (0x020359F0, 0x020B1954)):
        lists.linked(arm, at, entry)
    return spans, evidence


def native_cases(active, raw):
    cpu, call = trace.get_machine(active, raw)
    ports = call(PORTS - trace.BASE)
    _, graph = lists.port_graph(raw)
    buffer = lists.SCRATCH
    saved = bytes(cpu.mem_read(buffer, 64))
    marker = b"\xE5" * 64
    checks = []
    for center, expected_row in SLOTS.items():
        at = lists.NEIGHBORS + 8 + 7 * center
        actual = trace.code_at(raw, at, at + 7)
        assert actual == expected_row and at >= lists.EDGE_ROWS - 2
        entries = list(actual[:actual[6]])
        assert entries == ([] if center == 114 else [0, 0, 0, 3])
        candidates = ((NEIGHBOR_GETTER, (lists.NEIGHBORS, center, buffer)),
                      (0x020B1954, (ports, buffer, center, 8)), (0x020B1954, (ports, buffer, center, 0)),
                      (0x020B1864, (ports, buffer, center, 1)), (0x020B18DC, (ports, buffer, center, 1)))
        for entry, args in candidates:
            cpu.mem_write(buffer, marker)
            if entry in (0x020B1864, 0x020B18DC):
                cpu.mem_write(lists.picker.STACK, pack("<I", 8))
            count = call(entry - trace.BASE, *args)
            assert 0 <= count <= len(entries)
            output = bytes(cpu.mem_read(buffer, len(marker)))
            values = list(unpack(f"<{count}I", output[:4 * count]))
            assert output[4 * count:] == marker[4 * count:]
            pos = iter(entries)
            assert all(value in pos for value in values)
            if entry == NEIGHBOR_GETTER:
                assert values == entries
            checks.append(dict(center=center, address=at, bytes_read=actual.hex(), function=entry,
                               input_arguments=args, output_ports=values, complete_output_suffix_untouched=True))
    cpu.mem_write(buffer, saved)
    assert bytes(cpu.mem_read(trace.BASE, len(raw))) == raw
    return dict(port_graph_sha256=graph["edge_bytes_sha256"], tests=checks)


def main():
    release, earlier_graph, ordinary, startup = map(read, (current.RELEASE, docking.previous.OUT, docking.observed.OUT, current.STARTUP_CAPTURE))
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"] == startup["ROM_sha256"]
    assert startup["cold_boot"] and not startup["savestate_loaded"] and not startup["callback_errors"]
    original, arm = [NdsImage.open(path).read_file(current.ARM) for path in (CLEAN, current.ROM)]
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    report = []
    for label, snapshot in (("Registered Nagasaki startup", startup["read_only_RAM_snapshot"]),
                            ("Earlier ordinary Copenhagen docking", ordinary["after_ordinary_approach"]["snapshot"])):
        raw = trace.read_ram(snapshot)
        spans, ops = dependencies(original, arm, raw)
        proof = native_cases(arm, raw)
        assert proof["port_graph_sha256"] == earlier_graph["exact_initialized_graph_sha256"]
        report.append(dict(state=label, input_snapshot=snapshot, **proof))
    assert len({r["port_graph_sha256"] for r in report}) == 1
    assert sum(len(r["tests"]) for r in report) == 20
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], checked_code_spans=spans, relevant_operations=ops, states=report,
        evidence=list(map(reference, (current.RELEASE, docking.OUT, docking.previous.OUT, docking.observed.OUT, current.STARTUP_CAPTURE))),
        scope="Native isolated lookups and exact resident code evidence. The original filters only retain values supplied by the neighbor reader. The special center produces no candidate. The no-target center reads the adjacent edge data and yields only ports 0 or 3 in these initialized states.",
        unresolved="Initial/reloaded raw docking and headquarters byte producers and ordinary arrival into these conditional branches remain open.",
        actual_gameplay_added=False, ROM_changed=False, new_editorial_credit=0))
    print("Verified 20 native checks. The special slot supplies no neighbor and the no-target slot can supply only ports 0 or 3.")


if __name__ == "__main__":
    main()
