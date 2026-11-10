"""Complete actual source/English body/header/FE masks and unchanged original conditional execution."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_actual_v7895b')
FIXTURES=Path('work/analysis/Rafael_B45_scene_fixtures_v7892/two_complete_source_English_original_Rafael_prelude_fixtures.json')
RUNS=Path('work/analysis/Rafael_B45_scene_runs_v7893')
FONT=Path('work/analysis/Rafael_B45_source_name_planes_v7894/12_complete_source_pages2_names8_literal_alignments_distinct_FE.json')
NATIVE=Path('work/analysis/Rafael_B45_native_review_v7883/12_exact_native_pages_rebound_with_individual_row_review.json')
STORED=Path('work/analysis/Rafael_B45_stored_v7885/all12_stored_bodies28_fresh20_reused_alignments_exact_viewed_planes.json')
CURRENT=Path('work/analysis/Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json')
def masks(image,width):
    pixels=image.crop((16,296,16+width,360)).get_flattened_data()
    return {c:{(i%width,i//width) for i,v in enumerate(pixels) if v==c} for c in [(0,8,0),(98,97,98),(197,198,197)]}
if __name__=='__main__':
    assert not ROOT.exists();fixtures,font,native,stored,current=map(read,[FIXTURES,FONT,NATIVE,STORED,CURRENT])
    terminals=[]
    for fixture in fixtures['fixtures']:
        folder=RUNS/f"route0_{fixture['version']}";terminal=read(folder/'terminal.json')
        assert terminal['terminal'] and terminal['frames']==16001 and terminal['all_callbacks_readonly_andhost_slots_restored']
        terminals.append((fixture,folder,terminal))
    assert stored['native_viewed_proof_sha256']==sha(NATIVE.read_bytes()) and stored['all12_native_ink_planes_exact_to_already_viewed']
    ROOT.mkdir(parents=True);groups=[];unresolved=[]
    for fixture,folder,terminal in terminals:
        version=fixture['version'];rp,tp=Path(terminal['report']),Path(terminal['observer'])
        report,trace,plan=map(read,[rp,tp,folder/'run_plan.json'])
        assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(tp.read_bytes())==terminal['observer_sha256']
        assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
        assert not report['hardware_device_verification'] and not report['goal_complete'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
        assert report['scripted_input_schedule']==read(plan['inputs']) and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
        assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
        image=NdsImage.open(fixture['research_ROM']);arm,fnt=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
        banks={r:IlnkContainer.parse(image.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)}
        records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
        objects={r['fixture_command_offset']:(i,r) for i,r in enumerate(fixture['all_original_exchange_commands'])}
        expected={c['offset']:c for c in fixture['all_fixture_commands']}
        photos={}
        for p in report['frames_captured']:
            assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
            im=Image.open(p['path']).convert('RGB');assert im.size==(256,384)
            photos[p['frame']]=dict(reference=p,image=im,masks216=masks(im,216),masks228=masks(im,228))
        pairs=[];speeches=[];following=[];unknown=[];finished=False;lastnext=None;panels=[]
        for ri,row in enumerate(trace['rows']):
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source']
            if s['classification']!='original_SC_cache':unknown.append(dict(row=ri,frame=row['frame'],source=s));continue
            assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==s['registered_sha256']==sha(banks[s['route']][s['block']])
            if row['kind']!='after_command':continue
            if finished or (s['route'],s['block'])!=(0,44):
                following.append(dict(frame=row['frame'],route=s['route'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']));continue
            entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];command=expected[at];word=command['word']
            assert s['instruction_offset']==at and s['first_word']==word
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
                assert row['result_words']==[0,pairs[-2]['native_result'][1]]==[0,1];finished=True
            if at not in records:continue
            record=records[at];actor=record['source_selector'];is_FE=actor==254;width=228 if is_FE else 216
            model=next(r for r in font['source_records'] if r['id']==record['id']) if version=='clean_Japanese' else next(r for r in native['records'] if r['id']==record['id'])
            assert len(model['pages'])==1;page=model['pages'][0]
            if is_FE:
                if version=='clean_Japanese':
                    physical=Path(page['physical_plane']).read_bytes();assert sha(physical)==page['physical_plane_sha256']
                else:
                    logical=Path(page['native_plane']).read_bytes();assert len(logical)==228*48 and sha(logical)==page['native_plane_sha256']
                    physical=bytearray(228*64)
                    for y in range(48):
                        for x in range(228):physical[(y//12*16+y%12)*228+x]=int(bool(logical[y*228+x]))
                    physical=bytes(physical);assert sha(physical)==page['physical_plane_sha256']
                black={(i%228,i//228) for i,b in enumerate(physical) if b==(15 if version=='clean_Japanese' else 1)}
                ASCII_gray=set();CP_gray={(i%228,i//228) for i,b in enumerate(physical) if b==14} if version=='clean_Japanese' else set()
                np=None;nameink=set()
            else:
                pixels=Path(page['native_plane']).read_bytes();assert len(pixels)==216*64 and sha(pixels)==page['native_plane_sha256']
                black={(i%216,i//216) for i,b in enumerate(pixels) if b==1};gray={(i%216,i//216) for i,b in enumerate(pixels) if b==15}
                cp=expected_pixels(arm,fnt,[e for e in page['events'] if e['kind']=='cp932'])
                CP_gray={(i%216,i//216) for i,b in enumerate(cp) if b==15}&gray;ASCII_gray=gray-CP_gray
                np=next(n for n in font['name_planes'] if n['actor_ID']==actor)
                nameplane=Path(np['native_plane']).read_bytes();assert sha(nameplane)==np['native_plane_sha256']
                nameink={(i%216,i//216) for i,b in enumerate(nameplane) if b}
            holds=[];partial=[]
            for frame,photo in photos.items():
                if not entry['frame']+20<frame<row['frame']-4:continue
                found=photo['masks228' if is_FE else 'masks216']
                differences=dict(black=len(found[(0,8,0)]^black),ASCII_gray=len(found[(98,97,98)]^ASCII_gray),CP932_gray=len(found[(197,198,197)]^CP_gray))
                if any(differences.values()):
                    partial.append(dict(frame=frame,**differences,sampled_during_progression_ortransition_not_complete=True));continue
                im=photo['image']
                if is_FE:
                    actualname={(x,y) for y in range(276,289) for x in range(14,244) if im.getpixel((x,y))==(98,97,98)}
                    name_equal=not actualname
                else:
                    actualname={(x-16,y-276) for y in range(276,289) for x in range(14,18+np['original_pair_flush_width']) if im.getpixel((x,y))==(98,97,98)}
                    name_equal=actualname==nameink
                if not name_equal:
                    unresolved.append(dict(version=version,id=record['id'],frame=frame,kind='FE-stale-header' if is_FE else 'nameplate-mask',actual_pixels=len(actualname),expected_pixels=len(nameink)));continue
                holds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],native_page=1,
                    complete_black_ASCII_gray_CP932_gray_masks_equal=True,
                    complete_name_mask_equal=not is_FE,original_FE_absent_nameplate_preserved=is_FE,
                    actual_name=None if is_FE else np['text'],native_geometry=[width,64]))
            if not holds:unresolved.append(dict(version=version,id=record['id'],kind='no-complete-page-hold',interval=pair,partial=partial))
            else:panels.append(dict(id=record['id'],source_record_index=record['source_record_index'],selected_capture=holds[-1]))
            speeches.append(dict(id=record['id'],file_path=fixture['source_file'],source_record_index=record['source_record_index'],source_selector=actor,
                kind='system-FE' if is_FE else 'progressive',actual_name=None if is_FE else np['text'],interval=pair,native_page_count=1,
                native_plane=page['native_plane'],native_plane_sha256=page['native_plane_sha256'],complete_body_holds=holds,incomplete_sampled_holds=partial))
        assert finished and len(pairs)==32 and pairs[-1]['native_result']==[0,1]
        assert not trace['unreturned_at_capture_end'] and not unknown
        assert len(speeches)==12 and len({s['id'] for s in speeches})==12
        observed={p['exchange_command_ordinal'] for p in pairs if p['exchange_command_ordinal'] is not None}
        skipped=[o for i,o in enumerate(fixture['all_original_exchange_commands']) if i not in observed]
        assert len(observed)==22 and [s['word'] for s in skipped]==[0x400,0x100]
        predicate=next(p for p in pairs if p['word']==0x8000)
        assert predicate['native_result']==[2,1]
        assert any(p['word']==0x300 and p['observed_previous_result']==1 and p['decoded_length']==12 for p in pairs)
        assert sum(s['source_selector']==254 for s in speeches)==1
        exitframe=pairs[-1]['returned'];after=min(f for f in photos if f>exitframe+60);sheets=[]
        for start in range(0,len(panels),6):
            sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
            for i,panel in enumerate(panels[start:start+6]):
                h=panel['selected_capture'];x,y=i%3*520,i//3*416
                draw.text((x+4,y+3),f"Rafael {version} R{panel['source_record_index']} frame{h['frame']}",fill='white')
                sheet.paste(photos[h['frame']]['image'].crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
            path=ROOT/f'{version}_six_complete_panels_sheet{start//6+1:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
        frames=[panels[0]['selected_capture']['frame'],next(s['complete_body_holds'][-1]['frame'] for s in speeches if s['source_selector']==254),after,16000]
        transition=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(transition)
        for i,frame in enumerate(frames):
            draw.text((i*256+3,3),f'{version} frame{frame}',fill='white');transition.paste(photos[frame]['image'],(i*256,24))
        path=ROOT/f'{version}_first_FE_return_final.png';transition.save(path)
        groups.append(dict(route=0,route_identity='Rafael',version=version,fixture=fixture,
            capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),observer_report=str(tp),observer_report_sha256=sha(tp.read_bytes()),
            input_schedule_sha256=plan['inputs_sha256'],command_pairs=pairs,speech_observations=speeches,
            observed_original_exchange_commands=22,original_structural_commands_not_selected=skipped,actual_unique_speeches=12,
            complete_body_holds=sum(len(s['complete_body_holds']) for s in speeches),
            complete_progressive_header_holds=sum(len(s['complete_body_holds']) for s in speeches if s['source_selector']!=254),
            complete_FE_absent_header_holds=sum(len(s['complete_body_holds']) for s in speeches if s['source_selector']==254),
            incomplete_sampled_holds=sum(len(s['incomplete_sampled_holds']) for s in speeches),
            exit_frame=exitframe,native_terminal_result=[0,1],normal_return_sample_frame=after,
            following_commands=following,unidentified_trace_rows=unknown,unreturned_following_dialogues=trace['unreturned_at_capture_end'],
            review_sheets=sheets,transition_sheet=dict(path=str(path),sha256=sha(path.read_bytes()),frames=frames),visual_review_pending=True))
        print(version,'speeches',len(speeches),'holds',groups[-1]['complete_body_holds'],'partials',groups[-1]['incomplete_sampled_holds'],'commands',len(pairs),'exit',exitframe,'unresolved',len(unresolved),flush=True)
    assert len(groups)==2 and groups[0]['input_schedule_sha256']==groups[1]['input_schedule_sha256']
    save(ROOT/'paired12_source_English_actual_body_name_FE_branch_andnormal_return_audit.json',dict(
        groups=groups,unresolved=unresolved,all24_pages_complete=not unresolved,
        all22_progressive_nameplates_andtwo_FE_absent_nameplates_preserved=not unresolved,
        actual_FE_condition_result1_preserved_without_result_orstate_forcing=True,actual_normal_type0_value1_carry_both_languages=True,
        original_unselected0400_outer0100_have_native_branch_proof_not_individual_gameplay_coverage=True,
        paired_identical_ordinary_inputs_cold_boot_no_battery_save_RAM_roles_funds_RNG_forcing=True,
        original_ten_command_B44_ROM_entry_fixture_not_natural_B45_activation_Ceuta_location_orfull_route=True,
        FE_source_native15_foreground_black_native14_shadow_RGB197_198_197_bound_bycomplete_actual_masks=not unresolved,
        observer_readonly_slot_restoration_andall_complete_resident_payload_hashes_exact=True,
        visual_review_pending=True,paired_upper_scene_timing_RNG_component_andlater_RGB_comparison_pending=True,
        frozen_policy_atomic_production_andregistered_release_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [FIXTURES,FONT,NATIVE,STORED,CURRENT,Path(__file__)]},
        new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    if unresolved:raise SystemExit(1)
