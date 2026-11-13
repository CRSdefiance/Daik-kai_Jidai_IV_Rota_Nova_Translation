"""Original speaker providers, wrapper ABI and consumer branches for IDs1020-1069."""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.context_shared_dialogue_v781 import CURRENT, ROOT as CONTEXT, TABLES
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shared_integration_v782')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(CURRENT)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    context = read(CONTEXT/'native_context.json')
    assert context['candidate_sha256'] == sha(CURRENT.read_bytes())
    source = context['pre_fixture_snapshot']
    raw = Path(source['path']).read_bytes()
    assert sha(raw) == source['sha256']
    u = machine(arm)
    u.mem_write(BASE, raw)
    spans = [(0x53CB0, 0x5408C), (0x57408, 0x576CC), (0x576CC, 0x578E0),
             (0x57A5C, 0x57EBC), (0x58618, 0x58834), (0x58F24, 0x58F4C),
             (0x591D0, 0x5923C), (0x59F38, 0x59FA0), (0xB2CD8, 0xB2D58),
             (0xB5690, 0xB56A8), (0x7F1D4, 0x7F1F4)]
    for lo, hi in spans:
        assert arm[lo:hi] == clean[lo:hi], hex(lo)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    def ptr(at): return struct.unpack('<I', u.mem_read(at, 4))[0]
    def text(at): return bytes(u.mem_read(at, 1024)).split(b'\0')[0]

    towns, actors = get(0xCB178), get(0xCB184)
    npc_table = struct.unpack_from('<I', arm, 0x7F1EC)[0]
    city_rows = []
    for index in range(114):
        town = towns+4+index*108
        info = get(0xB5690, (town,))
        assert info == BASE+0x122560+index*0x74
        assert bytes(u.mem_read(info, 0x74)) == arm[info-BASE:info-BASE+0x74]
        culture = arm[info-BASE+0x15]
        assert culture == clean[info-BASE+0x15]
        slot = npc_table+culture*14+13
        npc_id = arm[slot-BASE]
        assert bytes(u.mem_read(slot, 1)) == arm[slot-BASE:slot-BASE+1] == clean[slot-BASE:slot-BASE+1]
        assert npc_id != 208
        speaker = get(0xB2CD8, (town, 13))
        assert speaker == actors+4+npc_id*32 and speaker
        city_rows.append({'town_ID': index, 'culture': culture, 'role13_actor_ID': npc_id, 'speaker': speaker})

    entries = common_message_entries(rom.read_file('/COMMON/MESFILE.DK4'), arm, clean=False)
    chosen, bound, branches = [], [], []
    scratch = 0x02478000
    argument = '１２３４'.encode('cp932')
    u.mem_write(scratch, argument+b'\0')

    def loader(c, pc, size, unused):
        n = c.reg_read(UC_ARM_REG_R0)
        assert 1020 <= n <= 1069
        chosen.append(n)
        c.mem_write(scratch+0x100, entries[n].text+b'\0')
        c.reg_write(UC_ARM_REG_R0, scratch+0x100)
        c.reg_write(UC_ARM_REG_PC, c.reg_read(UC_ARM_REG_LR))

    def core(c, pc, size, unused):
        sp, vargs = c.reg_read(UC_ARM_REG_SP), c.reg_read(UC_ARM_REG_R3)
        parent = c.reg_read(UC_ARM_REG_LR)
        assert parent in (BASE+0x53D24, BASE+0x53E38, BASE+0x54014)
        direct = parent == BASE+0x54014
        bound.append({'mode': c.reg_read(UC_ARM_REG_R0), 'speaker': c.reg_read(UC_ARM_REG_R1),
                      'parent': parent, 'SP': sp, 'saved_key': ptr(sp+(12 if direct else 20)),
                      'va_list': vargs, 'first_argument_hex': text(ptr(vargs)).hex(),
                      'template_hex': text(c.reg_read(UC_ARM_REG_R2)).hex()})

    def stop(c, pc, size, unused):
        branches.append(pc)
        c.emu_stop()

    hooks = [u.hook_add(UC_HOOK_CODE, fn, begin=BASE+at, end=BASE+at)
             for fn, at in ((loader, 0x5528C), (core, 0x54058), (stop, 0x5408C), (stop, 0x54774))]

    def run(wrapper, speaker, key):
        chosen.clear(); bound.clear(); branches.clear()
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.reg_write(UC_ARM_REG_LR, STOP)
        for reg, value in ((UC_ARM_REG_R0, speaker), (UC_ARM_REG_R1, key), (UC_ARM_REG_R2, scratch)):
            u.reg_write(reg, value)
        u.emu_start(BASE+wrapper, STOP, count=200000)
        assert len(chosen) == len(bound) == len(branches) == 1
        row = {'wrapper': BASE+wrapper, 'supplied_role_or_speaker': speaker, 'supplied_key': key,
               'selected_ID': chosen[0], 'core': bound[0], 'consumer_branch': branches[0]}
        result = bound[0]
        assert result['saved_key'] == key and result['va_list'] == STACK-8
        assert result['SP'] == STACK-(24 if wrapper == 0x53FE4 else 32)
        assert result['first_argument_hex'] == argument.hex()
        assert result['template_hex'] == entries[chosen[0]].text.hex()
        assert result['mode'] == int(wrapper == 0x53CB0)
        assert branches == [BASE+0x5408C if result['speaker'] else BASE+0x54774]
        return row

    try:
        # Native role provider and voice selector run unmodified in the real snapshot.
        roles = [run(0x53CB0, role, table) for role, table in
                 ((2, 0x021181C0), (1, 0x021181A0), (1, 0x02118180))]
        roles.append(run(0x53DCC, 2, 1020))
        assert all(r['core']['speaker'] and r['consumer_branch'] == BASE+0x5408C for r in roles)
        direct = []
        for town in city_rows:
            for key in range(1028, 1035):
                if key != 1030:
                    direct.append({'town_ID': town['town_ID'], **run(0x53FE4, town['speaker'], key)})
        personal = []
        for row in context['all21_private_barmaid_speeches']:
            actor = actors+4+row['actor_index']*32
            assert row['speaker_or_role'] == actor and row['table_or_ID'] == row['actor_index']+863
            personal.append({'town_ID': row['town_ID'], 'actor_ID': row['actor_index'],
                             **run(0x53FE4, actor, row['table_or_ID'])})
            direct.append({'town_ID': row['town_ID'], **run(0x53FE4, actor, 1030)})
        negative = run(0x53FE4, 0, 1028)
        assert negative['consumer_branch'] == BASE+0x54774
    finally:
        for hook in hooks:
            u.hook_del(hook)

    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    source_rows = [{'span': [lo, hi], 'sha256': sha(clean[lo:hi]),
                    'instructions': [{'address': i.address, 'mnemonic': i.mnemonic, 'operands': i.op_str}
                                     for i in cs.disasm(clean[lo:hi], BASE+lo)]} for lo, hi in spans]
    save(ROOT/'consumer_routing.json', {
        'source_ROM_sha256': sha(CURRENT.read_bytes()), 'source_context_sha256': sha((CONTEXT/'native_context.json').read_bytes()),
        'all114_immutable_city_role13_mappings': city_rows,
        'four_unmodified_real_role_and_voice_provider_bindings': roles,
        'all_native_city_and_barmaid_direct_bindings': direct,
        'all21_native_private_barmaid_bindings': personal, 'null_actor_negative_system_branch': negative,
        'original_source_executable_spans': source_rows,
        'message_loader_only_stubbed_to_actual_current_ROM_entries': True,
        'supplied_argument_is_ABI_sentinel_not_a_real_coordinate_or_earned_headcount': True,
        'source_callers_select_nonnull_portrait_core_for_these_families': True,
        'null_system_core_remains_unchanged': True,
        'full_caller_filter_tests_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'{len(city_rows)} immutable NPC mappings,4 real role bindings,{len(direct)} direct bindings,21 private bindings and null negative pass.', flush=True)


if __name__ == '__main__':
    main()
