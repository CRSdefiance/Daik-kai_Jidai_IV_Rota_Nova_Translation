"""Recompute whole source/revised fixture ownership, original traces and complete actual glyph/name holds."""
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

def fixtures(data,rows,parent,clean,rebuilt,require):
    inventory,_,_=scoped_inventory();arm=parent.read_file('/__arm9__.bin');path='/data/SC1.DK4';before=IlnkContainer.parse(parent.read_file(path)).blocks;original=IlnkContainer.parse(clean.read_file(path)).blocks;target=IlnkContainer.parse(rebuilt['target_archive']).blocks
    opening=before[42];commands,speeches=inventory(arm,opening);first=speeches[0]['offset'];initializers=[c for c in commands if c['offset']<first];prelude=opening[8:first]
    require(first==42 and len(prelude)==34 and len(initializers)==8 and prelude==original[42][8:first],'eight original opening initializers/34byte prefix')
    declared=data['fixtures']['fixtures'];require(len(declared)==4 and {(f['source_block'],f['version']) for f in declared}=={(b,v) for b in [47,48] for v in ['clean_Japanese','revised_English']},'four complete source/revised outcome fixtures')
    canonical={}
    for f in declared:
        number=f['source_block'];version=f['version'];selected=(original if version=='clean_Japanese' else target)[number];end=8+struct.unpack_from('<H',selected,4)[0]
        selected_commands,selected_speeches=inventory(arm,selected);source_commands,_=inventory(arm,original[number]);require(len(selected_speeches)==3,'complete three-utterance outcome source')
        logical=bytearray(opening[:8]+prelude+selected[8:end]);struct.pack_into('<H',logical,4,len(logical)-8);block=bytes(logical)+bytes(-len(logical)%4);parsed,texts=inventory(arm,block)
        require(f['route']==1 and f['route_identity']=='Hodram' and f['source_file']==path and f['fixture_block']==42,'source-qualified original-opening fixture')
        require(f['source_block_sha256']==sha(selected) and f['fixture_block_hex']==block.hex() and f['fixture_block_sha256']==sha(block) and f['fixture_stored_bytes']==len(block) and f['fixture_logical_end']==len(logical) and f['fixture_storage_tail_bytes']==len(block)-len(logical),'independent entire fixture payload/header/tail')
        require(f['original_opening_prelude_hex']==prelude.hex() and f['original_opening_prelude_commands']==initializers and f['constant_shift_bytes']==34 and f['all_fixture_commands']==parsed,'exact source prelude andwhole native command census')
        objects=[];members=[]
        for ordinal,(a,b) in enumerate(zip(source_commands,selected_commands,strict=True)):
            at=b['offset']+34;actual=next(c for c in parsed if c['offset']==at);require(actual['word']==a['word']==b['word'] and actual['native_extent']==b['native_extent'] and actual['whole_command_hex']==b['whole_command_hex'],'complete source/target effect/command in fixture')
            record=next((r for r in rows if r['block']==number and r['source_reference']['header_offset']==a['offset']),None) if a['word']==0x4000 else None
            objects.append(dict(original_block=number,source_command_ordinal=ordinal,canonical_clean_offset=a['offset'],original_command_offset=b['offset'],fixture_command_offset=at,native_extent=b['native_extent'],word=b['word'],whole_command_hex=b['whole_command_hex'],text_ID=None if record is None else record['id'],original_0100_ancestors=b['ancestor_0100_offsets'],fixture_0100_ancestors=actual['ancestor_0100_offsets']))
            if record is not None:members.append(dict(id=record['id'],source_record_index=record['source_reference']['record_index'],source_selector=record['source_selector'],source_reference=record['source_reference'],fixture_command_offset=at,fixture_body_offset=at+5))
        require(f['all_original_exchange_commands']==objects and f['original_text_records']==members and f['source_relative_sites']==0 and len(texts)==3 and len(parsed)==len(objects)+8,'all fixture command/text source memberships')
        for key in ['no_original_speech_branch_resource_effect_orend_omitted','all_relative_operands_unchanged_under_constant34byte_shift','all_other_ROM_bytes_recoverable_by_exact_opening_archive_inverse','initialized_original_Hodram_opening_not_original_event_location_oractivation','no_conditions_RNG_party_roster_funds_orresults_forced']:
            require(f[key] is True,'disclosed whole-fixture scope:'+key)
        rompath=Path(f['research_ROM']);image=NdsImage.open(rompath);require(sha(rompath.read_bytes())==f['research_ROM_sha256'],'actual fixture complete ROM identity')
        require(all(image.read_file(p)==v for p,v in parent.iter_components()) and [p for _,p,v in parent.iter_files() if image.read_file(p)!=v]==[path],'only fixture SC1 archive/no code orother file edit')
        bank=IlnkContainer.parse(image.read_file(path)).blocks;require(len(bank)==325 and bank[42]==block and all(a==b for i,(a,b) in enumerate(zip(before,bank,strict=True)) if i!=42),'only original opening block changed in actual fixture')
        inverse=deepcopy(image);inverse.replace_file(path,parent.read_file(path));require(bytes(inverse.rom.save())==bytes(parent.rom.save()),'whole actual fixture parent ROM inverse')
        canonical[number,version]=dict(declared=f,image=image,block=block,commands={c['offset']:c for c in parsed},objects={c['fixture_command_offset']:c for c in objects},records={r['fixture_command_offset']:r for r in members})
    return canonical

def pixel_masks(image,width):
    values=image.crop((16,296,16+width,360)).get_flattened_data()
    return {c:{(i%width,i//width) for i,v in enumerate(values) if v==c} for c in COLORS}

def check_actual(data,rows,parent,clean,rebuilt,native,load,require):
    canonical=fixtures(data,rows,parent,clean,rebuilt,require);arm=parent.read_file('/__arm9__.bin');font=parent.read_file('/GRP/KANJI.FNT');pixel_oracle=FunctionType(original_pixels.__code__,{**original_pixels.__globals__,'CURRENT_ARM9':sha(arm)},argdefs=original_pixels.__defaults__)
    name=native['name'];nameink={(i%216,i//216) for i,v in enumerate(name['plane']) if v};results=[];totalholds=0
    for number in [47,48]:
        proof=data['actual'+str(number)];require(proof['unresolved']==[] and proof['all_observed_complete_body_name_orFE_absent_header_holds_andnative_flow_pass'] is True,'actual whole-outcome proof has no unresolved body/header/flow')
        require([g['version'] for g in proof['groups']]==['clean_Japanese','revised_English'],'two ordered actual language groups')
        for group in proof['groups']:
            version=group['version'];f=canonical[number,version];require(group['fixture']==f['declared'] and group['block']==number and group['actual_frames']==10001,'actual group/fixture/frame identity')
            root=Path('work/analysis/Hodram_outcome_scene_runs_v8333' if number==47 else 'work/analysis/Hodram_outcome_FE_scene_runs_v8333b')/f'route1_B{number}_{version}'
            terminal,plan=map(load,[root/'terminal.json',root/'run_plan.json']);rp,tp=Path(terminal['report']),Path(terminal['observer']);report,trace=map(load,[rp,tp])
            require(terminal['terminal'] and terminal['frames']==plan['frames']==report['frames']==10001 and terminal['all_callbacks_readonly_andhost_slots_restored'],'terminal readonly whole-scene capture')
            require(sha(rp.read_bytes())==terminal['report_sha256'] and sha(tp.read_bytes())==terminal['observer_sha256'] and sha((root/'run_plan.json').read_bytes())==terminal['run_plan_sha256'],'capture/trace/plan exact files')
            require(group['capture_report']==str(rp) and group['observer']==str(tp) and report['ROM_sha256']==f['declared']['research_ROM_sha256'],'actual group exact ROM/capture/trace ownership')
            require(report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not report['goal_complete'] and not report['hardware_device_verification'] and not any(v for k,v in report.items() if k.startswith('synthetic_')),'ordinary coldboot no synthetic-state orfullroute/hardware claim')
            require(not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact'],'original callback/core restoration/error guards')
            base=load('work/analysis/hodram_opening_context_v2018/ordinary_Hodram_NewGame_inputs.json');schedule=base+[dict(start=frame,duration=5,buttons=['A']) for frame in range(4000,10001-480,240)]
            require(report['scripted_input_schedule']==load(plan['inputs'])==schedule and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']==group['input_schedule_sha256'],'exact ordinary same-controller schedule/no retiming')
            photos={}
            for p in report['frames_captured']:
                require(sha(Path(p['path']).read_bytes())==p['PNG_sha256'],'complete actual PNG digest');picture=Image.open(p['path']).convert('RGB');require(picture.size==(256,384),'whole native capture dimensions');photos[p['frame']]=dict(reference=p,image=picture,masks216=pixel_masks(picture,216),masks228=pixel_masks(picture,228))
            banks={i:IlnkContainer.parse(f['image'].read_file(f'/data/SC{i}.DK4')).blocks for i in range(4)};pairs=[];speechrows=[];following=[];unknown=[];last=None;normal=None
            for ri,row in enumerate(trace['rows']):
                require(row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'],'every original callback readonly');s=row['source']
                if s['classification']!='original_SC_cache':unknown.append(ri);continue
                require(s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==s['registered_sha256']==sha(banks[s['route']][s['block']]),'actual complete resident source payload/ROM association')
                values=struct.unpack('<32I',bytes.fromhex(row['CPU128_hex']));require(values[2]==row['PC'] and values[17]==row['player'],'actual original CPU/stack descriptor association')
                if row['kind']!='after_command':continue
                if normal is not None or (s['route'],s['block'])!=(1,42):following.append(dict(frame=row['frame'],route=s['route'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']));continue
                entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];c=f['commands'][at];require(entry['kind']=='before_command' and s['instruction_offset']==at and s['first_word']==c['word'] and row['decoded_length']==c['native_extent'],'native whole command entry/return/extent')
                for observed in [entry,row]:
                    resident=observed['source'];require(resident['route']==1 and resident['block']==42 and resident['actual_sha256']==sha(f['block']) and resident['payload_bytes']==len(f['block']) and resident['instruction_pointer']==resident['payload_address']+at and sha(Path(resident['actual_payload_file']).read_bytes())==sha(f['block']),'complete current fixture payload/command pointer')
                require(last is None or at==last,'unbroken original linear source command sequence');last=at+row['decoded_length'];original=f['objects'].get(at)
                pair=dict(fixture_offset=at,canonical_source_offset=None if original is None else original['canonical_clean_offset'],source_command_ordinal=None if original is None else original['source_command_ordinal'],word=c['word'],start=entry['frame'],returned=row['frame'],duration=row['frame']-entry['frame'],entry_row=row['entry_row'],return_row=ri,decoded_length=row['decoded_length'],observed_previous_result=entry['mode'],native_result=row['result_words'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_before=entry['native_UI_request_words'],UI_after=row['native_UI_request_words']);pairs.append(pair)
                if c['word']==0:
                    require(c['native_extent']==4 and row['result_words']==[0,pairs[-2]['native_result'][1]],'complete original fourbyte end carries previous value');normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True)
                if at not in f['records']:continue
                record=f['records'][at];ident=record['id'];actor=record['source_selector'];is_FE=actor==254;model=native['bodies'][version][ident];page=model['pages'][0];plane=page['native_plane_bytes'];require(model['source_selector']==actor,'actual glyph model source consumer')
                if is_FE:
                    physical=page['physical_plane_bytes'];black={(i%228,i//228) for i,v in enumerate(physical) if v==15};gray=set();cpgray={(i%228,i//228) for i,v in enumerate(physical) if v==14}
                else:
                    black={(i%216,i//216) for i,v in enumerate(plane) if v==1};allgray={(i%216,i//216) for i,v in enumerate(plane) if v==15};cp=pixel_oracle(arm,font,[e for e in page['events'] if e['kind']=='cp932']);cpgray={(i%216,i//216) for i,v in enumerate(cp) if v==15}&allgray;gray=allgray-cpgray
                expected=dict(zip(COLORS,[black,gray,cpgray],strict=True));holds=[];nameholds=[];partial=[]
                for frame,photo in photos.items():
                    if not entry['frame']+20<frame<row['frame']-4:continue
                    picture=photo['image'];actualname={(x-16,y-276) for y in range(276,289) for x in range(14,244 if is_FE else 18+name['width']) if picture.getpixel((x,y))==COLORS[1]};nameok=not actualname if is_FE else actualname==nameink
                    if nameok:nameholds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],FE_absent_nameplate=is_FE))
                    diffs={str(color):len(photo['masks228' if is_FE else 'masks216'][color]^expected[color]) for color in COLORS}
                    if any(diffs.values()) or not nameok:partial.append(dict(frame=frame,body_differences=diffs,name_pixels=len(actualname),not_counted_as_complete=True));continue
                    holds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],native_page=1,complete_black_ASCII_gray_CP932_gray_leading_internal_final_glyph_masks_equal=True,complete_name_mask_equal=not is_FE,original_FE_absent_nameplate_preserved=is_FE,actual_name=None if is_FE else name['text'],native_geometry=[228 if is_FE else 216,64]))
                require(holds,'at least one complete actual body/name orFE-absent-header hold:'+ident)
                speechrows.append(dict(id=ident,source_selector=actor,name=None if is_FE else name['text'],start=entry['frame'],returned=row['frame'],pages=1,kind='system-FE' if is_FE else 'progressive',complete_holds=holds,nameholds=nameholds,partial_ortransition_samples=partial,selected_capture=holds[-1]));totalholds+=len(holds)
            require(not unknown and normal==group['normal_return'] and pairs==group['command_pairs'] and speechrows==group['speeches'] and following==group['following_original_cache_commands'],'independent every actual trace/hold/header/return andlater-command field')
            require(len(pairs)==len(f['commands'])==(13 if number==47 else 18) and len(speechrows)==3 and group['unvisited_conditional_text_IDs']==[] and group['unknown_sources']==[],'all original initialized fixture commands/speeches visited')
            for speech in speechrows:
                approved=next(r for r in rows if r['id']==speech['id']);observation=next(o for o in approved['actual_display_observations'] if o['version']==version);require(observation['speech']==speech,'actual complete observation matches independently frozen per-record approval')
            results.append(dict(block=number,version=version,original_commands=5 if number==47 else 10,initializer_commands=8,actual_pages=3,complete_holds=sum(len(s['complete_holds']) for s in speechrows),normal_return=normal,all_trace_source_payloads_inputs_andcallbacks_bound=True))
    require(totalholds==100 and len(results)==4,'all100 complete source/revised body/name orFE-absent-header holds')
    return dict(actual_whole_scene_groups=results,whole_scene_frames=40004,complete_actual_pages=12,complete_actual_holds=100,all15_original_exchange_commands_bound_perlanguage=True,all_callbacks_readonly_andall_original_inputs_andfull_ROM_fixtures_independently_checked=True,new_emulator_runs=0)
