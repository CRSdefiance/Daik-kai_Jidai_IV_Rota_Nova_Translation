"""Independent native body/name masks and recorded actual command associations; read-only, no ROM commit."""
from pathlib import Path
from PIL import Image
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.research_lil_B209_native_pages_v6461 import pages as original_pages
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes

MODEL='work/analysis/Gerhard_actual_models_v8226/five_previous_body_planes_revised_exact_reuses_three_header_consumers.json'
PAGE_ADAPTER_SHA='dd68fc4a4eac0acaaa11984b30c0359129c4eca3e17dac13043ac3638f547cc1'
COLORS=((0,8,0),(98,97,98),(197,198,197))
VERSIONS=('parent_English','revised_English')

def expanded(raw):return raw.replace(b'FI',b'Lil').replace(b'FA',b'Argot').replace(b'FO',b'Argot Co.')

def check_evidence(data,rows,parent,reference,rebuilt,load,require):
    actual,native,stored,approval=[data[k] for k in ['actual','native_fonts','native_stored','actual_approval']]
    require(not actual['unresolved'] and len(actual['groups'])==6,'six scoped actual groups without unresolved masks')
    require(actual['complete_body_holds']==30 and actual['relevant_name_holds']==262,'30 body and262 name holds')
    require(actual['new_actual_frames']==int('152006') and actual['additional_B27_intro_display8_of8_is_not_full_branch_controlflow_ornatural_activation'],'actual initial frame/intro scope')
    require(actual['original_Hamburg_choice_selected_option0_only_option1_individual_actual_coverage_not_claimed'],'only original menu option0 observed')
    wanted={r['id'] for r in rows}
    require(set(actual['complete_changed_body_IDs_revised'])==wanted and len(native['records'])==len(stored['records'])==5,'five complete individual body proofs')
    require(native['fresh_compiled_alignment_cases']==20 and native['complete_progressive_pages']==5,'five native pages/twenty alignments')
    require(stored['fresh_native_alignment_cases']==4 and stored['exact_reused_native_alignment_cases']==16,'one fresh parity tail/four exact native bodies')
    require(len(approval['directly_viewed_sheets'])==11 and all(s['directly_viewed'] and sha(Path(s['path']).read_bytes())==s['sha256'] for s in approval['directly_viewed_sheets']),'eleven directly viewed sheet bindings')
    specs=[('whole',27,v) for v in VERSIONS]+[('whole',74,v) for v in VERSIONS]+[('intro-display',27,v) for v in VERSIONS]
    require([(g['scope'],g['block'],g['version']) for g in actual['groups']]==specs,'complete ordered actual fixture scopes')
    for row in rows:
        observations=[dict(scope=g['scope'],version=g['version'],block=g['block'],speech=s) for g in actual['groups'] for s in g['speeches'] if s['id']==row['id']]
        require(observations==row['actual_display_observations'],'frozen individual actual observations:'+row['id'])
    models=load(MODEL)
    require(sha(models['source_owned_page_adapter'].encode())==PAGE_ADAPTER_SHA,'exact original guarded native page adapter')
    require(set(models['native_models'])==set(models['name_planes'])==set(VERSIONS),'both original model versions')
    arm,font=parent.read_file('/__arm9__.bin'),parent.read_file('/GRP/KANJI.FNT')
    env={**original_pages.__globals__,'expected_pixels':expected_pixels,'codes':codes}
    exec(compile(models['source_owned_page_adapter'],__file__+'::guarded-original-pages','exec'),env)
    bodyplanes={};nameplanes={}
    for version in VERSIONS:
        bodymodels=models['native_models'][version];names=models['name_planes'][version]
        require(len(bodymodels)==5 and {r['id'] for r in bodymodels}==wanted,'complete unique native model IDs')
        require(len(names)==3 and {r['actor_ID'] for r in names}=={1,9,16},'three original header consumers')
        for row in rows:
            model=next(m for m in bodymodels if m['id']==row['id'])
            text=expanded(bytes.fromhex(row['current_hex'] if version=='parent_English' else row['compiled_hex'])[1:])
            require(model['expanded_native_hex']==text.hex() and model['source_selector']==row['source_selector'],'native source-bound model body:'+row['id'])
            fresh=env['pages'](arm,font,text)
            require(len(fresh['pages'])==len(model['pages'])==1 and fresh['complete_consumed_bytes']==len(text),'fresh complete single native page:'+row['id'])
            page,declared=fresh['pages'][0],model['pages'][0];plane=bytes.fromhex(page['native_plane_hex'])
            require(plane==Path(declared['native_plane']).read_bytes() and sha(plane)==declared['native_plane_sha256'],'recomputed every native model pixel:'+row['id'])
            for field in ['start','end','consumed_hex','events','first_visible_origin']:
                require(page[field]==declared[field],'native glyph/event/consumption metadata:'+row['id']+':'+field)
            if version=='revised_English':
                nf=next(n for n in native['records'] if n['id']==row['id']);st=next(n for n in stored['records'] if n['id']==row['id'])
                require(nf['compiled_hex']==row['compiled_hex'] and st['compiled_hex']==row['compiled_hex'] and st['stored_hex']==row['final_stored_hex'],'compiled/stored individual bodies:'+row['id'])
                require(st['compiler_owned_parity_space']==row['compiler_owned_parity_space'],'individual stored parity ownership:'+row['id'])
                complete=expanded(bytes.fromhex(st['stored_hex'])[1:]);require(st['expanded_stored_hex']==complete.hex(),'stored native macro expansion:'+row['id'])
                if complete!=text:
                    tail=env['pages'](arm,font,complete);require(len(tail['pages'])==1 and tail['complete_consumed_bytes']==len(complete) and bytes.fromhex(tail['pages'][0]['native_plane_hex'])==plane,'stored parity creates no extra page orink')
                require(nf['pages'][0]['native_plane_sha256']==sha(plane) and st['complete_native_ink_exact_to_directly_viewed_pages'],'stored/native viewed plane association')
            bodyplanes[version,row['id']]={COLORS[0]:{(i%216,i//216) for i,v in enumerate(plane) if v==1},COLORS[1]:{(i%216,i//216) for i,v in enumerate(plane) if v==15},COLORS[2]:set()}
        for n in names:
            actor=n['actor_ID'];text={1:'Hodram Bergstrom',9:'Camille Overijssel',16:'Gerhard '+('Ardelknatts' if version=='parent_English' else 'Adernkatz')}[actor]
            require(n['text']==text and n['original_pair_flush_width']==((len(text)+1)//2)*12,'exact full original progressive name andflush')
            events=[dict(kind='ascii',code=ord(c),style=11,x=6*i,y=0) for i,c in enumerate(text)]
            plane=expected_pixels(arm,font,events)
            require(plane==Path(n['native_plane']).read_bytes() and sha(plane)==n['native_plane_sha256'],'independent complete name glyph mask')
            nameplanes[version,actor]=(n,{(i%216,i//216) for i,v in enumerate(plane) if v})
    images={};reports={};totalbody=totalname=0
    parentbanks={v:IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for v,im in zip(VERSIONS,[parent,reference],strict=True)}
    sourcegroups={g['block']:g for g in data['source_context']['groups']};canonical={g['block']:g for g in data['whole_clean_contexts']['groups'] if g['file_path']=='/data/SC2.DK4'}
    for g in actual['groups']:
        scope,number,version=g['scope'],g['block'],g['version'];f=g['fixture'];bank=parentbanks[version];block=bank[number]
        terminal=load(g['terminal']);report=load(g['capture_report']);trace=load(terminal['observer'])
        horizon=32001 if scope=='whole' else 12001
        require(g['actual_frames']==terminal['frames']==report['frames']==horizon and terminal['terminal'] and terminal['all_callbacks_readonly_andhost_slots_restored'],'terminal actual coldboot horizon')
        require(sha(Path(g['capture_report']).read_bytes())==g['capture_report_sha256']==terminal['report_sha256'] and sha(Path(terminal['observer']).read_bytes())==terminal['observer_sha256'],'actual capture/observer report integrity')
        require(report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not report['hardware_device_verification'],'actual emulator/fixture limits')
        require(not any(v for k,v in report.items() if k.startswith('synthetic_')) and not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact'],'no state forcing/readonly observer integrity')
        require(f['route']==2 and f['source_block']==number and f['fixture_block']==22 and f['source_file']=='/data/SC2.DK4' and f['source_block_sha256']==sha(block),'actual source route/block identity')
        prelude=bank[22][8:56];require(f['original_opening_prelude_hex']==prelude.hex() and len(prelude)==48 and len(f['original_opening_prelude_commands'])==9,'nine original Lil initializer commands')
        commands=sourcegroups[number]['all_current_commands'] if version=='parent_English' else next(r for r in rebuilt['groups'] if r['block']==number)['all_target_commands']
        clean_commands=sourcegroups[number]['all_source_commands'];objects=f['all_original_exchange_commands']
        if scope=='whole':
            end=8+int.from_bytes(block[4:6],'little');segment=block[8:end]
            require(len(objects)==len(commands) and f['no_original_speech_branch_resource_effect_choice_orend_omitted'],'whole fixture includes every original command')
            require([o['source_command_ordinal'] for o in objects]==list(range(len(commands))),'complete whole original command membership')
        else:
            require(f['original_full_B27_conditions_andremaining_effects_NOT_executed_bythis_display_fixture'] and f['outer_branch_selection_bypassed_by_standalone_ROM_display_fixture'],'focused original outer condition unexecuted')
            outer=next(c for c in commands if c['offset']==f['selected_source_outer_0100_offset']);begin,end=outer['offset']+4,outer['offset']+outer['native_extent']
            require(outer['word']==0x100 and f['selected_original_body_slice']==dict(begin=begin,end=end,hex=block[begin:end].hex()),'exact focused original conditional body selection')
            segment=block[begin:end]+bytes.fromhex(commands[-1]['whole_command_hex'])
            ordinals=[i for i,c in enumerate(commands) if begin<=c['offset']<end]+[len(commands)-1]
            require([o['source_command_ordinal'] for o in objects]==ordinals and len(objects)==10,'eight original intro speeches/closing skip/end only')
        logical=bytearray(bank[22][:8]+prelude+segment);logical[4:6]=(len(logical)-8).to_bytes(2,'little');payload=bytes(logical)+bytes(-len(logical)%4)
        require(f['fixture_block_hex']==payload.hex() and f['fixture_block_sha256']==sha(payload) and f['fixture_logical_end']==len(logical) and f['fixture_stored_bytes']==len(payload),'independent whole fixture bytes andterminal/tail')
        fixture=NdsImage.open(f['research_ROM']);require(report['ROM_sha256']==f['research_ROM_sha256']==sha(Path(f['research_ROM']).read_bytes()),'actual fixture ROM identity')
        originalimage=parent if version=='parent_English' else reference
        require(all(fixture.read_file(p)==v for p,v in originalimage.iter_components()),'fixture keeps every original component')
        fixturebank=IlnkContainer.parse(fixture.read_file('/data/SC2.DK4')).blocks
        require(fixturebank[22]==payload and all(a==b for i,(a,b) in enumerate(zip(fixturebank,bank,strict=True)) if i!=22),'fixture changes only disclosed opening block')
        for o in objects:
            ordinal=o['source_command_ordinal'];nativecommand=commands[ordinal];cleancommand=clean_commands[ordinal];at=o['fixture_command_offset']
            require(o['canonical_clean_offset']==cleancommand['offset'] and o['original_command_offset']==nativecommand['offset'] and o['word']==nativecommand['word'] and o['whole_command_hex']==nativecommand['whole_command_hex'],'source-qualified actual original command')
            require(payload[at:at+o['native_extent']].hex()==o['whole_command_hex'] and o['native_extent']==nativecommand['native_extent'],'complete actual command extent')
        nativecommands={c['offset']:c for c in f['all_fixture_commands']};textrecords={s['fixture_command_offset']:s for s in f['original_text_records']};canon={r['id']:r for r in canonical[number]['complete_clean_source_records']}
        for at,s in textrecords.items():
            original=canon[s['id']];require(s['source_reference']==original['source_reference'] and s['source_selector']==original['source_selector'] and s['fixture_body_offset']==at+5,'exact original source speech membership')
        pairs=g['command_pairs'];last=None
        for pair in pairs:
            a,b=trace['rows'][pair['entry_row']],trace['rows'][pair['return_row']];at=pair['fixture_offset'];command=nativecommands[at]
            require(a['kind']=='before_command' and b['kind']=='after_command' and b['entry_row']==pair['entry_row'],'actual original entry/return association')
            require(pair['start']==a['frame'] and pair['returned']==b['frame'] and pair['duration']==b['frame']-a['frame'],'actual original command timing')
            require(pair['native_result']==b['result_words'] and pair['decoded_length']==b['decoded_length'] and pair['observed_previous_result']==a['mode'],'actual raw command result/length')
            require(pair['before_RNG']==a['original_RNG_seed'] and pair['after_RNG']==b['original_RNG_seed'] and pair['UI_before']==a['native_UI_request_words'] and pair['UI_after']==b['native_UI_request_words'],'actual raw RNG/UI measurements')
            require(last is None or last==at,'selected original native path continuity')
            word=command['word'];require(word==pair['word'],'actual command opcode')
            if word in [0x100,0x200,0x300,0x400]:
                span=int.from_bytes(payload[at+2:at+4],'little');mode=a['mode'];taken=word==0x100 or word==0x200 and mode==0 or word==0x300 and mode==1 or word==0x400 and mode==2
                require(pair['decoded_length']==4+(span if taken else 0),'actual unforced original relative result')
            else:require(pair['decoded_length']==command['native_extent'],'actual native nonrelative extent')
            last=at+pair['decoded_length'];original=next((o for o in objects if o['fixture_command_offset']==at),None)
            require(pair['canonical_source_offset']==(None if original is None else original['canonical_clean_offset']) and pair['source_command_ordinal']==(None if original is None else original['source_command_ordinal']),'actual canonical source ordinal')
            for observed in [a,b]:
                resident=observed['source']
                require(observed['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] and resident['classification']=='original_SC_cache' and resident['route']==2 and resident['block']==22,'actual original cache andreadonly callback')
                require(resident['instruction_offset']==at and resident['first_word']==word and resident['actual_sha256']==resident['registered_sha256']==sha(payload) and resident['payload_bytes']==len(payload),'actual exact resident fixture bytes')
                require(resident['instruction_pointer']==resident['payload_address']+at and resident['whole_resident_payload_exact_ROM'] and sha(Path(resident['actual_payload_file']).read_bytes())==sha(payload),'actual payload pointer/source association')
        require(pairs[-1]['word']==0 and pairs[-1]['decoded_length']==4 and pairs[-1]['native_result']==[0,pairs[-2]['native_result'][1]],'actual complete normal value-carry end')
        require(g['normal_return']==dict(frame=pairs[-1]['returned'],native_result=pairs[-1]['native_result'],complete_four_byte_end=True),'actual measured normal return')
        expected_count=35 if scope=='whole' and number==27 else 75 if scope=='whole' else 8
        expected_frame=12415 if scope=='whole' and number==27 else 22255 if scope=='whole' else 5695 if version=='parent_English' else 5694
        require(len(g['speeches'])==expected_count and g['normal_return']['frame']==expected_frame and not g['unknown_sources'],'disclosed actual membership/return scope')
        selected=[textrecords[p['fixture_offset']]['id'] for p in pairs if p['fixture_offset'] in textrecords]
        require([s['id'] for s in g['speeches']]==selected and len(set(selected))==expected_count,'all selected source speech IDs in order')
        require(g['unvisited_conditional_text_IDs']==[s['id'] for s in f['original_text_records'] if s['id'] not in selected],'exact explicitly unvisited text IDs')
        photos={p['frame']:p for p in report['frames_captured']};pictures={}
        def picture(frame):
            if frame not in pictures:
                photo=photos[frame];require(sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'],'actual PNG integrity')
                pictures[frame]=Image.open(photo['path']).convert('RGB');require(pictures[frame].size==(256,384),'original actual framebuffer geometry')
            return pictures[frame]
        for h in g['relevant_header_observations']:
            actor=h['actor_ID'];n,ink=nameplanes[version,actor];speech=next(s for s in g['speeches'] if s['id']==h['id'])
            require(h['name']==n['text'] and actor==speech['source_selector'] and h['holds'],'complete relevant header identity')
            for hold in h['holds']:
                frame=hold['frame'];photo=photos[frame];pic=picture(frame)
                require(speech['start']+20<frame<speech['returned']-4 and hold['capture']==photo['path'] and hold['sha256']==photo['PNG_sha256'] and hold['complete_first_internal_final_name_glyphs'],'actual complete header interval/capture')
                found={(x-16,y-276) for y in range(276,289) for x in range(14,18+n['original_pair_flush_width']) if pic.getpixel((x,y))==COLORS[1]}
                require(found==ink,'actual complete first/internal/final name mask');totalname+=1
        for s in g['speeches']:
            if s['id'] not in wanted:require(not s['changed_body'],'unchanged body not relabelled as reviewed');continue
            require(s['changed_body'] and s['pages']==1 and s['complete_holds'],'actual edited single-page body holds')
            masks=bodyplanes[version,s['id']]
            for hold in s['complete_holds']:
                frame=hold['frame'];photo=photos[frame];pixels=picture(frame).crop((16,296,232,360)).get_flattened_data()
                found={c:{(i%216,i//216) for i,v in enumerate(pixels) if v==c} for c in COLORS}
                require(found==masks and s['start']+20<frame<s['returned']-4,'actual full first/internal/final body masks')
                require(hold['capture']==photo['path'] and hold['sha256']==photo['PNG_sha256'] and hold['actual_name']==nameplanes[version,s['source_selector']][0]['text'] and hold['native_page']==1,'actual source-bound body capture/name')
                require(any(h['id']==s['id'] and any(n['frame']==frame for n in h['holds']) for h in g['relevant_header_observations']),'actual body has a complete simultaneous header');totalbody+=1
        images[scope,number,version]=pictures;reports[scope,number,version]=report
    require(totalbody==30 and totalname==262,'independently recounted complete actual masks')
    return dict(native_body_andname_planes_independently_recomputed=True,all_selected_actual_command_source_results_RNG_UI_timing_revalidated=True,
        complete_actual_body_masks_recomputed=totalbody,complete_actual_name_masks_recomputed=totalname,
        disclosed_whole_andfocused_fixture_memberships_andnormal_returns_preserved=True)
