"""Read-only current-build state and exact replay of the proposed 17-byte fixture."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_close_sighting_v1689 import ROM, apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/close_sighting_preflight_v1691')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/close_sighting_v1690_1676_closeReady8')


if __name__ == '__main__':
    assert not ROOT.exists()
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    path = CAP / 'frame_005100_arm9_ram.bin'
    raw = path.read_bytes()
    cpu, get = get_machine(arm, raw)
    root = get(0xCB1A8)
    fleets = []
    for number in (1, 8, 28):
        owner = root + 4 + 132 * number
        mobile = get(0x36C70, owner + 12)
        fleets.append({'fleet_ID': number, 'company_ID': get(0x35320, owner),
                       'cached_point': list(struct.unpack('<2i', cpu.mem_read(owner+0x34, 8))),
                       'mobile': mobile, 'active': bool(mobile and get(0x564C8, mobile)),
                       'mobile_point_fixed128': list(struct.unpack('<2i', cpu.mem_read(mobile+16, 8))) if mobile else None,
                       'flags_at50': cpu.mem_read(owner+0x50, 1)[0]})
    assert fleets[1]['active'] and not fleets[1]['flags_at50'] & 4
    after, fixture = apply_fixture(arm, raw, {'sighting_context': 'closeReady8'})
    assert len(fixture['owned_bytes']) == 17
    ROOT.mkdir(parents=True)
    report = {'ROM': str(ROM), 'ROM_sha256': sha(ROM.read_bytes()), 'frame': 5100,
              'RAM': str(path), 'RAM_sha256': sha(raw), 'fleets': fleets,
              'loaded_groups_before': list(cpu.mem_read(root+0x2080, 16)),
              'fixture_replay': fixture, 'fixture_not_yet_applied_in_emulator': True,
              'no_completion_credit': True, 'producer_sha256': sha(Path(__file__).read_bytes())}
    save(ROOT/'preflight.json', report)
    print({'fleets': fleets, 'loaded_groups': report['loaded_groups_before'],
           'fixture_bytes': len(fixture['owned_bytes']), 'point': fixture['original_own_position_set_to_native_water_point']})
