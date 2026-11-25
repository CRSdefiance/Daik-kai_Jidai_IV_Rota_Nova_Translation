"""Audit observed whole exchanges: native flow, complete body/name holds and returns.

Record any missing coverage without changing input schedules or claiming natural activation.
"""
import argparse,struct
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels as original_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_actual_v8742')
FIXTURES=Path('work/analysis/Hodram_B31_B53_fixtures_v8739/four_whole_scripts.json')
MODELS=Path('work/analysis/Hodram_B31_B53_models_v8741/native_models.json')
RUNS=Path('work/analysis/Hodram_B31_B53_scene_runs_v8740')
COLORS=[(0,8,0),(98,97,98),(197,198,197)]

def masks(image,width=216):
    pixels=image.crop((16,296,16+width,360)).get_flattened_data()
    return {c:{(i%width,i//width) for i,v in enumerate(pixels) if v==c} for c in COLORS}

def model_masks(arm,font,page,pixel_oracle):
    plane=Path(page['native_plane']).read_bytes();assert len(plane)==216*64 and sha(plane)==page['native_plane_sha256']
    black={(i%216,i//216) for i,v in enumerate(plane) if v==1};gray={(i%216,i//216) for i,v in enumerate(plane) if v==15}
    cp=pixel_oracle(arm,font,[e for e in page['events'] if e['kind']=='cp932'])
    cpgray={(i%216,i//216) for i,v in enumerate(cp) if v==15}&gray
    return {COLORS[0]:black,COLORS[1]:gray-cpgray,COLORS[2]:cpgray}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--block',type=int,choices=[31,53],required=True);number=ap.parse_args().block
    root=ROOT/f'B{number}';assert not root.exists();fixtures,models=map(read,[FIXTURES,MODELS]);root.mkdir(parents=True)
    groups=[];unresolved=[];evidence={str(p):sha(p.read_bytes()) for p in [FIXTURES,MODELS,Path(__file__)]}
    for fixture in [f for f in fixtures['fixtures'] if f['source_block']==number]:
        version=fixture['version'];folder=RUNS/f'route1_B{number}_{version}';terminal=read(folder/'terminal.json')
        rp,tp=Path(terminal['report']),Path(terminal['observer']);report,trace,plan=map(read,[rp,tp,folder/'run_plan.json'])
        assert terminal['terminal'] and report['frames']==terminal['frames']==plan['frames']=={31:6001,53:6001}[number]
        assert terminal['all_callbacks_readonly_andhost_slots_restored'] and sha(rp.read_bytes())==terminal['report_sha256'] and sha(tp.read_bytes())==terminal['observer_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
        assert not report['goal_complete'] and not report['hardware_device_verification'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
        assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
        assert report['scripted_input_schedule']==read(plan['inputs']) and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
        image=NdsImage.open(fixture['research_ROM']);arm=image.read_file('/__arm9__.bin');font=image.read_file('/GRP/KANJI.FNT')
        assert sha(arm)==models['ARM9_sha256'] and sha(font)==models['font_sha256']
        pixels=FunctionType(original_pixels.__code__,{**original_pixels.__globals__,'CURRENT_ARM9':sha(arm)},argdefs=original_pixels.__defaults__)
        banks={r:IlnkContainer.parse(image.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)}
        expected={c['offset']:c for c in fixture['all_fixture_commands']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
        objects={r['fixture_command_offset']:r for r in fixture['all_original_exchange_commands']};native={r['id']:r for r in models['native_models'][version]}
        names={r['actor_ID']:r for r in models['name_planes']};nameinks={}
        for actor,n in names.items():
            plane=Path(n['native_plane']).read_bytes();assert sha(plane)==n['native_plane_sha256'];nameinks[actor]={(i%216,i//216) for i,v in enumerate(plane) if v}
        photos={}
        for photo in report['frames_captured']:
            path=Path(photo['path']);assert sha(path.read_bytes())==photo['PNG_sha256'];pic=Image.open(path).convert('RGB');assert pic.size==(256,384)
            photos[photo['frame']]=dict(reference=photo,image=pic,masks216=masks(pic,216),masks228=masks(pic,228))
        pairs=[];speeches=[];following=[];unknown=[];lastnext=None;finished=False;normal=None
        for ri,row in enumerate(trace['rows']):
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];source=row['source']
            if source['classification']!='original_SC_cache':unknown.append(dict(row=ri,frame=row['frame'],source=source,after_return=finished));continue
            assert source['whole_resident_payload_exact_ROM'] and source['actual_sha256']==source['registered_sha256']==sha(banks[source['route']][source['block']])
            if row['kind']!='after_command':continue
            if finished or (source['route'],source['block'])!=(1,42):
                following.append(dict(frame=row['frame'],route=source['route'],block=source['block'],offset=source['instruction_offset'],word=source['first_word'],native_result=row['result_words']));continue
            entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];command=expected[at];word=command['word'];assert entry['kind']=='before_command'
            assert source['instruction_offset']==at and source['first_word']==word
            for observed in [entry,row]:
                resident=observed['source'];assert resident['route']==1 and resident['block']==42 and resident['actual_sha256']==fixture['fixture_block_sha256']
                assert resident['payload_bytes']==fixture['fixture_stored_bytes'] and resident['instruction_pointer']==resident['payload_address']+at
                assert sha(Path(resident['actual_payload_file']).read_bytes())==fixture['fixture_block_sha256']
            if lastnext is not None:assert at==lastnext
            if word in [0x100,0x200,0x300,0x400]:
                span=int.from_bytes(bytes.fromhex(command['whole_command_hex'])[2:4],'little');previous=entry['mode']
                taken=word==0x100 or word==0x200 and previous==0 or word==0x300 and previous==1 or word==0x400 and previous==2
                assert row['decoded_length']==4+(span if taken else 0)
            else:assert row['decoded_length']==command['native_extent']
            lastnext=at+row['decoded_length'];original=objects.get(at)
            pair=dict(fixture_offset=at,canonical_source_offset=None if original is None else original['canonical_clean_offset'],
                source_command_ordinal=None if original is None else original['source_command_ordinal'],word=word,start=entry['frame'],returned=row['frame'],duration=row['frame']-entry['frame'],
                entry_row=row['entry_row'],return_row=ri,decoded_length=row['decoded_length'],observed_previous_result=entry['mode'],native_result=row['result_words'],
                before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_before=entry['native_UI_request_words'],UI_after=row['native_UI_request_words'])
            pairs.append(pair)
            if word==0:
                assert row['result_words']==[0,entry['mode']];finished=True;normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True)
            if at not in records:continue
            record=records[at];actor=record['source_selector'];FE=actor==254;width=228 if FE else 216;model=native[record['id']];assert len(model['pages'])==1;page=model['pages'][0]
            plane=Path(page['native_plane']).read_bytes();assert sha(plane)==page['native_plane_sha256']
            if FE:
                physical=Path(page['physical_plane']).read_bytes();assert len(physical)==228*64 and sha(physical)==page['physical_plane_sha256']
                assert set(physical)<=({0,14,15} if version=='clean_Japanese' else {0,15})
                black={(i%228,i//228) for i,v in enumerate(physical) if v==15};gray=set();cpgray={(i%228,i//228) for i,v in enumerate(physical) if v==14}
            else:
                assert len(plane)==216*64
                black={(i%216,i//216) for i,v in enumerate(plane) if v==1};allgray={(i%216,i//216) for i,v in enumerate(plane) if v==15}
                cp=pixels(arm,font,[e for e in page['events'] if e['kind']=='cp932']);cpgray={(i%216,i//216) for i,v in enumerate(cp) if v==15}&allgray;gray=allgray-cpgray
            required=dict(zip(COLORS,[black,gray,cpgray],strict=True));holds=[];partial=[];nameholds=[]
            for frame,photo in photos.items():
                if not entry['frame']+20<frame<row['frame']-4:continue
                im=photo['image'];n=None if FE else names[actor]
                found={(x-16,y-276) for y in range(276,289) for x in range(14,244 if FE else 18+n['original_pair_flush_width']) if im.getpixel((x,y))==COLORS[1]}
                nameok=not found if FE else found==nameinks[actor]
                if nameok:nameholds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],FE_absent_nameplate=FE))
                differences={str(c):len(photo['masks228' if FE else 'masks216'][c]^required[c]) for c in COLORS}
                if any(differences.values()) or not nameok:
                    partial.append(dict(frame=frame,body_differences=differences,name_pixels=len(found),not_counted_as_complete=True));continue
                holds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],native_page=1,complete_black_ASCII_gray_CP932_gray_leading_internal_final_glyph_masks_equal=True,complete_name_mask_equal=not FE,original_FE_absent_nameplate_preserved=FE,actual_name=None if FE else n['text'],native_geometry=[width,64]))
            if not holds:unresolved.append(dict(version=version,block=number,id=record['id'],kind='no-complete-body-and-name-orFE-absent-header-hold',partial=partial))
            speeches.append(dict(id=record['id'],source_selector=actor,name=None if FE else n['text'],start=entry['frame'],returned=row['frame'],pages=1,kind='system-FE' if FE else 'progressive',complete_holds=holds,nameholds=nameholds,partial_ortransition_samples=partial,selected_capture=holds[-1] if holds else None))
        ids=[r['id'] for r in speeches];assert len(ids)==len(set(ids))
        missing=[r['id'] for r in fixture['original_text_records'] if r['id'] not in ids]
        if not normal:unresolved.append(dict(version=version,block=number,kind='normal-return-not-observed',pending=trace['unreturned_at_capture_end']))
        if unknown:unresolved.append(dict(version=version,block=number,kind='unidentified-observer-sources',rows=unknown))
        for p in [folder/'terminal.json',folder/'run_plan.json',rp,tp]:evidence[str(p)]=sha(p.read_bytes())
        groups.append(dict(version=version,block=number,fixture=fixture,capture_report=str(rp),observer=str(tp),actual_frames=report['frames'],command_pairs=pairs,
            speeches=speeches,normal_return=normal,unvisited_conditional_text_IDs=missing,following_original_cache_commands=following,unknown_sources=unknown,
            all_selected_command_boundaries_follow_native_relative_results=True,all_selected_payloads_exact_own_ROM_andcallbacks_readonly=True))
        print(version,number,'speeches',len(speeches),'bodyholds',sum(len(s['complete_holds']) for s in speeches),'nameholds',sum(len(s['nameholds']) for s in speeches),'missing',missing,'return',normal,flush=True)
    sheets=[]
    for start in range(0,len(groups[0]['speeches']),4):
        paired=[]
        for old in groups[0]['speeches'][start:start+4]:
            new=next((s for s in groups[1]['speeches'] if s['id']==old['id']),None)
            if new and old['selected_capture'] and new['selected_capture']:paired.append((old,new))
        if not paired:continue
        sheet=Image.new('RGB',(1024,410*len(paired)),'#263238');draw=ImageDraw.Draw(sheet)
        for i,pair in enumerate(paired):
            for j,speech in enumerate(pair):
                photo=speech['selected_capture'];pic=Image.open(photo['capture']).convert('RGB')
                draw.text((j*512+3,i*410+3),speech['id']+' '+groups[j]['version']+f' frame{photo["frame"]}',fill='white')
                sheet.paste(pic.resize((512,768),Image.Resampling.NEAREST).crop((0,384,512,768)),(j*512,i*410+24))
        path=root/f'B{number}_whole_dialogue_pair_sheet{start//4+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    save(root/'paired_actual_dialogue_headers_flow_returns.json',dict(groups=groups,unresolved=unresolved,review_sheets=sheets,visual_review_pending=True,
        all_observed_complete_body_name_holds_andnative_flow_pass=not unresolved,
        full_query_branch_transition_andlater_state_comparison_separate_pending=True,
        progressive216x64_masks_not_full_scene_orfuture_simulation_proof_no_FE_panel=True,
        initialized_opening_ROM_fixture_not_original_event_activation_location_eligibility_fullroute_orhardware=True,
        no_conditions_RNG_party_roster_funds_results_orinput_retiming=True,new_credit=0,full_goal_complete=False,evidence=evidence))
    print('Saved actual paired evidence; unresolved',len(unresolved),'review sheets',len(sheets),flush=True)
