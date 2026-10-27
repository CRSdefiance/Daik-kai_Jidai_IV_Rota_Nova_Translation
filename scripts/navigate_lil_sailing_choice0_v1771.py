"""Two complete native-matching holds before each ordinary B120 A advance."""
import json
import struct
import time
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_lessons_research_v1761 import ROM
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_sailing_navigation_v1771')
RUN=Path('work/analysis/lil_sailing_choice0_v1770')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_sailing_choice0_v1770_RESEARCH_ONLY')
JOURNAL=RUN/'navigation.jsonl'

def append(command):
    with JOURNAL.open('a',encoding='utf-8') as f:f.write(json.dumps(command)+'\n')

def snapshot(frame):
    raw_path=CAP/f'frame_{frame:06d}_arm9_ram.bin'; photo=CAP/f'frame_{frame:06d}_navigation.png'
    deadline=time.monotonic()+60
    while True:
        try:
            raw=raw_path.read_bytes(); assert len(raw)==0x400000
            im=Image.open(photo).convert('RGB');im.load()
            progress_path=RUN/'live_observer_progress.json'
            if progress_path.stat().st_mtime_ns < max(raw_path.stat().st_mtime_ns,photo.stat().st_mtime_ns):
                raise ValueError('Waiting for this pause observer flush')
            progress=read(progress_path)
            assert not progress['errors'] and progress['mismatches']==0
            return raw,im,progress,photo
        except (OSError,ValueError,AssertionError):
            if time.monotonic()>deadline:raise TimeoutError(f'Capture observation timed out at{frame};no restart or termination inferred')
            time.sleep(.05)

if __name__=='__main__':
    assert not ROOT.exists()
    mapping=next(b for b in read('work/analysis/lil_lessons_relocation_v1760/nested_source_relocation_research.json')['blocks'] if b['block']==120)
    by_offset={r['new_offset']-5:r for r in mapping['text_records']}
    font={r['id']:r for r in read('work/analysis/lil_Deck_label_approval_v1758/all60_current_native_font_reconciliation.json')['cases']}
    modal={r['id']:r for r in read('work/analysis/lil_Deck_label_approval_v1758/all9_current_FE_reconciliation.json')['reviewed_cases']}
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin'); wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    frame=22930; holds=[]; choice=[]; ROOT.mkdir(parents=True)
    for step in range(40):
        raw,im,progress,photo=snapshot(frame)
        pending=[progress['rows'][i] for i in progress['pending'].values()]
        active=[r for r in pending if r['source'].get('route')==2 and r['source'].get('block')==120]
        if not active:
            complete=[r for r in progress['rows'] if r['kind']=='after_command' and r['source'].get('route')==2
                and r['source'].get('block')==120 and r['source']['first_word']==0]
            assert complete,('B120 not active but no native end',frame,pending)
            save(ROOT/'closed_B120_unit_and_next_context.json',{'research_ROM':str(ROM),'research_ROM_sha256':sha(ROM.read_bytes()),
                'terminal_frame_requested':frame,'holds':holds,'choices':choice,'original_B120_end':complete[-1],
                'read_only_trace_prefix':progress,'next_pending_original_sources':[r['source'] for r in pending],
                'terminal_capture':str(photo),'terminal_capture_sha256':sha(photo.read_bytes()),
                'all_dialogues_have_two_full_native_matching_actual_holds':True,
                'current_manuscript_v5_and_research_v1761':True,
                'not_registered_candidate_or_editorial_completion':True,'producer_sha256':sha(Path(__file__).read_bytes()),
                'full_goal_complete':False})
            append({'stop':True}); print({'B120_unit_closed':True,'speeches':len(holds),'frame':frame},flush=True);break
        assert len(active)==1
        src=active[0]['source']; assert src['whole_resident_payload_exact_ROM'] and src['actual_sha256']==mapping['research_block_sha256']
        if src['first_word']==0x2100:
            assert src['instruction_offset']==mapping['choice_commands'][0]['new_offset'] and not choice
            choice.append({'frame':frame,'source':src,'capture':str(photo),'capture_sha256':sha(photo.read_bytes()),
                           'normal_A_selects_original_default_option0':True})
            save(ROOT/'choice_menu_observation.json',choice)
            append({'until':frame+300,'buttons':['A'],'duration':8});frame+=300;continue
        assert src['first_word']==0x4000,('Unhandled original pending command;leave paused',src)
        spec=by_offset[src['instruction_offset']]; ref=font[spec['id']]
        is_modal=ref['consumer']=='original_FE_modal_548A8'
        path=Path(modal[spec['id']]['display_preview'] if is_modal else ref['preview'])
        expected=Image.open(path).convert('RGB'); width=228 if is_modal else 216
        assert expected.size==(width,64)
        wanted={(16+x,296+y) for y in range(64) for x in range(width) if expected.getpixel((x,y))==(0,8,0)}
        group=[]
        for hold in range(2):
            raw,im,progress,photo=snapshot(frame)
            pending_now=[progress['rows'][i] for i in progress['pending'].values()]
            assert any(r['source']==src for r in pending_now)
            actual={(x,y) for y in range(296,360) for x in range(16,16+width) if im.getpixel((x,y))==(0,8,0)}
            if actual!=wanted:
                save(ROOT/'glyph_mismatch_observation.json',{'id':spec['id'],'frame':frame,
                    'missing_pixels':len(wanted-actual),'extra_pixels':len(actual-wanted),'source':src,
                    'run_left_paused_no_A_advance':True})
                raise AssertionError('Incomplete native text hold;run left paused for evidence')
            if not is_modal:
                assert cstring(raw,wrapped)==bytes.fromhex(spec['target_hex'])[1:].replace(b'FI',b'Lil')
            at=src['payload_address']-0x02000000
            assert sha(raw[at:at+src['payload_bytes']])==mapping['research_block_sha256']
            group.append({'frame':frame,'capture':str(photo),'capture_sha256':sha(photo.read_bytes()),
                          'RAM_sha256':sha(raw),'source':src,'complete_native_independent_actual_ink_plane_equal':True})
            if hold==0:append({'until':frame+30,'duration':1});frame+=30
        holds.append({'id':spec['id'],'source_speaker_hex':spec['target_hex'][:2],'system_FE':is_modal,'holds':group})
        save(ROOT/'verified_holds_LIVE.json',{'rows':holds,'not_terminal_or_full_scene_proof':True})
        print({'verified_speeches':len(holds),'id':spec['id'],'frames':[r['frame'] for r in group]},flush=True)
        append({'until':frame+300,'buttons':['A'],'duration':8});frame+=300
    else:raise AssertionError('Bounded B120 navigation exhausted;run left paused without forced completion')
