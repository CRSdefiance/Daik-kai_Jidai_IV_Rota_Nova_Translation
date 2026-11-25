"""Normal A inputs only;each revised line needs two complete pixel-exact holds."""
import json
import struct
import time
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save
from scripts.prepare_lil_opening_research_v1704 import ROM

ROOT=Path('work/analysis/lil_opening_navigation_v1707')
RUN=Path('work/analysis/lil_opening_trace_v1706')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY')
JOURNAL=RUN/'navigation.jsonl'


def snapshot(frame):
    p=CAP/f'frame_{frame:06d}_arm9_ram.bin';im=CAP/f'frame_{frame:06d}_navigation.png'
    deadline=time.monotonic()+60
    while not p.exists() or p.stat().st_size!=0x400000 or not im.exists():
        if time.monotonic()>deadline:raise TimeoutError(f'Capture observation timeout at{frame};no process termination or restart inferred')
        time.sleep(.1)
    deadline=time.monotonic()+5
    while True:
        try:progress=read(RUN/'live_observer_progress.json');image=Image.open(im).convert('RGB');image.load();break
        except (ValueError,OSError):
            assert time.monotonic()<deadline;time.sleep(.05)
    assert not progress['errors'] and not progress['mismatches']
    return p.read_bytes(),image,progress


def append(command):
    with JOURNAL.open('a',encoding='utf-8') as f:f.write(json.dumps(command)+'\n')


if __name__=='__main__':
    assert not ROOT.exists() and not JOURNAL.read_text(encoding='utf-8')
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[22]
    doc=read('translations/lil_opening_editorial_manuscript_v2.json');fonts=read(doc['native_font_proof'])
    mapping=read('work/analysis/lil_opening_relocation_v1701/parity_and_native_command_research.json')
    by_id={r['id']:r for r in mapping['mapped_texts']};font_by_id={r['id']:r for r in fonts['cases']}
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    ROOT.mkdir(parents=True);frame=6000;holds=[]
    for number,row in enumerate(doc['records']):
        spec=by_id[row['id']];reference=font_by_id[row['id']]
        expected=bytes.fromhex(spec['target_hex'])[1:].replace(b'FI',b'Lil')
        pixels=Image.open(reference['preview']).convert('RGB')
        wanted={(16+x,296+y) for y in range(64) for x in range(216) if pixels.getpixel((x,y))==(0,8,0)}
        pair=[];waits=0
        while len(pair)<2:
            raw,im,progress=snapshot(frame);value=cstring(raw,wrapped)
            pending=[progress['rows'][v] for v in progress['pending'].values()]
            matching=[r for r in pending if r['source'].get('classification')=='original_SC_cache'
                and (r['source']['route'],r['source']['block'],r['source']['instruction_offset'])==(2,22,spec['new_offset']-5)]
            actual={(x,y) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)}
            if value==expected and actual==wanted and len(matching)==1:
                ptr=matching[0]['source']['payload_address'];assert raw[ptr-0x02000000:ptr-0x02000000+len(block)]==block
                pair.append({'frame':frame,'id':row['id'],'speaker':row['speaker'],'source_speaker_hex':row['source_presentation_prefix_hex'],
                    'native_command_offset':spec['new_offset']-5,'native_script_source':matching[0]['source'],
                    'formatted_hex':value.hex(),'full_actual_ink_plane_equal_native':True,
                    'complete_leading_trailing_letters_zero_margins_and_bounds':True,
                    'RAM_sha256':sha(raw),'capture':str(CAP/f'frame_{frame:06d}_navigation.png'),
                    'capture_sha256':sha((CAP/f'frame_{frame:06d}_navigation.png').read_bytes())})
                if len(pair)==1:
                    append({'until':frame+30,'duration':1});frame+=30
            else:
                waits+=1
                observation={'row':row['id'],'frame':frame,'expected_hex':expected.hex(),'actual_hex':value.hex(),
                    'missing_ink_pixels':len(wanted-actual),'extra_ink_pixels':len(actual-wanted),
                    'pending_source_offsets':[p['source'] for p in pending]}
                save(ROOT/'latest_wait_observation.json',observation)
                print({'waiting_for':row['id'],'frame':frame,'missing':len(wanted-actual),'extra':len(actual-wanted)},flush=True)
                if waits>6:raise RuntimeError('Bounded stable-hold wait failed;run left paused for inspection,not restarted')
                append({'until':frame+100,'duration':1});frame+=100
        holds.append({'id':row['id'],'holds':pair})
        save(ROOT/'verified_holds_LIVE.json',{'rows':holds,'not_terminal_or_full_scene_proof':True,
            'only_normal_A_inputs':True,'ROM_sha256':sha(ROM.read_bytes())})
        print({'verified':number+1,'of':49,'id':row['id'],'frames':[p['frame'] for p in pair]},flush=True)
        # A is applied only after two complete native-matching holds. No other
        # input or state edit may manufacture a line or skip a failed panel.
        append({'until':frame+200,'buttons':['A'],'duration':8});frame+=200
    raw,im,progress=snapshot(frame)
    save(ROOT/'all49_holds_and_post_opening_pause.json',{'rows':holds,'post_last_A_frame':frame,
        'post_last_A_RAM_sha256':sha(raw),'post_last_A_capture':str(CAP/f'frame_{frame:06d}_navigation.png'),
        'normal_A_dismissal_of_all49_rows':True,'no_save_savestate_or_fixture_used':True,
        'full_scene_transition_audit_still_required':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('All49 revised lines have two complete pixel-exact actual holds;normal final A applied. Emulator remains paused for transition inspection.',flush=True)
