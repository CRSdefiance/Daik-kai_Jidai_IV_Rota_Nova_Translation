"""Read actual town-test RAM exports using original getters; no live mutation."""
import argparse
import struct
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.battle_aftermath_editorial import current_entries
from dk4tool.rom.nds import NdsImage
from scripts.native_aftermath_battle_fixture_v1269 import ROM
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/aftermath_town_v1291_1266')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--frames', type=int, nargs='+', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    entries = current_entries(rom.read_file('/COMMON/MESFILE.DK4'),arm)
    owner, wrapped = [struct.unpack_from('<I',arm,offset)[0] for offset in [0x552A0,0x54450]]
    rows = []
    for frame in args.frames:
        source = CAP/f'frame_{frame:06d}_arm9_ram.bin'
        raw = source.read_bytes()
        cpu, get = get_machine(arm,raw)
        fleets, world, towns = [get(fn) for fn in [0xCB1A8,0xCB19C,0xCB178]]
        own, town = fleets+4+132, towns+4+73*108
        mobile = get(0x36C70,own+12)
        mode = list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))
        row = {'frame':frame,'RAM':str(source),'RAM_sha256':sha(raw),'mode8_12_16':mode,
            'town_battle_ID':struct.unpack('<I',cpu.mem_read(world+0x1360,4))[0],
            'selected_fleet_ID':struct.unpack('<I',cpu.mem_read(world+0x135C,4))[0],
            'native_town_defenses':get(0xB3FD4,town,1),
            'First_Mate_actual_actor_ID':get(0x82478,fleets+0x2090,1),
            'CPU_query_only_no_emulator_or_file_mutation':True}
        if mobile:
            get(0x36A24,0x02470000,mobile)
            row['own_live_map_point'] = list(struct.unpack('<2i',cpu.mem_read(0x02470000,8)))
            row['own_live_Hull_Crew'] = [get(0x5543C,mobile),get(0x55444,mobile)]
        template = raw[owner-0x02000000+0x2030:owner-0x02000000+0x2230].split(b'\0')[0]
        text = raw[wrapped-0x02000000:wrapped-0x02000000+512].split(b'\0')[0]
        row.update(last_loaded_template=template.decode('cp932',errors='replace'),
            matching_native_message_IDs=[entry.message_id for entry in entries if entry.text == template],
            last_native_wrapped_output=text.decode('cp932',errors='replace'))
        rows.append(row)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    result = {'rows':rows,'candidate_sha256':sha(ROM.read_bytes()),'producer_sha256':sha(Path(__file__).read_bytes())}
    save(args.out,result)
    for row in rows:
        print(row)


if __name__ == '__main__':
    main()
