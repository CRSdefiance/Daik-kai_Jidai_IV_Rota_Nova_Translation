"""Independently reconstruct B31/B53 whole fixtures,traces andactual complete glyph/name holds."""
import struct
from copy import deepcopy
from pathlib import Path
from types import FunctionType
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels as original_pixels

COLORS=[(0,8,0),(98,97,98),(197,198,197)]

def check_fixtures(data,rows,parent,clean,rebuilt,require,number):
    rows=[r for r in rows if r["block"]==number]
    path='/data/SC1.DK4';arm=parent.read_file('/__arm9__.bin');inventory,_,_=scoped_inventory()
    before=IlnkContainer.parse(parent.read_file(path)).blocks;original=IlnkContainer.parse(clean.read_file(path)).blocks;target=IlnkContainer.parse(rebuilt['target_archive']).blocks
    opening=before[42];commands,speeches=inventory(arm,opening);first=speeches[0]['offset'];initializers=[c for c in commands if c['offset']<first];prelude=opening[8:first]
    require(first==42 and len(prelude)==34 and len(initializers)==8 and prelude==original[42][8:first],'eight original opening initializers/34byte prefix')
    source_commands,_=inventory(arm,original[number]);require(len(source_commands)==9,'all9 original block commands')
    canonical={}
    for scope,key in [('whole','fixtures')]:
        declared=[f for f in data[key]['fixtures'] if f['source_block']==number];require(len(declared)==2 and [f['version'] for f in declared]==['clean_Japanese','revised_English'],'two ordered original/reviewed '+scope+' fixtures')
        for f in declared:
            version=f['version'];selected=(original if version=='clean_Japanese' else target)[number];end=8+struct.unpack_from('<H',selected,4)[0]
            selected_commands,selected_speeches=inventory(arm,selected);require(len(selected_speeches)==len(rows) and len(selected_commands)==9,'complete selected block source commands')
            source_pairs={b['offset']:a for a,b in zip(source_commands,selected_commands,strict=True)}
            start=8;shift=34;entry=b'';outer=None;chosen=selected_commands
            logical=bytearray(opening[:8]+prelude+entry+selected[start:end]);struct.pack_into('<H',logical,4,len(logical)-8)
            block=bytes(logical)+bytes(-len(logical)%4);parsed,texts=inventory(arm,block)
            require(f['route']==1 and f['route_identity']=='Hodram' and f['source_block']==number and f['source_file']==path and f['fixture_block']==42,'source-qualified original-opening fixture')
            require(f['source_block_sha256']==sha(selected) and f['fixture_block_hex']==block.hex() and f['fixture_block_sha256']==sha(block) and f['fixture_stored_bytes']==len(block) and f['fixture_logical_end']==len(logical) and f['fixture_storage_tail_bytes']==len(block)-len(logical),'independent entire fixture/header/tail')
            require(f['original_opening_prelude_hex']==prelude.hex() and f['original_opening_prelude_commands']==initializers and f['all_fixture_commands']==parsed,'exact original prelude/whole fixture command census')
            objects=[];members=[];relative=0;menus=[]
            for c in chosen:
                a=source_pairs[c['offset']];ordinal=source_commands.index(a);at=c['offset']+34 if scope=='tail' and c['offset']<12 else c['offset']+shift
                actual=next(p for p in parsed if p['offset']==at)
                ancestors=[v+shift for v in c['ancestor_0100_offsets'] if v!=outer]
                require(actual['word']==a['word']==c['word'] and actual['native_extent']==c['native_extent'] and actual['whole_command_hex']==c['whole_command_hex'] and actual['ancestor_0100_offsets']==ancestors,'every original command/full extent/ancestor membership')
                if c['word'] in [0x100,0x200,0x300,0x400]:
                    span=struct.unpack_from('<H',selected,c['offset']+2)[0];require(at+4+span==c['offset']+4+span+shift,'unchanged internal relative operand');relative+=1
                record=next((r for r in rows if r['source_reference']['header_offset']==a['offset']),None) if c['word']==0x4000 else None
                objects.append(dict(original_block=number,source_command_ordinal=ordinal,canonical_clean_offset=a['offset'],original_command_offset=c['offset'],fixture_command_offset=at,native_extent=c['native_extent'],word=c['word'],whole_command_hex=c['whole_command_hex'],text_ID=None if record is None else record['id'],original_0100_ancestors=c['ancestor_0100_offsets'],fixture_0100_ancestors=ancestors))
                if record is not None:
                    require(block[at:at+6].hex()==record['source_complete_preamble_hex'],'actual fixture complete sixbyte preamble')
                    members.append(dict(id=record['id'],source_record_index=record['source_reference']['record_index'],source_selector=record['source_selector'],source_reference=record['source_reference'],fixture_command_offset=at,fixture_body_offset=at+5))
                if scope=='tail' and c['word']==0x2100:
                    base=at+6
                    for i in [0,1]:
                        label_at=base+struct.unpack_from('<H',block,at+2+2*i)[0];value=block[label_at:block.index(0,label_at)]
                        label=f['original_menu_records'][i]
                        require(label['option_index']==i and label['fixture_header_offset']==at and label['fixture_label_offset']==label_at and label['label_hex']==value.hex() and label['label']==value.decode('cp932') and label['fixture_record_index']==block[:label_at].count(b'\0'),'both exact original table/source-index label references')
                        menus.append(label)
            require(objects==f['all_original_exchange_commands'] and members==f['original_text_records'] and relative==f['source_relative_sites']==(4 if number==31 else 0),'complete selected original command/record/relative membership')
            require(len(objects)==9 and len(texts)==len(rows) and len(parsed)==len(objects)+8,'exact whole/bounded fixture membership counts')
            if scope=='whole':
                require(f['constant_shift_bytes']==34,'whole fixture unchanged relative shift')
                for k in ['no_original_speech_branch_resource_effect_orend_omitted','all_relative_operands_unchanged_under_constant34byte_shift','all_other_ROM_bytes_recoverable_by_exact_opening_archive_inverse','initialized_original_Hodram_opening_not_original_event_location_oractivation','no_conditions_RNG_party_roster_funds_orresults_forced']:require(f[k] is True,'whole source scope:'+k)
            else:
                require(len(menus)==2 and f['no_selected_tail_speech_choice_branch_effect_picture_hide_orend_omitted'] and f['all_five_internal_relative_operands_unchanged'] and f['all_other_ROM_bytes_recoverable_by_exact_opening_inverse'],'bounded tail complete controls/scope')
            rompath=Path(f['research_ROM']);image=NdsImage.open(rompath)
            require(sha(rompath.read_bytes())==f['research_ROM_sha256'] and f['parent_sha256']==sha(bytes(parent.rom.save())),'whole actual fixture/parent in-memory identity')
            require(all(image.read_file(p)==v for p,v in parent.iter_components()) and [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==[path],'only SC1 fixture file/no component edit')
            bank=IlnkContainer.parse(image.read_file(path)).blocks;require(len(bank)==325 and bank[42]==block and all(a==b for i,(a,b) in enumerate(zip(before,bank,strict=True)) if i!=42),'only original opening block changes')
            inverse=deepcopy(image);inverse.replace_file(path,parent.read_file(path));require(bytes(inverse.rom.save())==bytes(parent.rom.save()),'whole actual fixture parent ROM inverse')
            canonical[number,scope,version]=dict(declared=f,image=image,block=block,commands={c['offset']:c for c in parsed},objects={c['fixture_command_offset']:c for c in objects},records={r['fixture_command_offset']:r for r in members})
    return canonical

def pixel_masks(image,width):
    values=image.crop((16,296,16+width,360)).get_flattened_data()
    return {c:{(i%width,i//width) for i,v in enumerate(values) if v==c} for c in COLORS}

def check_actual(data,rows,parent,clean,rebuilt,native,load,require):
    canonical={}
    arm,font=parent.read_file('/__arm9__.bin'),parent.read_file('/GRP/KANJI.FNT')
    oracle=FunctionType(original_pixels.__code__,{**original_pixels.__globals__,'CURRENT_ARM9':sha(arm)},argdefs=original_pixels.__defaults__)
    names=native['names'];nameinks={actor:{(i%216,i//216) for i,v in enumerate(n['plane']) if v} for actor,n in names.items()}
    observations={r['id']:[] for r in rows};results=[];totalholds=0;page_occurrences=0
    for number,key in [(31,'B31_actual'),(53,'B53_actual')]:
        scope='whole';canonical.update(check_fixtures(data,rows,parent,clean,rebuilt,require,number))
        proof=data[key];require(proof['unresolved']==[],'actual proof hasno unresolved body/header/flow:'+scope)
        groups=proof['groups'];require(len(groups)==(2 if scope=='whole' else 4),'exact actual language/choice group count')
        if scope=='whole':require([g['version'] for g in groups]==['clean_Japanese','revised_English'],'ordered whole-source languages')
        else:require([(g['choice'],g['version']) for g in groups]==[(c,v) for c in ['accept','decline'] for v in ['clean_Japanese','revised_English']],'ordered tail languages/both choices')
        for group in groups:
            version=group['version'];choice=group.get('choice');f=canonical[number,scope,version]
            require(group['fixture']==f['declared'] and group['block']==number and group['actual_frames']==6001,'actual fixture/group identity')
            root=Path('work/analysis/Hodram_B31_B53_scene_runs_v8740')/f'route1_B{number}_{version}'
            terminal,plan=map(load,[root/'terminal.json',root/'run_plan.json']);rp,tp=Path(terminal['report']),Path(terminal['observer']);report,trace=map(load,[rp,tp])
            require(terminal['terminal'] and terminal['frames']==plan['frames']==report['frames']==6001 and terminal['all_callbacks_readonly_andhost_slots_restored'],'terminal readonly actual run')
            require(sha(rp.read_bytes())==terminal['report_sha256'] and sha(tp.read_bytes())==terminal['observer_sha256'] and sha((root/'run_plan.json').read_bytes())==terminal['run_plan_sha256'],'capture/trace/plan exact immutable files')
            require(group['capture_report']==str(rp) and group['observer']==str(tp) and report['ROM_sha256']==f['declared']['research_ROM_sha256'],'actual full ROM/capture/trace ownership')
            require(report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not report['goal_complete'] and not report['hardware_device_verification'] and not any(v for k,v in report.items() if k.startswith('synthetic_')),'coldboot no synthetic state/fullroute/hardware claim')
            require(not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact'],'original observer callbacks/core restoration')
            base=load('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json')
            schedule=base+[dict(start=frame,duration=5,buttons=['A']) for frame in range(4000,5521,240)]
            if choice=='decline':schedule=sorted(schedule+[dict(start=4350,duration=5,buttons=['DOWN'])],key=lambda r:r['start'])
            require(report['scripted_input_schedule']==load(plan['inputs'])==schedule and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256'],'exact ordinary controller schedule/no retiming')
            photos={}
            for p in report['frames_captured']:
                require(sha(Path(p['path']).read_bytes())==p['PNG_sha256'],'actual full PNG digest')
                pic=Image.open(p['path']).convert('RGB');require(pic.size==(256,384),'native screenshot dimensions')
                photos[p['frame']]=dict(reference=p,image=pic,masks216=pixel_masks(pic,216),masks228=pixel_masks(pic,228))
            banks={i:IlnkContainer.parse(f['image'].read_file(f'/data/SC{i}.DK4')).blocks for i in range(4)}
            pairs=[];speechrows=[];following=[];unknown=[];last=None;normal=None
            for ri,row in enumerate(trace['rows']):
                require(row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'],'every original callback readonly');s=row['source']
                if s['classification']!='original_SC_cache':unknown.append(ri);continue
                require(s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==s['registered_sha256']==sha(banks[s['route']][s['block']]),'complete original resident source payload/ROM')
                values=struct.unpack('<32I',bytes.fromhex(row['CPU128_hex']));require(values[2]==row['PC'] and values[17]==row['player'],'original CPU/stack descriptor association')
                if row['kind']!='after_command':continue
                if normal is not None or (s['route'],s['block'])!=(1,42):
                    following.append(dict(frame=row['frame'],route=s['route'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']));continue
                entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];c=f['commands'][at];word=c['word']
                require(entry['kind']=='before_command' and s['instruction_offset']==at and s['first_word']==word,'native whole command entry/return')
                for observed in [entry,row]:
                    resident=observed['source'];require((resident['route'],resident['block'])==(1,42) and resident['actual_sha256']==sha(f['block']) and resident['payload_bytes']==len(f['block']) and resident['instruction_pointer']==resident['payload_address']+at and sha(Path(resident['actual_payload_file']).read_bytes())==sha(f['block']),'whole current fixture resident payload andinstruction pointer')
                require(last is None or at==last,'unbroken original command sequence')
                if word in [0x100,0x200,0x300,0x400]:
                    span=struct.unpack_from('<H',f['block'],at+2)[0];v=entry['mode'];taken=word==0x100 or word==0x200 and v==0 or word==0x300 and v==1 or word==0x400 and v==2
                    require(row['decoded_length']==4+(span if taken else 0),'original relative control/result endpoint')
                else:require(row['decoded_length']==c['native_extent'],'original complete command extent')
                last=at+row['decoded_length'];original=f['objects'].get(at)
                pair=dict(fixture_offset=at,canonical_source_offset=None if original is None else original['canonical_clean_offset'],source_command_ordinal=None if original is None else original['source_command_ordinal'],word=word,start=entry['frame'],returned=row['frame'],duration=row['frame']-entry['frame'],entry_row=row['entry_row'],return_row=ri,decoded_length=row['decoded_length'],observed_previous_result=entry['mode'],native_result=row['result_words'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_before=entry['native_UI_request_words'],UI_after=row['native_UI_request_words']);pairs.append(pair)
                if word==0:
                    require(c['native_extent']==4 and row['result_words']==[0,pairs[-2]['native_result'][1]],'original normal fourbyte end/value carry')
                    normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True)
                    if number==53:normal.update(previous_parser_result_value=pairs[-2]['native_result'][1],separate_interpreter_carried_mode=entry['mode'],source_proven_distinct_channels_not_assumed_equal=True)
                if at not in f['records']:continue
                record=f['records'][at];ident=record['id'];actor=record['source_selector'];FE=actor==254
                model=native['bodies'][version][ident];page=model['pages'][0];plane=page['native_plane_bytes'];require(model['source_selector']==actor,'actual glyph model source consumer')
                if FE:
                    physical=page['physical_plane_bytes'];black={(i%228,i//228) for i,v in enumerate(physical) if v==15};gray=set();cpgray={(i%228,i//228) for i,v in enumerate(physical) if v==14};name=None
                else:
                    black={(i%216,i//216) for i,v in enumerate(plane) if v==1};allgray={(i%216,i//216) for i,v in enumerate(plane) if v==15}
                    cp=oracle(arm,font,[e for e in page['events'] if e['kind']=='cp932']);cpgray={(i%216,i//216) for i,v in enumerate(cp) if v==15}&allgray;gray=allgray-cpgray;name=names[actor]
                wanted=dict(zip(COLORS,[black,gray,cpgray],strict=True));holds=[];nameholds=[];partial=[]
                for frame,photo in photos.items():
                    if not entry['frame']+20<frame<row['frame']-4:continue
                    pic=photo['image'];found={(x-16,y-276) for y in range(276,289) for x in range(14,244 if FE else 18+name['width']) if pic.getpixel((x,y))==COLORS[1]}
                    nameok=not found if FE else found==nameinks[actor]
                    if nameok:nameholds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],FE_absent_nameplate=FE))
                    diffs={str(color):len(photo['masks228' if FE else 'masks216'][color]^wanted[color]) for color in COLORS}
                    if any(diffs.values()) or not nameok:partial.append(dict(frame=frame,body_differences=diffs,name_pixels=len(found),not_counted_as_complete=True));continue
                    holds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],native_page=1,complete_black_ASCII_gray_CP932_gray_leading_internal_final_glyph_masks_equal=True,complete_name_mask_equal=not FE,original_FE_absent_nameplate_preserved=FE,actual_name=None if FE else name['text'],native_geometry=[228 if FE else 216,64]))
                require(holds,'complete actual body/name-orabsent-FE-header hold:'+ident)
                speech=dict(id=ident,source_selector=actor,name=None if FE else name['text'],start=entry['frame'],returned=row['frame'],pages=1,complete_holds=holds,nameholds=nameholds,partial_ortransition_samples=partial,selected_capture=holds[-1])
                speech['kind']='system-FE' if FE else 'progressive'
                speechrows.append(speech);totalholds+=len(holds);page_occurrences+=1
                observations[ident].append(dict(version=version,source_selector=actor,name=None if FE else name['text'],selected_capture=holds[-1],complete_holds=len(holds)))
            require(not unknown and normal==group['normal_return'] and pairs==group['command_pairs'] and speechrows==group['speeches'] and following==group['following_original_cache_commands'],'every independently reconstructed actual trace/hold/header/return/following-command field')
            require(group['unknown_sources']==[],'no unidentified actual source')
            ids=['DK4_MES_B31_R0018'] if number==31 else ['DK4_MES_B53_R0007'];require(len(pairs)==(15 if number==31 else 17) and not any(p['word']==0x2100 for p in pairs),'whole block selected commands/one observed speech/no menu')
            path=[8,10,18,22,90,188,192] if number==31 else [8,10,12,98,106,114,122,130,132]
            require([p['canonical_source_offset'] for p in pairs if p['source_command_ordinal'] is not None]==path,'complete unforced selected native source path')
            require([s['id'] for s in speechrows]==ids and group['unvisited_conditional_text_IDs']==[r['id'] for r in f['declared']['original_text_records'] if r['id'] not in ids],'exact observed andexplicitly unvisited source memberships')
            results.append(dict(block=number,scope=scope,version=version,choice=choice,actual_pages=len(speechrows),complete_holds=sum(len(s['complete_holds']) for s in speechrows),normal_return=normal,original_selected_commands=len(pairs)-8,all_trace_source_payloads_inputs_callbacks_andnormal_returns_bound=True))
    expected_observations={r['id']:[] for r in rows}
    for number,key in [(31,'B31_actual'),(53,'B53_actual')]:
        for group in data[key]['groups']:
            for speech in group['speeches']:
                expected_observations[speech['id']].append(dict(version=group['version'],source_selector=speech['source_selector'],name=speech['name'],selected_capture=speech['selected_capture'],complete_holds=len(speech['complete_holds'])))
    for row in rows:
        require(observations[row['id']]==expected_observations[row['id']],'independent scoped per-record actual approval:'+row['id'])
        require(bool(observations[row['id']])==(row['actual_observation_status']=='paired-whole-script-body-name-andportrait-observed'),'approved actual versus offline-only scope:'+row['id'])
    require(sorted(k for k,v in observations.items() if v)==data['actual_review']['actual_unique_text_IDs'] and data['actual_review']['offline_only_text_IDs']==['DK4_MES_B31_R0013'],'two observed utterances andone explicitly unvisited short variant')
    require(len(results)==4 and page_occurrences==4 and totalholds==76,'four actual groups/four page occurrences/76 complete body-name holds')
    return dict(summary=dict(actual_groups=results,whole_actual_frames=24004,complete_actual_page_occurrences=4,complete_actual_holds=76,unique_speech_IDs=2,all18_original_commands_retained_unforced_selected_paths_andnormal_resultword_channels_verified=True,full_fixture_ROM_inverses_use_parent_memory_not_source_path=True,all_actual_source_inputs_resident_payloads_callbacks_andnative_planes_independently_checked=True,new_emulator_runs=0),canonical_fixtures=canonical)
