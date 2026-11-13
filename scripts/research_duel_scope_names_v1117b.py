"""Execute original duel caller ABI and inventory actual opponent-name expansions.

CPU research only. The native message loader and font entry are explicit boundary
models, not emulator message injection or proof of production runtime behavior.
"""
import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.sighting_grammar_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.duel_postmacro_layout_v1114 import layout
from scripts.probe_button_prompt_native import STACK
from scripts.probe_duel_postmacro_v1115 import ROM, CAP, BASE
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_scope_names_v1117b')
TABLES = (0x02117340, 0x02117360, 0x021174E0)


def selected_scope(lr, parent, table):
    return lr == BASE + 0xDAC4 and parent == BASE + 0xD4BC and table in TABLES


def execute(arm, raw, actor, name, family, table, expected_id, text, *, direct=False):
    cpu, get = get_machine(arm, raw)
    controller, source, argument = 0x02460000, 0x02468000, 0x02469000
    widget = controller + 0x214
    cpu.mem_write(controller, bytes(0x600))
    cpu.mem_write(controller + 0x34, struct.pack('<2I', actor, actor))
    cpu.mem_write(source, text + b'\0')
    cpu.mem_write(argument, name + b'\0')
    get(0xE14C, widget)
    registered, clears, loaded, drawn = [], [], [], []

    def bypass(u):
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    def registration(u, pc, size, data):
        assert u.reg_read(UC_ARM_REG_R0) == widget
        registered.append(pc)
        bypass(u)

    hook = cpu.hook_add(UC_HOOK_CODE, registration, begin=BASE + 0xD351C, end=BASE + 0xD351C)
    try:
        get(0xDEF4, widget)
    finally:
        cpu.hook_del(hook)
    header = struct.unpack('<I', cpu.mem_read(widget + 0x3C + 16, 4))[0]
    h = struct.unpack('<5I', cpu.mem_read(header, 20))
    assert h[:3] == (4, 52, 36)

    def clear(u, pc, size, data):
        assert u.reg_read(UC_ARM_REG_R0) == header and u.reg_read(UC_ARM_REG_R1) == 0
        cpu.mem_write((header + h[4]) & 0xFFFFFFFF, bytes(208 * 36 // 2))
        clears.append(pc)
        bypass(u)

    def loader(u, pc, size, data):
        number = u.reg_read(UC_ARM_REG_R0)
        assert number == expected_id
        loaded.append(number)
        u.reg_write(UC_ARM_REG_R0, source)
        bypass(u)

    def font(u, pc, size, data):
        sp = u.reg_read(UC_ARM_REG_SP)
        context, pointer = u.reg_read(UC_ARM_REG_R0), u.reg_read(UC_ARM_REG_R1)
        expanded = bytes(u.mem_read(pointer, 1024)).split(b'\0')[0]
        expected = text.replace(b'%s', name)
        assert expanded == expected, (expected_id, expanded, expected)
        assert context == sp + 0x410 and pointer == sp + 0x10
        lr = u.reg_read(UC_ARM_REG_LR)
        parent = struct.unpack('<I', u.mem_read(sp + 0x47C, 4))[0]
        saved_table = struct.unpack('<I', u.mem_read(sp + 0x4A4, 4))[0]
        assert lr == BASE + 0xDAC4
        assert parent == BASE + (0xD528 if direct else 0xD4BC)
        assert saved_table == (expected_id if direct else table)
        assert selected_scope(lr, parent, saved_table) == (not direct and table in TABLES)
        drawn.append({'expanded_hex': expanded.hex(), 'font_return': lr,
                      'original_parent_return': parent, 'saved_table': saved_table,
                      'context_offset': context - sp, 'text_buffer_offset': pointer - sp,
                      'selected_by_proposed_scope': selected_scope(lr, parent, saved_table)})
        u.reg_write(UC_ARM_REG_R0, pointer + len(expanded))
        bypass(u)

    hooks = [cpu.hook_add(UC_HOOK_CODE, clear, begin=0x01FFB2DC, end=0x01FFB2DC),
             cpu.hook_add(UC_HOOK_CODE, loader, begin=BASE + 0x5528C, end=BASE + 0x5528C),
             cpu.hook_add(UC_HOOK_CODE, font, begin=BASE + 0xD5404, end=BASE + 0xD5404)]
    cpu.mem_write(STACK, struct.pack('<I', argument))
    side = 0 if family == 'challenge' else 1
    try:
        get(0xD4D0 if direct else 0xD458, controller, side, 60, expected_id if direct else table)
    finally:
        for hook in hooks:
            cpu.hook_del(hook)
    assert len(registered) == len(clears) == len(loaded) == len(drawn) == 1
    assert bytes(cpu.mem_read(source, len(text) + 1)) == text + b'\0'
    assert bytes(cpu.mem_read(argument, len(name) + 1)) == name + b'\0'
    return {'family': family, 'message_ID': expected_id, 'side': side,
            'native_D458_or_D4D0_selector_printf_macro_context_and_return_executed': True,
            'native_message_loader_and_font_entry_are_explicit_boundary_models': True,
            'full_stack_and_callee_saved_ABI_pass': True, **drawn[0]}


def main():
    assert not ROOT.exists()
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    candidate_hash = sha(ROM.read_bytes())
    assert candidate_hash == '64b1da09fe0f75007af73b0f44a39ce9d2d3c6dedbb70cf6c0ca20223a7f1c29'
    report = read(CAP / 'capture_report.json')
    raw_path = CAP / 'frame_005310_arm9_ram.bin'
    raw = raw_path.read_bytes()
    assert report['ROM_sha256'] == candidate_hash
    assert sha(raw) == next(row['sha256'] for row in report['read_only_pause_RAM_snapshots'] if row['frame'] == 5310)
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0xD458, 0xD538), (0xDA28, 0xDB5C), (0xEA1C, 0xEB94)):
        assert arm[lo:hi] == clean[lo:hi]
    doc = read('translations/duel_editorial_manuscript_v3.json')
    records = {row['message_id']: row for row in doc['records']}
    current = current_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm)
    cpu, get = get_machine(arm, raw)
    actors, captain = get(0xCB184), get(0x7F244)
    names, layouts, representatives = [], [], {}
    tables = {'challenge': TABLES[0], 'acceptance': TABLES[1], 'threat': TABLES[2],
              'named_escape_negative': 0x02117500, 'admiral_escape_negative': 0x02117620}
    for actor in range(208):
        obj = actors + 0x19E4 if actor == captain else actors + 4 + actor * 32
        native_id = get(0x7EE08, obj)
        assert native_id == (captain if actor == 207 else actor)
        vt = struct.unpack('<I', cpu.mem_read(obj, 4))[0]
        offset = 0x24 if 28 <= native_id <= 43 else 0x20
        getter = struct.unpack('<I', cpu.mem_read(vt + offset, 4))[0]
        pointer = get(getter - BASE, obj)
        name = bytes(cpu.mem_read(pointer, 128)).split(b'\0')[0]
        name.decode('cp932')
        assert name and b'\n' not in name and b'%' not in name
        names.append({'actor_slot': actor, 'actor_ID': native_id, 'object': obj, 'virtual_getter_offset': offset,
                      'getter': getter, 'name_hex': name.hex(), 'name': name.decode('cp932')})
        for number, row in records.items():
            if number < 1951:
                paragraph = row['english'].encode('ascii').replace(b'%s', name)
                output, lines = layout(paragraph)
                assert b' '.join(output.split()) == paragraph
                assert len(lines) <= 3 and all(len(line.encode('cp932')) <= 24 for line in lines)
                layouts.append({'actor_slot': actor, 'actor_ID': native_id, 'message_ID': number,
                                'paragraph_hex': paragraph.hex(), 'generated_hex': output.hex(),
                                'lines': lines})
        for family, table in tables.items():
            number = get(0x53F4C, obj, table)
            representatives.setdefault((family, number), (obj, name))
    assert len(names) == 208 and len(layouts) == 4160
    assert {row['actor_ID'] for row in names} == set(range(207))
    assert names[207]['object'] == names[captain]['object']
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_name_layout_catalogue.json', {
        'candidate': str(ROM), 'candidate_sha256': candidate_hash,
        'snapshot': str(raw_path), 'snapshot_sha256': sha(raw),
        'original_EA1C_getter_rule_and_all208_native_getters_executed': True,
        'names': names, 'all4160_complete_word_layouts': layouts,
        'native_slots208_cover207_IDs_with_slot207_aliasing_current_captain': True,
        'predecessor_v1117_rejected_false_slot207_equals_actor207_assumption': True,
        'CP932_name_bytes_preserved': True,
        'layout_only_not_complete_font_or_assembled_runtime_proof': True,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    calls = []
    for (family, number), (obj, name) in sorted(representatives.items()):
        text = records[number]['english'].encode('ascii')
        row = execute(arm, raw, obj, name, family, tables[family], number, text)
        calls.append(row)
    assert {row['message_ID'] for row in calls if row['selected_by_proposed_scope']} == set(range(1931, 1951))
    for number in range(1931, 1951):
        obj, name = representatives[('challenge', 1931)]
        calls.append(execute(arm, raw, obj, name, 'direct_negative', 0, number,
                             records[number]['english'].encode('ascii'), direct=True))
    # Independent predicate corruption controls:each single guard must matter.
    assert all(selected_scope(BASE + 0xDAC4, BASE + 0xD4BC, table) for table in TABLES)
    assert not selected_scope(BASE + 0xDAC0, BASE + 0xD4BC, TABLES[0])
    assert not selected_scope(BASE + 0xDAC4, BASE + 0xD528, TABLES[0])
    assert not selected_scope(BASE + 0xDAC4, BASE + 0xD4BC, 0x02117500)
    save(ROOT / 'original_caller_ABI_scope.json', {
        'candidate': str(ROM), 'candidate_sha256': candidate_hash, 'cases': calls,
        'all20_selected_paragraphs_original_voice_selector_printf_macro_and_caller_ABI_pass': True,
        'other_voice_tables_and_all20_direct_static_calls_excluded': True,
        'native_font_entry_LR': BASE + 0xDAC4, 'outer_return_at_font_SP_plus': 0x47C,
        'voice_table_at_font_SP_plus': 0x4A4, 'owned_expanded_text_bytes': 0x400,
        'explicit_boundary_models': ['message loader supplies reviewed CPU text',
                                     'SDK full-plane graphics clear', 'widget registration',
                                     'font entry capture with consumed-pointer return'],
        'font_raster_and_actual_emulator_injection_not_claimed': True,
        'no_ROM_runtime_registry_or_completion_credit_change': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    ledger['duel_prose_v1103'].update(source_name_layout_catalogue=str(ROOT / 'source_name_layout_catalogue.json'),
        original_caller_scope_ABI=str(ROOT / 'original_caller_ABI_scope.json'),
        all208_native_name_getters_and4160_prospective_layouts_pass=True,
        full_CP932_font_planes_and_assembled_runtime_and_fixed_storage_still_pending=True)
    save(ledger_path, ledger)
    print(f'208 native names and4160 layouts; {len(calls)} original caller/scope cases pass. CPU boundaries explicit; no ROM change.')


if __name__ == '__main__':
    main()
