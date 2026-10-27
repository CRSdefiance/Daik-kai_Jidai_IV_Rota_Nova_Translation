"""Real Guild/crew providers, original wrappers and exact argument binding."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_item_diplomacy_v784 import CURRENT, ROOT as CONTEXT, TABLES
from scripts.native_call_abi_v764 import call
from scripts.prepare_item_common_v788 import ROOT, RUNTIME, IDS
from scripts.prepare_recruitment_common_v772 import local_entries
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.research_scheme_name_width_v787 import live, RAM
from scripts.review_item_diplomacy_v784 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save


def main():
    plan = read(ROOT/'prospective_common_repack.json')
    arm = (ROOT/'COMBINED_ARM9_RESEARCH_ONLY.bin').read_bytes()
    common = (ROOT/'COMMON_RESEARCH_ONLY.bin').read_bytes()
    assert sha(arm) == plan['target_ARM9_sha256'] and sha(common) == plan['target_COMMON_sha256']
    entries = local_entries(plan['directory_sha256'])(common, arm, clean=False)
    runtime = RUNTIME.read_bytes()
    cpu = live(runtime, True)
    # Only guarded directory fields differ from V787. Preserve the actual heap.
    for at, size in plan['metadata_fields']:
        assert bytes(cpu.mem_read(BASE+at, size)) == runtime[at:at+size]
        cpu.mem_write(BASE+at, arm[at:at+size])
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x53CB0, 0x5408C), (0x5B558, 0x5BB30), (0x5BC8C, 0x5BDEC),
             (0x5BE00, 0x5C450), (0xB2CD8, 0xB2D58), (0xB51B4, 0xB51CC),
             (0x7F1D4, 0x7F1F4), (0x7F37C, 0x7F39C), (0x825E4, 0x82600)]
    for lo, hi in spans:
        assert arm[lo:hi] == clean[lo:hi]
        assert bytes(cpu.mem_read(BASE+lo, hi-lo)) == arm[lo:hi]

    def get(fn, args=()):
        call(cpu, fn, args)
        return cpu.reg_read(UC_ARM_REG_R0)
    def ptr(at): return struct.unpack('<I', cpu.mem_read(at, 4))[0]
    def text(at): return bytes(cpu.mem_read(at, 1024)).split(b'\0', 1)[0]

    rows = {r['message_id']: r for r in read(MANUSCRIPT)['records']}
    context = read(CONTEXT/'native_context.json')
    assert context['candidate_sha256'] == sha(CURRENT.read_bytes()) == plan['source_ROM_sha256']
    assert context['producer_sha256'] == sha(Path('scripts/context_item_diplomacy_v784.py').read_bytes())
    selections = context['all2080_actor_voice_selections']
    assert len(selections) == 2080 and set(r['table'] for r in selections) == set(TABLES)
    for table, values in TABLES.items():
        assert struct.unpack('<8i', cpu.mem_read(table, 32)) == values
        assert arm[table-BASE:table-BASE+32] == clean[table-BASE:table-BASE+32]
    towns, actors = get(0xCB178), get(0xCB184)
    city_rows = []
    for n in range(90):
        town = towns+4+n*108
        culture = get(0xB51B4, (town,))
        actor = get(0xB2CD8, (town, 5))
        actor_id = (actor-actors-4)//32
        assert actor_id == arm[0x11948C+culture*14+6] and actor_id in (147, 148, 149, 150)
        city_rows.append({'town_ID': n, 'culture': culture, 'actor_ID': actor_id, 'speaker': actor})

    first_mate_controller = get(0xCB1A8)+0x2090
    role_ids = {role: get(0x82478, (first_mate_controller, role)) for role in (1, 3)}
    sentinel = get(0x7F244)
    fallback = struct.unpack_from('<I', arm, 0x53D40)[0]
    providers = {role: actors+(fallback if n == sentinel else 4+n*32) for role, n in role_ids.items()}
    number = text(get(0xABF50, (1234,)))
    kind = text(get(0x93D5C, (2,)))
    assert kind == b'pact termination notice'
    # Distinct ABI sentinels identify faction-argument order without claiming
    # either faction pair is eligible for a real diplomatic operation.
    scratch = 0x02478000
    values = (number, kind, b'RECIPIENT_A', b'ENEMY_B')
    pointers = [scratch+i*128 for i in range(len(values))]
    for at, value in zip(pointers, values): cpu.mem_write(at, value+b'\0')
    selected, bound, branches = [], [], []

    def loader(c, pc, size, data):
        n = c.reg_read(UC_ARM_REG_R0)
        assert n in IDS
        selected.append(n)
        c.mem_write(scratch+0x400, entries[n].text+b'\0')
        c.reg_write(UC_ARM_REG_R0, scratch+0x400)
        c.reg_write(UC_ARM_REG_PC, c.reg_read(UC_ARM_REG_LR))

    def core(c, pc, size, data):
        parent, sp = c.reg_read(UC_ARM_REG_LR), c.reg_read(UC_ARM_REG_SP)
        assert parent in (BASE+0x54014, BASE+0x53FCC, BASE+0x53DB8, BASE+0x53D24)
        direct = parent in (BASE+0x54014, BASE+0x53FCC)
        count = len(rows[selected[0]]['source_native_arguments'])
        va = c.reg_read(UC_ARM_REG_R3)
        bound.append({'parent': parent, 'mode': c.reg_read(UC_ARM_REG_R0),
            'speaker': c.reg_read(UC_ARM_REG_R1), 'SP': sp, 'saved_key': ptr(sp+(12 if direct else 20)),
            'va_list': va, 'argument_hex': [text(ptr(va+4*i)).hex() for i in range(count)],
            'template_hex': text(c.reg_read(UC_ARM_REG_R2)).hex()})

    def stop(c, pc, size, data): branches.append(pc); c.emu_stop()
    hooks = [cpu.hook_add(UC_HOOK_CODE, fn, begin=BASE+at, end=BASE+at)
             for fn, at in ((loader, 0x5528C), (core, 0x54058), (stop, 0x5408C), (stop, 0x54774))]

    def run(wrapper, speaker, key, args=()):
        selected.clear(); bound.clear(); branches.clear()
        cpu.reg_write(UC_ARM_REG_SP, STACK); cpu.reg_write(UC_ARM_REG_LR, STOP)
        passed = tuple(args)+(pointers[0], pointers[1])
        for reg, value in ((UC_ARM_REG_R0, speaker), (UC_ARM_REG_R1, key),
                           (UC_ARM_REG_R2, passed[0]), (UC_ARM_REG_R3, passed[1])):
            cpu.reg_write(reg, value)
        cpu.emu_start(BASE+wrapper, STOP, count=200000)
        assert len(selected) == len(bound) == len(branches) == 1
        result, n = bound[0], selected[0]
        direct = wrapper in (0x53FE4, 0x53F9C)
        assert result['saved_key'] == key and result['va_list'] == STACK-8
        assert result['SP'] == STACK-(24 if direct else 32)
        assert result['argument_hex'] == [text(p).hex() for p in args]
        assert result['template_hex'] == entries[n].text.hex()
        assert result['mode'] == int(wrapper in (0x53CB0, 0x53F9C))
        assert result['speaker'] == (speaker if direct else providers[speaker])
        assert branches == [BASE+(0x5408C if result['speaker'] else 0x54774)]
        return {'wrapper': BASE+wrapper, 'supplied_role_or_speaker': speaker, 'supplied_key': key,
                'selected_ID': n, 'core': result, 'consumer_branch': branches[0]}

    try:
        direct = []
        keys = (1070, 1071, 1072, 1073, 1074, 1083, 1084, 1085, 1086, 1095, 1096, 1097, 1123, 1130)
        for town in city_rows:
            for key in keys:
                args = (pointers[0],) if len(rows[key]['source_native_arguments']) else ()
                direct.append({'town_ID': town['town_ID'], **run(0x53F9C if key in (1073, 1086) else 0x53FE4,
                                                                town['speaker'], key, args)})
        role_cases = []
        for table in TABLES:
            role = 3 if table in (0x02118160, 0x02118140) else 1
            yesno = table in (0x02117F60, 0x021180C0, 0x021180A0)
            if table == 0x02118120: args = (pointers[1],)
            elif table == 0x02117F60: args = (pointers[2], pointers[3])
            elif table == 0x021180C0: args = (pointers[2], pointers[1])
            elif table == 0x021180A0: args = (pointers[2],)
            else: args = ()
            role_cases.append(run(0x53CB0 if yesno else 0x53D44, role, table, args))
        negative = run(0x53FE4, 0, 1071)
    finally:
        for hook in hooks: cpu.hook_del(hook)
    assert set(r['selected_ID'] for r in direct) | set(r['selected_ID'] for r in selections) == set(IDS)
    assert all(r['core']['speaker'] for r in role_cases+direct)
    save(ROOT/'consumer_routing.json', {
        'source_ROM_sha256': plan['source_ROM_sha256'], 'research_COMMON_sha256': sha(common),
        'research_ARM9_sha256': sha(arm), 'live_snapshot': str(RAM), 'live_snapshot_sha256': sha(RAM.read_bytes()),
        'all90_real_Guild_NPC_mappings': city_rows, 'all1260_direct_Guild_wrapper_bindings': direct,
        'native_role_actor_IDs': role_ids, 'native_role_actor_pointers': providers,
        'ten_real_role_and_voice_provider_bindings': role_cases, 'null_actor_negative_system_branch': negative,
        'prior_all2080_immutable_native_voice_selections': str(CONTEXT/'native_context.json'),
        'prior_voice_selection_proof_sha256': sha((CONTEXT/'native_context.json').read_bytes()),
        'all76_message_IDs_covered_by_original_direct_or_voice_selectors': list(IDS),
        'exact_argument_count_order_and_template_binding': True,
        'only_message_loader_stubbed_to_research_ROM_entries': True,
        'source_executable_spans_unchanged': [{'offset_range': [lo, hi], 'sha256': sha(clean[lo:hi])} for lo, hi in spans],
        'ABI_sentinels_are_not_real_diplomatic_eligibility_or_economic_outcomes': True,
        'full_branch_eligibility_registered_ROM_and_actual_revised_scene_samples_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('90 Guild mappings, 1260 direct bindings, 10 original role wrappers, exact two-argument order and null-actor control pass.', flush=True)


if __name__ == '__main__':
    main()
