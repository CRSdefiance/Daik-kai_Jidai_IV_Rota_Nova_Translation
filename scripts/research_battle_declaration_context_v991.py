"""Source-bound voice, argument and cancellation proofs; no gameplay or editorial credit."""
import struct
import unicodedata
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_PC, UC_ARM_REG_LR

from dk4tool.patch.activity_special_editorial_v987b import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.prepare_work_comments_v842 import snapshot, machine_at
from scripts.verify_village_wrap_v608 import read, save

BASE = 0x02000000
ROOT = Path('work/analysis/battle_declaration_v991')
ROM = Path('out/all_routes_combined_v987_candidate.nds')
TABLES = {
    'unknown': (0x02117400, (1904, 1905, 1906, -1, 1907, 1908, 1909, 1910)),
    'named': (0x02117420, (1897, -1, 1898, 1899, 1900, 1901, 1902, 1903)),
    'ready': (0x02117440, tuple(range(1889, 1897))),
    'opponent_control': (0x021184E0, tuple(range(2201, 2209))),
}
REPS = {0: 4, 1: 16, 2: 9, 3: 7, 4: 5, 5: 6, 6: 14, 7: 19}
TEXT, SHIM = 0x02465000, 0x02470000


def ptr(u, at):
    return struct.unpack('<I', u.mem_read(at, 4))[0]


def text(u, at):
    return bytes(u.mem_read(at, 256)).split(b'\0')[0]


def actor_object(actors, actor, captain):
    return actors + 0x19E4 if actor == captain else actors + 4 + actor * 32


def name(u, get, obj):
    address = get(ptr(u, ptr(u, obj) + 0x20) - BASE, obj)
    raw = text(u, address)
    return {'name': unicodedata.normalize('NFKC', raw.decode('cp932')),
            'name_hex': raw.hex(), 'pointer': address}


def assign_first_mate(u, get, actor):
    controller = get(0xCB1A8) + 0x2090
    model = get(0x82E04, controller)
    before = bytes(u.mem_read(BASE, 0x400000))
    for slot in range(31):
        if u.mem_read(model + 0x1E + slot, 1) == b'\x06' or u.mem_read(controller + 6 + slot, 1) == bytes([actor]):
            u.mem_write(controller + 6 + slot, b'\xD0')
    u.mem_write(model + 0x1E + 12, b'\x06')
    u.mem_write(controller + 6 + 12, bytes([actor]))
    selected = get(0x82478, controller, 1)
    assert selected == actor and get(0x7B60, 1) == 6
    after = bytes(u.mem_read(BASE, 0x400000))
    changes = [{'address': BASE+i, 'before': a, 'after': b} for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
    assert all(controller+6 <= r['address'] < controller+37 or r['address'] == model+0x1E+12 for r in changes)
    return {'actor_ID': actor, 'selected_by_original_82478': selected, 'room_type': 6,
            'only_disposable_occupant_and_one_room_type_changes': changes}


def speech_bridge(u, japanese, events, ui_result):
    selected = [None]

    def loader(cpu, pc, size, unused):
        selected[0] = cpu.reg_read(UC_ARM_REG_R0)
        cpu.mem_write(TEXT, japanese[selected[0]].text + b'\0')
        cpu.reg_write(UC_ARM_REG_R0, TEXT)
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    def popup(cpu, pc, size, unused):
        kind, actor, message, va = [cpu.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        n = selected[0]
        assert message == TEXT and text(cpu, message) == japanese[n].text
        count = japanese[n].text.count(b'%s')
        assert count in (0, 1)
        arguments = [ptr(cpu, va+i*4) for i in range(count)]
        events.append({'message_ID': n, 'kind': kind, 'actor_object': actor,
                       'source_text_hex': japanese[n].text.hex(), 'source_argument_count': count,
                       'argument_pointers': arguments, 'argument_hex': [text(cpu, p).hex() for p in arguments],
                       'original_wrapper_return_parent': cpu.reg_read(UC_ARM_REG_LR),
                       'UI_result': ui_result if kind == 1 else 0})
        cpu.reg_write(UC_ARM_REG_R0, ui_result if kind == 1 else 0)
        cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))

    return [u.hook_add(UC_HOOK_CODE, loader, begin=BASE+0x5528C, end=BASE+0x5528C),
            u.hook_add(UC_HOOK_CODE, popup, begin=BASE+0x54058, end=BASE+0x54058)]


def main():
    assert not ROOT.exists()
    ROOT.mkdir(parents=True)
    inventory_path = Path('work/analysis/battle_declaration_v990/source_inventory.json')
    inventory = read(inventory_path)
    ledger = read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed'] == 1174 and ledger['records_with_source_and_prose_pass'] == 1177
    assert sha(ROM.read_bytes()) == ledger['current_integrated_candidate']['sha256'] == inventory['candidate_sha256']
    current, clean = map(NdsImage.open, (ROM, 'work/clean.nds'))
    arm, source = current.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    jp = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), source)
    en = current_entries(current.read_file('/COMMON/MESFILE.DK4'), arm)
    source_spans = [(0x6EE90, 0x6F0C8), (0x6F4D4, 0x6F7A4), (0x53CB0, 0x54058),
                    (0x82478, 0x825E4), (0x7B60, 0x7C30), (0x7E988, 0x7E9A0),
                    (0x3CD2C, 0x3CD78), (0x3CF9C, 0x3CFC8), (0x7DAF0, 0x7DB14),
                    (0x3CB30, 0x3CB90)]
    for a, b in source_spans:
        assert arm[a:b] == source[a:b], hex(a)
    raw, receipt = snapshot('activity_special_v988_987_EmilioAfter', 16100)
    report = read(Path(receipt['path']).parent / 'capture_report.json')
    assert report['ROM_sha256'] == sha(ROM.read_bytes())
    u, get = machine_at(arm, raw)
    actors, companies = get(0xCB184), get(0xCB160)
    captain, player = get(0x7F244), get(0x397D8, companies)
    assert captain == 1 and player == 2
    selections, nulls, table_proofs = [], [], []
    for family, (table, values) in TABLES.items():
        assert struct.unpack_from('<8i', arm, table-BASE) == values
        assert arm[table-BASE:table-BASE+32] == source[table-BASE:table-BASE+32]
        table_proofs.append({'family': family, 'table': table, 'IDs': list(values), 'sha256': sha(source[table-BASE:table-BASE+32])})
        for actor in range(208):
            # This inventory follows original regular-object and active-captain-object storage.
            obj = actors+4+actor*32 if actor < 207 else actors+0x19E4
            voice = get(0x7E988, obj)
            expected = values[voice] if values[voice] != -1 else next(n for n in values if n != -1)
            selected = get(0x53F4C, obj, table)
            assert selected == expected
            selections.append({'family': family, 'source_object_index': actor, 'actor_object': obj,
                               'voice': voice, 'selected_ID': selected, 'original_full_ABI_pass': True})
        assert get(0x53F4C, 0, table) == values[0]
        nulls.append({'family': family, 'null_actor_voice0_ID': values[0]})
    assert {r['selected_ID'] for r in selections if r['family'] != 'opponent_control'} == set(range(1889, 1911))
    names = {actor: name(u, get, actor_object(actors, actor, captain)) for actor in [*REPS.values(), captain]}
    catalog = []
    for company_id in range(20):
        obj = companies+4+company_id*76
        getter = ptr(u, ptr(u, obj)+8)
        pointer = get(getter-BASE, obj)
        label = text(u, pointer)
        leader = get(0x3CD2C, obj)
        catalog.append({'company_ID': company_id, 'company_object': obj, 'virtual_name_getter': getter,
                        'complete_faction_label': unicodedata.normalize('NFKC', label.decode('cp932')),
                        'label_hex': label.hex(), 'label_pointer': pointer,
                        'leader_object': leader, 'leader_name': name(u, get, leader),
                        'leader_byte26': get(0x7DB0C, leader), 'player_custom_name_branch': company_id == player})
    assert catalog[0]['complete_faction_label'] == 'Castor Co.' and catalog[2]['complete_faction_label'] == 'Bergstrom Fleet'
    assert catalog[9]['complete_faction_label'] == 'Pasha'
    wrappers = []
    for actor in [*REPS.values(), captain]:
        for family, ui_result in [('named', 0), ('named', 1), ('unknown', 0), ('unknown', 1), ('ready', 0)]:
            cpu, g = machine_at(arm, raw)
            fixture = assign_first_mate(cpu, g, actor)
            actor_ptr = actor_object(actors, actor, captain)
            voice = g(0x7E988, actor_ptr)
            if actor != captain:
                assert voice == next(v for v, a in REPS.items() if a == actor)
            table, values = TABLES[family]
            selected = values[voice] if values[voice] != -1 else values[0]
            faction = catalog[9]
            argument = faction['label_pointer']
            events = []
            hooks = speech_bridge(cpu, jp, events, ui_result)
            prepared = bytes(cpu.mem_read(BASE, len(raw)))
            try:
                result = g(0x53D44 if family == 'ready' else 0x53CB0, 1, table, *([argument] if family == 'named' else []))
            finally:
                for h in hooks: cpu.hook_del(h)
            assert len(events) == 1 and events[0]['message_ID'] == selected
            assert events[0]['actor_object'] == actor_ptr and events[0]['kind'] == (0 if family == 'ready' else 1)
            assert events[0]['argument_pointers'] == ([argument] if family == 'named' else [])
            if family != 'ready': assert result == 1-ui_result
            assert bytes(cpu.mem_read(BASE, len(raw))) == prepared
            wrappers.append({'family': family, 'speaker_actor_ID': actor, 'speaker': names[actor]['name'],
                             'voice': voice, 'fixture': fixture, 'events': events, 'wrapper_result': result,
                             'complete_captured4MiB_unchanged_after_prepared_role_fixture': True,
                             'genuine_captain_object_used_when_selected': actor == captain})
    assert len(wrappers) == 45
    branch_specs = [('new_hostility', k, f, choice) for k in (0, 1, 2) for f in (0, 1) for choice in (0, 1)]
    branch_specs += [('already_war', k, f, choice) for k in (0, 1, 2) for f, choice in ((0, 0), (1, 0), (1, 1))]
    branch_specs += [('pirate_sentinel21', None, f, choice) for f, choice in ((0, 0), (1, 0), (1, 1))]
    branches = []
    for situation, knowledge, flag, ui_result in branch_specs:
        cpu, g = machine_at(arm, raw)
        fixture = assign_first_mate(cpu, g, 4)
        fleet_root, companies, actors = g(0xCB1A8), g(0xCB160), g(0xCB184)
        target_id = 21 if situation == 'pirate_sentinel21' else 9
        fleet_index = 57 if target_id == 21 else 9
        fleet = fleet_root+4+fleet_index*0x84
        assert g(0x35320, fleet) == target_id and g(0x34674, fleet) == 115
        leader, relation_address = None, None
        if target_id != 21:
            company = companies+4+target_id*76
            leader = g(0x3CD2C, company)
            cpu.mem_write(leader+0x1A, bytes([knowledge]))
            # Original 3CB30 uses the lower-company row, with the other company's index.
            relation_address = companies+4+player*76+0x1F+target_id
            cpu.mem_write(relation_address, bytes([2 if situation == 'already_war' else 0]))
            assert g(0x3CB30, company, player) == (2 if situation == 'already_war' else 0)
        code = f'push {{r4-r10,lr}}; mov r4,#{flag}; ldr r5,=0x02462000; mov r6,#{target_id}; mov r8,#{player}; ldr r9,={fleet}; ldr r10,=0x02461000; b 0x0206ef10'
        encoded = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(code, SHIM)[0])
        cpu.mem_write(SHIM, encoded)
        events, boundary, mutations = [], [], []
        hooks = speech_bridge(cpu, jp, events, ui_result)

        def stop_before_battle(c, pc, size, unused):
            boundary.append(pc)
            c.reg_write(UC_ARM_REG_PC, BASE+0x6F0A8)

        def observe_mutation(c, pc, size, unused):
            mutations.append({'callee': pc, 'arguments': [c.reg_read(r) for r in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]})

        hooks.append(cpu.hook_add(UC_HOOK_CODE, stop_before_battle, begin=BASE+0x6F054, end=BASE+0x6F054))
        for at in (0x3C8F4, 0x3C748, 0x7DAF0):
            hooks.append(cpu.hook_add(UC_HOOK_CODE, observe_mutation, begin=BASE+at, end=BASE+at))
        prepared = bytes(cpu.mem_read(BASE, len(raw)))
        try: g(SHIM-BASE)
        finally:
            for h in hooks: cpu.hook_del(h)
        confirm = situation == 'new_hostility' or flag != 0
        accepted = not confirm or ui_result == 0
        assert bool(boundary) == accepted and len(boundary) <= 1
        expected_family = 'named' if situation == 'new_hostility' and knowledge != 0 and flag == 0 else 'unknown' if confirm else 'ready'
        expected_id = TABLES[expected_family][1][0]
        assert events[0]['message_ID'] == expected_id and events[0]['kind'] == int(confirm)
        assert events[0]['actor_object'] == actor_object(actors, 4, captain)
        assert events[0]['argument_hex'] == ([catalog[9]['label_hex']] if expected_family == 'named' else [])
        changed = [{'address': BASE+i, 'before': a, 'after': b} for i, (a, b) in enumerate(zip(prepared, bytes(cpu.mem_read(BASE, len(raw))), strict=True)) if a != b]
        if accepted and situation == 'new_hostility':
            assert len(events) == 2 and events[1]['actor_object'] == leader and events[1]['kind'] == 0
            expected_opponent = g(0x53F4C, leader, TABLES['opponent_control'][0])
            assert events[1]['message_ID'] == expected_opponent
            assert g(0x3CB30, company, player) == 2 and g(0x7DB0C, leader) == max(1, knowledge)
            assert [r['callee'] for r in mutations] == ([BASE+0x7DAF0] if knowledge == 0 else [])+[BASE+0x3C8F4, BASE+0x3C748]
        else:
            assert len(events) == 1 and not mutations and not changed
        assert g(0x7F244) == captain
        branches.append({'situation': situation, 'input_flag_from_menu_object_byte8': flag,
                         'leader_byte26_prepared': knowledge, 'source_UI_result': ui_result,
                         'confirmation': confirm, 'accepted': accepted, 'family': expected_family,
                         'fixture': fixture, 'target_company_ID': target_id, 'real_target_fleet_index': fleet_index,
                         'real_target_fleet_object': fleet, 'relation_address': relation_address,
                         'events': events, 'original_mutations_executed': mutations,
                         'all_post_prepared4MiB_changes': changed, 'battle_initializer_not_executed': True,
                         'cancellation_has_no_state_change': not accepted and not changed,
                         'CPU_shim_hex': encoded.hex(), 'original_full_callee_saved_ABI_pass': True})
    assert len(branches) == 24
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    disassembly = [{'address': i.address, 'mnemonic': i.mnemonic, 'operands': i.op_str}
                   for a, b in ((0x6EF10, 0x6F0A8), (0x6F4D4, 0x6F530), (0x6F70C, 0x6F734))
                   for i in md.disasm(source[a:b], BASE+a)]
    assert [struct.unpack_from('<I', source, a)[0] for a in (0x6F0B4, 0x6F0B8, 0x6F0BC, 0x6F0C0)] == [TABLES[k][0] for k in ('unknown', 'ready', 'named', 'opponent_control')]
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'COMMON_sha256': sha(current.read_file('/COMMON/MESFILE.DK4')), 'ARM9_sha256': sha(arm),
             'source_clean_ROM_sha256': sha(Path('work/clean.nds').read_bytes()),
             'source_inventory': str(inventory_path), 'source_inventory_sha256': sha(inventory_path.read_bytes()),
             'read_only_cold_boot_snapshot': receipt, 'captain_identity': captain, 'player_company': player,
             'exact_clean_current_code_spans': [{'start_offset': a, 'end_offset': b, 'sha256': sha(source[a:b])} for a, b in source_spans],
             'source_tables': table_proofs, 'all832_original_object_voice_selections': selections,
             'all4_null_actor_controls': nulls, 'all45_original_role_wrapper_argument_and_UI_result_cases': wrappers,
             'all24_original_branch_fragment_cases': branches, 'all20_native_complete_faction_labels': catalog,
             'native_actor_names': names, 'bounded_original_caller_disassembly': disassembly,
             'records_and_immediate_neighbors': inventory['records_and_neighbors'],
             'original_named_argument_is_complete_faction_label_not_leader_name': True,
             'unknown_selector_is_input_flag_override_or_leader_byte26_zero_not_knowledge_alone': True,
             'input_flag_provenance': 'Original 6F4D4 obtains a menu object through original dynamic cast05720,then6F714 loads its word at+8 as r2 for6EE90. Broader UI meaning remains unmapped;do not infer visual disguise or knowledge from this flag.',
             'ready1889_1896_uses_player_First_Mate_only_in_already_war_or_pirate_flag0_paths': True,
             'new_war_enemy_announcement_is_separate2201_2208_not_ready1889_1896': True,
             'opponent2201_2208_controls_no_new_editorial_credit': True,
             'CPU_scope': 'Original helpers and branch fragment with a disclosed register-prologue shim. Exact clean text provider bridged at5528C;UI boundary54058 observed and stubbed. Stops at6F054 before battle initialization. Not native glyphs,real scene playback,earned travel,war or battle verification.',
             'full_ROM_actor_identity_saves_and_registered_release_unchanged': True,
             'completed_entries_added': 0, 'source_prose_reviews_added': 0, 'full_goal_complete': False,
             'producer_sha256': sha(Path(__file__).read_bytes())}
    for row in proof['records_and_immediate_neighbors']:
        assert jp[row['message_id']].text.hex() == row['source_hex'] and en[row['message_id']].text.hex() == row['current_text_hex']
    save(ROOT/'source_context_packet.json', proof)
    print('Source context:832 original object/table selections,4 null controls,45 wrapper/UI cases,24 cancellation/acceptance branches and20 complete faction-name getters pass. No new editorial or gameplay completion credit.')


if __name__ == '__main__':
    main()
