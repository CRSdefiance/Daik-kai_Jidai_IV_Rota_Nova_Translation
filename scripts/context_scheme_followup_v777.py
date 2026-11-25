"""Execute unchanged follow-up callers with real captured faction/town providers."""

import struct
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_R3, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_SP)

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.review_scheme_followup_v777 import ROOT, CURRENT, TABLES
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read, save


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(CURRENT)
    arm = rom.read_file('/__arm9__.bin')
    source = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    path = Path('E:/Rota Nova translations/Generated/work/emulation_v193/schemes_v776_qualified_live/capture_report.json')
    report = read(path)
    snapshot = next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame'] == 3200)
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256'] and report['ROM_sha256'] == sha(CURRENT.read_bytes())
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    def ptr(at): return struct.unpack('<I', u.mem_read(at, 4))[0]
    def text(at): return bytes(u.mem_read(at, 256)).split(b'\0')[0]
    def name(obj): return text(get(ptr(ptr(obj) + 8) - BASE, (obj,)))

    officers, factions, towns = get(0xCB184), get(0xCB160), get(0xCB178)
    voices = []
    for table, ids in TABLES.items():
        assert arm[table-BASE:table-BASE+32] == source[table-BASE:table-BASE+32]
        assert struct.unpack('<8i', u.mem_read(table, 32)) == ids
        for i in range(40):
            actor = officers + 4 + 32 * i
            voice = get(0x7E988, (actor,))
            selected = get(0x53F4C, (actor, table))
            assert selected == (ids[voice] if ids[voice] != -1 else ids[0])
            voices.append({'table': table, 'actor_index': i, 'voice': voice, 'selected_ID': selected})
        assert get(0x53F4C, (0, table)) == ids[0]
    current_town = get(0xB6618)
    npc = get(0xB2CD8, (current_town, 13))
    faction = factions + 4 + 76 * 4  # Clifford,not the edited player company.
    town_id = 2  # Amsterdam,supplied native object;not earned travel.
    town_name, faction_name = name(towns + 4 + 108 * town_id), name(faction)
    assert town_name == b'Amsterdam' and faction_name == b'Clifford'
    events, cases, spans = [], [], []

    def observe(c, pc, size, unused):
        key = c.reg_read(UC_ARM_REG_R1)
        argc = 2 if key == 0x02118200 else 0
        args = [text(c.reg_read(r)).hex() for r in (UC_ARM_REG_R2, UC_ARM_REG_R3)[:argc]]
        events.append({'wrapper': pc, 'speaker_or_role': c.reg_read(UC_ARM_REG_R0),
                       'table_or_ID': key, 'arguments_hex': args})
        c.emu_stop()

    hooks = [u.hook_add(UC_HOOK_CODE, observe, begin=BASE+off, end=BASE+off)
             for off in (0x53D44, 0x53CB0, 0x53FE4)]
    try:
        def run(lo, hi, registers, key, args, speaker=2):
            assert arm[lo:hi] == source[lo:hi]
            spans.append([lo, hi])
            events.clear()
            u.reg_write(UC_ARM_REG_SP, STACK)
            for reg, value in registers:
                u.reg_write(reg, value)
            u.emu_start(BASE+lo, BASE+hi, count=10000)
            assert len(events) == 1 and events[0]['table_or_ID'] == key
            assert events[0]['speaker_or_role'] == speaker
            assert events[0]['arguments_hex'] == [a.hex() for a in args]
            cases.append({'original_fragment': [lo, hi], **events[0]})

        run(0x57390, 0x5739C, (), 0x02118240, ())
        run(0x57104, 0x5715C, ((UC_ARM_REG_R0, 9), (UC_ARM_REG_R1, 0), (UC_ARM_REG_R2, 0)), 0x02118220, ())
        run(0x56A10, 0x56A54, ((UC_ARM_REG_R5, town_id), (UC_ARM_REG_R6, faction)), 0x02118200, (town_name, faction_name))
        run(0x572F4, 0x57300, (), 0x021181E0, ())
        run(0x57A30, 0x57A3C, ((UC_ARM_REG_R6, npc),), 972, (), npc)
        condition_cases = []
        assert arm[0x57A20:0x57A3C] == source[0x57A20:0x57A3C]
        for state in range(16):
            events.clear()
            u.reg_write(UC_ARM_REG_SP, STACK)
            u.reg_write(UC_ARM_REG_R0, state)
            u.reg_write(UC_ARM_REG_R6, npc)
            u.emu_start(BASE+0x57A20, BASE+0x57A3C, count=10000)
            assert bool(events) == (5 <= state < 12)
            if events:
                assert events == [{'wrapper': BASE+0x53FE4, 'speaker_or_role': npc, 'table_or_ID': 972, 'arguments_hex': []}]
            condition_cases.append({'supplied_original_condition_return': state, 'emits_972': bool(events)})
    finally:
        for hook in hooks:
            u.hook_del(hook)
    control_spans = [(0x57384, 0x573EC), (0x572D0, 0x57308), (0x56A04, 0x56A84),
                     (0x56FCC, 0x57048), (0x579C4, 0x57A3C)]
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    disassembly = []
    for lo, hi in control_spans:
        assert arm[lo:hi] == source[lo:hi]
        disassembly.append({'span': [lo, hi], 'source_current_sha256': sha(source[lo:hi]),
                            'instructions': [{'address': x.address, 'mnemonic': x.mnemonic, 'operands': x.op_str}
                                             for x in cs.disasm(source[lo:hi], BASE+lo)]})
    save(ROOT / 'native_context.json', {
        'candidate': str(CURRENT), 'candidate_sha256': sha(CURRENT.read_bytes()),
        'source_ARM9_sha256': sha(source), 'current_ARM9_sha256': sha(arm),
        'capture_report': str(path), 'pre_fixture_snapshot': snapshot,
        'all160_actual_actor_voice_selections': voices, 'four_original_null_fallbacks_verified': True,
        'original_voice_tables': {hex(k): v for k, v in TABLES.items()},
        'five_original_consumer_fragments': cases, 'source_current_executable_fragments_exact': spans,
        'sixteen_condition_branch_cases_for_972': condition_cases,
        'original_control_and_provider_context': disassembly,
        'bribe_arguments': ['town', 'faction'], 'rumor_NPC_original_getter_result': npc,
        'followup_is_arrangements_before_original1000_gold_deduction_not_successful_outcome': True,
        'crowded_failure_returns_before_scheme_selection_and_charge': True,
        'scope': 'Original CPU fragments and source branches on captured RAM;not actual new scheme,barmaid-rumor or crowded gameplay activation.',
        'no_gameplay_activation_or_playable_ROM_claim': True,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print('160 voice selections,four fallbacks,five original argument callers and16 condition branches pass.', flush=True)


if __name__ == '__main__':
    main()
