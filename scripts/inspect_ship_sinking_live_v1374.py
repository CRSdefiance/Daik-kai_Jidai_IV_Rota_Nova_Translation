"""Read-only native snapshot summaries for the V1373 gunnery test."""
import argparse
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import save

ROM = Path('out/all_routes_combined_v1364_candidate.nds')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_gunnery_v1373_1364')
ROOT = Path('work/analysis/ship_sinking_inspection_v1374')
BASE = 0x02000000


def inspect(frame,arm):
    path = CAP/f'frame_{frame:06d}_arm9_ram.bin'
    body = path.read_bytes()
    assert len(body)==0x400000
    cpu,get = get_machine(arm,body)
    fleets = get(0xCB1A8)
    result = {'frame':frame,'snapshot':str(path),'snapshot_sha256':sha(body),
        'mode':list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12))),
        'party_bytes':bytes(cpu.mem_read(fleets+0x2080,16)).hex(),'ships':[]}
    for fleet_id in [1,5]:
        fleet = fleets+4+132*fleet_id
        for slot in range(5):
            mobile = get(0x36C70,fleet+12+slot*8)
            if not mobile:
                continue
            model = get(0x36C94,fleet+12+slot*8)
            point = list(struct.unpack('<2i',cpu.mem_read(mobile+16,8)))
            result['ships'].append({'fleet':fleet_id,'slot':slot,'mobile':mobile,
                'name':bytes(cpu.mem_read(model+8,24)).split(b'\0')[0].decode('cp932'),
                'Hull_Crew':[get(0x5543C,mobile),get(0x55444,mobile)],
                'map_point':[v//128 for v in point],
                'mobile8_16_hex':bytes(cpu.mem_read(mobile+8,8)).hex()})
    owner,wrapped = [struct.unpack_from('<I',arm,o)[0] for o in [0x552A0,0x54450]]
    result['owner_text_hex'] = body[owner-BASE+0x2030:owner-BASE+0x2230].split(b'\0')[0].hex()
    text = body[wrapped-BASE:wrapped-BASE+512].split(b'\0')[0]
    result['wrapped_text'] = text.decode('cp932',errors='backslashreplace')
    result['wrapped_text_is_not_alone_proof_of_visible_dialogue'] = True
    return result


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('frames',type=int,nargs='+')
    args = parser.parse_args()
    rom = NdsImage.open(ROM)
    assert sha(ROM.read_bytes())=='dbf86d020cb868f443f9c6a9f68706e8cda28e9268ce0318a63ef765f4f3281c'
    arm = rom.read_file('/__arm9__.bin')
    ROOT.mkdir(parents=True,exist_ok=True)
    for frame in args.frames:
        result = inspect(frame,arm)
        target = ROOT/f'frame_{frame:06d}.json'
        assert not target.exists()
        save(target,{**result,'read_only_snapshot_inspection':True,'producer_sha256':sha(Path(__file__).read_bytes())})
        print(result,flush=True)
