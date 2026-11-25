"""Trace the two port-object destination writers to route edges and docking state."""

from struct import iter_unpack

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from scripts import reconcile_fleet_destination_inputs_20261124 as previous
from scripts import register_athens_item_rumor_20261124 as current
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


lists, trace = previous.previous, previous.previous.prior
OUT = previous.OUT.with_name("fleet_port_origins_20261124.json")
ATTACK = 0x020481F8
ARRIVAL = 0x020347AC
PORT_INDEX = 0x020B5600
DOCK_SLOT = 0x02034674
EDGE_ENDPOINT = 0x02089B2C
ENTRY_CALLS = {ATTACK: (0x0202FC40, 0x02034838, 0x020348B4), ARRIVAL: (0x0203307C, 0x0203327C),
               0x0202FB70: (0x0202FD94,)}
SPANS = ((0x0202FB70, 0x0202FC48), (0x0202FCE4, 0x0202FD98), (0x0203303C, 0x02033094),
    (0x02033240, 0x02033294), (DOCK_SLOT, 0x02034688), (ARRIVAL, 0x020348B8),
    (0x02035558, 0x02035658), (ATTACK, 0x02048A24), (EDGE_ENDPOINT, 0x02089B58),
    (0x0208A6C0, 0x0208A6E8), (PORT_INDEX, 0x020B5630), (0x020369C8, 0x020369D0),
    (0x020CB178, 0x020CB184), (trace.WRITER, trace.WRITER + 12), (0x020340A8, 0x020340D0),
    (0x0203A5F8, 0x0203A608), (0x0203A8B0, 0x0203A984), (0x0203CD24, 0x0203CD2C))
SCRATCH = 0x023F0200


def direct_calls(image):
    found = {key: [] for key in ENTRY_CALLS}
    for component, base, data in trace.loaded_components(image):
        for index, (word,) in enumerate(iter_unpack("<I", data[:len(data) & ~3])):
            address = base + index * 4
            target = trace.direct_bl_target(word, address)
            assert word not in ENTRY_CALLS, (component, address, word)
            if target in found:
                found[target].append((component, address))
    assert found == {key: [("arm9_section_0", pc) for pc in pcs] for key, pcs in ENTRY_CALLS.items()}
    return found


def runtime_cases(arm, raw, edges):
    cpu, call = trace.get_machine(arm, raw)
    checked = []
    for index, endpoints in enumerate(edges):
        for side, value in enumerate(endpoints):
            route = bytes((0, 0, 0, 0, index, 0, 0, side))
            cpu.mem_write(SCRATCH, route)
            actual = call(EDGE_ENDPOINT - trace.BASE, SCRATCH)
            assert actual == value and 0 <= actual < 90
            assert bytes(cpu.mem_read(SCRATCH, len(route))) == route
            checked.append(dict(edge=index, side=side, town_slot=actual))

    model = call(lists.PORT_MANAGER - trace.BASE)
    for slot in range(116):
        assert call(PORT_INDEX - trace.BASE, model + 4 + 108 * slot) == slot
        for away in (0, 8):
            payload = bytearray(0x54)
            payload[0x3C] = slot
            payload[0x50] = away
            cpu.mem_write(SCRATCH, bytes(payload))
            assert call(DOCK_SLOT - trace.BASE, SCRATCH) == (115 if away else slot)
            assert bytes(cpu.mem_read(SCRATCH, len(payload))) == bytes(payload)
    companies = call(0xCB160)
    headquarters = [call(0x3CD24, companies + 4 + 76 * slot) for slot in range(21)]
    assert all(0 <= town < 90 for town in headquarters)
    return dict(route_edges=checked, town_pointer_cases=116, docking_byte_cases=232,
                all_21_startup_company_headquarters=headquarters)


def prove_flow(ops, arm):
    expected = {
        ATTACK + 12: "mov r4, r1", 0x020489BC: "movne r5, #0", 0x020489C4: "mov r2, r0",
        0x020B5610: "sub r0, r4, r0", 0x02035568: "mov r6, r2",
        0x0203559C: "mov r2, r6", 0x02035648: "mov r2, r6", 0x02035A28: "strb r2, [r0, #0x3f]",
        0x020347BC: "mov r5, r1", 0x020347D0: "mul r4, r5, r1",
        0x020347DC: "add r5, r1, r4", 0x02034834: "add r1, r1, r4", 0x020348AC: "mov r1, r5",
        0x02033048: "mov r5, r0", 0x02033078: "mov r1, r5", 0x02033240: "ldrb r4, [sl, #0x3c]",
        0x02033274: "mov r1, r4", 0x0202FB78: "ldrb r6, [r5, #0x3f]", 0x0202FB8C: "mla r8, r6, r0, r1",
        0x0202FC38: "mov r1, r8", 0x0202FD00: "mov r4, r0", 0x0202FD3C: "ldrb r0, [r6, #0x3f]",
        0x0202FD40: "cmp r4, r0", 0x0202FD44: "bne #0x202ffe0",
        0x0202FD88: "cmp r0, #5", 0x0202FD8C: "bne #0x202fda0",
        0x0203467C: "movne r0, #0x73", 0x02034680: "ldrbeq r0, [r0, #0x3c]",
        0x02089B34: "ldrb r0, [r4, #4]", 0x02089B3C: "ldrb r1, [r4, #7]",
        0x02089B44: "ldreq r0, [r0, #4]", 0x02089B4C: "ldrne r0, [r0, #0x18]",
        0x0208A6C8: "cmp r0, #0xb1", 0x0208A6D0: "movlt r1, #0x1c",
        0x0203CD24: "ldrb r0, [r0, #0xb]", 0x0203A5F8: "mov r0, #0x73",
        0x0203A5FC: "strb r0, [fp, #0xb]", 0x0203A8B0: "mov sb, #0",
        0x0203A8B4: "mov fp, #0x73", 0x0203A8B8: "str fp, [sp]", 0x0203A8C0: "mov r7, sb",
        0x0203A918: "mov fp, r7", 0x0203A94C: "strlt r7, [sp]", 0x0203A954: "add r7, r7, #1",
        0x0203A958: "cmp r7, #0x72", 0x0203A95C: "blt #0x203a8d0", 0x0203A960: "ldr r0, [sp]",
        0x0203A964: "cmp r0, #0x73", 0x0203A96C: "strbne r0, [sl, #0xb]",
        0x0203A974: "cmp fp, #0x73", 0x0203A978: "strbne fp, [sl, #0xb]",
        0x020340AC: "cmp r0, #0x73", 0x020340B0: "bne #0x20340c0", 0x020340BC: "str r0, [sp]",
        0x020340CC: "strb r0, [sl, #0x3c]",
    }
    assert all(ops[address] == inst for address, inst in expected.items())
    for pc, entry in ((0x02033040, 0x020369C8), (0x02033044, EDGE_ENDPOINT), (0x02089B38, 0x0208A6C0),
                      (0x0202FCFC, DOCK_SLOT), (0x020489C0, PORT_INDEX), (0x020489D0, 0x02035558),
                      (0x020355A4, trace.WRITER), (0x02035650, trace.WRITER), (0x020340B8, 0x0203CD24)):
        lists.linked(arm, pc, entry)
    return expected


def main():
    release, existing = map(read, (current.RELEASE, previous.OUT))
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"] == existing["candidate_sha256"]
    clean, image = map(NdsImage.open, (CLEAN, current.ROM))
    assert direct_calls(clean) == direct_calls(image)
    jp, arm = (rom.read_file(current.ARM) for rom in (clean, image))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    capture = read(current.STARTUP_CAPTURE)
    assert capture["ROM_sha256"] == release["candidate_sha256"] and capture["cold_boot"] and not capture["savestate_loaded"]
    snapshot = capture["read_only_RAM_snapshot"]
    raw = trace.read_ram(snapshot)
    codec = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    codec.skipdata = True
    ops, code = {}, []
    for lo, hi in SPANS:
        part = trace.code_at(arm, lo, hi)
        assert part == trace.code_at(jp, lo, hi) == trace.code_at(raw, lo, hi)
        code.append(dict(start=lo, end=hi, exact_hex=part.hex()))
        ops.update({i.address: f"{i.mnemonic} {i.op_str}" for i in codec.disasm(part, lo)})
    required = prove_flow(ops, arm)
    _, graph = lists.port_graph(raw)
    earlier_graph = read(lists.OUT)["initialized_port_graph"]
    assert graph["edge_bytes_sha256"] == earlier_graph["edge_bytes_sha256"]
    assert graph["exact_neighbor_rows_hex"] == earlier_graph["exact_neighbor_rows_hex"]
    cases = runtime_cases(arm, raw, graph["edges"])
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_current_and_resident_code=code,
        relevant_operations=required, aligned_callers=ENTRY_CALLS, exact_initialized_graph_sha256=graph["edge_bytes_sha256"],
        route_arrival_call=0x0203307C, route_arrival_port_bounds=[0, 89], docking_reevaluation_call=0x0203327C,
        dock_and_order_equality_call=0x0202FC40, existing_dock_byte_owner_open=True,
        headquarters_reassignment_writers=[0x0203A96C, 0x0203A978], headquarters_reassignment_range=[0, 113],
        headquarters_clear_writer=0x0203A5FC, empty_headquarters=115, headquarters_to_docking_store=0x020340CC,
        other_headquarters_byte_producers_open=True,
        conditional_writers=[0x020355A4, 0x02035650], native_cases=cases,
        evidence=list(map(reference, (current.RELEASE, current.STARTUP_CAPTURE, previous.OUT, lists.OUT))),
        startup_snapshot=snapshot, offline_only=True, ordinary_missionary_reachability_open=True,
        new_editorial_credit=0, ROM_changed=False))
    print("Checked all 354 route endpoints, 116 port objects and 232 docking reads. The active route branch yields ports 0–89.")


if __name__ == "__main__":
    main()
