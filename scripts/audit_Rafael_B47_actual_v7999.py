"""Audit observed source/English paths,complete native pages/names andordinary R53 pagination."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B47_actual_v7999')
FIXTURES=Path('work/analysis/Rafael_B47_scene_fixtures_v7997/two_complete_source_English_original_Rafael_prelude_fixtures.json')
RUNS=Path('work/analysis/Rafael_B47_scene_runs_v7998')
FONT=Path('work/analysis/Rafael_B47_source_name_planes_v7986/15_complete_source_pages4_names16_literal_alignments_all_progressive.json')
NATIVE=Path('work/analysis/Rafael_B47_pages_v7985/15_complete_native_paragraphs16_pages60_compiled_alignments.json')
STORED=Path('work/analysis/Rafael_B47_stored_v7990/all15_stored_bodies32_fresh28_reused_alignments16_exact_viewed_pages.json')
CURRENT=Path('work/analysis/Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json')
FLOW=Path('work/analysis/Rafael_B47_source_paths_v7978/625_source_result_compositions_six_text_paths_two_exclusive_alternatives.json')
COLORS=[(0,8,0),(98,97,98),(197,198,197)]
def masks(image):
    pixels=image.crop((16,296,232,360)).get_flattened_data()
    return {c:{(i%216,i//216) for i,v in enumerate(pixels) if v==c} for c in COLORS}
def model_page(arm,font,page):
    pixels=Path(page['native_plane']).read_bytes()
    assert len(pixels)==216*64 and sha(pixels)==page['native_plane_sha256']
    black={(i%216,i//216) for i,b in enumerate(pixels) if b==1}
    gray={(i%216,i//216) for i,b in enumerate(pixels) if b==15}
    cp=expected_pixels(arm,font,[e for e in page['events'] if e['kind']=='cp932'])
    cpgray={(i%216,i//216) for i,b in enumerate(cp) if b==15}&gray
    return {COLORS[0]:black,COLORS[1]:gray-cpgray,COLORS[2]:cpgray}
if __name__=='__main__':
    assert not ROOT.exists();fixtures,font,native,stored,current,flow=map(read,[FIXTURES,FONT,NATIVE,STORED,CURRENT,FLOW])
    assert stored['native_viewed_proof_sha256']==sha(NATIVE.read_bytes()) and stored['all15_native_ink_planes_exact_to_already_viewed']
    ROOT.mkdir(parents=True);groups=[];unresolved=[]
    for fixture in fixtures['fixtures']:
        version=fixture['version'];folder=RUNS/f'route0_{version}';terminal=read(folder/'terminal.json')
        assert terminal['terminal'] and terminal['frames']==16001 and terminal['all_callbacks_readonly_andhost_slots_restored']
        rp,tp=Path(terminal['report']),Path(terminal['observer']);report,trace,plan=map(read,[rp,tp,folder/'run_plan.json'])
        assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(tp.read_bytes())==terminal['observer_sha256']
        assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
        assert not report['hardware_device_verification'] and not report['goal_complete'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
        schedule=read(plan['inputs'])
        assert report['scripted_input_schedule']==schedule and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
        assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
        image=NdsImage.open(fixture['research_ROM']);arm,fnt=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
        banks={r:IlnkContainer.parse(image.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)}
        records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
        objects={r['fixture_command_offset']:(i,r) for i,r in enumerate(fixture['all_original_exchange_commands'])}
        expected={c['offset']:c for c in fixture['all_fixture_commands']};assert len(expected)==58 and len(records)==15
        photos={}
        for p in report['frames_captured']:
            assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
            im=Image.open(p['path']).convert('RGB');assert im.size==(256,384)
            photos[p['frame']]=dict(reference=p,image=im,masks=masks(im))
        pairs=[];speeches=[];following=[];unknown=[];finished=False;lastnext=None;panels=[]
        for ri,row in enumerate(trace['rows']):
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source']
            if s['classification']!='original_SC_cache':
                unknown.append(dict(row=ri,frame=row['frame'],source=s,after_B47_return=finished));continue
            assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==s['registered_sha256']==sha(banks[s['route']][s['block']])
            if row['kind']!='after_command':continue
            if finished or (s['route'],s['block'])!=(0,44):
                following.append(dict(frame=row['frame'],route=s['route'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']));continue
            entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];command=expected[at];word=command['word']
            assert s['instruction_offset']==at and s['first_word']==word and entry['kind']=='before_command'
            for observed in [entry,row]:
                resident=observed['source']
                assert resident['route']==0 and resident['block']==44 and resident['actual_sha256']==fixture['fixture_block_sha256']
                assert resident['payload_bytes']==fixture['fixture_stored_bytes'] and resident['instruction_pointer']==resident['payload_address']+at
                assert sha(Path(resident['actual_payload_file']).read_bytes())==fixture['fixture_block_sha256']
            if lastnext is not None:assert at==lastnext
            if word in [0x100,0x200,0x300,0x400]:
                span=int.from_bytes(bytes.fromhex(command['whole_command_hex'])[2:4],'little');previous=entry['mode']
                taken=word==0x100 or word==0x200 and previous==0 or word==0x300 and previous==1 or word==0x400 and previous==2
                assert row['decoded_length']==4+(span if taken else 0)
            else:assert row['decoded_length']==command['native_extent']
            lastnext=at+row['decoded_length'];ordinal,original=objects.get(at,(None,None))
            pair=dict(fixture_offset=at,exchange_command_ordinal=ordinal,canonical_source_offset=None if ordinal is None else current['groups'][0]['all_source_commands'][ordinal]['offset'],
                word=word,start=entry['frame'],returned=row['frame'],entry_row=row['entry_row'],return_row=ri,decoded_length=row['decoded_length'],
                observed_previous_result=entry['mode'],native_result=row['result_words'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],
                UI_before=entry['native_UI_request_words'],UI_after=row['native_UI_request_words'])
            pairs.append(pair)
            if word==0:
                assert row['result_words']==[0,pairs[-2]['native_result'][1]];finished=True
            if at not in records:continue
            record=records[at];actor=record['source_selector'];assert actor in [0,4,5,6]
            model=next(r for r in (font['source_records'] if version=='clean_Japanese' else native['records']) if r['id']==record['id'])
            models=[model_page(arm,fnt,p) for p in model['pages']]
            np=next(n for n in font['name_planes'] if n['actor_ID']==actor)
            pixels=Path(np['native_plane']).read_bytes();assert sha(pixels)==np['native_plane_sha256']
            nameink={(i%216,i//216) for i,b in enumerate(pixels) if b}
            holds=[];partial=[];ordered=[]
            for frame,photo in photos.items():
                if not entry['frame']+20<frame<row['frame']-4:continue
                diffs=[{str(color):len(photo['masks'][color]^expected_mask[color]) for color in COLORS} for expected_mask in models]
                matched=[i for i,d in enumerate(diffs) if not any(d.values())]
                if not matched:
                    partial.append(dict(frame=frame,differences_to_complete_pages=diffs,
                        not_counted_as_complete_display=True));continue
                assert len(matched)==1;page=matched[0]+1
                found={(x-16,y-276) for y in range(276,289) for x in range(14,18+np['original_pair_flush_width']) if photo['image'].getpixel((x,y))==(98,97,98)}
                if found!=nameink:
                    unresolved.append(dict(version=version,id=record['id'],frame=frame,kind='complete-body-nameplate-mismatch',missing=len(nameink-found),extra=len(found-nameink)));continue
                hold=dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],native_page=page,
                    complete_black_ASCII_gray_CP932_gray_masks_equal=True,complete_name_mask_equal=True,actual_name=np['text'],native_geometry=[216,64])
                holds.append(hold)
                if not ordered or ordered[-1]!=page:ordered.append(page)
            pageholds=[[h for h in holds if h['native_page']==i+1] for i in range(len(models))]
            if not all(pageholds) or ordered!=list(range(1,len(models)+1)):
                unresolved.append(dict(version=version,id=record['id'],kind='missing-or-out-of-order-complete-pages',pages=ordered,expected_pages=len(models),partial=partial))
            transitions=[]
            for before,after in zip(pageholds,pageholds[1:]):
                if not before or not after:continue
                last,first=before[-1]['frame'],after[0]['frame']
                presses=[r for r in schedule if last<r['start']<=first and r['buttons']==['A']]
                assert len(presses)==1
                transitions.append(dict(from_page=before[-1]['native_page'],to_page=after[0]['native_page'],
                    last_complete_before=last,first_complete_after=first,ordinary_A_input=presses[0],
                    same_original_command_active_across_page_turn=True,no_state_result_orinput_retiming=True))
            for i,ph in enumerate(pageholds):
                if ph:panels.append(dict(id=record['id'],source_record_index=record['source_record_index'],native_page=i+1,selected_capture=ph[-1]))
            speeches.append(dict(id=record['id'],file_path=fixture['source_file'],source_record_index=record['source_record_index'],source_selector=actor,
                kind='progressive',actual_name=np['text'],interval=pair,native_page_count=len(models),
                native_planes=[dict(path=p['native_plane'],sha256=p['native_plane_sha256']) for p in model['pages']],
                complete_body_holds=holds,actual_complete_page_holds=pageholds,ordinary_page_transitions=transitions,
                incomplete_sampled_holds=partial))
        assert finished and not unknown and not trace['unreturned_at_capture_end']
        visited=[p['canonical_source_offset'] for p in pairs if p['exchange_command_ordinal'] is not None]
        matchedpaths=[p for p in flow['source_result_compositions'] if p['visited_source_offsets']==visited]
        assert matchedpaths and all(p['source_speech_IDs']==[s['id'] for s in speeches] for p in matchedpaths)
        assert len(speeches)==len({s['id'] for s in speeches})
        selected_ids={s['id'] for s in speeches};offline=[r['id'] for r in current['records'] if r['id'] not in selected_ids]
        observed={p['exchange_command_ordinal'] for p in pairs if p['exchange_command_ordinal'] is not None}
        skipped=[o for i,o in enumerate(fixture['all_original_exchange_commands']) if i not in observed]
        exitframe=pairs[-1]['returned'];after=min(f for f in photos if f>exitframe+60);sheets=[]
        for start in range(0,len(panels),6):
            sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
            for i,panel in enumerate(panels[start:start+6]):
                h=panel['selected_capture'];x,y=i%3*520,i//3*416
                draw.text((x+4,y+3),f"Rafael {version} R{panel['source_record_index']} p{panel['native_page']} frame{h['frame']}",fill='white')
                sheet.paste(photos[h['frame']]['image'].crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
            path=ROOT/f'{version}_complete_pages_sheet{start//6+1:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
        r53=next(s for s in speeches if s['id']=='DK4_MES_B47_R0053')
        frames=[panels[0]['selected_capture']['frame'],r53['complete_body_holds'][-1]['frame'],after,16000]
        transition=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(transition)
        for i,frame in enumerate(frames):
            draw.text((i*256+3,3),f'{version} frame{frame}',fill='white');transition.paste(photos[frame]['image'],(i*256,24))
        path=ROOT/f'{version}_R53_return_final.png';transition.save(path)
        groups.append(dict(route=0,route_identity='Rafael',version=version,fixture=fixture,
            capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),observer_report=str(tp),observer_report_sha256=sha(tp.read_bytes()),
            input_schedule_sha256=plan['inputs_sha256'],command_pairs=pairs,speech_observations=speeches,
            observed_original_exchange_commands=len(observed),original_structural_commands_not_selected=skipped,
            actual_unique_speeches=len(speeches),actual_complete_native_pages=sum(s['native_page_count'] for s in speeches),
            native_only_unvisited_speech_IDs=offline,complete_body_holds=sum(len(s['complete_body_holds']) for s in speeches),
            complete_progressive_header_holds=sum(len(s['complete_body_holds']) for s in speeches),
            incomplete_sampled_holds=sum(len(s['incomplete_sampled_holds']) for s in speeches),
            exit_frame=exitframe,native_terminal_result=pairs[-1]['native_result'],normal_return_sample_frame=after,
            observed_native_composition_matches=len(matchedpaths),following_commands=following,unidentified_trace_rows=unknown,
            unreturned_following_dialogues=trace['unreturned_at_capture_end'],review_sheets=sheets,
            transition_sheet=dict(path=str(path),sha256=sha(path.read_bytes()),frames=frames),visual_review_pending=True))
        print(version,'speeches',len(speeches),'pages',groups[-1]['actual_complete_native_pages'],'holds',groups[-1]['complete_body_holds'],
            'partials',groups[-1]['incomplete_sampled_holds'],'commands',len(pairs),'exit',exitframe,'unresolved',len(unresolved),flush=True)
    source,en=groups
    assert source['input_schedule_sha256']==en['input_schedule_sha256']
    assert [s['id'] for s in source['speech_observations']]==[s['id'] for s in en['speech_observations']]
    original53=next(s for s in source['speech_observations'] if s['id']=='DK4_MES_B47_R0053')
    english53=next(s for s in en['speech_observations'] if s['id']=='DK4_MES_B47_R0053')
    assert original53['native_page_count']==1 and english53['native_page_count']==2 and len(english53['ordinary_page_transitions'])==1
    assert source['native_terminal_result']==en['native_terminal_result']==[0,0]
    save(ROOT/'paired_source_English_observed_path_complete_pages_names_andR53_transition.json',dict(
        groups=groups,unresolved=unresolved,all_observed_source_English_complete_page_masks_andnames_pass=not unresolved,
        actual_source_R53_one_page_English_two_pages_ordinary_A_turn_andfollowing_return_preserved=True,
        no_excluded_complete_page_masks_orforced_gameplay_conditions=True,
        actual_normal_type0_value0_carry_both_languages=True,actual_total_frames=32002,
        all15_source_objects_retained_butonly_observed_path_is_actual_gameplay_coverage=True,
        native_only_unvisited_speech_IDs=source['native_only_unvisited_speech_IDs'],
        original_ten_command_B44_ROM_entry_fixture_not_natural_B47_activation_original_location_orfullroute=True,
        no_battery_savestate_RAM_roles_roster_funds_RNG_condition_result_orinput_retiming=True,
        actual_paired_comparison_timing_RNG_components_later_RGB_andvisual_review_pending=True,
        frozen_policy_atomic_registered_release_andstartup_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [FIXTURES,FONT,NATIVE,STORED,CURRENT,FLOW,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Observed source/English pages andR53 ordinary page turn audited;unresolved',len(unresolved),'.Actual scope excludes four conditional source objects;comparison/view/release pending.')
    if unresolved:raise SystemExit(1)
