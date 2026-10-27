"""Source navigation census and correct live output-buffer position queries.

V1284b failed before querying: its extra source guard included localized menu
data. Clean and current menu words are recorded separately here, not asserted
identical. No output or memory is supplied to the running emulator.
"""
import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/city_controls_v1284c')
RAW = Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_city_v1283b_1266/frame_006010_arm9_ram.bin')


def main():
    assert not ROOT.exists()
    arm = NdsImage.open('out/all_routes_combined_v1266_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    raw = RAW.read_bytes()
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    ROOT.mkdir(parents=True)
    menu_spans = []
    for lo, hi in [(0x6F0C8, 0x6F4D4), (0x36A24, 0x36A68)]:
        for name, body in [('clean', clean), ('current', arm)]:
            (ROOT/f'{name}_{lo:05X}_{hi:05X}.txt').write_text('\n'.join(
                f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in md.disasm(body[lo:hi], 0x02000000+lo))+'\n', encoding='utf-8')
        menu_spans.append({'lo': lo, 'hi': hi, 'source_equal': arm[lo:hi] == clean[lo:hi],
            'changed_offsets': [i for i in range(lo, hi) if arm[i] != clean[i]]})
    cpu, get = get_machine(arm, raw)
    fleets, towns = get(0xCB1A8), get(0xCB178)
    rows = []
    for index in [1, 22, 24]:
        fleet = fleets+4+132*index
        mobile = get(0x36C70, fleet+12)
        row = {'fleet_ID': index, 'native_town_ID': get(0x34674, fleet),
               'native_company_ID': get(0x35320, fleet), 'native_captain_ID': get(0x7EE08, get(0x3697C, fleet)),
               'mobile': mobile}
        if mobile:
            vt = struct.unpack('<I', cpu.mem_read(mobile, 4))[0]
            getter = struct.unpack('<I', cpu.mem_read(vt+0x5C, 4))[0]
            assert getter == 0x02036A24 and arm[0x36A24:0x36A68] == clean[0x36A24:0x36A68]
            get(getter-0x02000000, 0x02470000, mobile)
            row['position'] = list(struct.unpack('<2i', cpu.mem_read(0x02470000, 8)))
            row['hull'] = get(0x5543C, mobile)
            row['crew'] = get(0x55444, mobile)
        rows.append(row)
    mode = get(0x3F0F8)
    save(ROOT/'actual_state.json', {'snapshot': str(RAW), 'snapshot_sha256': sha(raw), 'fleets': rows,
         'mode': list(struct.unpack('<3I', cpu.mem_read(mode+8, 12))),
         'Madeira_defense_B3FD4_1': get(0xB3FD4, towns+4+30*108, 1),
         'code_spans': menu_spans, 'CPU_query_only_no_emulator_mutation': True,
         'predecessor_1284_positions_invalid': True, 'predecessor_1284b_failed_pre_query': True,
         'producer_sha256': sha(Path(__file__).read_bytes())})


if __name__ == '__main__':
    main()
