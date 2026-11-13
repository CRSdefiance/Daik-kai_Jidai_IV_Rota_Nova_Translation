"""Execute original trend, relief and promoter selection with declared getter inputs."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/town_events_v750')
TOWN, ACTOR, GOODS, NAME, VTABLE, GET_NAME, STATE, PLAYER = (
    0x02450000, 0x02450800, 0x02451000, 0x02451400, 0x02451800, 0x02451900, 0x02452000, 0x02456000)


def trend(arm):
    cpu = machine(arm)
    value, coin, category = [0], [0], [0]
    selected = []
    cpu.mem_write(GOODS, struct.pack('<I', VTABLE) + bytes(12))
    cpu.mem_write(VTABLE + 8, struct.pack('<I', GET_NAME))
    cpu.mem_write(NAME, b'Wheat\0')

    def bridge(u, address, size, unused):
        if address == BASE + 0x53FE4:
            selected.append((u.reg_read(UC_ARM_REG_R1), u.reg_read(UC_ARM_REG_R2)))
            result = 0
        elif address == BASE + 0xB6618:
            result = TOWN
        elif address == BASE + 0xB2CD8:
            result = ACTOR
        elif address == BASE + 0xC5B7C:
            result = 0
        elif address == BASE + 0xB31E0:
            result = value[0]
        elif address == BASE + 0x519D4:
            result = coin[0]
        elif address == BASE + 0xC5BA0:
            result = NAME + 32
        elif address == GET_NAME:
            result = NAME
        else:
            return
        u.reg_write(UC_ARM_REG_R0, result)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, bridge)
    rows = []
    try:
        for state in (0, 24, 25, 74, 75, 134, 135, 255):
            value[0] = state
            for random_result in (0, 1):
                coin[0] = random_result
                for n in range(18):
                    category[0] = n
                    cpu.mem_write(GOODS + 12, bytes([n]))
                    selected.clear()
                    call(cpu, 0x5FB54, (0, GOODS))
                    expected = (732 if state >= 135 else 734) if state >= 75 and not random_result else (
                        654 if state >= 135 else 733) if state >= 75 else (
                        653 if not random_result else 655) if state >= 25 else (
                        730 if not random_result else 731)
                    assert len(selected) == 1 and selected[0][0] == expected, (state, random_result, selected)
                    if expected in (653, 654, 655, 730, 731, 733):
                        assert selected[0][1] == (NAME + 32 if expected == 730 else NAME)
                    rows.append({'supplied_trend_state': state, 'supplied_random2': random_result,
                        'supplied_product_category': n, 'original_selected_message': expected,
                        'name_kind': 'category' if expected == 730 else 'product' if expected in (653, 654, 655, 731, 733) else 'none'})
    finally:
        cpu.hook_del(hook)
    return rows


def relief(arm):
    cpu = machine(arm)
    requested, selected = [0], []

    def bridge(u, address, size, unused):
        if address == BASE + 0xB6618:
            result = TOWN
        elif address == BASE + 0xB3FD4:
            result = 0
        elif address == BASE + 0xB2E04:
            result = requested[0]
        elif address == BASE + 0xCB124:
            result = GOODS - 4
        elif address == BASE + 0xB2CD8:
            result = ACTOR
        elif address == BASE + 0x53FE4:
            selected.append(u.reg_read(UC_ARM_REG_R1))
            result = 0
        elif address == BASE + 0xB2DC0:
            result = 0
        else:
            return
        u.reg_write(UC_ARM_REG_R0, result)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, bridge)
    rows = []
    mapping = {1: 13, 2: 0, 5: 1, 6: 3, 7: 4, 8: 5, 9: 8, 10: 14, 11: 16}
    try:
        for request in range(12):
            requested[0] = request
            for category in range(18):
                for count in (4, 5):
                    selected.clear()
                    cpu.mem_write(GOODS + 12, bytes([category]))
                    cpu.mem_write(NAME, b'\0' * (12 * 5))
                    call(cpu, 0x5EBC4, (0, NAME, count))
                    expected = []
                    if count == 5 and mapping.get(request) == category:
                        expected = [736 if category == 0 else 735 if category == 13 else 737]
                    assert selected == expected, (request, category, count, selected, expected)
                    rows.append({'supplied_town_request': request, 'supplied_goods_category': category,
                        'supplied_distinct_matching_entries': count, 'supplied_original_value_for_threshold_calculation': 0,
                        'original_selected_messages': selected.copy()})
    finally:
        cpu.hook_del(hook)
    return rows


def promoter(arm):
    cpu = machine(arm)
    answer, strength, selected = [0], [0], []
    cpu.mem_write(GOODS, struct.pack('<I', VTABLE) + bytes(12))
    cpu.mem_write(VTABLE + 8, struct.pack('<I', GET_NAME))
    cpu.mem_write(NAME, b'Olive Oil\0')

    def bridge(u, address, size, unused):
        if address == BASE + 0xCB178:
            result = STATE
        elif address == BASE + 0xCB184:
            result = PLAYER
        elif address == BASE + 0xB65E4:
            result = 22
        elif address == BASE + 0xB6618:
            result = TOWN
        elif address == BASE + 0xB30EC:
            result = TOWN + 0x100
        elif address == BASE + 0xCB124:
            result = GOODS - 4 - 14 * 16
        elif address == BASE + 0x7F244:
            result = 0
        elif address == GET_NAME:
            result = NAME
        elif address in (BASE + 0x53FE4, BASE + 0x53F9C):
            selected.append({'message_id': u.reg_read(UC_ARM_REG_R1),
                'question': address == BASE + 0x53F9C})
            result = answer[0] if address == BASE + 0x53F9C else 0
        elif address == BASE + 0xB3194:
            result = 0
        else:
            return
        u.reg_write(UC_ARM_REG_R0, result)
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, bridge)
    rows = []
    try:
        for level in (24, 25):
            strength[0] = level
            for choice in (0, 1):
                answer[0] = choice
                cpu.mem_write(STATE + 0x3020, bytes((22, 14)))
                cpu.mem_write(PLAYER + 0x1A4C, bytes(4))
                cpu.mem_write(TOWN + 0x100, bytes((14, level)))
                selected.clear()
                call(cpu, 0x5E458, (0,))
                expected = [675, 676] + ([739, 740 if choice else 741] if level >= 25 else [])
                assert [r['message_id'] for r in selected] == expected
                assert [r['message_id'] for r in selected if r['question']] == ([739] if level >= 25 else [])
                flag = struct.unpack('<I', cpu.mem_read(PLAYER + 0x1A4C, 4))[0]
                assert flag == (4 if level >= 25 and choice else 0)
                rows.append({'supplied_town_stock_parameter': level, 'supplied_question_answer': choice,
                    'original_message_sequence': selected.copy(), 'resulting_original_travel_flag': flag})
        for city in (22, 23):
            cpu.mem_write(STATE + 0x3020, bytes((city, 14)))
            cpu.mem_write(PLAYER + 0x1A4C, struct.pack('<I', 4))
            selected.clear()
            call(cpu, 0x5E458, (0,))
            assert [r['message_id'] for r in selected] == ([] if city == 22 else [738])
            flag = struct.unpack('<I', cpu.mem_read(PLAYER + 0x1A4C, 4))[0]
            assert flag == (4 if city == 22 else 0)
            rows.append({'supplied_tracked_city': city, 'original_current_city': 22,
                'original_message_sequence': selected.copy(), 'resulting_original_travel_flag': flag})
    finally:
        cpu.hook_del(hook)
    return rows


def main():
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    current = NdsImage.open('out/all_routes_combined_v749_candidate.nds').read_file('/__arm9__.bin')
    spans = ((0x5FB54, 0x5FCA0), (0x5EBC4, 0x5ED34), (0x5E458, 0x5E680), (0x53F9C, 0x54058))
    assert all(clean[a:b] == current[a:b] for a, b in spans)
    checks = {}
    for name, fn in (('trend', trend), ('relief', relief), ('promoter', promoter)):
        a, b = fn(clean), fn(current)
        assert a == b
        checks[name] = a
        print(name, len(a), 'cases each clean/current pass', flush=True)
    cpu = machine(current)
    categories = []
    for n in range(18):
        call(cpu, 0xC5BA0, (n,))
        pointer = cpu.reg_read(UC_ARM_REG_R0)
        text = bytes(cpu.mem_read(pointer, 32)).split(b'\0')[0].decode('ascii')
        categories.append({'index': n, 'current_category_argument': text, 'pointer': pointer})
    save(ROOT / 'native_context.json', {'original_code_spans': [{'start': a, 'end': b, 'sha256': sha(clean[a:b])} for a, b in spans],
        'clean_and_current_original_selection_cases': checks, 'category_arguments': categories,
        'all18_supported_categories_bound_by_original_category_loop_lt18': True,
        'getter_and_UI_results_supplied_not_earned_gameplay': True,
        '739_question_parent': 0x02053FCC, 'ordinary_portrait_parent': 0x02054014,
        '730_full_category_expansion_pending': True, '742_746_caller_review_pending': True,
        'ROM_and_release_unchanged': True, 'full_goal_complete': False,
        'script_sha256': sha(Path(__file__).read_bytes())})
    doc = read('translations/town_events_editorial_manuscript_v1.json')
    for row in doc['records']:
        if 730 <= row['message_id'] <= 741:
            row['review']['context'] = True
            row['context'] = row['context'].replace('Original5EBB0', 'Original5EBC4')
    save('translations/town_events_editorial_manuscript_v1.json', doc)


if __name__ == '__main__':
    main()
