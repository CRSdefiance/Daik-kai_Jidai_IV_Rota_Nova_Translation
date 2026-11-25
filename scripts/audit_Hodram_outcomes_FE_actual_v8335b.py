"""Audit every selected command and complete body/header hold in both whole outcome fixtures."""
import argparse
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels as original_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_actual_v8335b')
FIXTURES=Path('work/analysis/Hodram_outcome_fixtures_v8332/four_complete_clean_revised_SC1_scripts_original_Hodram_prelude_fixtures.json')
MODELS=Path('work/analysis/Hodram_outcome_actual_models_v8334/six_clean_six_stored_native_bodies_one_Lil_header_distinct_FE.json')
COLORS=[(0,8,0),(98,97,98),(197,198,197)]

def masks(image,width):
    values=image.crop((16,296,16+width,360)).get_flattened_data()
    return {c:{(i%width,i//width) for i,v in enumerate(values) if v==c} for c in COLORS}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--block',type=int,choices=[48],required=True);number=ap.parse_args().block
    root=ROOT/f'B{number}';assert not root.exists();fixtures,models=map(read,[FIXTURES,MODELS]);root.mkdir(parents=True);groups=[];unresolved=[]
    runs=Path('work/analysis/Hodram_outcome_scene_runs_v8333' if number==47 else 'work/analysis/Hodram_outcome_FE_scene_runs_v8333b')
    evidence={str(p):sha(p.read_bytes()) for p in [FIXTURES,MODELS,Path(__file__)]}
    for fixture in [f for f in fixtures['fixtures'] if f['source_block']==number]:
        version=fixture['version'];folder=runs/f'route1_B{number}_{version}';terminal=read(folder/'terminal.json');rp,tp=Path(terminal['report']),Path(terminal['observer']);report,trace,plan=map(read,[rp,tp,folder/'run_plan.json'])
        assert terminal['terminal'] and terminal['frames']==report['frames']==plan['frames']==10001 and terminal['all_callbacks_readonly_andhost_slots_restored']
        assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(tp.read_bytes())==terminal['observer_sha256'] and sha(Path(terminal['run_plan']).read_bytes())==terminal['run_plan_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not report['goal_complete'] and not report['hardware_device_verification']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_')) and not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
        assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()) and report['scripted_input_schedule']==read(plan['inputs']) and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
        image=NdsImage.open(fixture['research_ROM']);arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT');assert sha(arm)==models['ARM9_sha256'] and sha(font)==models['font_sha256']
        pixel_oracle=FunctionType(original_pixels.__code__,{**original_pixels.__globals__,'CURRENT_ARM9':sha(arm)},argdefs=original_pixels.__defaults__)
        banks={r:IlnkContainer.parse(image.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)};expected={c['offset']:c for c in fixture['all_fixture_commands']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']};objects={c['fixture_command_offset']:c for c in fixture['all_original_exchange_commands']}
        native={r['id']:r for r in models['native_models'][version]};name=models['name_planes'][0];assert name['actor_ID']==2;nameplane=Path(name['native_plane']).read_bytes();assert sha(nameplane)==name['native_plane_sha256'];nameink={(i%216,i//216) for i,v in enumerate(nameplane) if v}
        photos={}
        for p in report['frames_captured']:
            assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];picture=Image.open(p['path']).convert('RGB');assert picture.size==(256,384)
            photos[p['frame']]=dict(reference=p,image=picture,masks216=masks(picture,216),masks228=masks(picture,228))
        pairs=[];speeches=[];following=[];unknown=[];lastnext=None;normal=None;finished=False
        for ri,row in enumerate(trace['rows']):
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];source=row['source']
            if source['classification']!='original_SC_cache':unknown.append(dict(row=ri,frame=row['frame'],source=source,after_return=finished));continue
            assert source['whole_resident_payload_exact_ROM'] and source['actual_sha256']==source['registered_sha256']==sha(banks[source['route']][source['block']])
            if row['kind']!='after_command':continue
            if finished or (source['route'],source['block'])!=(1,42):
                following.append(dict(frame=row['frame'],route=source['route'],block=source['block'],offset=source['instruction_offset'],word=source['first_word'],native_result=row['result_words']));continue
            entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];command=expected[at];word=command['word'];assert entry['kind']=='before_command' and source['instruction_offset']==at and source['first_word']==word and row['decoded_length']==command['native_extent']
            for observed in [entry,row]:
                resident=observed['source'];assert resident['route']==1 and resident['block']==42 and resident['actual_sha256']==fixture['fixture_block_sha256'] and resident['payload_bytes']==fixture['fixture_stored_bytes'] and resident['instruction_pointer']==resident['payload_address']+at
                assert sha(Path(resident['actual_payload_file']).read_bytes())==fixture['fixture_block_sha256']
            if lastnext is not None:assert at==lastnext
            lastnext=at+row['decoded_length'];original=objects.get(at)
            pair=dict(fixture_offset=at,canonical_source_offset=None if original is None else original['canonical_clean_offset'],source_command_ordinal=None if original is None else original['source_command_ordinal'],word=word,start=entry['frame'],returned=row['frame'],duration=row['frame']-entry['frame'],entry_row=row['entry_row'],return_row=ri,decoded_length=row['decoded_length'],observed_previous_result=entry['mode'],native_result=row['result_words'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_before=entry['native_UI_request_words'],UI_after=row['native_UI_request_words']);pairs.append(pair)
            if word==0:
                assert command['native_extent']==4 and row['result_words']==[0,pairs[-2]['native_result'][1]];finished=True;normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True)
            if at not in records:continue
            record=records[at];actor=record['source_selector'];is_FE=actor==254;width=228 if is_FE else 216;model=native[record['id']];assert len(model['pages'])==1;page=model['pages'][0]
            plane=Path(page['native_plane']).read_bytes();assert sha(plane)==page['native_plane_sha256']
            if is_FE:
                physical=Path(page['physical_plane']).read_bytes();assert len(physical)==228*64 and sha(physical)==page['physical_plane_sha256']
                assert set(physical)<=({0,14,15} if version=='clean_Japanese' else {0,15})
                black={(i%228,i//228) for i,v in enumerate(physical) if v==15};gray=set();cpgray={(i%228,i//228) for i,v in enumerate(physical) if v==14} if version=='clean_Japanese' else set()
            else:
                assert actor==2 and len(plane)==216*64
                black={(i%216,i//216) for i,v in enumerate(plane) if v==1};allgray={(i%216,i//216) for i,v in enumerate(plane) if v==15};cp=pixel_oracle(arm,font,[e for e in page['events'] if e['kind']=='cp932']);cpgray={(i%216,i//216) for i,v in enumerate(cp) if v==15}&allgray;gray=allgray-cpgray
            required=dict(zip(COLORS,[black,gray,cpgray],strict=True));holds=[];partial=[];nameholds=[]
            for frame,photo in photos.items():
                if not entry['frame']+20<frame<row['frame']-4:continue
                im=photo['image'];foundname={(x-16,y-276) for y in range(276,289) for x in range(14,244 if is_FE else 18+name['original_pair_flush_width']) if im.getpixel((x,y))==COLORS[1]};nameok=not foundname if is_FE else foundname==nameink
                if nameok:nameholds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],FE_absent_nameplate=is_FE))
                differences={str(c):len(photo['masks228' if is_FE else 'masks216'][c]^required[c]) for c in COLORS}
                if any(differences.values()) or not nameok:partial.append(dict(frame=frame,body_differences=differences,name_pixels=len(foundname),not_counted_as_complete=True));continue
                holds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],native_page=1,complete_black_ASCII_gray_CP932_gray_leading_internal_final_glyph_masks_equal=True,complete_name_mask_equal=not is_FE,original_FE_absent_nameplate_preserved=is_FE,actual_name=None if is_FE else name['text'],native_geometry=[width,64]))
            if not holds:unresolved.append(dict(version=version,block=number,id=record['id'],kind='no-complete-body-and-name-orFE-absent-header-hold',partial=partial))
            speeches.append(dict(id=record['id'],source_selector=actor,name=None if is_FE else name['text'],start=entry['frame'],returned=row['frame'],pages=1,kind='system-FE' if is_FE else 'progressive',complete_holds=holds,nameholds=nameholds,partial_ortransition_samples=partial,selected_capture=holds[-1] if holds else None))
        missing=[r['id'] for r in fixture['original_text_records'] if r['id'] not in {s['id'] for s in speeches}]
        if missing:unresolved.append(dict(version=version,block=number,kind='missing-source-speeches',IDs=missing))
        if not normal:unresolved.append(dict(version=version,block=number,kind='normal-return-unobserved',pending=trace['unreturned_at_capture_end']))
        if unknown:unresolved.append(dict(version=version,block=number,kind='unidentified-observer-sources',rows=unknown))
        if normal:assert len(pairs)==len(expected)==(13 if number==47 else 18) and {p['source_command_ordinal'] for p in pairs if p['source_command_ordinal'] is not None}==set(range(5 if number==47 else 10))
        transitions=[]
        if normal and all(s['selected_capture'] for s in speeches):
            after=min(f for f in photos if f>normal['frame']+60);frames=[speeches[0]['selected_capture']['frame'],speeches[-1]['selected_capture']['frame'],after,10000];sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
            for i,frame in enumerate(frames):draw.text((i*256+3,3),f'{version} frame{frame}',fill='white');sheet.paste(photos[frame]['image'],(i*256,24))
            path=root/f'{version}_notice_dialogue_return_final.png';sheet.save(path);transitions=[dict(path=str(path),sha256=sha(path.read_bytes()),frames=frames)]
        for p in [folder/'terminal.json',folder/'run_plan.json',rp,tp]:evidence[str(p)]=sha(p.read_bytes())
        groups.append(dict(version=version,block=number,fixture=fixture,capture_report=str(rp),observer=str(tp),actual_frames=10001,input_schedule_sha256=plan['inputs_sha256'],command_pairs=pairs,speeches=speeches,normal_return=normal,unvisited_conditional_text_IDs=missing,following_original_cache_commands=following,unknown_sources=unknown,transition_sheets=transitions,all_selected_command_boundaries_lengths_andresident_payloads_exact=True,all_callbacks_readonly=True))
        print(version,number,'speeches',len(speeches),'completeholds',sum(len(s['complete_holds']) for s in speeches),'normal',normal,'unresolved',len(unresolved),flush=True)
    assert len(groups)==2 and groups[0]['input_schedule_sha256']==groups[1]['input_schedule_sha256'];paired=[]
    for old in groups[0]['speeches']:
        new=next(s for s in groups[1]['speeches'] if s['id']==old['id'])
        if old['selected_capture'] and new['selected_capture']:paired.append((old,new))
    sheets=[]
    if paired:
        sheet=Image.new('RGB',(1024,410*len(paired)),'#263238');draw=ImageDraw.Draw(sheet)
        for i,pair in enumerate(paired):
            for j,s in enumerate(pair):
                p=s['selected_capture'];pic=Image.open(p['capture']).convert('RGB');draw.text((j*512+3,i*410+3),s['id']+' '+groups[j]['version']+f' frame{p["frame"]}',fill='white');sheet.paste(pic.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(j*512,i*410+24))
        path=root/f'B{number}_three_complete_source_English_panels.png';sheet.save(path);sheets=[dict(path=str(path),sha256=sha(path.read_bytes()))]
    save(root/'paired_actual_dialogue_headers_FE_flow_returns.json',dict(groups=groups,unresolved=unresolved,review_sheets=sheets,visual_review_pending=True,all_observed_complete_body_name_orFE_absent_header_holds_andnative_flow_pass=not unresolved,
        native_FE_physical_indices_preserved_not_binarized=True,actual_typed_FE_descriptors_palette_andlater_native_state_comparison_separate_pending=True,all_selected_original_nontext_effect_commands_observed_not_all_outer_eligibility_orattainable_effects=True,
        initialized_whole_script_opening_fixture_not_natural_optional_activation_original_location_earned_progress_fullroute_orhardware=True,no_flags_party_roster_roles_funds_RNG_results_orinput_retiming=True,new_credit=0,full_goal_complete=False,evidence=evidence))
    print('Saved actual paired proof;unresolved',len(unresolved),'body sheets',len(sheets),'transition sheets',sum(len(g['transition_sheets']) for g in groups),flush=True)
