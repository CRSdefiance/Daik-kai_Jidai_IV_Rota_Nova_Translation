"""Bounded actual scene/control/return and final-state comparisons, without replay or retiming."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_comparison_v8410')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);groups=[];sheets=[];evidence={str(Path(__file__)):sha(Path(__file__).read_bytes())}
    for number in [49]:
        path=Path(f'work/analysis/Hodram_B49_actual_v8409/B{number}/paired_actual_dialogue_headers_flow_returns.json');proof=read(path)
        assert not proof['unresolved'] and proof['all_observed_complete_body_name_holds_andnative_flow_pass'];evidence[str(path)]=sha(path.read_bytes())
        old,new=proof['groups'];assert old['version']=='clean_Japanese' and new['version']=='revised_English'
        assert all(g['normal_return'] for g in [old,new])
        assert old['unvisited_conditional_text_IDs']==new['unvisited_conditional_text_IDs'] and len(old['unvisited_conditional_text_IDs'])==8
        assert len(old['speeches'])==len(new['speeches'])==6
        reports=[read(g['capture_report']) for g in [old,new]];assert reports[0]['scripted_input_schedule']==reports[1]['scripted_input_schedule']
        photos=[{p['frame']:p for p in r['frames_captured']} for r in reports];cache={}
        def picture(version,frame):
            key=version,frame
            if key not in cache:
                p=photos[version][frame];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];cache[key]=Image.open(p['path']).convert('RGB')
            return cache[key]
        commanddiff=[];durationdiff=[];UIchanges=[]
        for a,b in zip(old['command_pairs'],new['command_pairs'],strict=True):
            assert (a['source_command_ordinal'],a['word'],a['native_result'])==(b['source_command_ordinal'],b['word'],b['native_result'])
            fields={k:dict(clean=a[k],revised=b[k]) for k in ['start','returned','decoded_length','before_RNG','after_RNG','UI_before','UI_after'] if a[k]!=b[k]}
            if fields:commanddiff.append(dict(source_command_ordinal=a['source_command_ordinal'],canonical_source_offset=a['canonical_source_offset'],word=a['word'],different_fields=fields))
            if a['duration']!=b['duration']:durationdiff.append(dict(source_command_ordinal=a['source_command_ordinal'],word=a['word'],clean=a['duration'],revised=b['duration']))
            if a['UI_before']!=b['UI_before'] or a['UI_after']!=b['UI_after']:UIchanges.append(dict(source_command_ordinal=a['source_command_ordinal'],word=a['word'],clean=[a['UI_before'],a['UI_after']],revised=[b['UI_before'],b['UI_after']]))
        scenes=[];unpaired=[]
        for a,b in zip(old['speeches'],new['speeches'],strict=True):
            assert (a['id'],a['source_selector'])==(b['id'],b['source_selector'])
            common=sorted({p['frame'] for p in a['complete_holds']}&{p['frame'] for p in b['complete_holds']})
            if not common:unpaired.append(a['id']);continue
            f=common[-1];ia,ib=picture(0,f),picture(1,f)
            scenes.append(dict(id=a['id'],frame=f,clean=photos[0][f],revised=photos[1][f],
                upper_scene_portrait_RGB_equal=ia.crop((0,0,256,272)).tobytes()==ib.crop((0,0,256,272)).tobytes(),
                complete_header_region_RGB_equal=ia.crop((0,272,256,296)).tobytes()==ib.crop((0,272,256,296)).tobytes()))
        native=[]
        for group,report in zip([old,new],reports,strict=True):
            snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
            arm=NdsImage.open(group['fixture']['research_ROM']).read_file('/__arm9__.bin');assert sha(arm)=='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'
            cpu,get=get_machine(arm,raw);actor=get(0xCB184);captain=get(0x7F244)
            components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]};components['tasks']=dict(bytes=len(components['tasks']),sha256=sha(components['tasks']))
            native.append(dict(version=group['version'],snapshot=snap,captain_ID=captain,components=components,
                whole_actor_sha256=sha(bytes(cpu.mem_read(actor,0x1A04))),PRNG_seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little'),
                disposable_CPU_queries_only_not_emulator_mutation=True))
        equality={k:native[0]['components'][k]==native[1]['components'][k] for k in native[0]['components']}
        threshold=max(g['normal_return']['frame'] for g in [old,new])+60
        late=[];frames=sorted(f for f in photos[0] if f>threshold and f in photos[1]);assert frames
        for f in frames:
            ia,ib=picture(0,f),picture(1,f);delta=ImageChops.difference(ia,ib)
            late.append(dict(frame=f,clean=photos[0][f],revised=photos[1][f],whole_RGB_equal=ia.tobytes()==ib.tobytes(),changed_RGB_bbox=delta.getbbox()))
        chosen=[frames[0],frames[len(frames)//2],frames[-1]];resource=None
        if number==49:
            display=[next(c for c in g['command_pairs'] if c['word']==0x4820) for g in [old,new]]
            hide=[next(c for c in g['command_pairs'] if c['word']==0x4700) for g in [old,new]]
            for g,c in zip([old,new],display,strict=True):
                command=next(v for v in g['fixture']['all_original_exchange_commands'] if v['fixture_command_offset']==c['fixture_offset'])
                assert command['whole_command_hex']=='204894a8' and command['canonical_clean_offset']==32
            common=sorted(f for f in photos[0] if f in photos[1] and max(c['returned'] for c in display)+30<f<min(c['start'] for c in hide)-4)
            before=sorted(f for f in photos[0] if f in photos[1] and f<min(c['start'] for c in display))
            after=sorted(f for f in photos[0] if f in photos[1] and f>max(c['returned'] for c in hide)+30)
            assert common and before and after
            resource=dict(original_4820_calls=display,original_4700_calls=hide,common_display_sample_frames=common,
                descriptor=[0,148,1,5],layout=[2,0,0],original_Ullr_Bow_item148_source_4820_layout2=True,
                selected_before_display_frame=before[-1],selected_item_display_frame=common[-1],selected_after_hide_frame=after[0],
                actual_full_original_resource_andhide_command_executions=True,
                descriptor_layout_from_exact_original_operand_and8384_native_consumer_not_dialogue_UI_request_words=True,
                visual_item_card_andhide_review_pending=True)
            chosen=[before[-1],common[-1],after[0]]
        sheet=Image.new('RGB',(1536,410),'#263238');draw=ImageDraw.Draw(sheet)
        for i,f in enumerate(chosen):
            for j,label in enumerate(['Japanese','English']):
                x=(i*2+j)*256;draw.text((x+3,3),label+f' B{number} frame{f}',fill='white');sheet.paste(picture(j,f),(x,24))
        sp=ROOT/f'B{number}_full_scene_transition_pairs.png';sheet.save(sp);sheets.append(dict(path=str(sp),sha256=sha(sp.read_bytes())))
        groups.append(dict(block=number,scene_pairs=scenes,no_common_complete_hold=unpaired,command_comparison_differences=commanddiff,duration_differences=durationdiff,
            UI_request_differences=UIchanges,normal_returns=[g['normal_return'] for g in [old,new]],final_native_values=native,five_native_component_equality=equality,
            whole_actors_equal=native[0]['whole_actor_sha256']==native[1]['whole_actor_sha256'],final_PRNG_seeds=[v['PRNG_seed'] for v in native],
            raw_calendars_uninterpreted=[v['components']['calendar'] for v in native],later_RGB_comparisons=late,
            later_RGB_difference_count=sum(not r['whole_RGB_equal'] for r in late),original4820_4700_actual=resource,unvisited_conditional_text_IDs=old['unvisited_conditional_text_IDs'],
            following_commands=[g['following_original_cache_commands'] for g in [old,new]],following_commands_equal=old['following_original_cache_commands']==new['following_original_cache_commands']))
        print('B',number,'commanddiff',len(commanddiff),'durationdiff',len(durationdiff),'UIchanges',len(UIchanges),'components',equality,'actors',groups[-1]['whole_actors_equal'],'captains',[n['captain_ID'] for n in native],'laterRGBdiff',groups[-1]['later_RGB_difference_count'],'of',len(late),flush=True)
    save(ROOT/'paired_selected_path_comparison.json',dict(groups=groups,review_sheets=sheets,visual_review_pending=True,
        total_actual_frames=20002,all_measured_differences_retained_no_input_state_seed_orresult_forcing=True,
        initialized_original_Hodram_opening_not_optional_event_activation_original_location_orall_attainable_paths=True,
        no_every_frame_causality_future_outcome_broad_simulation_fullroute_orhardware_claim=True,
        current_registered_V8377_andmainV4701_unchanged=True,new_credit=0,full_goal_complete=False,evidence=evidence))
