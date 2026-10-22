"""Source-bound item bargaining and diplomatic voice/provider research."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3,
                               UC_ARM_REG_R4, UC_ARM_REG_R5, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R10,
                               UC_ARM_REG_R11, UC_ARM_REG_SP, UC_ARM_REG_LR)

from dk4tool.patch.crew_role_labels import ORIGINAL
from dk4tool.patch.common_literal_prefix import guard
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/item_diplomacy_editorial_v784')
CURRENT = Path('out/all_routes_combined_v783_candidate.nds')
TABLES = {0x02118160: (1075, 1076, 1077, 1078, 1079, 1080, 1081, 1082),
          0x02118140: (1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094),
          0x02118120: (1098, -1, 1099, -1, -1, 1100, 1101, 1102),
          0x02118100: (1103, -1, 1104, -1, -1, 1105, 1106, 1107),
          0x02117F60: (1108, -1, 1109, -1, -1, 1110, 1111, 1112),
          0x021180C0: (1113, -1, 1114, -1, -1, 1115, 1116, -1),
          0x02117FE0: (1117, -1, 1118, -1, 1119, 1120, 1121, 1122),
          0x02118020: (1124, -1, 1125, -1, 1126, 1127, 1128, 1129),
          0x02118040: (1131, 1132, 1133, -1, 1134, 1135, 1136, 1137),
          0x021180A0: (1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145)}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(CURRENT)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    report_path = Path('E:/Rota Nova translations/Generated/work/emulation_v193/shared_v783_private_live2/capture_report.json')
    report = read(report_path)
    snapshot = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == 3200)
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256'] and report['ROM_sha256'] == sha(CURRENT.read_bytes())
    spans = [(0x53914, 0x53AC4), (0x53CB0, 0x54058), (0x51A28, 0x51BD4),
             (0x5B558, 0x5BB30), (0x5BC8C, 0x5BDEC), (0x5BE00, 0x5C450), (0x93D5C, 0x93D6C)]
    for a, b in spans[1:]:
        assert arm[a:b] == clean[a:b], hex(a)
    assert sha(clean[0x53914:0x53AC4]) == '71f0a5626d1992a8e2a2f0fb5a287bb42d719c0861488c64aec7ea5fe5386d87'
    u = machine(arm)
    u.mem_write(BASE, raw)
    literal = read(CURRENT.with_suffix('.manifest.json'))['relocations']['/__arm9__.bin']['common_literal_prefix']
    restored = bytearray(arm[0x53914:0x53AC4])
    for at, prefix in ((0x5397C, 'F'), (0x53A44, 'I')):
        row = next(r for r in literal['changes'] if r['offset'] == at)
        assert struct.unpack_from('<I', arm, at)[0] == row['after']
        assert struct.unpack_from('<I', clean, at)[0] == row['before']
        restored[at-0x53914:at-0x53914+4] = clean[at:at+4]
        entry = literal['helpers'][prefix]['entry']
        code = guard(entry, prefix)
        assert bytes(u.mem_read(entry, len(code))) == code
    assert bytes(restored) == clean[0x53914:0x53AC4]

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    def ptr(at): return struct.unpack('<I', u.mem_read(at, 4))[0]
    def text(at): return bytes(u.mem_read(at, 512)).split(b'\0')[0]

    roles = []
    current_roles = get(0x86314)
    for role, jp, en in ((1, '副官', 'First Mate'), (3, '主計長', 'Purser')):
        original_ptr = struct.unpack_from('<I', clean, ORIGINAL-BASE+role*4)[0]
        assert clean[original_ptr-BASE:].split(b'\0')[0].decode('cp932') == jp
        assert text(ptr(current_roles+role*4)).decode('ascii').strip() == en
        controller = get(0xCB1A8)+0x2090
        roles.append({'role': role, 'Japanese': jp, 'English': en,
                      'assigned_actor': get(0x825E4, (controller, role)),
                      'native_speech_actor_with_fallback': get(0x82478, (controller, role))})
    actors, selections = get(0xCB184), []
    for table, values in TABLES.items():
        assert tuple(struct.unpack('<8i', u.mem_read(table, 32))) == values
        assert arm[table-BASE:table-BASE+32] == clean[table-BASE:table-BASE+32]
        for i in range(208):
            actor = actors+4+i*32 if i < 207 else actors+0x19E4
            voice = get(0x7E988, (actor,))
            selected = get(0x53F4C, (actor, table))
            assert selected == (values[voice] if values[voice] != -1 else values[0])
            selections.append({'table': table, 'actor_ID': i, 'voice': voice, 'selected_ID': selected})
        assert get(0x53F4C, (0, table)) == values[0]
    types = [{'type': i, 'Japanese': text(get(0x93D5C, (i,))).decode('cp932')} for i in range(6)]
    assert [r['Japanese'] for r in types] == ['親善', '協定締結', '協定破約', '停戦', '宣戦布告', '威圧']
    prior_schemes = [{'type': i, 'text': text(get(0x93D5C, (i,))).decode('cp932')} for i in range(6, 10)]
    assert all(r['text'].isascii() and r['text'] for r in prior_schemes)
    numbers = [{'value': n, 'native_hex': text(get(0xABF50, (n,))).hex()} for n in (1, 9, 10, 1000, 123456)]
    # Only execute original calling fragments; stop before actual UI/event work.
    observed, cases = [], []

    def stop(c, pc, size, unused):
        observed.append({'wrapper': pc, 'speaker_or_role': c.reg_read(UC_ARM_REG_R0),
                         'ID_or_table': c.reg_read(UC_ARM_REG_R1),
                         'R2': c.reg_read(UC_ARM_REG_R2), 'R3': c.reg_read(UC_ARM_REG_R3)})
        c.emu_stop()

    hooks = [u.hook_add(UC_HOOK_CODE, stop, begin=BASE+fn, end=BASE+fn)
             for fn in (0x53D44, 0x53CB0, 0x53F9C, 0x53FE4)]

    def run(start, registers, expected, stack=()):
        observed.clear()
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        for reg, val in registers:
            u.reg_write(reg, val)
        for at, val in stack:
            u.mem_write(STACK+at, struct.pack('<I', val))
        u.emu_start(BASE+start, STOP, count=100000)
        assert len(observed) == 1 and observed[0]['ID_or_table'] == expected, (hex(start), observed)
        cases.append({'fragment': BASE+start, **observed[0]})
        return observed[0]

    npc_sentinel = actors+4+207*32  # ABI sentinel, not a claimed Guild actor mapping.
    try:
        for start, key in ((0x5BF8C, 0x02118140), (0x5C32C, 0x02118160)):
            r = run(start, ((UC_ARM_REG_R5, 3), (UC_ARM_REG_R11, 3)), key)
            assert r['speaker_or_role'] == 3 and r['wrapper'] == BASE+0x53D44
        for start, key in ((0x51B54, 0x02118040), (0x51B6C, 0x02118100),
                           (0x5B864, 0x02118120), (0x5BCF4, 0x02118020), (0x5BD08, 0x02117FE0)):
            r = run(start, (), key)
            assert r['speaker_or_role'] == 1 and r['wrapper'] == BASE+0x53D44
        r = run(0x5B760, ((UC_ARM_REG_R0, 1),), 0x02117F60)
        assert r['speaker_or_role'] == 1 and r['wrapper'] == BASE+0x53CB0
        r = run(0x5B924, ((UC_ARM_REG_R0, 1),), 0x021180C0)
        assert r['speaker_or_role'] == 1 and r['wrapper'] == BASE+0x53CB0
        r = run(0x5B650, (), 0x021180A0)
        assert r['speaker_or_role'] == 1 and r['wrapper'] == BASE+0x53CB0
        for start, key in ((0x5C43C, 1070), (0x5C21C, 1071), (0x5C368, 1074),
                           (0x5C078, 1084), (0x5BE84, 1085), (0x5BFC8, 1096),
                           (0x5BCD8, 1097), (0x5BAD0, 1123), (0x5BCC4, 1130)):
            run(start, ((UC_ARM_REG_R0, npc_sentinel), (UC_ARM_REG_R10, npc_sentinel),
                        (UC_ARM_REG_R4, npc_sentinel)), key)
        for start, key, registers, stack in (
                (0x5C3F0, 1072, ((UC_ARM_REG_R8, 1234),), ((0x1C, 1072),)),
                (0x5C29C, 1073, ((UC_ARM_REG_R8, 1234),), ()),
                (0x5C33C, 1083, ((UC_ARM_REG_R8, 1234),), ()),
                (0x5BEF0, 1086, ((UC_ARM_REG_R7, 1234),), ()),
                (0x5BF9C, 1095, ((UC_ARM_REG_R7, 1234),), ())):
            r = run(start, registers+((UC_ARM_REG_R10, npc_sentinel),), key, stack)
            assert text(r['R2']) == '１２３４'.encode('cp932')
            r['argument_hex'] = text(r['R2']).hex()
    finally:
        for h in hooks:
            u.hook_del(h)
    selected = {r['selected_ID'] for r in selections} | {r['ID_or_table'] for r in cases if r['ID_or_table'] < 3668}
    assert selected == set(range(1070, 1146)), sorted(set(range(1070, 1146))-selected)
    save(ROOT/'native_context.json', {'candidate': str(CURRENT), 'candidate_sha256': sha(CURRENT.read_bytes()),
        'pre_fixture_snapshot': snapshot, 'roles': roles, 'tables': {hex(k): v for k, v in TABLES.items()},
        'all2080_actor_voice_selections': selections, 'original_call_fragments': cases,
        'letter_type_provider': BASE+0x93D5C, 'all_six_current_runtime_letter_types': types,
        'earlier_Tavern_scheme_type_indices6_to9_must_remain_exact': prior_schemes,
        'current_letter_type_values_still_Japanese': True, 'native_number_provider': BASE+0xABF50,
        'native_numbers': numbers, 'all76_context_IDs': sorted(selected),
        'IC_source_meaning': 'Original53914 consumes IC as the character-dependent Japanese first-person pronoun;English I/we/our follows grammar,not an actor name.',
        'inherited_macro_guard_exception': 'Only the exact registered F/I branch slots differ from clean53914;both resident guards match their complete producer bytes and preserve IC semantics.',
        'price1072_is_insufficient_funds_statement_not_a_purchase_question': True,
        'Guild_service_cost1000_subtracted_at': BASE+0x5BB00,
        'original_executable_spans': [{'span': [a, b], 'sha256': sha(clean[a:b])} for a, b in spans],
        'declared_CPU_role_actor_amount_inputs_not_actual_gameplay': True,
        'Guild_NPC_initializer_core_binding_and_full_branch_filters_still_pending': True,
        'English_letter_type_localization_and_production_formatting_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('76 original context IDs;2080 voice selections,role1 First Mate/role3 Purser,and six still-Japanese type values mapped. Production and actual scenes pending.', flush=True)


if __name__ == '__main__':
    main()
