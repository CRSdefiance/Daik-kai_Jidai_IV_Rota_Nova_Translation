"""Bind the Lisbon Fleet Info dock inputs to their native boundaries."""

from struct import iter_unpack, pack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R5

from scripts import reconcile_fleet_docking_inputs_20261124 as prior
from scripts import register_lisbon_roster_galley_20261124 as current
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


trace = prior.trace
BASE = trace.BASE
OUT = prior.OUT.with_name("fleet_force_dock_current_20261124.json")
SCRIPT_START, FORCE_DOCK_CALL, RETURN = 0x020294D8, 0x0202957C, 0x02029580
SCRATCH = 0x023F0200
ENTRIES = {
    0x0202EC2C: (0x0202957C, 0x0202E9FC),
    0x0209083C: (0x0203E1B8,),
}
SPANS = (
    (SCRIPT_START, RETURN + 4), (0x0202E9C4, 0x0202EA08), (0x0202EC2C, 0x0202ECD8),
    (0x02035888, 0x02035934), (0x0203E180, 0x0203E1BC),
    (0x0205A7C8, 0x0205A7DC), (0x020B6618, 0x020B6650),
    (0x02090168, 0x020901C4), (0x02090844, 0x020908F4),
    (0x020909B4, 0x02090A24), (0x02090AA4, 0x02090BC0), (0x0209132C, 0x02091368),
)


def references(image):
    calls = {entry: [] for entry in ENTRIES}
    literal = []
    for name, base, data in trace.loaded_components(image):
        for offset, (word,) in enumerate(iter_unpack("<I", data[:len(data) & ~3])):
            pc = base + offset * 4
            target = trace.direct_bl_target(word, pc)
            if target in calls:
                calls[target].append((name, pc))
            if word in ENTRIES or word == 0x02090AA4:
                literal.append((name, pc, word))
    assert calls == {entry: [("arm9_section_0", pc) for pc in pcs] for entry, pcs in ENTRIES.items()}
    assert literal == [("arm9_section_0", 0x020901C0, 0x02090AA4)]
    return dict(aligned_calls=calls, aligned_pending_port_literal=literal[0])


def bind_code(clean, arm, raw):
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.skipdata = True
    evidence, ops = [], {}
    for lo, hi in SPANS:
        bytes_now = trace.code_at(arm, lo, hi)
        assert bytes_now == trace.code_at(clean, lo, hi) == trace.code_at(raw, lo, hi)
        evidence.append(dict(start=lo, end=hi, exact_hex=bytes_now.hex()))
        ops.update({i.address: f"{i.mnemonic} {i.op_str}" for i in cs.disasm(bytes_now, lo)})
    expected = {
        0x020294EC: "ldrh r0, [r0, #2]", 0x020294F0: "ands r0, r0, #0xff",
        0x020294F8: "cmp r0, #0x72", 0x02029504: "cmp r0, #0xff",
        0x02029524: "ldrb r4, [r1, #0x3c]", 0x02029530: "cmp r4, #0x72",
        0x0202E9E8: "bl #0x2034674", 0x0202E9F0: "cmp r1, #0x73",
        0x0202EC38: "mov r4, r1", 0x0202ECD4: "bl #0x2034688",
        0x0203588C: "bl #0x2034674", 0x020358A8: "cmp r0, #0xb2",
        0x020358B4: "ldrb r6, [r4, #0x3f]", 0x0203592C: "ldrb r1, [r4, #0x3f]",
        0x02035930: "bl #0x2034688", 0x0205A7C8: "bl #0x20b65e4",
        0x020B6634: "bl #0x2034674", 0x020901BC: "bx ip",
        0x02090848: "ldr r1, [r6, #0x28]", 0x020908CC: "ldr r5, [r6, #0x2c]",
        0x020908EC: "bl #0x2034688", 0x020909C0: "str r1, [r6, #0xc]",
        0x020909F8: "str r1, [r6, #0x2c]", 0x02090AC0: "ldr r2, [r1, #8]",
        0x02090B2C: "bl #0x2021d0c", 0x02090B34: "ldr r5, [sp, #0x40]",
        0x02090B84: "ldr r1, [sp, #8]", 0x02090B8C: "str r1, [r4, #0x2c]",
        0x02091334: "ldr r0, [r4, #0xc]", 0x02091338: "str r0, [r4, #0x2c]",
    }
    assert all(ops[pc] == inst for pc, inst in expected.items())
    return evidence, expected


def script_gate(arm, raw):
    cpu, get = trace.get_machine(arm, raw)
    model, fleet = get(0xCB1A8), get(0x2E58C)
    dock = model + 4 + fleet * 132 + 0x3C
    actor = bytes(cpu.mem_read(dock - 0x34, 1))[0]
    assert get(0x2CAE0, model, actor) == fleet
    original = bytes(cpu.mem_read(SCRATCH, 64))
    port_at = SCRATCH + 40
    state, cursor = SCRATCH, SCRATCH + 24
    cases = []
    for port_arg, stored in [(value, None) for value in range(255)] + [(255, value) for value in range(256)]:
        cpu.mem_write(SCRATCH, bytes(64))
        cpu.mem_write(state + 4, pack("<I", port_at))
        cpu.mem_write(cursor, pack("<I", port_at))
        cpu.mem_write(port_at, pack("<HH", actor, port_arg))
        if stored is not None:
            cpu.mem_write(dock, bytes((stored,)))
        cpu.reg_write(UC_ARM_REG_R2, cursor)
        cpu.reg_write(UC_ARM_REG_R5, state)
        seen = []

        def stop(uc, pc, size, _):
            if pc in (FORCE_DOCK_CALL, RETURN):
                seen.append(uc.reg_read(UC_ARM_REG_R1) if pc == FORCE_DOCK_CALL else None)
                uc.emu_stop()

        handle = cpu.hook_add(UC_HOOK_CODE, stop, begin=FORCE_DOCK_CALL, end=RETURN)
        try:
            cpu.emu_start(SCRIPT_START, RETURN + 4, count=10000)
        finally:
            cpu.hook_del(handle)
        value = stored if stored is not None else port_arg
        assert seen == [value if value < 114 else None], (port_arg, stored, seen, cpu.reg_read(UC_ARM_REG_PC))
        assert unpack_from("<I", cpu.mem_read(cursor, 4))[0] == port_at + 2
        cases.append(dict(argument=port_arg, current_dock_fixture=stored, force_dock_argument=seen[0]))
    cpu.mem_write(dock, raw[dock - BASE:dock - BASE + 1])
    cpu.mem_write(SCRATCH, original)
    assert bytes(cpu.mem_read(BASE, len(raw))) == raw
    return dict(protagonist_actor=actor, protagonist_fleet=fleet, cases=cases)


def main():
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    old, new = map(NdsImage.open, (CLEAN, current.ROM))
    owners = references(new)
    assert owners == references(old)
    clean, arm = [image.read_file(current.ARM) for image in (old, new)]
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    startup = read(current.STARTUP_CAPTURE)
    assert startup["ROM_sha256"] == release["candidate_sha256"] and startup["cold_boot"] and not startup["savestate_loaded"]
    snapshot = startup["read_only_RAM_snapshot"]
    raw = trace.read_ram(snapshot)
    code, instructions = bind_code(clean, arm, raw)
    tests = script_gate(arm, raw)
    write(OUT, dict(
        candidate_sha256=release["candidate_sha256"], release=reference(current.RELEASE),
        inherited_docking_coverage=reference(prior.OUT), startup_snapshot=snapshot,
        original_installed_resident_code=code, exact_instructions=instructions, **owners,
        native_completed_script_gate=tests,
        current_dock_copy_call=0x0202E9FC, formation_current_dock_call=0x0205A7D8,
        destination_reuse_call=0x02035930,
        pending_ingress=dict(request_copy=0x02090B8C, request_result=0x02090B34,
                             resource_return_call=0x02090B2C, copies_active_slot=0x02091338, swaps_slots=0x020909F8),
        ordinary_missionary_activation_observed=False, offline_native_gate_only=True,
        unexecuted_boundary="Force-dock call or the original return block. No supplied dock value was written by the ROM.",
        remaining="Trace the accepted request result through 0x02021D0C and the first write that can supply destination 114.",
        new_editorial_credit=0,
    ))
    print(f"Bound the two force-dock callers and checked {len(tests['cases'])} native script inputs.")


if __name__ == "__main__":
    main()
