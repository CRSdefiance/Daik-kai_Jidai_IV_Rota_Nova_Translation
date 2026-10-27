"""Terminal ordinary current/revised Maria opening with existing system unlock."""
from pathlib import Path
import json
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_opening_actual_v2044')
PLAN=Path('work/analysis/maria_opening_relocation_v2040/complete_B33_CS0101_typed_relocation_research.json')
FONT=Path('work/analysis/maria_opening_fonts_v2037c/all38_progressive_native_macros_and_complete_font_planes.json')
CAPBASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
    assert not ROOT.exists()
    plan,font=map(read,(PLAN,FONT));versions=[];all_photos={};dependencies={}
    for label,stem,capname,romkey in(
        ('current','maria_opening_context_v2035','maria_opening_context_v2035_V2030','parent'),
        ('research','maria_opening_revised_v2042','maria_opening_revised_v2042_RESEARCH','research_ROM')):
        run=Path('work/analysis')/stem;cap=CAPBASE/capname
        terminal,runplan,report,trace,journal=map(read,(run/'terminal.json',run/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json',cap/'navigation_command_journal.json'))
        image=NdsImage.open(plan[romkey]);blocks=IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks
        assert terminal['terminal']and terminal['observer_host_slots_restored']and terminal['frame']==report['frames']>=31000
        assert sha(Path(plan[romkey]).read_bytes())==plan[romkey+'_sha256']==report['ROM_sha256']==runplan['candidate_sha256']
        assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
        assert all(k=='synthetic_gallery_fixtures'or not v for k,v in report.items()if k.startswith('synthetic_'))
        fixture=read(runplan['fixture_manifest']);assert sha(Path(runplan['fixture_manifest']).read_bytes())==runplan['fixture_manifest_sha256']
        assert fixture['only_system_low_four_bits_and_original_checksum_changed']and fixture['all_six_route_save_slots_and_footer_unchanged']
        assert fixture['earned_unlock_verified']is False and fixture['production_ROM_sha256']==report['ROM_sha256']
        assert len(report['synthetic_gallery_fixtures'])==1 and report['synthetic_gallery_fixtures'][0]['manifest_sha256']==runplan['fixture_manifest_sha256']
        battery=report['battery_save_preloaded'];assert battery['copied_byte_exact_before_cold_boot']and not battery['savestate_loaded']
        assert sha(Path(runplan['existing_isolated_system_unlock_save']).read_bytes())==runplan['save_sha256']==fixture['fixture_save_sha256']
        assert not trace['errors']and not trace['mismatches']and not trace['unreturned_at_capture_end']and trace['all_host_slots_restored_and_core_file_exact']
        commands=[json.loads(s)for s in(run/'navigation.jsonl').read_text().splitlines()if s.strip()]
        assert commands==[r['command']for r in journal['commands_received']]and commands[-1]=={'stop':True}
        schedule=list(read(runplan['inputs']));assert sha(Path(runplan['inputs']).read_bytes())==runplan['inputs_sha256']
        for r in journal['commands_received']:
            assert r['validation_passed'];c=r['command']
            if c.get('buttons')or c.get('touch')is not None:
                event=dict(start=r['frame']+1,duration=c['duration'],buttons=c.get('buttons',[]))
                if c.get('touch')is not None:event['touch']=c['touch']
                schedule.append(event)
        assert schedule==report['scripted_input_schedule']
        photos={}
        for r in report['frames_captured']:
            p=Path(r['path']);assert sha(p.read_bytes())==r['PNG_sha256'];im=Image.open(p).convert('RGB');assert im.size==(256,384)
            if r['frame']in photos:assert photos[r['frame']][1].tobytes()==im.tobytes()
            photos[r['frame']]=(r,im)
        for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
            raw=Path(r['path']).read_bytes();assert len(raw)==r['bytes']==4194304 and sha(raw)==r['sha256']and r['read_only_export']
        pairs=[];intervals=[];rows=trace['rows'];textmap={r['new_command_offset']if label=='research'else r['old_command_offset']:r for r in plan['text_records']}
        for r in rows:
            assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=r['source']
            assert s['classification']=='original_SC_cache'and s['route']==3 and s['whole_resident_payload_exact_ROM']and s['actual_sha256']==sha(blocks[s['block']])
            if r['kind']!='after_command':continue
            b=rows[r['entry_row']];s=b['source'];at=s['instruction_offset'];word=int.from_bytes(blocks[s['block']][at:at+2],'little')
            pair=dict(block=s['block'],offset=at,word=word,start=b['frame'],returned=r['frame'],extent=r['decoded_length'],result_words=r['result_words']);pairs.append(pair)
            if s['block']==33 and word==0x4000:intervals.append(dict(**pair,id=textmap[at]['id'],prefix=blocks[33][at+5]))
        b33=[r for r in pairs if r['block']==33];assert len(b33)==85 and b33[-1]['word']==0 and b33[-1]['result_words']==[0,0]
        assert len(intervals)==len({r['id']for r in intervals})==38
        assert{r['id']for r in intervals}=={r['id']for r in plan['text_records']}
        cmap={r['new_offset']if label=='research'else r['old_offset']:r for r in plan['mapped_native_commands']}
        for row in b33:
            command=cmap[row['offset']];assert row['extent']==command['new_native_extent'if label=='research'else'old_native_extent']
        versions.append(dict(label=label,ROM_sha256=plan[romkey+'_sha256'],terminal_frame=report['frames'],capture_report=str(cap/'capture_report.json'),
            observer_report=str(cap/'observer/commands.json'),all_original_commands=pairs,opening_speech_intervals=intervals,
            all38_opening_speeches85_commands_and_normal_exit_verified=True,existing_system_unlock_not_earned=True,
            other_observed_blocks_unreviewed_no_editorial_credit=sorted(set(r['block']for r in pairs)-{33})))
        all_photos[label]=photos
        for p in(run/'terminal.json',run/'run_plan.json',run/'navigation.jsonl',cap/'capture_report.json',cap/'observer/commands.json',cap/'navigation_command_journal.json',Path(runplan['fixture_manifest'])):
            dependencies[str(p)]=sha(p.read_bytes())
    assert read(Path('work/analysis/maria_opening_context_v2035')/'run_plan.json')['inputs_sha256']==read(Path('work/analysis/maria_opening_revised_v2042')/'run_plan.json')['inputs_sha256']
    proofs={r['id']:r for r in font['cases']};actual=[];unmatched=[]
    for interval in versions[1]['opening_speech_intervals']:
        proof=proofs[interval['id']];p=Path(proof['preview']);assert sha(p.read_bytes())==proof['preview_sha256'];im=Image.open(p).convert('RGB')
        pixels=bytes(int(im.getpixel((x,y))==(0,8,0))for y in range(64)for x in range(216));assert sha(pixels)==proof['native_font_plane_sha256']
        expected={(x,y)for y in range(64)for x in range(216)if pixels[y*216+x]};holds=[]
        for frame,(photo,im)in all_photos['research'].items():
            if not interval['start']<frame<interval['returned']:continue
            ink={(x,y)for y in range(64)for x in range(216)if im.getpixel((16+x,296+y))==(0,8,0)}
            if ink!=expected:unmatched.append(dict(id=interval['id'],frame=frame,missing=len(expected-ink),extra=len(ink-expected)));continue
            holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],complete_native_independent_actual_ink_equal=True));dependencies[photo['path']]=photo['PNG_sha256']
        actual.append(dict(id=interval['id'],prefix=interval['prefix'],holds=holds))
    matched=[r for r in actual if r['holds']];assert{r['prefix']for r in matched}=={3,10,11,12,21,74}and len(matched)>=35,(len(matched),unmatched)
    ROOT.mkdir(parents=True);sheets=[];pictures=[(r,r['holds'][0])for r in matched]
    for start in range(0,len(pictures),6):
        sheet=Image.new('RGB',(780,690),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(r,hold)in enumerate(pictures[start:start+6]):
            x,y=390*(i%2),230*(i//2);im=Image.open(hold['capture']).convert('RGB');draw.text((x+4,y+3),r['id']+' / '+str(hold['frame']),fill='white')
            sheet.paste(im.crop((0,260,256,384)).resize((384,186)),(x+3,y+25))
        p=ROOT/f'actual_opening_sheet_{start//6+1:02d}.png';sheet.save(p);sheets.append(str(p))
    p=ROOT/'revised_normal_Hangzhou_return.png';all_photos['research'][31000][1].save(p);sheets.append(str(p))
    save(ROOT/'ordinary_current_revised_opening_and_full_actual_planes.json',dict(research_ROM=plan['research_ROM'],research_ROM_sha256=plan['research_ROM_sha256'],
        versions=versions,plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),observed_speech_panels=actual,
        complete_matching_speech_panels=len(matched),complete_matching_speech_holds=sum(len(r['holds'])for r in matched),unmatched_capture_planes_no_full_pixel_claim=unmatched,
        actual_all_six_presentation_states_and_complete_native_planes_match=True,all38_speeches85_commands_and_normal_Hangzhou_return=True,
        existing_isolated_system_unlock_save_not_earned_and_no_savestate_story_location_RNG_funds_outcome_fixture=True,
        original_current_following_town_facilities_unreviewed_context_no_new_editorial_credit=True,
        all_inputs_captures_RAM_hashes_callbacks_host_restoration_and_fixture_scope_verified=True,
        representative_contact_sheets=sheets,visual_review_pending=True,evidence=dependencies,
        registration_and_clean_patch_pending=True,not_full_route_or_hardware_proof=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(actual_speeches=38,matching_panels=len(matched),holds=sum(len(r['holds'])for r in matched),unmatched=unmatched))
