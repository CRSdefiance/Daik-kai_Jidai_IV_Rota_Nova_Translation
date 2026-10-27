"""Original callers for shared warnings, rumors, recruitment and personal chat."""

import struct
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                               UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7,
                               UC_ARM_REG_R9, UC_ARM_REG_R11, UC_ARM_REG_LR, UC_ARM_REG_SP, UC_ARM_REG_PC)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.native_machine_scoped_v764 import machine
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shared_editorial_v781')
CURRENT = Path('out/all_routes_combined_v780_candidate.nds')
TABLES = {0x021181C0: (1021, 1022, 1023, -1, 1024, 1025, 1026, 1027),
          0x021181A0: (1035, -1, 1036, 1037, 1038, 1039, 1040, 1041),
          0x02118180: (1042, -1, 1043, 1044, 1045, 1046, 1047, 1048)}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(CURRENT)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    report_path = Path('E:/Rota Nova translations/Generated/work/emulation_v193/barmaid_v780_seoul_live2/capture_report.json')
    report = read(report_path)
    snapshot = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == 3200)
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256'] and report['ROM_sha256'] == sha(CURRENT.read_bytes())
    spans = [(0x53CB0, 0x53E4C), (0x56A00, 0x56AE8), (0x56B50, 0x56C38),
             (0x56CA8, 0x56D8C), (0x56E24, 0x56F14), (0x56F60, 0x56FF4),
             (0x57408, 0x576CC), (0x57868, 0x578E0), (0x57C1C, 0x57C90),
             (0x57E50, 0x57EB8), (0x587EC, 0x58834), (0x58F24, 0x58F4C),
             (0x591D0, 0x5923C), (0x7EE08, 0x7EE20)]
    for a, b in spans:
        assert arm[a:b] == clean[a:b], (hex(a), hex(b))
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    def ptr(p): return struct.unpack('<I', u.mem_read(p, 4))[0]
    def text(p): return bytes(u.mem_read(p, 256)).split(b'\0')[0]
    def name(obj): return text(get(ptr(ptr(obj)+8)-BASE, (obj,)))

    officers, towns, villages = get(0xCB184), get(0xCB178), get(0xCB118)
    here = get(0xB6618)
    assert 0 <= here-towns-4 < 114*108 and (here-towns-4) % 108 == 0
    npc = get(0xB2CD8, (here, 13))
    voices = []
    for table, values in TABLES.items():
        assert tuple(struct.unpack('<8i', u.mem_read(table, 32))) == values
        assert arm[table-BASE:table-BASE+32] == clean[table-BASE:table-BASE+32]
        for i in range(208):
            obj = officers+4+i*32 if i < 207 else officers+0x19E4
            voice = get(0x7E988, (obj,))
            assert 0 <= voice < 8
            selected = get(0x53F4C, (obj, table))
            assert selected == (values[voice] if values[voice] != -1 else values[0])
            voices.append({'table': table, 'actor_index': i, 'voice': voice, 'selected_ID': selected})
        assert get(0x53F4C, (0, table)) == values[0]
    events, cases = [], []

    def observe(c, pc, size, unused):
        key = c.reg_read(UC_ARM_REG_R1)
        argc = 1 if key in (*range(1028, 1035), 0x021181A0, 0x02118180) else 0
        events.append({'wrapper': pc, 'speaker_or_role': c.reg_read(UC_ARM_REG_R0), 'table_or_ID': key,
                       'arguments_hex': [text(c.reg_read(UC_ARM_REG_R2)).hex()] if argc else []})
        c.emu_stop()

    hooks = [u.hook_add(UC_HOOK_CODE, observe, begin=BASE+fn, end=BASE+fn)
             for fn in (0x53FE4, 0x53CB0, 0x53DCC)]

    def run(a, b, registers=(), stack=()):
        events.clear()
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        for reg, val in registers:
            u.reg_write(reg, val)
        for off, val in stack:
            u.mem_write(STACK+off, struct.pack('<I', val))
        try:
            u.emu_start(BASE+a, BASE+b, count=100000)
        except Exception as error:
            raise RuntimeError((hex(a), hex(u.reg_read(UC_ARM_REG_PC)),
                                [hex(u.reg_read(reg)) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R9)])) from error
        assert len(events) == 1, (hex(a), events)
        row = {'original_fragment': [a, b], **events[0]}
        cases.append(row)
        return row

    try:
        # Original role-2 warnings and the missing-contract-information branch.
        for a, b in ((0x56A68, 0x56A74), (0x56BB8, 0x56BC4),
                     (0x56D0C, 0x56D18), (0x56E7C, 0x56E88)):
            r = run(a, b)
            assert (r['speaker_or_role'], r['table_or_ID'], r['arguments_hex']) == (2, 0x021181C0, [])
        r = run(0x56FB4, 0x56FC0)
        assert (r['speaker_or_role'], r['table_or_ID'], r['arguments_hex']) == (2, 1020, [])
        # The original initializer sets both continuation prompts to role1.
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_R5, 0)
        u.emu_start(BASE+0x574E0, BASE+0x574E8, count=10)
        assert ptr(STACK+4) == 1
        u.emu_start(BASE+0x574F4, BASE+0x57540, count=100)
        assert ptr(STACK+0x34) == ptr(STACK+0x38) == 1
        amounts = []
        for value in (1, 9, 10, 99, 100, 999, 1000, 9999, 10000, 65535):
            encoded = text(get(0xABF50, (value,)))
            amounts.append({'value': value, 'native_hex': encoded.hex(), 'native_text': encoded.decode('cp932')})
            for a, b, key, reg in ((0x57644, 0x5765C, 0x021181A0, UC_ARM_REG_R7),
                                   (0x57668, 0x57680, 0x02118180, UC_ARM_REG_R6)):
                r = run(a, b, ((reg, value+321), (UC_ARM_REG_R9, 321)), ((0x34, 1), (0x38, 1)))
                assert (r['speaker_or_role'], r['table_or_ID'], r['arguments_hex']) == (1, key, [encoded.hex()])
                r['supplied_CPU_difference'] = value
        # All real barmaids: actor identity + original base selects private speech.
        personal = []
        for town in range(114):
            info = get(0x79D8, (town,))
            if not info:
                continue
            actor_index = bytes(u.mem_read(info, 3))[0]
            actor = officers+4+actor_index*32
            idx = get(0x7EE08, (actor,))
            r = run(0x58F24, 0x58F48, ((UC_ARM_REG_R0, 0), (UC_ARM_REG_R1, town), (UC_ARM_REG_R2, actor)))
            assert r['table_or_ID'] == 863+idx == 863+actor_index and r['speaker_or_role'] == actor
            personal.append({'town_ID': town, 'actor_index': actor_index, 'name': name(actor).decode('cp932'), **r})
        assert sorted(r['table_or_ID'] for r in personal) == list(range(1049, 1070))
        # Original village-point provider and full coordinate string, before printf.
        scratch, coordinate_rows = 0x02478000, []
        for village in range(24):
            model = get(0xCACAC, (villages, village))
            for formal in (0, 1):
                u.mem_write(scratch, struct.pack('<3I', 0, 0, formal))
                r = run(0x57868, 0x578C8, ((UC_ARM_REG_R9, village), (UC_ARM_REG_R11, here-towns-4)), ((0, scratch),))
                expected = 1028 if formal else 1029
                assert r['table_or_ID'] == expected and r['speaker_or_role'] == npc
                point = list(struct.unpack('<2i', u.mem_read(STACK+0x24, 8)))
                coordinate_rows.append({'village_ID': village, 'village_model': model, 'point': point, **r})
        # Unidentified fleet rumors use one town name, not a faction argument.
        fleet = get(0xCB1A8)+4+get(0x2E58C)*0x84
        original_town = bytes(u.mem_read(fleet+0x3C, 1))
        original_flags = bytes(u.mem_read(fleet+0x50, 2))
        original_destination = bytes(u.mem_read(fleet+0x3F, 1))
        town_rows, rumors = [], []
        try:
            for town in range(114):
                obj = towns+4+town*108
                town_name = name(obj)
                town_rows.append({'town_ID': town, 'name_hex': town_name.hex(), 'name': town_name.decode('cp932')})
                u.mem_write(fleet+0x3C, bytes([town]))
                u.mem_write(fleet+0x3F, bytes([town]))
                u.mem_write(fleet+0x50, struct.pack('<H', struct.unpack('<H', original_flags)[0] & ~8))
                for formal in (0, 1):
                    u.mem_write(scratch, struct.pack('<3I', 0, 0, formal))
                    r = run(0x57C1C, 0x57C68, ((UC_ARM_REG_R5, fleet), (UC_ARM_REG_R6, npc)), ((0, scratch),))
                    assert r['table_or_ID'] == (1033 if formal else 1034) and r['arguments_hex'] == [town_name.hex()]
                    rumors.append({'town_ID': town, **r})
                    r = run(0x57E50, 0x57E94, ((UC_ARM_REG_R4, fleet), (UC_ARM_REG_R6, npc)), ((0, scratch),))
                    assert r['table_or_ID'] == (1031 if formal else 1032) and r['arguments_hex'] == [town_name.hex()]
                    rumors.append({'town_ID': town, **r})
                r = run(0x587EC, 0x5880C, ((UC_ARM_REG_R5, obj),), ((4, officers+4+202*32),))
                assert r['table_or_ID'] == 1030 and r['arguments_hex'] == [town_name.hex()]
                rumors.append({'town_ID': town, **r})
        finally:
            u.mem_write(fleet+0x3C, original_town)
            u.mem_write(fleet+0x3F, original_destination)
            u.mem_write(fleet+0x50, original_flags)
    finally:
        for hook in hooks:
            u.hook_del(hook)
    all_ids = {r['selected_ID'] for r in voices} | {r['table_or_ID'] for r in cases if r['table_or_ID'] < 3668}
    assert all_ids == set(range(1020, 1070)), sorted(set(range(1020, 1070))-all_ids)
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    save(ROOT/'native_context.json', {
        'candidate': str(CURRENT), 'candidate_sha256': sha(CURRENT.read_bytes()),
        'source_ARM9_sha256': sha(clean), 'current_ARM9_sha256': sha(arm),
        'capture_report': str(report_path), 'pre_fixture_snapshot': snapshot,
        'tables': {hex(k): v for k, v in TABLES.items()}, 'all624_original_actor_voice_selections': voices,
        'all_original_fragments': cases, 'all21_private_barmaid_speeches': personal,
        'all24_village_coordinate_providers_two_modes': coordinate_rows,
        'all114_native_town_names': town_rows, 'all570_unknown_fleet_town_argument_fragments': rumors,
        'native_headcount_strings': amounts, 'all50_context_IDs': sorted(all_ids),
        'recruitment_speaker': 'Role1 Barkeep, proved by the original initializer and continuation call sites',
        'recruitment_arguments': 'required-minus-recruited or capacity-minus-recruited, formatted by original ABF50',
        'private_speech_consumer': 'Original58F24,selected by native actor index+863;called by original591D0 after its second chance selection',
        'coordinate_contract': 'Native51580 supplies a coordinate string with its original layout bytes;not a town/village name. Production normalization and wrapping remain pending.',
        'source_executable_spans': [{'span': [a, b], 'sha256': sha(clean[a:b]),
                                    'instructions': [{'address': x.address, 'mnemonic': x.mnemonic, 'operands': x.op_str}
                                                     for x in cs.disasm(clean[a:b], BASE+a)]} for a, b in spans],
        'CPU_supplied_town_headcount_and_mode_inputs_not_earned_events': True,
        'full_caller_filter_and_production_formatting_not_proven_here': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('50 original context IDs;624 voice selections,21 barmaids,48 coordinates,570 town rumor fragments and20 headcount fragments.', flush=True)


if __name__ == '__main__':
    main()
