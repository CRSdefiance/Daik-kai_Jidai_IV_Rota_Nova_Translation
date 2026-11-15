"""Advance only after two complete native-matching actual B24 text holds."""
import argparse
import json
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import navigate_lil_crew_v1759b as prior
from scripts.prepare_lil_B24_research_v1829 import ROM
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_navigation_v1837')
RUN=Path('work/analysis/lil_B24_research_run_v1834')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_B24_research_run_v1834_RESEARCH_ONLY')
JOURNAL=RUN/'navigation.jsonl'
snapshot=FunctionType(prior.snapshot.__code__,{**prior.__dict__,'RUN':RUN,'CAP':CAP})

def append(command):
    with JOURNAL.open('a',encoding='utf-8')as f:f.write(json.dumps(command)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--frame',type=int,required=True);args=parser.parse_args()
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    mapping=read('work/analysis/lil_B24_relocation_v1828/parity_and17_native_command_research.json')
    by_offset={r['new_offset']-5:r for r in mapping['texts']}
    fonts={r['id']:r for r in read('work/analysis/lil_B24_fonts_v1826/all13_native_macros_and_complete_font_planes.json')['cases']}
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    frame=args.frame;holds=[]
    for step in range(14):
        raw,im,progress,photo=snapshot(frame)
        pending=[progress['rows'][i]for i in progress['pending'].values()]
        active=[r for r in pending if r['source'].get('route')==2 and r['source'].get('block')==24]
        if not active:
            complete=[r for r in progress['rows']if r['kind']=='after_command'and r['source'].get('route')==2
                      and r['source'].get('block')==24 and r['source']['first_word']==0]
            assert len(holds)==13 and complete,('B24 not active but scene not complete;left paused',frame)
            save(ROOT/'closed_B24_unit_and_next_context.json',{'research_ROM':str(ROM),
                'research_ROM_sha256':sha(ROM.read_bytes()),'terminal_frame_requested':frame,'holds':holds,
                'original_B24_end':complete[-1],'next_pending_original_sources':[r['source']for r in pending],
                'terminal_capture':str(photo),'terminal_capture_sha256':sha(photo.read_bytes()),
                'all13_dialogues_have_two_full_native_matching_actual_holds':True,
                'read_only_trace_prefix_sha256':sha((RUN/'live_observer_progress.json').read_bytes()),
                'not_registered_candidate_or_editorial_completion':True,'producer_sha256':sha(Path(__file__).read_bytes()),
                'full_goal_complete':False})
            append({'stop':True});print({'B24_unit_closed':True,'speeches':13,'frame':frame},flush=True);break
        assert len(active)==1
        src=active[0]['source']
        assert src['whole_resident_payload_exact_ROM']and src['actual_sha256']==mapping['target_block_sha256']
        assert src['first_word']==0x4000,('Unhandled original pending command;left paused',src)
        spec=by_offset[src['instruction_offset']];ref=fonts[spec['id']]
        assert spec['id']not in [r['id']for r in holds]
        expected=Image.open(ref['preview']).convert('RGB');assert expected.size==(216,64)
        wanted={(16+x,296+y)for y in range(64)for x in range(216)if expected.getpixel((x,y))==(0,8,0)}
        group=[]
        for hold in range(2):
            raw,im,progress,photo=snapshot(frame)
            assert any(progress['rows'][i]['source']==src for i in progress['pending'].values())
            actual={(x,y)for y in range(296,360)for x in range(16,232)if im.getpixel((x,y))==(0,8,0)}
            if actual!=wanted:
                save(ROOT/'glyph_mismatch_observation.json',{'id':spec['id'],'frame':frame,
                    'missing_pixels':len(wanted-actual),'extra_pixels':len(actual-wanted),
                    'run_left_paused_no_A_advance':True,'source':src})
                raise AssertionError('Incomplete native text hold;run left paused for evidence')
            assert cstring(raw,wrapped)==bytes.fromhex(spec['encoded_hex'])[1:].replace(b'FI',b'Lil')
            at=src['payload_address']-0x02000000
            assert sha(raw[at:at+src['payload_bytes']])==mapping['target_block_sha256']
            group.append({'frame':frame,'capture':str(photo),'capture_sha256':sha(photo.read_bytes()),
                          'RAM_sha256':sha(raw),'source':src,'complete_native_independent_actual_ink_equal':True})
            if hold==0:append({'until':frame+30,'duration':1});frame+=30
        holds.append({'id':spec['id'],'source_speaker_hex':spec['encoded_hex'][:2],'holds':group})
        save(ROOT/'verified_holds_LIVE.json',{'rows':holds,'not_terminal_or_full_scene_proof':True})
        print({'verified_speeches':len(holds),'id':spec['id'],'frames':[r['frame']for r in group]},flush=True)
        append({'until':frame+300,'buttons':['A'],'duration':8});frame+=300
    else:raise AssertionError('Bounded navigation exhausted;left paused without forced completion')
