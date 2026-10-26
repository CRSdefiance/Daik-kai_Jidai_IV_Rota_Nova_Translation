"""Observe one original London path; no revised-text or all-branch credit."""
import argparse
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_lil_london_live_v1887 import snapshot, JOURNAL
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_London_context_navigation_v1888')
PACKET=Path('work/analysis/lil_London_source_v1879b/all111_clean_current_native_source_context.json')

def append(command):
    with JOURNAL.open('a',encoding='utf-8') as f:f.write(json.dumps(command)+'\n')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--frame',type=int,required=True)
    p.add_argument('--limit',type=int,default=150)
    args=p.parse_args()
    packet=read(PACKET)
    by_offset={r['current_reference']['header_offset']:r for r in packet['records']}
    commands={r['offset']:r for r in packet['all_current_native_commands']}
    assert not any(r['word']==0x2100 for r in commands.values())
    live=ROOT/'original_presentation_observations_LIVE.json'
    if ROOT.exists():
        state=read(live)
        assert state['next_pause_frame']==args.frame
        holds,art=state['rows'],state['art_pauses']
    else:
        ROOT.mkdir(parents=True)
        holds,art=[],[]
    frame=args.frame
    for step in range(args.limit):
        raw,im,progress,photo=snapshot(frame)
        pending=[progress['rows'][i] for i in progress['pending'].values()]
        active=[r for r in pending if r['source'].get('route')==2 and r['source'].get('block')==26]
        if not active:
            ends=[r for r in progress['rows'] if r['kind']=='after_command' and r['source'].get('route')==2
                and r['source'].get('block')==26 and r['source']['first_word']==0]
            assert holds and ends,('no active B26 or terminal;left paused',frame,pending)
            save(ROOT/'closed_original_B26_context.json',dict(candidate=packet['candidate'],candidate_sha256=packet['candidate_sha256'],
                terminal_frame_requested=frame,old_text_observations=holds,source2000_interstitials=art,
                original_B26_end=ends[-1],observed_speaker_prefixes=sorted({r['prefix_hex'] for r in holds}),
                unique_observed_record_IDs=sorted({r['id'] for r in holds}),
                terminal_capture=str(photo),terminal_capture_sha256=sha(photo.read_bytes()),
                no_revised_text_font_or_all_conditional_branch_approval=True,full_goal_complete=False))
            append({'stop':True})
            print(dict(original_B26_context_closed=True,observations=len(holds),unique_speeches=len({r['id'] for r in holds}),frame=frame),flush=True)
            break
        assert len(active)==1
        src=active[0]['source']
        assert src['whole_resident_payload_exact_ROM'] and src['actual_sha256']==packet['current_block_sha256']
        at=src['payload_address']-0x02000000
        assert sha(raw[at:at+src['payload_bytes']])==packet['current_block_sha256']
        assert src['first_word'] in (0x2000,0x4000),('unclassified pending command;leftpaused',src)
        group=[]
        for h in range(2):
            raw,im,progress,photo=snapshot(frame)
            assert any(progress['rows'][i]['source']==src for i in progress['pending'].values())
            group.append(dict(frame=frame,capture=str(photo),capture_sha256=sha(photo.read_bytes()),RAM_sha256=sha(raw)))
            if h==0:
                append(dict(until=frame+30,duration=1))
                frame+=30
        if src['first_word']==0x2000:
            native=commands[src['instruction_offset']]
            assert native['whole_command_hex']=='0020'
            art.append(dict(source=src,native_command=native,holds=group,original_art_pause_not_padding_generated_blank=True))
        else:
            row=by_offset[src['instruction_offset']]
            holds.append(dict(id=row['id'],prefix_hex=row['source_presentation_prefix_hex'],source=src,
                speaker_from_source_context=row['speaker'],holds=group,old_prose_not_revised_display_approval=True,
                repeated_instruction_possible_original_pagination=sum(r['id']==row['id'] for r in holds)))
            print(dict(old_scene_observations=len(holds),id=row['id'],prefix=row['source_presentation_prefix_hex'],frame=frame),flush=True)
        append(dict(until=frame+300,buttons=['A'],duration=8))
        frame+=300
        save(live,dict(rows=holds,art_pauses=art,next_pause_frame=frame,not_terminal_or_revised_prose_approval=True))
    else:
        print(dict(bounded_segment_complete=True,observations=len(holds),next_pause_frame=frame,original_process_left_live=True),flush=True)
