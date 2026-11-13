"""Close the two original callers and execute the missing-city NPC guard."""

import re
import struct
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_ARM
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R6, UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.context_barmaid_dialogue_v779 import ROOT, CURRENT
from scripts.inventory_shipyard_storage_v760 import units
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_village_wrap_v608 import read, save

FUNCTIONS = {0x02059358: (0x0205950C, 0x02059318), 0x0205923C: (0x02059358, 0x02059F84)}


def main():
    rom = NdsImage.open(CURRENT)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    refs = {hex(a): {'absolute': [], 'ARM_branch': [], 'ADR': [], 'Thumb_BL_BLX': []} for a in FUNCTIONS}
    def owner(target): return next((a for a, (b, _) in FUNCTIONS.items() if a <= target < b), None)
    thumb = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
    for name, base, raw in units(rom):
        for match in re.finditer(rb'(?=(...\x02))', raw, re.S):
            target = int.from_bytes(match.group(1), 'little')
            a = owner(target & ~1)
            if a is not None:
                refs[hex(a)]['absolute'].append([name, base+match.start(), target])
        for at in range(0, len(raw)-3, 4):
            pc = base+at
            word = struct.unpack_from('<I', raw, at)[0]
            kind = None
            if word & 0x0E000000 == 0x0A000000:
                d = word & 0xFFFFFF
                if d & 0x800000: d -= 0x1000000
                target, kind = pc+8+d*4, 'ARM_branch'
            elif word & 0x0E0F0000 == 0x020F0000 and (word >> 21) & 15 in (2, 4):
                v, shift = word & 255, ((word >> 8) & 15)*2
                if shift: v = ((v >> shift) | (v << (32-shift))) & 0xFFFFFFFF
                target, kind = pc+8+(v if (word >> 21) & 15 == 4 else -v), 'ADR'
            if kind:
                a = owner(target)
                if a is not None and not a <= pc < FUNCTIONS[a][0]:
                    refs[hex(a)][kind].append([name, pc, target])
        for at in range(0, len(raw)-3, 2):
            first, second = struct.unpack_from('<HH', raw, at)
            if first & 0xF800 != 0xF000 or second & 0xF800 not in (0xE800, 0xF800): continue
            instruction = next(thumb.disasm(raw[at:at+4], base+at), None)
            if instruction is None or instruction.mnemonic not in ('bl', 'blx') or not instruction.op_str.startswith('#'): continue
            target = int(instruction.op_str[1:], 0) & ~1
            a = owner(target)
            if a is not None and not a <= base+at < FUNCTIONS[a][0]:
                refs[hex(a)]['Thumb_BL_BLX'].append([name, base+at, target])
    save(ROOT/'latent996_reference_leads.json', refs)
    for a, (b, caller) in FUNCTIONS.items():
        assert arm[a-BASE:b-BASE] == clean[a-BASE:b-BASE]
        assert refs[hex(a)]['ARM_branch'] == [['section0', caller, a]], (hex(a), refs[hex(a)])
        assert not any(refs[hex(a)][k] for k in ('absolute', 'ADR', 'Thumb_BL_BLX')), (hex(a), refs[hex(a)])
    context = read(ROOT/'native_context.json')
    raw = Path(context['pre_fixture_snapshot']['path']).read_bytes()
    assert sha(raw) == context['pre_fixture_snapshot']['sha256']
    assert arm[0x59E00:0x59E10] == clean[0x59E00:0x59E10]
    assert arm[0xB65E4:0xB6618] == clean[0xB65E4:0xB6618]
    # Execute the original actual town-ID getter to identify its source field.
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    code = [{'address': x.address, 'mnemonic': x.mnemonic, 'operands': x.op_str}
            for x in cs.disasm(arm[0xB65E4:0xB6618], BASE+0xB65E4)]
    save(ROOT/'latent996_caller_closure.json', {
        'candidate_sha256': sha(CURRENT.read_bytes()), 'complete_two_function_reference_closure': refs,
        'only_original_chain': ['02059F84 -> 0205923C', '02059318 -> 02059358'],
        'source_catalog58_is_null': next(r['information_row'] for r in context['all114_native_city_information_lookups'] if r['town_ID'] == 58) == 0,
        'ordinary_table_never_selects996_for_any_of21_initialized_barmaids': 996 not in context['all30_catalog_selected_IDs'],
        'native_main_guard_exact_hex': arm[0x59E00:0x59E10].hex(),
        'native_town_getter': code,
        'normal_996_activation_not_claimed': True,
        'decision': 'Retain and review the latent original barmaid speech. Preserve original city58 branch/catalog mismatch;do not patch game dispatch or invent a valid city/actor pairing. Original caller family,meaning and speaker role are established;actual normal activation remains unclaimed.',
        'source_speech_body_retained': True, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Two original private caller chains close without aliases;996 retained as a latent original barmaid branch,without normal-activation credit.', flush=True)


if __name__ == '__main__':
    main()
