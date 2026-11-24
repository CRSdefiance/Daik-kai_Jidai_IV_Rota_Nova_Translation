"""Bind additional Fleet Info destination inputs to their original producer paths."""

from struct import iter_unpack

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from scripts import reconcile_fleet_destination_lists_20261123 as previous
from scripts import register_athens_item_rumor_20261124 as current
from scripts.stage_cartridge_title_20261123 import CLEAN, NdsImage, digest, read, reference, write


OUT = previous.OUT.with_name("fleet_destination_inputs_20261124.json")
WRAPPERS = {0x02035558: (0x020489D0,),
    0x0203593C: (0x02033D30, 0x02034120, 0x02035660, 0x020357F0, 0x02035848, 0x020714B4, 0x020714C8),
    0x020359B0: (0x0202EDF4, 0x0202F038, 0x0202F808, 0x02035838, 0x0203AAEC),
    0x0203C168: (0x0203AE30, 0x0203AE7C, 0x0203AFA8, 0x0203B41C, 0x0203B47C, 0x0203B80C)}
OPEN_WRITERS = (0x02033E18, 0x020355A4, 0x02035650, 0x02035960, 0x020359D4, 0x0203C198)
SPANS = ((0x02033DD0, 0x02033E20), (0x020352CC, 0x0203536C), (0x02035558, 0x02035678),
    (0x0203593C, 0x020359E0), (0x02035A24, 0x02035A30), (0x0203ADF4, 0x0203AE80),
    (0x0203AF28, 0x0203AFAC), (0x0203B3BC, 0x0203B49C), (0x0203B77C, 0x0203B82C),
    (0x0203C168, 0x0203C19C), (0x0203CD24, 0x0203CD2C), (0x020489A0, 0x020489D8),
    (0x020B1864, 0x020B1954), (0x020B290C, 0x020B2978), (0x020B5600, 0x020B5630))


def wrapper_calls(image):
    calls, literals = {entry: [] for entry in WRAPPERS}, {entry: [] for entry in WRAPPERS}
    for section, base, raw in previous.prior.loaded_components(image):
        for index, (word,) in enumerate(iter_unpack("<I", raw[:len(raw) // 4 * 4])):
            address = base + 4 * index
            target = previous.prior.direct_bl_target(word, address)
            if target in calls:
                calls[target].append((section, address))
            if word in literals:
                literals[word].append((section, address))
    assert not any(literals.values())
    assert calls == {entry: [("arm9_section_0", pc) for pc in refs] for entry, refs in WRAPPERS.items()}
    return calls


def main():
    earlier = read(previous.OUT)
    receipt = read(current.RELEASE)
    assert earlier["other_open_direct_writers"] == list(OPEN_WRITERS)
    assert digest(receipt["candidate"]) == receipt["candidate_sha256"] and digest(CLEAN) == receipt["clean_input_sha256"]
    clean, installed = map(NdsImage.open, (CLEAN, receipt["candidate"]))
    jp, en = (image.read_file(current.ARM) for image in (clean, installed))
    read_at = previous.prior.code_at
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    ops, spans = {}, []
    for lo, hi in SPANS:
        raw = read_at(en, lo, hi)
        assert raw == read_at(jp, lo, hi)
        spans.append(dict(start=lo, end=hi, exact_hex=raw.hex()))
        ops.update({i.address: f"{i.mnemonic} {i.op_str}" for i in decoder.disasm(raw, lo)})
    assert wrapper_calls(clean) == wrapper_calls(installed)
    for pc in OPEN_WRITERS:
        previous.linked(en, pc, previous.prior.WRITER)
    assert ops[0x02035A28] == "strb r2, [r0, #0x3f]"
    assert ops[0x0203C17C] == "mov r6, r3" and ops[0x0203C194] == "mov r2, r6"
    assert ops[0x0203B77C] == "mov r4, #0" and ops[0x0203B808] == "mov r3, r4"
    assert ops[0x0203B810] == "add r4, r4, #1" and ops[0x0203B814] == "cmp r4, #0x72"
    assert ops[0x0203B818] == "bge #0x203b82c" and ops[0x0203B828] == "blt #0x203b790"
    assert ops[0x020B2920] == "mov r5, r6" and ops[0x020B2910] == "mov r6, #0"
    assert ops[0x020B295C] == "strne r5, [sb, r6, lsl #2]"
    assert ops[0x020B2968] == "cmp r5, #0x5a" and ops[0x020B296C] == "blt #0x20b2934"
    for pc in (0x0203AF34, 0x0203B3D0, 0x0203B444):
        previous.linked(en, pc, 0x020B290C)
    assert ops[0x0203AF98] == "ldr r3, [fp, r0, lsl #2]"
    assert ops[0x0203B40C] == "ldr r3, [r1, r2, lsl #2]" and ops[0x0203B470] == "ldr r3, [r4, r7, lsl #2]"
    assert ops[0x0203CD24] == "ldrb r0, [r0, #0xb]"
    for pc in (0x02035950, 0x020359C4):
        assert ops[pc] == "cmp r2, #0x73"
    assert ops[0x02035568] == "mov r6, r2"
    assert ops[0x0203559C] == ops[0x02035648] == "mov r2, r6"
    previous.linked(en, 0x020489C0, 0x020B5600)
    assert ops[0x020489C4] == "mov r2, r0" and ops[0x020B5610] == "sub r0, r4, r0"
    bounds = {pc: [0, 89] for pc in (0x0203AFA8, 0x0203B41C, 0x0203B47C)} | {0x0203B80C: [0, 113]}
    write(OUT, dict(candidate_sha256=receipt["candidate_sha256"], original_and_installed_code=spans,
        earlier_destination_scope=reference(previous.OUT), confirmed_immediate_WRITER_inputs=list(OPEN_WRITERS),
        wrapper_calls=WRAPPERS, dispatch_writer=0x0203C198, bounded_dispatch_callers=bounds,
        HQ_neighbor_dispatch_calls=[0x0203AE30, 0x0203AE7C],
        original_HQ_company_byte_writers=[0x02035960, 0x020359D4], HQ_slot_producers_open=True,
        port_pointer_to_index_writers=[0x020355A4, 0x02035650], original_pointer_upstream_open=True,
        fallback_docking_slot_writer=0x02033E18, fallback_docking_slot_open=True,
        ordinary_missionary_reachability_open=True, actual_gameplay=False))
    print("Bound four of six dispatch inputs to ports that exclude slot 114. Traced the other direct writer inputs upstream.")


if __name__ == "__main__":
    main()
