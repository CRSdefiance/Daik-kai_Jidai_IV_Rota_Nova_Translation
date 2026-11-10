"""Actual bounded-tail branch/menu results and complete progressive/FE/name masks,without broader activation claims."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels as original_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_tail_actual_v8417')
FIXTURES=Path('work/analysis/Hodram_B49_tail_v8415/bounded_tail_fixtures.json')
MODELS=Path('work/analysis/Hodram_B49_models_v8408/native_models.json')
RUNS=Path('work/analysis/Hodram_B49_tail_runs_v8416')
COLORS=[(0,8,0),(98,97,98),(197,198,197)]

def masks(im,width):
    pixels=im.crop((16,296,16+width,360)).get_flattened_data()
    return {c:{(i%width,i//width) for i,v in enumerate(pixels) if v==c} for c in COLORS}

def selected_path(fixture,selection):
    commands={c['offset']:c for c in fixture['all_fixture_commands']};pointer=8;value=0;visited=[]
    while pointer<fixture['fixture_logical_end']:
        command=commands[pointer];word=command['word'];visited.append(pointer)
        if word in [0x100,0x200,0x300,0x400]:
            span=int.from_bytes(bytes.fromhex(command['whole_command_hex'])[2:4],'little')
            taken=word==0x100 or word==0x200 and value==0 or word==0x300 and value==1 or word==0x400 and value==2
            pointer+=4+(span if taken else 0)
        else:
            pointer+=command['native_extent']
            if word==0x2100:value=selection
        if word==0:break
    assert pointer==fixture['fixture_logical_end'] and commands[visited[-1]]['word']==0
    return visited

if __name__=='__main__':
    assert not ROOT.exists();fixtures,models=map(read,[FIXTURES,MODELS]);ROOT.mkdir(parents=True)
    groups=[];unresolved=[];evidence={str(p):sha(p.read_bytes()) for p in [FIXTURES,MODELS,Path(__file__)]}
    for choice in ['accept','decline']:
        selected=0 if choice=='accept' else 1
        for fixture in fixtures['fixtures']:
            version=fixture['version'];folder=RUNS/f'route1_{version}_{choice}';terminal=read(folder/'terminal.json')
            rp,tp=Path(terminal['report']),Path(terminal['observer']);report,trace,plan=map(read,[rp,tp,folder/'run_plan.json'])
            assert terminal['terminal'] and terminal['frames']==report['frames']==plan['frames']==10001 and terminal['choice']==choice
            assert terminal['all_callbacks_readonly_andhost_slots_restored'] and sha(rp.read_bytes())==terminal['report_sha256'] and sha(tp.read_bytes())==terminal['observer_sha256']
            assert sha(Path(terminal['run_plan']).read_bytes())==terminal['run_plan_sha256']
            assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
            assert not report['goal_complete'] and not report['hardware_device_verification'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
            assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
            assert report['scripted_input_schedule']==read(plan['inputs']) and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
            assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
            image=NdsImage.open(fixture['research_ROM']);arm,font=image.read_file('/__arm9__.bin'),image.read_file('/GRP/KANJI.FNT')
            assert sha(arm)==models['ARM9_sha256'] and sha(font)==models['font_sha256']
            oracle=FunctionType(original_pixels.__code__,{**original_pixels.__globals__,'CURRENT_ARM9':sha(arm)},argdefs=original_pixels.__defaults__)
            banks={r:IlnkContainer.parse(image.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)}
            expected={c['offset']:c for c in fixture['all_fixture_commands']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
            objects={r['fixture_command_offset']:r for r in fixture['all_original_exchange_commands']};native={r['id']:r for r in models['native_models'][version]}
            names={r['actor_ID']:r for r in models['name_planes']};nameinks={}
            for actor,n in names.items():
                plane=Path(n['native_plane']).read_bytes();assert sha(plane)==n['native_plane_sha256'];nameinks[actor]={(i%216,i//216) for i,v in enumerate(plane) if v}
            photos={}
            for p in report['frames_captured']:
                assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];im=Image.open(p['path']).convert('RGB');assert im.size==(256,384)
                photos[p['frame']]=dict(reference=p,image=im,masks216=masks(im,216),masks228=masks(im,228))
            pairs=[];speeches=[];following=[];unknown=[];normal=None;lastnext=None
            for ri,row in enumerate(trace['rows']):
                assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source']
                if s['classification']!='original_SC_cache':unknown.append(dict(row=ri,frame=row['frame'],source=s,after_return=bool(normal)));continue
                assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==s['registered_sha256']==sha(banks[s['route']][s['block']])
                if row['kind']!='after_command':continue
                if normal or (s['route'],s['block'])!=(1,42):
                    following.append(dict(frame=row['frame'],route=s['route'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']));continue
                entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];command=expected[at];word=command['word']
                assert entry['kind']=='before_command' and s['instruction_offset']==at and s['first_word']==word
                for observed in [entry,row]:
                    resident=observed['source'];assert (resident['route'],resident['block'])==(1,42) and resident['actual_sha256']==fixture['fixture_block_sha256']
                    assert resident['payload_bytes']==fixture['fixture_stored_bytes'] and resident['instruction_pointer']==resident['payload_address']+at
                    assert sha(Path(resident['actual_payload_file']).read_bytes())==fixture['fixture_block_sha256']
                if lastnext is not None:assert at==lastnext
                if word in [0x100,0x200,0x300,0x400]:
                    span=int.from_bytes(bytes.fromhex(command['whole_command_hex'])[2:4],'little');previous=entry['mode']
                    taken=word==0x100 or word==0x200 and previous==0 or word==0x300 and previous==1 or word==0x400 and previous==2
                    assert row['decoded_length']==4+(span if taken else 0)
                else:assert row['decoded_length']==command['native_extent']
                lastnext=at+row['decoded_length'];original=objects.get(at)
                pair=dict(fixture_offset=at,canonical_source_offset=None if original is None else original['canonical_clean_offset'],source_command_ordinal=None if original is None else original['source_command_ordinal'],word=word,start=entry['frame'],returned=row['frame'],duration=row['frame']-entry['frame'],entry_row=row['entry_row'],return_row=ri,decoded_length=row['decoded_length'],observed_previous_result=entry['mode'],native_result=row['result_words'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_before=entry['native_UI_request_words'],UI_after=row['native_UI_request_words']);pairs.append(pair)
                if word==0:
                    assert command['native_extent']==4 and row['result_words']==[0,pairs[-2]['native_result'][1]]==[0,selected]
                    normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True)
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
                    cp=oracle(arm,font,[e for e in page['events'] if e['kind']=='cp932']);cpgray={(i%216,i//216) for i,v in enumerate(cp) if v==15}&allgray;gray=allgray-cpgray
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
                if not holds:unresolved.append(dict(version=version,choice=choice,id=record['id'],kind='no-complete-body-and-name-orFE-absent-header-hold',partial=partial))
                speeches.append(dict(id=record['id'],source_selector=actor,name=None if FE else n['text'],start=entry['frame'],returned=row['frame'],pages=1,kind='system-FE' if FE else 'progressive',complete_holds=holds,nameholds=nameholds,partial_ortransition_samples=partial,selected_capture=holds[-1] if holds else None))
            assert normal and not unknown and [p['fixture_offset'] for p in pairs]==selected_path(fixture,selected)
            menu=next(p for p in pairs if p['word']==0x2100);assert menu['native_result']==[2,selected]
            expected_IDs=['DK4_MES_B49_R0040','DK4_MES_B49_R0043']+(['DK4_MES_B49_R0058'] if selected==0 else ['DK4_MES_B49_R0064','DK4_MES_B49_R0067','DK4_MES_B49_R0071','DK4_MES_B49_R0074'])+['DK4_MES_B49_R0081']
            assert [s['id'] for s in speeches]==expected_IDs and sum(s['source_selector']==254 for s in speeches)==1
            sheets=[]
            for first in range(0,len(speeches),4):
                complete=[s for s in speeches[first:first+4] if s['selected_capture']]
                if not complete:continue
                sheet=Image.new('RGB',(1024,410*((len(complete)+1)//2)),'#263238');draw=ImageDraw.Draw(sheet)
                for i,s in enumerate(complete):
                    hold=s['selected_capture'];x,y=i%2*512,i//2*410;draw.text((x+3,y+3),version+' '+choice+' '+s['id']+' frame'+str(hold['frame']),fill='white');sheet.paste(photos[hold['frame']]['image'].crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x,y+24))
                path=ROOT/f'{version}_{choice}_pages{first//4+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
            following_frame=min(f for f in photos if f>normal['frame']+60)
            FEhold=next(s['selected_capture'] for s in speeches if s['source_selector']==254)
            display=next(p for p in pairs if p['word']==0x4800);hide=next(p for p in pairs if p['word']==0x4700)
            item_frame=max(f for f in photos if display['returned']+20<f<hide['returned']-4)
            frames=[FEhold['frame'],item_frame,following_frame,10000] if FEhold else [item_frame,following_frame,10000]
            strip=Image.new('RGB',(256*len(frames),410),'#263238');draw=ImageDraw.Draw(strip)
            for i,f in enumerate(frames):draw.text((i*256+3,3),version+' '+choice+' '+str(f),fill='white');strip.paste(photos[f]['image'],(i*256,24))
            path=ROOT/f'{version}_{choice}_FE_item_return.png';strip.save(path);transitions=[dict(path=str(path),sha256=sha(path.read_bytes()),frames=frames)]
            for p in [folder/'terminal.json',folder/'run_plan.json',rp,tp,Path(terminal['menu_observer']),Path(terminal['readonly_menu_snapshots'])]:evidence[str(p)]=sha(p.read_bytes())
            groups.append(dict(version=version,choice=choice,block=49,fixture=fixture,capture_report=str(rp),observer=str(tp),run_folder=str(folder),actual_frames=10001,input_schedule_sha256=plan['inputs_sha256'],command_pairs=pairs,speeches=speeches,actual_menu_pair=menu,normal_return=normal,unvisited_conditional_text_IDs=[r['id'] for r in fixture['original_text_records'] if r['id'] not in expected_IDs],following_original_cache_commands=following,unknown_sources=unknown,review_sheets=sheets,transition_sheets=transitions,all_selected_command_boundaries_follow_native_results=True,all_selected_resident_payloads_exact_andcallbacks_readonly=True))
            print(version,choice,'speeches',len(speeches),'completeholds',sum(len(s['complete_holds']) for s in speeches),'menu',menu['native_result'],'normal',normal,flush=True)
    for choice in ['accept','decline']:
        pair=[g for g in groups if g['choice']==choice];assert len(pair)==2 and pair[0]['input_schedule_sha256']==pair[1]['input_schedule_sha256']
    assert len(groups)==4 and len({s['id'] for g in groups for s in g['speeches']})==8
    save(ROOT/'bounded_tail_actual.json',dict(groups=groups,unresolved=unresolved,total_actual_frames=40004,unique_tail_speeches=8,actual_source_English_page_occurrences=sum(len(g['speeches']) for g in groups),complete_body_name_orabsent_FE_header_holds=sum(len(s['complete_holds']) for g in groups for s in g['speeches']),all_observed_complete_glyph_masks_singlepages_names_native_flow_andreturns_pass=not unresolved,actual_menu_indices0_1_forwarded_as_original_state2_andnormal_end_carries0_1=True,all_five_source_relative_sites_preserved_in_bounded_tail=True,visual_review_pending=True,actual_menu_backing_visible_caption_highlights_andFE_VRAM_binding_separate_pending=True,bounded_original_possession_dialogue_tail_not_natural_event_inventory_quest_eligibility_trade_mechanics_original_location_fullroute_orhardware_proof=True,no_flags_inventory_RNG_party_roles_funds_results_orcontroller_retiming=True,new_credit=0,full_goal_complete=False,evidence=evidence))
    print('Four bounded tail captures audited;unresolved',len(unresolved),'unique8speech displays/bothchoices/native normalreturns. Actual menu backing/FE native binding anddirectview pending.No credit.')
