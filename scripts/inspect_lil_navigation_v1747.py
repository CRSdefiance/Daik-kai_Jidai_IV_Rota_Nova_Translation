"""Read captured fleet/port coordinates and pending native scene without mutation."""
import argparse
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.prepare_lil_lessons_research_v1739 import ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_navigation_coordinates_v1747')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lesson_navigation_v1745_RESEARCH_ONLY')

if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('frame',type=int); args=parser.parse_args()
    path=CAP/f'frame_{args.frame:06d}_arm9_ram.bin'
    raw=path.read_bytes(); assert len(raw)==0x400000
    cpu,get=get_machine(NdsImage.open(ROM).read_file('/__arm9__.bin'),raw)
    index=get(0x2E58C); assert index==2
    fleet=get(0xCB1A8)+4+index*132; mobile=get(0x36C70,fleet+12)
    point=list(struct.unpack('<2i',cpu.mem_read(fleet+0x34,8)))
    fixed=list(struct.unpack('<2i',cpu.mem_read(mobile+16,8)))
    towns=[]
    for town in (2,3):
        city=get(0xCD6B8,town)
        towns.append({'index':town,'data':city,'port_point':list(struct.unpack('<2i',cpu.mem_read(city+12,8)))})
    progress=read('work/analysis/lil_lesson_navigation_v1745/live_observer_progress.json')
    assert not progress['errors'] and not progress['mismatches']
    pending=[progress['rows'][v]['source'] for v in progress['pending'].values()]
    ROOT.mkdir(parents=True,exist_ok=True); out=ROOT/f'frame_{args.frame:06d}_readonly_coordinates.json'
    assert not out.exists()
    save(out, {'frame':args.frame,'captured_RAM':str(path),'RAM_sha256':sha(raw),'fleet_index':index,
        'fleet':fleet,'mobile':mobile,'cached_map_point':point,'fixed_mobile_point':fixed,
        'nearby_original_port_models':towns,'pending_original_sources':pending,
        'observer_callbacks_so_far':progress['callbacks'],'original_getters_on_offline_copy_only':True,
        'no_live_gameplay_mutation':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print({'frame':args.frame,'point':point,'pending':pending})
