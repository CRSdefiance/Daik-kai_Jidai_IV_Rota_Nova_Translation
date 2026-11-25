"""Observe original B27 presentation controls;old English,not revised-font approval."""
import argparse
import json
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from scripts import navigate_lil_crew_v1759b as prior
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Stockholm_context_navigation_v1854b')
RUN=Path('work/analysis/lil_Stockholm_context_run_v1851')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_Stockholm_context_run_v1851_RESEARCH_ONLY')
JOURNAL=RUN/'navigation.jsonl'
snapshot=FunctionType(prior.snapshot.__code__,{**prior.__dict__,'RUN':RUN,'CAP':CAP})

def append(command):
    with JOURNAL.open('a',encoding='utf-8')as f:f.write(json.dumps(command)+'\n')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--frame',type=int,required=True);args=parser.parse_args()
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    packet=read('work/analysis/lil_Stockholm_source_v1848b/all51_clean_current_native_source_context.json')
    by_offset={r['current_reference']['header_offset']:r for r in packet['records']}
    assert not any(r['word']==0x2100 for r in packet['all_current_native_commands'])
    frame=args.frame;holds=read('work/analysis/lil_Stockholm_context_navigation_v1854/original_presentation_observations_LIVE.json')['rows'];interstitials=[]
    assert len(holds)==1 and holds[0]['id']=='DK4_MES_B27_R0005'
    for step in range(80):
        raw,im,progress,photo=snapshot(frame)
        pending=[progress['rows'][i]for i in progress['pending'].values()]
        active=[r for r in pending if r['source'].get('route')==2 and r['source'].get('block')==27]
        if not active:
            ends=[r for r in progress['rows']if r['kind']=='after_command'and r['source'].get('route')==2
                  and r['source'].get('block')==27 and r['source']['first_word']==0]
            assert holds and ends,('B27 not active and no original terminal;leftpaused',frame)
            save(ROOT/'closed_original_B27_context.json',{'candidate':packet['candidate'],'candidate_sha256':packet['candidate_sha256'],
                'terminal_frame_requested':frame,'old_text_observations':holds,'source2000_interstitials':interstitials,'original_B27_end':ends[-1],
                'observed_speaker_prefixes':sorted({r['prefix_hex']for r in holds}),
                'terminal_capture':str(photo),'terminal_capture_sha256':sha(photo.read_bytes()),
                'not_revised_text_font_or_branch_coverage_approval':True,'full_goal_complete':False})
            append({'stop':True});print({'original_B27_context_closed':True,'observations':len(holds),'frame':frame},flush=True);break
        assert len(active)==1;src=active[0]['source']
        if src['first_word']==0x2000:
            native=next(r for r in packet['all_current_native_commands']if r['offset']==src['instruction_offset'])
            assert native['whole_command_hex']=='0020'and native['native_extent']==2
            assert src['whole_resident_payload_exact_ROM']and src['actual_sha256']==packet['current_block_sha256']
            group=[]
            for h in range(2):
                raw,im,progress,photo=snapshot(frame)
                assert any(progress['rows'][i]['source']==src for i in progress['pending'].values())
                group.append({'frame':frame,'capture':str(photo),'capture_sha256':sha(photo.read_bytes()),'RAM_sha256':sha(raw)})
                if h==0:append({'until':frame+30,'duration':1});frame+=30
            interstitials.append({'source':src,'native_command':native,'holds':group,
                'original_art_pause_not_missing_English_or_padding_generated_blank':True})
            save(ROOT/'original2000_art_pause_observations.json',interstitials)
            append({'until':frame+300,'buttons':['A'],'duration':8});frame+=300;continue
        assert src['first_word']==0x4000
        row=by_offset[src['instruction_offset']]
        assert src['whole_resident_payload_exact_ROM']and src['actual_sha256']==packet['current_block_sha256']
        at=src['payload_address']-0x02000000
        assert sha(raw[at:at+src['payload_bytes']])==packet['current_block_sha256']
        group=[]
        for hold in range(2):
            raw,im,progress,photo=snapshot(frame)
            assert any(progress['rows'][i]['source']==src for i in progress['pending'].values())
            group.append({'frame':frame,'capture':str(photo),'capture_sha256':sha(photo.read_bytes()),'RAM_sha256':sha(raw)})
            if hold==0:append({'until':frame+30,'duration':1});frame+=30
        holds.append({'id':row['id'],'prefix_hex':row['source_presentation_prefix_hex'],
            'source':src,'speaker_from_original_actor_catalog':row['speaker'],'holds':group,
            'old_prose_not_revised_display_approval':True})
        save(ROOT/'original_presentation_observations_LIVE.json',{'rows':holds,'not_terminal_or_revised_prose_approval':True})
        print({'old_scene_observations':len(holds),'id':row['id'],'prefix':row['source_presentation_prefix_hex'],
               'frame':frame},flush=True)
        append({'until':frame+300,'buttons':['A'],'duration':8});frame+=300
    else:raise AssertionError('Bounded context observation exhausted;gameleftpaused')
