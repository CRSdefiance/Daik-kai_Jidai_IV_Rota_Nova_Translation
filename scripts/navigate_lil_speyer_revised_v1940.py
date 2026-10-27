"""Complete revised original Speyer path with native/actual glyph and menu checks."""
import json
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import navigate_lil_crew_v1759b as prior
from scripts.calibrate_lil_speyer_choice_v1939 import planes,verify as verify_menu
from scripts.prepare_lil_speyer_research_v1929 import ROM
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Speyer_revised_navigation_v1940')
RUN=Path('work/analysis/lil_Speyer_revised_run_v1938')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Speyer_revised_run_v1938_RESEARCH_ONLY')
JOURNAL=RUN/'navigation.jsonl'
snapshot=FunctionType(prior.snapshot.__code__,{**prior.__dict__,'RUN':RUN,'CAP':CAP})

def append(command):
    with JOURNAL.open('a',encoding='utf-8')as stream:stream.write(json.dumps(command)+'\n')

if __name__=='__main__':
    assert not ROOT.exists()
    original=read('work/analysis/lil_Speyer_original_navigation_v1934/closed_original_scene_context.json')
    expected_ids=set(original['unique_observed_record_IDs'])
    assert len(expected_ids)==51
    mapping=next(r for r in read('work/analysis/lil_Speyer_relocation_v1928/nested_source_relocation_research.json')['blocks']if r['block']==128)
    by_offset={r['new_offset']-5:r for r in mapping['text_records']}
    fonts={r['id']:r for r in read('work/analysis/lil_Speyer_font_approval_v1937b/all57_complete_native_font_and_macro_reconciliation.json')['cases']}
    calibration=read('work/analysis/lil_Speyer_choice_calibration_v1939/original_current_menu_fixed_margin_calibration.json')
    assert calibration['calibrated_only_from_original_menu_before_revised_pixels']
    ui=read('work/analysis/lil_Speyer_choice_v1927/original_choice_decoder_VM_geometry_and_native_pixels.json')
    menu=next(r for r in ui['current_and_reviewed_VM_and_font_cases']if r['version']=='reviewed-research')
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin')
    menu_planes=planes(arm,menu)
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    ROOT.mkdir(parents=True)
    frame=76620
    holds,choices=[],[]
    for step in range(70):
        raw,im,progress,photo=snapshot(frame)
        pending=[progress['rows'][i]for i in progress['pending'].values()]
        active=[r for r in pending if r['source'].get('route')==2 and r['source'].get('block')==128]
        if not active:
            ends=[r for r in progress['rows']if r['kind']=='after_command'and r['source'].get('route')==2
                and r['source'].get('block')==128 and r['source']['first_word']==0]
            assert ends and {r['id']for r in holds}==expected_ids and len(choices)==1
            save(ROOT/'closed_revised_B128_unit_and_normal_Hamburg_return.json',dict(research_ROM=str(ROM),
                research_ROM_sha256=sha(ROM.read_bytes()),terminal_frame_requested=frame,holds=holds,choices=choices,
                original_B128_end=ends[-1],terminal_capture=str(photo),terminal_capture_sha256=sha(photo.read_bytes()),
                all51_activated_revised_speeches102_holds_complete_native_independent_actual_ink=True,
                both_revised_choice_labels_two_holds_complete_native_actual_ink=True,
                six_other_speeches_not_individually_activated=True,alternate_choice1_not_played=True,
                not_registered_candidate_or_editorial_completion=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
            append({'stop':True})
            print(dict(revised_B128_closed=True,speeches=51,complete_speech_holds=102,choice_holds=2,frame=frame),flush=True)
            break
        assert len(active)==1
        src=active[0]['source']
        assert src['whole_resident_payload_exact_ROM']and src['actual_sha256']==mapping['research_block_sha256']
        at=src['payload_address']-0x02000000
        assert sha(raw[at:at+src['payload_bytes']])==mapping['research_block_sha256']
        assert src['first_word']in(0x4000,0x2100),('unknown revised pending command;leftpaused',src)
        choice=src['first_word']==0x2100
        if choice:
            assert not choices and src['instruction_offset']==mapping['choice_commands'][0]['new_offset']
            spec=None
        else:
            spec=by_offset[src['instruction_offset']]
            assert spec['id']not in {r['id']for r in holds},('unexpected pagination/repeated speech;leftpaused',spec['id'])
            expected=Image.open(fonts[spec['id']]['preview']).convert('RGB')
            assert expected.size==(216,64)
            wanted={(16+x,296+y)for y in range(64)for x in range(216)if expected.getpixel((x,y))==(0,8,0)}
        group=[]
        for hold in range(2):
            raw,im,progress,photo=snapshot(frame)
            assert any(progress['rows'][i]['source']==src for i in progress['pending'].values())
            if choice:
                menu_proof=verify_menu(im,menu,menu_planes)
            else:
                actual={(x,y)for y in range(296,360)for x in range(16,232)if im.getpixel((x,y))==(0,8,0)}
                if actual!=wanted:
                    save(ROOT/'glyph_mismatch_observation.json',dict(id=spec['id'],frame=frame,source=src,
                        missing_pixels=len(wanted-actual),extra_pixels=len(actual-wanted),run_left_paused_no_A_advance=True))
                    raise AssertionError('Incomplete revised glyph hold;leftpaused')
                target=bytes.fromhex(spec['target_hex'])[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
                assert cstring(raw,wrapped)==target
            at=src['payload_address']-0x02000000
            assert sha(raw[at:at+src['payload_bytes']])==mapping['research_block_sha256']
            group.append(dict(frame=frame,capture=str(photo),capture_sha256=sha(photo.read_bytes()),RAM_sha256=sha(raw),
                source=src,complete_native_independent_actual_ink_equal=True,menu_proof=menu_proof if choice else None))
            if hold==0:append(dict(until=frame+30,duration=1));frame+=30
        if choice:choices.append(dict(source=src,holds=group,ordinary_A_selects_original_default0=True))
        else:holds.append(dict(id=spec['id'],prefix_hex=spec['target_hex'][:2],consumer='original_progressive_54020',holds=group))
        save(ROOT/'verified_revised_holds_LIVE.json',dict(rows=holds,choices=choices,next_pause_frame=frame+300,not_terminal_or_complete_scene_proof=True))
        print(dict(verified_speeches=len(holds),id=spec['id']if spec else 'typed-choice',frame=frame),flush=True)
        append(dict(until=frame+300,buttons=['A'],duration=8))
        frame+=300
    else:raise AssertionError('Bounded revised navigation exhausted;leftpaused')
