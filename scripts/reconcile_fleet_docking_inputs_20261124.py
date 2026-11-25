"""Bind six original docking calls and check hidden-port neighbor rows in two initialized states."""

from struct import iter_unpack, pack

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from scripts import reconcile_fleet_port_origins_20261124 as previous
from scripts import verify_copenhagen_docking_20261124 as observed
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


lists, trace = previous.lists, previous.trace
current = observed.played.current
OUT = previous.OUT.with_name("fleet_docking_inputs_20261124.json")
DOCK, FORM, REFORM = 0x02034688, 0x02033BE4, 0x02033EB8
STORE = observed.played.NATIVE_DOCK_STORE
ENTRIES = {DOCK: (0x0202ECD4, 0x02033064, 0x02033090, 0x02033290, 0x02035930, 0x020908EC),
           FORM: (0x0205A7D8,), REFORM: (0x020339FC,)}
SPANS = ((0x0202ECC4, 0x0202ECDC), (0x0203303C, 0x02033094), (0x02033240, 0x02033294),
    (0x020339F0, 0x02033A00), (FORM, 0x02033CCC), (REFORM, 0x02033ED4), (0x020340A8, 0x020340D0),
    (DOCK, DOCK + 16), (0x02034798, 0x020347AC), (0x02035918, 0x02035938), (0x0203ADF4, 0x0203AE80),
    (0x0205A7B8, 0x0205A7DC), (0x020908CC, 0x020908F0), (0x02089DB8, 0x02089DF4),
    (0x02089DF4, 0x02089E38), (0x020B1864, 0x020B19D8), (0x020B2AC8, 0x020B2B48),
    (0x020B65E4, 0x020B6650), (0x0203CD24, 0x0203CD2C), (0x020CDBC4, 0x020CDBD4))


def references(image):
    calls = {entry: [] for entry in ENTRIES}
    literals = {entry: [] for entry in ENTRIES}
    for name, base, data in trace.loaded_components(image):
        for offset, (word,) in enumerate(iter_unpack("<I", data[:len(data) & ~3])):
            pc = base + 4 * offset
            target = trace.direct_bl_target(word, pc)
            if target in calls:
                calls[target].append((name, pc))
            if word in literals:
                literals[word].append((name, pc))
    assert calls == {entry: [("arm9_section_0", pc) for pc in pcs] for entry, pcs in ENTRIES.items()}
    assert not any(literals.values())
    return calls


def bind_code(clean, arm, snapshots):
    disasm = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    disasm.skipdata = True
    rows, ops = [], {}
    for lo, hi in SPANS:
        value = trace.code_at(arm, lo, hi)
        assert value == trace.code_at(clean, lo, hi)
        assert all(value == trace.code_at(raw, lo, hi) for raw in snapshots)
        rows.append(dict(start=lo, end=hi, exact_hex=value.hex()))
        ops.update({i.address: f"{i.mnemonic} {i.op_str}" for i in disasm.disasm(value, lo)})
    evidence = {
        0x0202ECD0: "mov r1, r4", 0x02033048: "mov r5, r0", 0x02033060: "mov r1, r5", 0x0203308C: "mov r1, r5",
        0x02033240: "ldrb r4, [sl, #0x3c]", 0x0203328C: "mov r1, r4", 0x0203592C: "ldrb r1, [r4, #0x3f]",
        0x020908CC: "ldr r5, [r6, #0x2c]", 0x020908E8: "mov r1, r5", 0x02034690: "mov r5, r1",
        STORE: "strb r5, [r6, #0x3c]", 0x02033BF4: "mov r4, r2", 0x02033C54: "strb r4, [r5, #0x3c]",
        0x0205A7CC: "mov r2, r0", 0x020339F8: "mov r2, #0x73", 0x02033EC4: "str r2, [sp]",
        0x020340AC: "cmp r0, #0x73", 0x020340C4: "cmp r0, #0x73", 0x020340CC: "strb r0, [sl, #0x3c]",
        0x020CDBC4: "ldrb r4, [r7, #0x10]", 0x020CDBD0: "strb r4, [r8, #0x3c]",
        0x02089DC0: "mla r3, r1, r0, r3", 0x02089DC4: "ldrb r0, [r3, #6]", 0x02089DD0: "ble #0x2089dec",
    }
    for pc, instruction in evidence.items():
        assert ops[pc] == instruction, (hex(pc), ops.get(pc))
    for pc, target in ((0x02033044, previous.EDGE_ENDPOINT), (0x020340B8, 0x0203CD24),
                       (0x0205A7C8, 0x020B65E4), (0x020B6634, previous.DOCK_SLOT), (0x020B2AD4, previous.PORT_INDEX),
                       (0x020B2AE4, 0x02089DB8), (0x020B1880, 0x020B1954), (0x020B1978, 0x020B2AC8),
                       (0x0203AE10, 0x020B18DC), (0x0203AE5C, 0x020B1864)):
        lists.linked(arm, pc, target)
    return rows


def hidden_centers(arm, raw, snapshot):
    # Read the rows before running them. Test the existing hidden town objects
    # only while the initialized state shows empty, in-bounds rows for them.
    first = lists.NEIGHBORS + 8
    tail = first + 114 * 7
    assert tail + 2 == lists.EDGE_ROWS
    hidden = trace.code_at(raw, first + 90 * 7, tail)
    assert hidden == bytes(24 * 7)
    cpu, get = trace.get_machine(arm, raw)
    ports, companies = get(0xCB178), get(0xCB160)
    before = bytes(cpu.mem_read(lists.SCRATCH, 64))
    marker = b"\xE5" * 64
    addresses = (0x02089DB8, 0x020B1954, 0x020B1864, 0x020B18DC)
    for center in range(90, 114):
        cpu.mem_write(lists.SCRATCH, marker)
        cpu.mem_write(lists.picker.STACK, pack("<I", 8))
        cases = ((lists.NEIGHBORS, center, lists.SCRATCH), (ports, lists.SCRATCH, center, 8),
                 (ports, lists.SCRATCH, center, 1), (ports, lists.SCRATCH, center, 1))
        for address, args in zip(addresses, cases, strict=True):
            assert get(address - trace.BASE, *args) == 0, (hex(address), center)
            assert bytes(cpu.mem_read(lists.SCRATCH, 64)) == marker
    cpu.mem_write(lists.SCRATCH, before)
    headquarters = [get(0x3CD24, companies + 4 + 76 * i) for i in range(21)]
    assert all(v < 114 or v == 115 for v in headquarters)
    assert bytes(cpu.mem_read(trace.BASE, len(raw))) == raw
    return dict(snapshot=snapshot, exact_hidden_rows=hidden.hex(), indices=[90, 113], selectors=list(addresses),
                zero_count_and_unchanged_output_cases=24 * len(addresses), headquarters=headquarters)


def main():
    release, gameplay, earlier = map(read, (current.RELEASE, observed.OUT, previous.OUT))
    assert digest(CLEAN) == release["clean_input_sha256"] and digest(REGISTRY) == release["registry_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"] == gameplay["candidate_sha256"]
    assert earlier["route_arrival_port_bounds"] == [0, 89] and earlier["headquarters_reassignment_range"] == [0, 113]
    startup = read(current.STARTUP_CAPTURE)
    assert startup["ROM_sha256"] == release["candidate_sha256"] and startup["cold_boot"] and not startup["savestate_loaded"]
    snaps = (startup["read_only_RAM_snapshot"], gameplay["after_ordinary_approach"]["snapshot"])
    raw = list(map(trace.read_ram, snaps))
    clean, installed = map(NdsImage.open, (CLEAN, current.ROM))
    ja, arm = [image.read_file(current.ARM) for image in (clean, installed)]
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    calls = references(installed)
    assert calls == references(clean)
    code = bind_code(ja, arm, raw)
    proof = [hidden_centers(arm, ram, snap) for ram, snap in zip(raw, snaps, strict=True)]
    for ram in raw:
        _, graph = lists.port_graph(ram)
        assert graph["edge_bytes_sha256"] == earlier["exact_initialized_graph_sha256"]
    read_source = {0x0202ECD4: "incoming port in r4", 0x02033064: "initialized route endpoint",
        0x02033090: "initialized route endpoint", 0x02033290: "existing docking byte",
        0x02035930: "existing destination byte", 0x020908EC: "port selected by accepted prompt"}
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], original_and_resident_code=code, aligned_direct_callers=calls,
        docking_call_inputs=read_source, formation_input="Current protagonist docking index returned by 0x020B65E4",
        reformation_input="The sole aligned caller supplies 115. The callee reads the owning company's HQ, and skips its byte store if HQ is also 115.",
        hidden_port_neighbor_checks=proof, exact_other_fleet_write_count=len(gameplay["other_fleet_docking_stores"]),
        ordinary_gameplay_evidence=reference(observed.OUT), offline_scope_only=True, remaining="Indirect entry paths, saved field provenance and special or sentinel neighbor centers require separate evidence.",
        evidence=list(map(reference, (current.RELEASE, current.STARTUP_CAPTURE, previous.OUT))), ROM_changed=False, new_editorial_credit=0))
    print("Bound six docking callers and verified 192 empty-neighbor cases for hidden-port centers in two initialized states.")


if __name__ == "__main__":
    main()
