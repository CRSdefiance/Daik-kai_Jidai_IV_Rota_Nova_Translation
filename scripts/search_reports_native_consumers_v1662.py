"""Original source numeric arguments,role1/7 selection and literal-modal pipelines."""
import struct
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_SP, UC_ARM_REG_LR
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_personal_gameplay_v841 import get_machine


def source_numbers(cpu, get, values):
    arguments = []
    for value in values:
        assert 0 <= value <= 2147483647
        pointer = get(0xABF50, value)
        text = bytes(cpu.mem_read(pointer, 64)).split(b'\0')[0]
        expected = ''.join(chr(0xFF10+int(c)) for c in str(value)).encode('cp932')
        assert text == expected
        arguments.append((pointer, text))
    assert all(bytes(cpu.mem_read(p, len(t)+1)) == t+b'\0' for p, t in arguments)
    return arguments


def speech(arm, common, raw, plan, role, table, values=()):
    assert (role, table, len(values)) in [(1, 0x02116EC0, 0), (7, 0x02116E80, 2)]
    cpu, get, provider = machine(arm, common, raw, plan)
    arguments = source_numbers(cpu, get, values)
    seen = {}
    def observe(u, pc, size, data):
        if pc == BASE+0x5408C:
            u.reg_write(UC_ARM_REG_PC, BASE+0x54144)
        elif pc == 0x01FFCF3C:
            sp = u.reg_read(UC_ARM_REG_SP)
            seen.update(parent=struct.unpack('<I', u.mem_read(sp+0x264, 4))[0],
                        selector=struct.unpack('<I', u.mem_read(sp+0x27C, 4))[0],
                        input_hex=bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1), 512)).split(b'\0')[0].hex(),
                        output=u.reg_read(UC_ARM_REG_R0))
        else:
            seen['formatted_hex'] = bytes(u.mem_read(seen['output'], 512)).split(b'\0')[0].hex()
            u.emu_stop()
    for pc in [BASE+0x5408C, 0x01FFCF3C, BASE+0x54164]:
        cpu.hook_add(UC_HOOK_CODE, observe, begin=pc, end=pc)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    for reg, value in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3],
                          [role, table, *(p for p, t in arguments), *([0]*(2-len(arguments)))]):
        cpu.reg_write(reg, value)
    cpu.emu_start(BASE+0x53D44, STOP, count=3000000)
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE+0x54164
    assert seen['parent'] == BASE+0x53DB8 and seen['selector'] == table
    return {**seen, 'role': role, 'source_table': table, 'original_entry': BASE+0x53D44,
            'source_amounts': list(values), 'source_ABF50_argument_hex': [t.hex() for p, t in arguments],
            'file_reads': provider.reads, 'original_selection_loader_varargs_macro_and_post_expansion_formatter_execute': True,
            'CPU_only_file_success_and_UI_constructor_boundaries_not_gameplay': True}


def loss(arm, common, raw, plan, value):
    cpu, get, provider = machine(arm, common, raw, plan)
    arguments = source_numbers(cpu, get, [value])
    seen = {}
    def observe(u, pc, size, data):
        if pc == BASE+0x54788:
            seen['loaded_template_hex'] = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R1), 256)).split(b'\0')[0].hex()
        elif pc == BASE+0x54798:
            sp = u.reg_read(UC_ARM_REG_SP)
            seen['parent'] = struct.unpack('<I', u.mem_read(sp+0xC4, 4))[0]
        else:
            out = struct.unpack_from('<I', arm, 0x54894)[0]
            seen['formatted_hex'] = bytes(u.mem_read(out, 256)).split(b'\0')[0].hex()
            u.emu_stop()
    for pc in [BASE+0x54788, BASE+0x54798, BASE+0x5479C]:
        cpu.hook_add(UC_HOOK_CODE, observe, begin=pc, end=pc)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    cpu.reg_write(UC_ARM_REG_R0, 312)
    cpu.reg_write(UC_ARM_REG_R1, arguments[0][0])
    cpu.emu_start(BASE+0x546B8, STOP, count=3000000)
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE+0x5479C and seen['parent'] == BASE+0x546E8
    return {**seen, 'message_ID': 312, 'source_amounts': [value], 'source_ABF50_argument_hex': [arguments[0][1].hex()],
            'original_entry': BASE+0x546B8, 'file_reads': provider.reads,
            'CPU_numeric_modal_only_no_original_sailor_loss_event_or_crew_edit': True}


def assigned_role(arm, raw, role, actor_id, actor):
    cpu, get = get_machine(arm, raw)
    assert role in [1, 7] and get(0x7EE08, actor) == actor_id
    duty = get(0xCB1A8)+0x2090
    job = get(0x7B60, role)
    assert job == {1: 6, 7: 1}[role]
    layout = get(0x82E04, duty)
    vt = struct.unpack('<I', cpu.mem_read(layout, 4))[0]
    method = struct.unpack('<I', cpu.mem_read(vt+0x18, 4))[0]
    slots = [i for i in range(31) if get(method-BASE, layout, i) == job]
    assert slots == ([15] if role == 1 else [3])
    slot = slots[0]
    assert get(0x82BC4, duty, slot) == 208
    get(0x82BB8, duty, slot, actor_id)
    changed = bytes(cpu.mem_read(BASE, 0x400000))
    addresses = [BASE+i for i, (a, b) in enumerate(zip(raw, changed, strict=True)) if a != b]
    assert addresses == [duty+6+slot]
    assert get(0x82478, duty, role) == actor_id
    return changed, {'existing_actor_ID': actor_id, 'actor': actor, 'original_role': role, 'source_job': job,
                     'source_virtual_layout_method': method, 'original_slot': slot, 'one_roster_byte_changed': addresses,
                     'all_actor_objects_skills_RNG_and_other4MiB_bytes_exact': True,
                     'CPU_alternative_voice_fixture_not_emulator_state': True}
