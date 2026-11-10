"""First complete B49 current/effective comparison after clean gloss/native view; fresh own-V8377 dispatches."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_outcomes_registered_route_context_v8380 import RouteCurrentContext
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.prove_lil_B212_consumers_v6595 import choice_getters
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_current_v8387')
GLOSS=Path('work/analysis/Hodram_B49_clean_gloss_v8358/fourteen_first_clean_glosses_two_choice_labels_wristband_trade_direction_andqualified_Hodram_reply.json')
DISPLAY=Path('work/analysis/Hodram_B49_source_display_v8386b/source_display.json')
VIEW=Path('work/analysis/Hodram_B49_source_view_v8386c/source_view.json')
CONTROLS=Path('work/analysis/Hodram_B49_source_controls_v8384/source_controls.json')
INPUT=Path('work/analysis/current_V8377_Hodram_native_v8380/current_native_input.json')
HANDOFF=Path('work/analysis/editorial_handoff_verification_v8383/verified_handoff.json')
if __name__=='__main__':
    assert not ROOT.exists();gloss,display,view,controls,inp,verified=map(read,[GLOSS,DISPLAY,VIEW,CONTROLS,INPUT,HANDOFF]);ledger=Path('translations/editorial_review_current_v1.json');assert sha(ledger.read_bytes())==verified['ledger_sha256'] and verified['completed']==7205
    assert gloss['all14_clean_utterances_andtwo_choices_glossed_before_current_English'] and display['current_English_dialogue_bodies_unconsulted'] and controls['current_B49_English_dialogue_bodies_still_unconsulted'] and view['all14_source_pages_directly_viewed']
    assert display['source_gloss_sha256']==controls['first_clean_gloss_sha256']==sha(GLOSS.read_bytes()) and view['source_native_proof_sha256']==sha(DISPLAY.read_bytes());assert sha(Path(display['review_sheet']['path']).read_bytes())==display['review_sheet']['sha256']
    image=NdsImage.open(inp['current_ROM']);assert sha(Path(inp['current_ROM']).read_bytes())==inp['current_ROM_sha256']==verified['candidate_sha256']
    previous=NdsImage.open(display['candidate']);assert all(previous.read_file(p)==image.read_file(p) for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT','/data/EV1.DK4'])
    arm=image.read_file('/__arm9__.bin');archive=image.read_file('/data/SC1.DK4');bank=IlnkContainer.parse(archive).blocks;source=gloss['groups'][0];number=source['block'];assert number==49
    block=bank[number];clean=bytes.fromhex(source['clean_block_hex']);inventory,walker,fn=scoped_inventory();commands,speeches=inventory(arm,block);assert len(commands)==len(source['commands'])==36 and len(speeches)==len(source['records'])==14
    logical=8+int.from_bytes(block[4:6],'little');assert commands[-1]['word']==0 and commands[-1]['offset']+4==logical and block[logical:]==bytes(len(block)-logical)
    pairs_by_source={a['offset']:b for a,b in zip(source['commands'],commands,strict=True)};offset_map={a['offset']:b['offset'] for a,b in zip(source['commands'],commands,strict=True)};offset_map[source['clean_logical_end']]=logical
    pairs=[];relative_maps=[];menu=None
    for a,b in zip(source['commands'],commands,strict=True):
        assert a['word']==b['word'] and [offset_map[x] for x in a['ancestor_0100_offsets']]==b['ancestor_0100_offsets'];word=a['word'];av=bytes.fromhex(a['whole_command_hex']);bv=bytes.fromhex(b['whole_command_hex'])
        if word==0x4000:assert av[:6]==bv[:6];kind='speech'
        elif word in [0x100,0x200,0x300,0x400]:
            sa,ca=[struct.unpack_from('<H',raw,2)[0] for raw in [av,bv]];st=a['offset']+4+sa;ct=b['offset']+4+ca;assert ct==offset_map[st] and b['offset']+4==offset_map[a['offset']+4]
            relative_maps.append(dict(source_offset=a['offset'],current_offset=b['offset'],word=word,source_span=sa,current_span=ca,source_next=a['offset']+4,current_next=b['offset']+4,source_skip_target=st,current_skip_target=ct,ancestor_0100_offsets=a['ancestor_0100_offsets']));kind='relative'
        elif word==0x2100:
            assert menu is None;oldget,newget=choice_getters(arm,a),choice_getters(arm,b);assert len(oldget)==len(newget)==2 and all(c['count']==2 for c in oldget+newget)
            rows=[]
            for index,(sc,cc,gl) in enumerate(zip(oldget[0]['labels'],newget[0]['labels'],gloss['source_typed_choice']['labels'],strict=True)):
                assert sc['text']==gl['source_Japanese'] and sc['hex']==gl['source_hex'] and sc['offset']==gl['source_reference']['offset']
                rows.append(dict(id=f'DK4_MES_B49_CHOICE_{a["offset"]}_O{index}',file_path='/data/SC1.DK4',block=49,option_index=index,source_Japanese=sc['text'],first_clean_source_gloss=gl['first_clean_source_gloss'],source_reference=dict(block=49,command_offset=a['offset'],offset=sc['offset'],bytes=len(bytes.fromhex(sc['hex']))),source_hex=sc['hex'],current_reference=dict(block=49,command_offset=b['offset'],offset=cc['offset'],bytes=len(bytes.fromhex(cc['hex']))),current_hex=cc['hex'],current_English=cc['text'],current_body_not_contextually_approved=True))
            menu=dict(source_command=a,current_command=b,source_getters_in_current_code=oldget,current_getters=newget,records=rows,full_choice_UI_geometry_glyphs_result_routing_andlocalization_pending=True);kind='typed-choice'
        else:assert av==bv;kind='opaque-control-or-terminal'
        pairs.append(dict(word=word,kind=kind,source_offset=a['offset'],current_offset=b['offset'],source_extent=a['native_extent'],current_extent=b['native_extent'],source_hex=av.hex(),current_hex=bv.hex(),bytes_equal=av==bv))
    assert len(relative_maps)==8 and menu is not None
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context');ns={**inherited.__dict__,'SOURCE':INPUT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    for name,text in display['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::exact-original-'+name,'exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image);exec(compile(display['source_owned_macro_body_adapter'],__file__+'::measured-captain1-defaults','exec'),ns)
    rows=[];dispatches=[];relative_cases=[];query_cases=[]
    for original,command in zip(source['records'],speeches,strict=True):
        at=command['offset']+5;raw=block[at:block.index(0,at+1)];FE=raw[0]==254;assert raw[0]==original['source_selector'] and block[at-5:at+1].hex()==original['source_complete_preamble_hex'];bodies=[]
        for version,value in [('source-Japanese',bytes.fromhex(original['source_hex'])),('current-English',raw)]:
            result=ctx.execute(ns['dispatch'],value[0],value[1:]);ctx.machines.pop();assert result['resolved_actor_ID']==(None if FE else value[0]) and result['source_voice_class']==(None if FE else {1:1,2:3}[value[0]])
            boundary=next(q for q in result['boundaries'] if q['kind']==('unexecuted-FE-modal-body' if FE else 'unexecuted-progressive-body'));selected=ns['CATALOG_LOOKUP'].get(value[1:]);template=selected['target'] if selected else value[1:];expanded=template.replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet');assert boundary['text_hex']==expanded.hex()
            if FE:assert len(result['FE_original_null_actor_calls'])==1 and result['FE_original_null_actor_calls'][0]['args'][2]==0
            if version=='source-Japanese':assert selected is None
            bodies.append((template,expanded,result));dispatches.append(dict(id=original['id'],version=version,**result))
        template,expanded,result=bodies[1];row=deepcopy(original);row.update(kind='system-FE' if FE else 'progressive',source_kind='system-FE' if FE else 'progressive',current_reference=dict(file_path='/data/SC1.DK4',block=number,offset=at,bytes=len(raw),header_offset=at-5,record_index=block[:at].count(b'\0')),current_hex=raw.hex(),current_record_index=block[:at].count(b'\0'),current_native_extent=command['native_extent'],current_0100_ancestors=command['ancestor_0100_offsets'],current_raw_storage_English=raw[1:].decode('cp932'),raw_storage_comparison_paragraph=' '.join(raw[1:].decode('cp932').split()),effective_predecessor_template_hex=template.hex(),effective_predecessor_paragraph=' '.join(template.decode('cp932').split()),current_actual_default_expanded_hex=expanded.hex(),registered_catalogue_match=result['registered_catalog_match'],current_English_body_unread=False,current_English_dialogue_still_unconsulted=False,current_English_body_now_exposed=True,current_effective_dispatch_andcatalogue_pending=False,source_native_display_in_prior8300_context_preserved=True,source_andcurrent_dispatches_fresh_own8377_context=True,source_prose_orcompletion_credit_added=False,current_contextual_prose_formatting_actual_andrelease_pending=True);rows.append(row)
    for a,b in zip(source['commands'],commands,strict=True):
        if a['word'] in [0x100,0x200,0x300,0x400]:
            for version,payload,command in [('source',clean,a),('current',block,b)]:relative_cases.append(dict(version=version,**ctx.execute(native_skip,payload,command)));ctx.machines.pop()
        elif a['word'] in [0x8000,0x8100]:
            for version,payload,command in [('source',clean,a),('current',block,b)]:query_cases.append(dict(version=version,**ctx.execute(probe,payload,command)));ctx.machines.pop()
    assert len(rows)==14 and len(dispatches)==28 and len(relative_cases)==16 and len(query_cases)==2 and not ctx.machines
    group=dict(block=49,file_path='/data/SC1.DK4',clean_block_hex=clean.hex(),clean_block_sha256=sha(clean),source_header_hex=clean[:8].hex(),current_block_hex=block.hex(),current_block_sha256=sha(block),current_header_hex=block[:8].hex(),current_stored_bytes=len(block),current_logical_end=logical,current_tail_bytes=len(block)-logical,all_source_commands=source['commands'],all_current_commands=commands,all_command_reference_pairs=pairs,relative_operand_maps=relative_maps,source_event_records=source['source_event_records'],records=rows)
    save(ROOT/'current_effective.json',dict(current_ROM=inp['current_ROM'],current_ROM_sha256=inp['current_ROM_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),current_archive_sha256=sha(archive),file_path='/data/SC1.DK4',records=rows,groups=[group],typed_choices=[menu],source_first_glosses_andcomplete_native_page_view_precede_current_English=True,source_native_view=display['review_sheet'],source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),source_native_display=str(DISPLAY),source_native_display_sha256=sha(DISPLAY.read_bytes()),source_controls=str(CONTROLS),source_controls_sha256=sha(CONTROLS.read_bytes()),source_native_context_historical8300_not_overlaid_orcalled_current=True,all28_source_current_dispatches_in_new_own8377_context=dispatches,source_current_native_relative_cases=relative_cases,source_current_native_query_cases=query_cases,registered_current_catalogue_binding=catalogue,all36_commands14_preambles8_relative_targets_two_typed_labels_opaque_effects_andcomplete_end_bound=True,current_comparison_not_English_editorial_orUI_approval=True,current_native_input=str(INPUT),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),inventory_walker=walker,inventory_function=fn,no_ROM_write_orledger_credit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,DISPLAY,VIEW,CONTROLS,INPUT,HANDOFF,Path(__file__)]}))
    for r in rows:print(r['id'],repr(r['effective_predecessor_paragraph']),'catalogue',r['registered_catalogue_match'])
    print('CHOICES',[(r['option_index'],r['source_Japanese'],r['current_English']) for r in menu['records']]);print('Fresh8377:28dispatches/80relative cases/2rawqueries;all36commands/source-current references bound.No editorial approval orcredit.')
