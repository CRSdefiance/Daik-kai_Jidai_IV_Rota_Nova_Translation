"""Actual conditional source/English speech pages, complete headers and original normal returns."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.maria_existing_unlock_contract_v7680 import validate_capture
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_actual_v7752')
FIXTURES=Path('work/analysis/maria_story_scene_fixtures_v7749/six_complete_source_English_original_prelude_fixtures.json')
RUNS=Path('work/analysis/maria_story_scene_runs_v7750')
FONT=Path('work/analysis/maria_story_source_name_planes_v7751/67_clean_source_native_pages8_complete_name_planes32_literal_alignments.json')
STORED=Path('work/analysis/maria_story_stored_v7743/67_final_stored_targets268_alignments33_zero_ink_tails68_pages.json')
CURRENT=Path('work/analysis/maria_story_current_v7728/all67_complete_source_current_refs_before_new_English_manuscript.json')
def masks(image):
    pixels=list(image.crop((16,296,232,360)).getdata())
    return {color:{(i%216,i//216) for i,v in enumerate(pixels) if v==color} for color in [(0,8,0),(98,97,98),(197,198,197)]}
if __name__=='__main__':
    assert not ROOT.exists();fixtures,font,stored,current=map(read,[FIXTURES,FONT,STORED,CURRENT]);terminals=[]
    for fixture in fixtures['fixtures']:
        folder=RUNS/f'route3_B{fixture["source_block"]}_{fixture["version"]}';terminal=read(folder/'terminal.json')
        assert terminal['terminal'] and terminal['frames']==16001 and terminal['all_callbacks_readonly_andhost_slots_restored'];terminals.append((fixture,folder,terminal))
    ROOT.mkdir(parents=True);groups=[];unresolved=[]
    for fixture,folder,terminal in terminals:
        blocknumber,version=fixture['source_block'],fixture['version'];rp,tp=Path(terminal['report']),Path(terminal['observer'])
        report,trace,plan=map(read,[rp,tp,folder/'run_plan.json']);validate_capture(report)
        assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(tp.read_bytes())==terminal['observer_sha256']
        assert report['frames']==16001 and not report['hardware_device_verification'] and not report['goal_complete']
        assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
        assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
        assert report['scripted_input_schedule']==read(plan['inputs']) and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
        image=NdsImage.open(fixture['research_ROM']);arm,nativefont=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
        banks={r:IlnkContainer.parse(image.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)}
        records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
        objects={r['fixture_command_offset']:(i,r) for i,r in enumerate(fixture['all_original_exchange_commands'])}
        expected={c['offset']:c for c in fixture['all_fixture_commands']};sourcegroup=next(g for g in current['groups'] if g['block']==blocknumber)
        photos={}
        for photo in report['frames_captured']:
            assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'];im=Image.open(photo['path']).convert('RGB');assert im.size==(256,384)
            photos[photo['frame']]=dict(reference=photo,image=im,masks=masks(im))
        pairs=[];speeches=[];following=[];unknown=[];finished=False;lastnext=None;panels=[]
        for ri,row in enumerate(trace['rows']):
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source']
            if s['classification']!='original_SC_cache':unknown.append(dict(row=ri,frame=row['frame'],source=s));continue
            assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==s['registered_sha256']==sha(banks[s['route']][s['block']])
            if row['kind']!='after_command':continue
            if finished or (s['route'],s['block'])!=(3,fixture['fixture_block']):
                following.append(dict(frame=row['frame'],route=s['route'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']));continue
            entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];command=expected[at];word=command['word']
            assert s['instruction_offset']==at and word==s['first_word']
            if lastnext is not None:assert at==lastnext
            if word in [0x100,0x200,0x300,0x400]:
                span=int.from_bytes(bytes.fromhex(command['whole_command_hex'])[2:4],'little');previous=entry['mode']
                taken=word==0x100 or word==0x200 and previous==0 or word==0x300 and previous==1 or word==0x400 and previous==2
                assert row['decoded_length']==4+(span if taken else 0)
            else:assert row['decoded_length']==command['native_extent']
            lastnext=at+row['decoded_length'];ordinal,original=objects.get(at,(None,None))
            pair=dict(fixture_offset=at,exchange_command_ordinal=ordinal,canonical_source_offset=None if ordinal is None else sourcegroup['all_source_commands'][ordinal]['offset'],
                word=word,start=entry['frame'],returned=row['frame'],decoded_length=row['decoded_length'],observed_previous_result=entry['mode'],native_result=row['result_words'],
                before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words'])
            pairs.append(pair)
            if word==0:
                assert row['result_words']==[0,0];finished=True
            if at not in records:continue
            record=records[at];actor=record['source_selector'];np=next(n for n in font['name_planes'] if n['actor_ID']==actor)
            nameplane=Path(np['native_plane']).read_bytes();assert sha(nameplane)==np['native_plane_sha256']
            nameink={(i%216,i//216) for i,b in enumerate(nameplane) if b}
            native=next(n for n in font['source_records'] if n['id']==record['id']) if version=='clean_Japanese' else next(n for n in stored['records'] if n['id']==record['id'])['complete_pages']
            pages=native['pages'];models=[]
            for page in pages:
                pixels=Path(page['native_plane']).read_bytes();assert sha(pixels)==page['native_plane_sha256']
                black={(i%216,i//216) for i,b in enumerate(pixels) if b==1};gray={(i%216,i//216) for i,b in enumerate(pixels) if b==15}
                cp=expected_pixels(arm,nativefont,[e for e in page['events'] if e['kind']=='cp932'])
                cpgray={(i%216,i//216) for i,b in enumerate(cp) if b==15}&gray
                models.append(dict(page=page,black=black,ASCII_gray=gray-cpgray,CP932_gray=cpgray,holds=[],header_holds=[]))
            partial=[]
            for frame,photo in photos.items():
                if not entry['frame']+20<frame<row['frame']-4:continue
                found=photo['masks'];candidate=next((m for m in models if found[(0,8,0)]==m['black']),None)
                if candidate is None:
                    partial.append(dict(frame=frame,minimum_black_difference=min(len(m['black']^found[(0,8,0)]) for m in models),sampled_during_progression_ortransition=True));continue
                ascii_equal=found[(98,97,98)]==candidate['ASCII_gray'];cp_equal=found[(197,198,197)]==candidate['CP932_gray']
                if version=='English' and not (ascii_equal and cp_equal):
                    partial.append(dict(frame=frame,black_complete=True,ASCII_gray_difference=len(found[(98,97,98)]^candidate['ASCII_gray']),
                        CP932_gray_difference=len(found[(197,198,197)]^candidate['CP932_gray']),palette_ortransition_not_approved=True));continue
                im=photo['image'];actualname={(x-16,y-276) for y in range(276,289) for x in range(14,18+np['original_pair_flush_width']) if im.getpixel((x,y))==(98,97,98)}
                if actualname!=nameink:
                    unresolved.append(dict(block=blocknumber,version=version,id=record['id'],frame=frame,kind='header-mask',missing=len(nameink-actualname),extra=len(actualname-nameink)));continue
                hold=dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],native_page=candidate['page']['page'],
                    complete_black_body_mask_equal=True,ASCII_gray_equal=ascii_equal,CP932_gray_equal=cp_equal,gray_required=version=='English',
                    complete_name_mask_equal=True,actual_name=np['text'])
                candidate['holds'].append(hold);candidate['header_holds'].append(hold)
            for m in models:
                if not m['holds']:
                    unresolved.append(dict(block=blocknumber,version=version,id=record['id'],page=m['page']['page'],kind='no-complete-page-hold',interval=pair,partial=partial))
                else:
                    panels.append(dict(id=record['id'],source_record_index=record['source_record_index'],page=m['page']['page'],selected_capture=m['holds'][-1]))
            speeches.append(dict(id=record['id'],file_path=fixture['source_file'],source_record_index=record['source_record_index'],source_selector=actor,actual_name=np['text'],
                interval=pair,native_page_count=len(pages),pages=[dict(native_page=m['page']['page'],native_plane=m['page']['native_plane'],native_plane_sha256=m['page']['native_plane_sha256'],
                    complete_body_andname_holds=m['holds']) for m in models],incomplete_sampled_holds=partial))
        assert pairs and finished and pairs[-1]['word']==0 and pairs[-1]['native_result']==[0,0]
        assert not any((trace['rows'][r['entry_row']]['source'].get('route'),trace['rows'][r['entry_row']]['source'].get('block'))==(3,fixture['fixture_block']) for r in trace['unreturned_at_capture_end'])
        observed={r['id'] for r in speeches};unplayed=[r['id'] for r in fixture['original_text_records'] if r['id'] not in observed]
        exitframe=pairs[-1]['returned'];after=min(f for f in photos if f>exitframe+60);sheets=[]
        for start in range(0,len(panels),6):
            sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
            for i,panel in enumerate(panels[start:start+6]):
                h=panel['selected_capture'];x,y=i%3*520,i//3*416
                draw.text((x+4,y+3),f'B{blocknumber} {version} R{panel["source_record_index"]} p{panel["page"]} frame{h["frame"]}',fill='white')
                sheet.paste(photos[h['frame']]['image'].crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
            path=ROOT/f'B{blocknumber}_{version}_complete_panels_sheet{start//6+1:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
        frames=[panels[0]['selected_capture']['frame'],panels[-1]['selected_capture']['frame'],after,16000] if panels else [4220,4280,after,16000]
        transition=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(transition)
        for i,frame in enumerate(frames):
            draw.text((i*256+3,3),f'B{blocknumber} {version} frame{frame}',fill='white');transition.paste(photos[frame]['image'],(i*256,24))
        path=ROOT/f'B{blocknumber}_{version}_first_last_return_final.png';transition.save(path)
        group=dict(block=blocknumber,version=version,fixture=fixture,capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),
            observer_report=str(tp),observer_report_sha256=sha(tp.read_bytes()),input_schedule_sha256=plan['inputs_sha256'],
            command_pairs=pairs,speech_observations=speeches,actual_unique_speeches=len(observed),actual_complete_page_panels=len(panels),unplayed_conditional_speech_IDs=unplayed,
            complete_body_andheader_holds=sum(len(p['complete_body_andname_holds']) for s in speeches for p in s['pages']),
            incomplete_sampled_holds=sum(len(s['incomplete_sampled_holds']) for s in speeches),exit_frame=exitframe,normal_return_sample_frame=after,
            native_terminal_result=pairs[-1]['native_result'],following_commands=following,unidentified_trace_rows=unknown,
            unreturned_following_dialogues=trace['unreturned_at_capture_end'],review_sheets=sheets,
            transition_sheet=dict(path=str(path),sha256=sha(path.read_bytes()),frames=frames),visual_review_pending=True,full_catalogue_UI_unvisited=True)
        groups.append(group);print('ACTUAL',blocknumber,version,'speeches',len(observed),'complete-pages',len(panels),'holds',group['complete_body_andheader_holds'],'partial',group['incomplete_sampled_holds'],'commands',len(pairs),'exit',exitframe,'unplayed',unplayed,flush=True)
    for number in [34,108,35]:
        a,b=[next(g for g in groups if g['block']==number and g['version']==v) for v in ['clean_Japanese','English']]
        assert a['input_schedule_sha256']==b['input_schedule_sha256']
    save(ROOT/'six_scene_captures_actual_pages_headers_branches_returns_andunplayed_conditions.json',dict(
        groups=groups,unresolved=unresolved,total_actual_speech_occurrences=sum(g['actual_unique_speeches'] for g in groups),
        complete_actual_page_panels=sum(g['actual_complete_page_panels'] for g in groups),all_six_jobs_terminal_andreaped=True,
        all_callbacks_readonly_host_slots_restored_corefile_exact=True,all_observed_resident_payloads_equal_fixture_ROM=True,
        actual_branch_decoded_extents_verified_from_observed_previous_result=True,unplayed_conditionals_offline_only_not_individually_visited=True,
        source_Japanese_black_masks_verified_English_black_andperglyph_ASCII_CP932_gray_required=True,
        complete_native_headers_required_for_each_complete_body_hold=True,source_English_inputs_identical=True,
        actual_normal_return_results_all_zero=True,visual_review_portrait_scene_comparison_late_state_andrelease_pending=True,
        initialized_original_prelude_ROM_fixtures_not_natural_optional_activation_original_location_earned_progress_full_effects_routes_orhardware=True,
        existing_system_only_unlock_fixture=True,earned_unlock_verified=False,all_formatting_gates_false=True,
        evidence={str(p):sha(p.read_bytes()) for p in [FIXTURES,FONT,STORED,CURRENT,Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('UNRESOLVED',len(unresolved))
    if unresolved:raise SystemExit(1)
