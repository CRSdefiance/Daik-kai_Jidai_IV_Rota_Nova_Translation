"""Terminal ordinary current/revised opening; complete glyph planes and scope."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hodram_opening_actual_v2027')
PLAN=Path('work/analysis/hodram_opening_relocation_v2023/complete_three_block_typed_relocation_research.json')
FONT=Path('work/analysis/hodram_opening_fonts_v2021/all67_progressive_native_macros_and_complete_font_planes.json')
FE=Path('work/analysis/hodram_opening_FE_v2022/all6_separate_FE_native_planes_and48_macro_calls.json')
CAPBASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,font,fe=map(read,(PLAN,FONT,FE));versions=[];all_photos={};dependencies={}
    for label,stem,capname,romkey,endframe in(
        ('current','hodram_opening_context_v2018','hodram_opening_context_v2018_V2013','parent',30140),
        ('research','hodram_opening_revised_v2025','hodram_opening_revised_v2025_RESEARCH','research_ROM',20420)):
        run=Path('work/analysis')/stem;cap=CAPBASE/capname
        terminal,runplan,report,trace,journal=map(read,(run/'terminal.json',run/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json',cap/'navigation_command_journal.json'))
        image=NdsImage.open(plan[romkey]);blocks=IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
        assert terminal['terminal']and terminal['observer_host_slots_restored']and terminal['frame']==report['frames']==endframe
        assert sha(Path(plan[romkey]).read_bytes())==plan[romkey+'_sha256']==report['ROM_sha256']==runplan['candidate_sha256']
        assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
        assert not any(v for k,v in report.items()if k.startswith('synthetic_'))and 'battery_save_preloaded'not in report
        assert not trace['errors']and not trace['mismatches']and not trace['unreturned_at_capture_end']
        assert trace['all_host_slots_restored_and_core_file_exact']
        commands=[json.loads(s)for s in(run/'navigation.jsonl').read_text().splitlines()if s.strip()]
        assert commands==[r['command']for r in journal['commands_received']]and commands[-1]=={'stop':True}
        schedule=list(read(runplan['inputs']));assert sha(Path(runplan['inputs']).read_bytes())==runplan['inputs_sha256']
        for r in journal['commands_received']:
            assert r['validation_passed'];c=r['command']
            if c.get('buttons'):schedule.append(dict(start=r['frame']+1,duration=c['duration'],buttons=c['buttons']))
        assert schedule==report['scripted_input_schedule']
        photos={}
        for r in report['frames_captured']:
            p=Path(r['path']);assert sha(p.read_bytes())==r['PNG_sha256'];im=Image.open(p).convert('RGB');assert im.size==(256,384)
            if r['frame']in photos:assert photos[r['frame']][1].tobytes()==im.tobytes()
            photos[r['frame']]=(r,im)
        for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
            raw=Path(r['path']).read_bytes();assert len(raw)==r['bytes']==4194304 and sha(raw)==r['sha256']and r['read_only_export']
        pairs=[];speech_intervals=[];rows=trace['rows']
        textmap={r['new_command_offset']if label=='research'else r['old_command_offset']:r for r in plan['blocks'][0]['text_records']}
        for r in rows:
            assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=r['source']
            assert s['classification']=='original_SC_cache'and s['route']==1 and s['whole_resident_payload_exact_ROM']
            assert s['actual_sha256']==sha(blocks[s['block']])
            if r['kind']!='after_command':continue
            b=rows[r['entry_row']];s=b['source'];at=s['instruction_offset'];word=int.from_bytes(blocks[s['block']][at:at+2],'little')
            pair=dict(block=s['block'],offset=at,word=word,start=b['frame'],returned=r['frame'],extent=r['decoded_length'],result_words=r['result_words'])
            pairs.append(pair)
            if s['block']==42 and word==0x4000:speech_intervals.append(dict(**pair,id=textmap[at]['id'],prefix=blocks[42][at+5]))
        b42=[r for r in pairs if r['block']==42];assert len(b42)==93 and b42[-1]['word']==0 and b42[-1]['result_words']==[0,0]
        assert len(speech_intervals)==len({r['id']for r in speech_intervals})==37
        assert {r['id']for r in speech_intervals}=={r['id']for r in plan['blocks'][0]['text_records']}
        if label=='research':assert set(r['block']for r in pairs)=={42}
        else:assert set(r['block']for r in pairs)=={42,127,135}
        versions.append(dict(label=label,ROM_sha256=plan[romkey+'_sha256'],terminal_frame=endframe,
            capture_report=str(cap/'capture_report.json'),observer_report=str(cap/'observer/commands.json'),
            all_original_commands=pairs,opening_speech_intervals=speech_intervals,
            all37_opening_speeches93_commands_and_normal_exit_verified=True,
            other_observed_blocks_unreviewed_no_editorial_completion_credit=sorted(set(r['block']for r in pairs)-{42})))
        all_photos[label]=photos
        for p in(run/'terminal.json',run/'run_plan.json',run/'navigation.jsonl',cap/'capture_report.json',cap/'observer/commands.json',cap/'navigation_command_journal.json'):
            dependencies[str(p)]=sha(p.read_bytes())
    proofs={r['id']:r for r in font['cases']};proofs.update({r['id']:r for r in fe['cases']})
    actual=[];unmatched=[]
    for interval in versions[1]['opening_speech_intervals']:
        proof=proofs[interval['id']];modal=interval['prefix']==254
        if modal:
            path=Path(proof['physical_mask']);pixels=path.read_bytes();assert sha(pixels)==proof['physical_mask_sha256'];width=228
        else:
            path=Path(proof['native_plane']);pixels=path.read_bytes();assert sha(pixels)==proof['native_plane_sha256'];width=216
        expected={(x,y)for y in range(64)for x in range(width)if pixels[y*width+x]}
        holds=[]
        for frame,(photo,im)in all_photos['research'].items():
            if not interval['start']<frame<interval['returned']:continue
            ink={(x,y)for y in range(64)for x in range(width)if im.getpixel((16+x,296+y))==(0,8,0)}
            if ink!=expected:
                unmatched.append(dict(id=interval['id'],frame=frame,missing=len(expected-ink),extra=len(ink-expected)));continue
            holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],
                complete_native_independent_actual_ink_equal=True))
            dependencies[photo['path']]=photo['PNG_sha256']
        actual.append(dict(id=interval['id'],prefix=interval['prefix'],consumer='FE_mode1_228x48'if modal else'progressive_216x64',holds=holds))
    matched=[r for r in actual if r['holds']]
    assert {r['prefix']for r in matched}=={1,16,18,23,254}
    assert len(matched)>=30,(len(matched),unmatched)
    ROOT.mkdir(parents=True);sheets=[]
    pictures=[(r,r['holds'][0])for r in matched]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(780,690),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(r,hold)in enumerate(pictures[start:start+6]):
            x,y=390*(i%2),230*(i//2);im=Image.open(hold['capture']).convert('RGB')
            draw.text((x+4,y+3),r['id']+' / '+str(hold['frame']),fill='white')
            sheet.paste(im.crop((0,260,256,384)).resize((384,186)),(x+3,y+25))
        p=ROOT/f'actual_opening_sheet_{start//6+1:02d}.png';sheet.save(p);sheets.append(str(p))
    # Preserve two complete town/sailing endpoint views with scope explicit.
    for label,frame in(('research',20420),('current',30140)):
        photo,im=all_photos[label][frame];p=ROOT/(label+'_normal_endpoint.png');im.save(p);sheets.append(str(p))
    save(ROOT/'ordinary_current_revised_opening_and_full_actual_planes.json',dict(
        research_ROM=plan['research_ROM'],research_ROM_sha256=plan['research_ROM_sha256'],versions=versions,
        plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),observed_speech_panels=actual,
        complete_matching_speech_panels=len(matched),complete_matching_speech_holds=sum(len(r['holds'])for r in matched),
        unmatched_capture_planes_no_full_pixel_claim=unmatched,
        actual_Hodram_Gerhard_Charles_Manuel_and_FE_complete_native_planes_match=True,
        all37_opening_speeches93_commands_and_town_return=True,
        source_bound_B43_B44_offline_only_not_actual_visits=True,
        current_B135_port_and_B127_sailing_context_unreviewed_no_completion_credit=True,
        no_save_savestate_location_RNG_funds_crew_outcome_or_event_fixture=True,
        all_inputs_captures_RAM_hashes_callbacks_and_host_restoration_verified=True,
        representative_contact_sheets=sheets,visual_review_pending=True,evidence=dependencies,
        registration_and_clean_patch_pending=True,not_full_route_or_hardware_proof=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(actual_speeches=37,native_matching_panels=len(matched),holds=sum(len(r['holds'])for r in matched),unmatched=unmatched))
