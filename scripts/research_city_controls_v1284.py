"""Read-only original city-command disassembly and actual pilot state."""
import struct
from pathlib import Path
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/city_controls_v1284')
RAW = Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_city_v1283b_1266/frame_005610_arm9_ram.bin')


def main():
    assert not ROOT.exists()
    arm = NdsImage.open('out/all_routes_combined_v1266_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    raw = RAW.read_bytes()
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    spans = [(0x6ED34, 0x6EE90), (0x6F4C0, 0x6F840), (0x6F840, 0x6FA00), (0x7251C, 0x72BDC)]
    ROOT.mkdir(parents=True)
    for lo, hi in spans:
        assert arm[lo:hi] == clean[lo:hi]
        (ROOT/f'original_{lo:05X}_{hi:05X}.txt').write_text('\n'.join(
            f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in md.disasm(clean[lo:hi], 0x02000000+lo))+'\n', encoding='utf-8')
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
            row['position'] = list(struct.unpack('<2i', cpu.mem_read(get(struct.unpack('<I', cpu.mem_read(vt+0x5C, 4))[0]-0x02000000, mobile), 8)))
            row['hull'] = get(0x5543C, mobile)
            row['crew'] = get(0x55444, mobile)
        rows.append(row)
    mode = get(0x3F0F8)
    save(ROOT/'actual_state.json', {'snapshot': str(RAW), 'snapshot_sha256': sha(raw), 'fleets': rows,
         'mode': list(struct.unpack('<3I', cpu.mem_read(mode+8, 12))),
         'Madeira_defense_B3FD4_1': get(0xB3FD4, towns+4+30*108, 1),
         'CPU_query_only_no_emulator_mutation': True,
         'producer_sha256': sha(Path(__file__).read_bytes())})


if __name__ == '__main__':
    main()
