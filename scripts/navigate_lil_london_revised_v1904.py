"""Verify revised original London path with exact full native/actual glyph holds."""
import argparse
import json
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import navigate_lil_crew_v1759b as prior
from scripts.prepare_lil_london_research_v1901 import ROM
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_London_revised_navigation_v1904')
RUN=Path('work/analysis/lil_London_revised_run_v1903')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_London_revised_run_v1903_RESEARCH_ONLY')
JOURNAL=RUN/'navigation.jsonl'
snapshot=FunctionType(prior.snapshot.__code__,{**prior.__dict__,'RUN':RUN,'CAP':CAP})

def append(command):
    with JOURNAL.open('a',encoding='utf-8') as f:f.write(json.dumps(command)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--frame',type=int,default=49440)
    args=p.parse_args()
    assert not ROOT.exists()
    mapping=read('work/analysis/lil_London_relocation_v1899/nested_source_relocation_research.json')
    by_offset={r['new_offset']-5:r for r in mapping['text_records']}
    doc=read('translations/lil_london_editorial_manuscript_v4.json')
    fonts={r['id']:r for r in read(doc['native_font_proof'])['cases']}
    original=read('work/analysis/lil_London_context_navigation_v1891/closed_original_B26_context.json')
    expected_ids=set(original['unique_observed_record_IDs'])
    assert len(expected_ids)==105
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin')
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    ROOT.mkdir(parents=True)
    frame=args.frame
    holds,art,pans=[],[],[]
    for step in range(150):
        raw,im,progress,photo=snapshot(frame)
        pending=[progress['rows'][i] for i in progress['pending'].values()]
        active=[r for r in pending if r['source'].get('route')==2 and r['source'].get('block')==26]
        if not active:
            ends=[r for r in progress['rows'] if r['kind']=='after_command' and r['source'].get('route')==2
                and r['source'].get('block')==26 and r['source']['first_word']==0]
            assert ends and {r['id'] for r in holds}==expected_ids,('incomplete revised path;leftpaused',frame)
            save(ROOT/'closed_revised_B26_unit_and_next_context.json',dict(research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
                terminal_frame_requested=frame,holds=holds,original2000_art_pauses=art,original4905_art_pans=pans,
                original_B26_end=ends[-1],terminal_capture=str(photo),terminal_capture_sha256=sha(photo.read_bytes()),
                all105_activated_revised_speeches_have_two_complete_native_matching_holds=True,
                six_conditional_records_not_individually_activated=True,
                not_registered_candidate_or_editorial_completion=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
            append({'stop':True})
            print(dict(revised_B26_closed=True,speeches=len(holds),frame=frame),flush=True)
            break
        assert len(active)==1
        src=active[0]['source']
        assert src['whole_resident_payload_exact_ROM'] and src['actual_sha256']==mapping['research_block_sha256']
        at=src['payload_address']-0x02000000
        assert sha(raw[at:at+src['payload_bytes']])==mapping['research_block_sha256']
        if src['first_word']==0x4905:
            before=dict(frame=frame,capture=str(photo),capture_sha256=sha(photo.read_bytes()),RAM_sha256=sha(raw),source=src)
            append(dict(until=frame+900,duration=1))
            frame+=900
            raw,im,progress,photo=snapshot(frame)
            after=[progress['rows'][i] for i in progress['pending'].values()]
            assert any(r['source'].get('block')==26 and r['source']['instruction_offset']==src['instruction_offset']+2
                and r['source']['first_word']==0x2000 for r in after)
            pans.append(dict(before=before,after=dict(frame=frame,capture=str(photo),capture_sha256=sha(photo.read_bytes()),RAM_sha256=sha(raw)),
                original_timed_pan_completes_without_input=True))
            continue
        if src['first_word']==0x2000:
            group=[]
            for h in range(2):
                raw,im,progress,photo=snapshot(frame)
                assert any(progress['rows'][i]['source']==src for i in progress['pending'].values())
                group.append(dict(frame=frame,capture=str(photo),capture_sha256=sha(photo.read_bytes()),RAM_sha256=sha(raw)))
                if h==0:append(dict(until=frame+30,duration=1));frame+=30
            art.append(dict(source=src,holds=group,original_art_pause_not_padding_generated_blank=True))
            append(dict(until=frame+300,buttons=['A'],duration=8))
            frame+=300
            continue
        assert src['first_word']==0x4000,('new unclassified original pending command;leftpaused',src)
        spec=by_offset[src['instruction_offset']]
        ref=fonts[spec['id']]
        assert spec['id'] not in {r['id'] for r in holds},('unexpected repeated page/instruction;leftpaused',spec['id'],frame)
        modal=spec['consumer']=='original_FE_modal_5473C_mode1'
        width=228 if modal else 216
        expected=Image.open(ref['preview']).convert('RGB')
        assert expected.size==(width,64)
        wanted={(16+x,296+y) for y in range(64) for x in range(width) if expected.getpixel((x,y))==(0,8,0)}
        group=[]
        for h in range(2):
            raw,im,progress,photo=snapshot(frame)
            assert any(progress['rows'][i]['source']==src for i in progress['pending'].values())
            ink={(x,y) for y in range(296,360) for x in range(16,16+width) if im.getpixel((x,y))==(0,8,0)}
            if ink!=wanted:
                save(ROOT/'glyph_mismatch_observation.json',dict(id=spec['id'],frame=frame,source=src,
                    missing_pixels=len(wanted-ink),extra_pixels=len(ink-wanted),run_left_paused_no_A_advance=True))
                raise AssertionError('Incomplete revised native glyph hold;leftpaused')
            if not modal:
                target=bytes.fromhex(spec['target_hex'])[1:].replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')
                assert cstring(raw,wrapped)==target
            at=src['payload_address']-0x02000000
            assert sha(raw[at:at+src['payload_bytes']])==mapping['research_block_sha256']
            group.append(dict(frame=frame,capture=str(photo),capture_sha256=sha(photo.read_bytes()),RAM_sha256=sha(raw),
                source=src,complete_native_independent_actual_ink_equal=True))
            if h==0:append(dict(until=frame+30,duration=1));frame+=30
        holds.append(dict(id=spec['id'],prefix_hex=spec['target_hex'][:2],consumer=spec['consumer'],holds=group))
        save(ROOT/'verified_revised_holds_LIVE.json',dict(rows=holds,next_pause_frame=frame+300,not_terminal_or_complete_scene_proof=True))
        print(dict(verified_revised_speeches=len(holds),id=spec['id'],frames=[r['frame'] for r in group]),flush=True)
        append(dict(until=frame+300,buttons=['A'],duration=8))
        frame+=300
    else:raise AssertionError('Bounded revised navigation exhausted;leftpaused')
