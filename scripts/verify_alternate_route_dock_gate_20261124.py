"""Verify the route-travel gate before the alternate ordinary docking request."""

from collections import Counter
from struct import pack, unpack_from

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM

from scripts import reconcile_fleet_destination_lists_20261123 as lists
from scripts import reconcile_fleet_port_origins_20261124 as earlier
from scripts import register_riga_recruitment_20261124 as current
from scripts import verify_personal_gameplay_v841 as runtime
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write

OUT = earlier.OUT.with_name("alternate_route_dock_gate_20261124.json")
BASE = earlier.trace.BASE
GATE, TARGET, ROUTE, EDGE, VTABLE = 0x020896EC, 0x02033304, 0x020369C8, 0x02089B2C, 0x0214B3E0
SCRATCH, MISSIONARY = 0x023F0200, 114
SPANS = ((ROUTE, ROUTE + 8), (TARGET, TARGET + 8), (GATE, 0x02089738), (EDGE, 0x02089B58),
         (0x0208A6C0, 0x0208A6E8), (VTABLE, VTABLE + 16), (0x02078100, 0x02078134),
         (0x02078168, 0x02078184), (0x020904CC, 0x020904F4))


def exact_code(clean, arm, raw):
    code_at = earlier.trace.code_at
    spans = []
    for start, end in SPANS:
        value = code_at(arm, start, end)
        assert value == code_at(clean, start, end) == code_at(raw, start, end), hex(start)
        spans.append(dict(start=start, end=end, exact_hex=value.hex()))
    assert unpack_from("<2I", arm, VTABLE - BASE + 8) == (GATE, TARGET)
    engine = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    instructions = {
        0x02078104: "bl #0x20369c8", 0x0207810C: "ldr r1, [r1, #8]", 0x02078110: "blx r1",
        0x02078114: "cmp r0, #0", 0x02078118: "beq #0x2078214", 0x02078120: "bl #0x20369c8",
        0x02078128: "ldr r1, [r1, #0xc]", 0x0207812C: "blx r1", 0x02078130: "mov r4, r0",
        0x0207816C: "mov r1, r4", 0x02078174: "bl #0x20904cc", 0x020904DC: "str r1, [r0, #8]",
        0x020896FC: "cmp r1, #0xb2", 0x02089708: "cmp r1, #7", 0x02089710: "bl #0x2089b2c",
        0x02089720: "ldr r1, [r1, #0xc]", 0x02089724: "blx r1",
        0x02089728: "cmp r4, r0", 0x0208972C: "moveq r5, #1",
        ROUTE: "add r0, r0, #0x54", TARGET: "ldrb r0, [r0, #9]",
    }
    for pc, expected in instructions.items():
        op, = engine.disasm(code_at(arm, pc, pc + 4), pc)
        assert f"{op.mnemonic} {op.op_str}" == expected
    return spans, instructions


def verify_gate(arm, raw, edges):
    cpu, call = runtime.get_machine(arm, raw)
    root = call(0xCB1A8)
    observed = Counter()
    for index in range(64):
        fleet = root + 4 + 132 * index
        obj = call(ROUTE - BASE, fleet)
        assert obj == fleet + 0x54
        table = unpack_from("<I", raw, obj - BASE)[0]
        observed[table] += 1
    assert observed == {VTABLE: 63, 0: 1}
    before = bytes(cpu.mem_read(SCRATCH, 16))

    def gate(edge, side, phase, proposed):
        data = pack("<I6B", VTABLE, edge, 0, phase, side, 0, proposed) + bytes(6)
        cpu.mem_write(SCRATCH, data)
        expected_return = call(TARGET - BASE, SCRATCH)
        result = call(GATE - BASE, SCRATCH)
        assert bytes(cpu.mem_read(SCRATCH, len(data))) == data and expected_return == proposed
        return result

    samples = []
    for index, pair in enumerate(edges):
        for side, endpoint in enumerate(pair):
            assert 0 <= endpoint < 90
            ready = gate(index, side, 7, endpoint)
            mismatched = gate(index, side, 7, MISSIONARY)
            wrong_phase = gate(index, side, 6, endpoint)
            assert (ready, mismatched, wrong_phase) == (1, 0, 0), (index, side, endpoint)
            samples.append(dict(edge=index, side=side, endpoint=endpoint, ready=ready,
                                supplied_Missionary_slot_result=mismatched, wrong_phase_result=wrong_phase))
    assert [gate(178, side, 7, MISSIONARY) for side in (0, 1)] == [0, 0]
    cpu.mem_write(SCRATCH, before)
    assert bytes(cpu.mem_read(BASE, len(raw))) == raw
    return dict(stock_route_object_table_counts=dict(observed), route_edge_cases=samples,
                gate_invocations=3 * len(samples) + 2, no_route_sentinel_controls=2)


def main():
    rel = read(current.RELEASE)
    assert digest(REGISTRY) == rel["registry_sha256"] and digest(CLEAN) == rel["clean_input_sha256"]
    assert digest(current.ROM) == rel["candidate_sha256"]
    clean, install = map(NdsImage.open, (CLEAN, current.ROM))
    ja, arm = (r.read_file(current.ARM) for r in (clean, install))
    assert sha256(arm).hexdigest() == rel["target_ARM9_sha256"]
    snap = read(rel["own_registered_startup"])["read_only_snapshot"]
    raw = earlier.trace.read_ram(snap)
    code, operations = exact_code(ja, arm, raw)
    _, graph = lists.port_graph(raw)
    upstream = read(earlier.OUT)
    assert graph["edge_bytes_sha256"] == upstream["exact_initialized_graph_sha256"]
    supplied = verify_gate(arm, raw, graph["edges"])
    write(OUT, dict(candidate_sha256=rel["candidate_sha256"], offline_only=True, source_startup_snapshot=snap,
        exact_code_spans=code, exact_operations=operations, graph=graph["edge_bytes_sha256"],
        source_graph_proof=reference(earlier.OUT), **supplied, ordinary_route_port_bounds=[0, 89],
        ordinary_Missionary_reachability_open=True, ROM_changed=False, new_editorial_credit=0))
    print(f"Verified {supplied['gate_invocations']} route-ready cases. Every valid edge endpoint is in slots 0–89.")


if __name__ == "__main__":
    main()