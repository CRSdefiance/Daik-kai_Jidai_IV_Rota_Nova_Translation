"""Execute relocated stored dispatches/query/picture boundaries and preserve complete native controls."""
from pathlib import Path
import struct
from tempfile import TemporaryDirectory
from dk4tool.patch.hodram_B49_native_guards_v1 import trusted_adapter,CONTROLS,TRUSTED
from scripts.prove_lil_B234_entry_v7576 import native_entry
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.research_wedding_command_v676 import walk
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_outcomes_registered_route_context_v8380 import RouteCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.prove_lil_B145_picture_controls_v3587 import picture
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B49_controls_v8401d')
MAP=Path('work/analysis/Hodram_B49_relocation_v8398/reconstruction.json')
CURRENT=Path('work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json')
SOURCE=Path('work/analysis/Hodram_B49_source_controls_v8384/source_controls.json')
DISPLAY=Path('work/analysis/Hodram_B49_source_display_v8386b/source_display.json')
STORED=Path('work/analysis/Hodram_B49_stored_v8399/stored_bodies.json')
INPUT=Path('work/analysis/current_V8377_Hodram_native_v8380/current_native_input.json')

def check_controls(data,rows,parent,reference,rebuilt,native,load,require):
    mapping,current,source,display,stored=[data[k] for k in ['relocation','current','source_controls','source_display','stored']]
    assert stored['relocation_sha256']==sha(MAP.read_bytes())
    image=parent;assert sha(bytes(image.rom.save()))==mapping['candidate_sha256']
    g=mapping['groups'][0];block=rebuilt['target_block'];assert sha(block)==g['target_block_sha256']==stored['research_block_sha256']
    assert image.read_file('/__arm9__.bin')==reference.read_file('/__arm9__.bin')
    trusted=load(CONTROLS)
    require(sha(CONTROLS.read_bytes())==TRUSTED[str(CONTROLS)],'trusted original source control artifact')
    for key in ['source_owned_entry_adapter','source_owned_skip_probe','source_owned_query_probe']:
        require(source[key]==trusted[key],'exact trusted original control adapter:'+key)
    trusted_adapter('dispatch',display['source_owned_dispatch_adapters']);trusted_adapter('macro_body',display['source_owned_macro_body_adapter'])
    trusted_adapter('picture',source['source_owned_picture_adapter']);trusted_adapter('seeded_end',source['source_owned_seeded_end_adapter'])
    ns={**inherited.__dict__,'SOURCE':INPUT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    for name,text in display['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::exact-'+name,'exec'),ns)
    exec(compile(display['source_owned_macro_body_adapter'],__file__+'::measured-defaults','exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    pe=dict(picture.__globals__);exec(compile(source['source_owned_picture_adapter'],__file__+'::original-two-layouts-andhide','exec'),pe)
    context_temporary=TemporaryDirectory(prefix='Hodram-B49-controls-');ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',Path(context_temporary.name)/'current_context')
    en=dict(native_entry.__globals__);exec(compile(source['source_owned_entry_adapter'],__file__+'::trusted-entry','exec'),en)
    sk=dict(native_skip.__globals__);exec(compile(source['source_owned_skip_probe'],__file__+'::trusted-skip','exec'),sk)
    qp=dict(probe.__globals__);exec(compile(source['source_owned_query_probe'],__file__+'::trusted-query','exec'),qp)
    events=source['source_event_records'];assert [(e['event_ID'],e['script_block'],e['must_be_completed']) for e in events]==[(48,48,[]),(49,49,[48])]
    entry=ctx.execute(en['native_entry'],image.read_file('/data/EV1.DK4'),events);ctx.machines.pop();require(entry==source['original_EV1_entry'],'original EV1 getter fields for prerequisite48/event49')
    branches=[];byoffset={c['offset']:c for c in g['all_target_commands']};boundaries=set(byoffset)|{g['target_logical_end']}
    for fix,declared in zip(g['relative_fixups'],g['relocated_skip_cases'],strict=True):
        result=ctx.execute(sk['native_skip'],block,byoffset[fix['new_offset']]);ctx.machines.pop()
        require(result==declared and all(c['next_offset'] in boundaries and c['next_offset']==(fix['new_matched_skip_target'] if c['taken'] else fix['new_unmatched_next']) for c in result['cases']),'fresh relocated native branch endpoints/ABI/value fields')
        branches.append(result)
    opaque=[];cleanarm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for declared in source['isolated_opaque_effect_structural_pairs']:
        raw=bytes.fromhex(declared['source_command_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw
        versions=[]
        for label,code in [('clean-decoder',cleanarm),('current-decoder',image.read_file('/__arm9__.bin'))]:versions.append(dict(version=label,**walk(code,isolated)))
        require(versions==declared['versions'],'original paired opaque structural decoder fields without invented effect semantics');opaque.append(versions)
    require(len(opaque)==7,'all seven original opaque effects')

    dispatches=[];pictures=[];queries=[];controls=[]
    for ref in g['text_records']:
        raw=bytes.fromhex(ref['target_hex']);at=ref['new_offset'];FE=raw[0]==254
        assert block[at:at+len(raw)+1]==raw+b'\0' and ns['CATALOG_LOOKUP'].get(raw[1:]) is None
        result=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop()
        boundary=next(r for r in result['boundaries'] if r['kind']==('unexecuted-FE-modal-body' if FE else 'unexecuted-progressive-body'))
        expected=next(r for r in stored['records'] if r['id']==ref['id'])['expanded_stored_hex']
        assert boundary['text_hex']==expected and result['resolved_actor_ID']==(None if FE else raw[0])
        assert result['source_voice_class']==(None if FE else {1:1,2:3}[raw[0]])
        if FE:assert len(result['FE_original_null_actor_calls'])==1 and result['FE_original_null_actor_calls'][0]['args'][2]==0
        else:assert not result['FE_original_null_actor_calls']
        dispatches.append(dict(id=ref['id'],final_offset=at,final_stored_hex=raw.hex(),**result))
    for before,after,cm in zip(current['groups'][0]['all_source_commands'],g['all_target_commands'],g['command_map'],strict=True):
        word=before['word'];assert word==after['word']==cm['word']
        if word in [0x4000,0x100,0x200,0x300,0x400]:continue
        if word==0x2100:
            assert after['whole_command_hex']==g['choice_commands'][0]['target_hex'];continue
        assert before['whole_command_hex']==after['whole_command_hex']
        controls.append(dict(word=word,source_offset=before['offset'],final_offset=after['offset'],whole_command_hex=after['whole_command_hex']))
        if word==0x8000:
            result=ctx.execute(qp['probe'],block,after);ctx.machines.pop()
            original=next(r for r in current['source_current_native_query_cases'] if r['version']=='current')
            assert result['native_result']==original['native_result']==[2,0,0,0,0,0]
            assert result['source_command_hex']==original['source_command_hex']
            queries.append(dict(source_offset=before['offset'],final_offset=after['offset'],current_original=original,relocated=result))
        elif word in [0x4820,0x4800,0x4700]:
            result=ctx.execute(pe['picture'],block,after);ctx.machines.pop()
            original=next(r for r in source['source_picture_andhide_cases'] if r['source_offset']==before['offset'])
            expected=[]
            for call in original['original_picture_boundary_calls']:
                relocated={**call,'args':list(call['args'])}
                if word==0x4700:
                    assert call['descriptor'] is None and call['layout'] is None
                    relocated['args'][3]+=after['offset']-before['offset']
                expected.append(relocated)
            assert result['original_picture_boundary_calls']==expected
            result['original_unrelocated_boundary_calls']=original['original_picture_boundary_calls']
            result['hide_carried_script_pointer_relocated_by_exact_command_delta']=word==0x4700
            pictures.append(dict(word=word,original_source_offset=before['offset'],final_offset=after['offset'],**result))
    assert len(dispatches)==14 and sum(r['resolved_actor_ID'] is None for r in dispatches)==1
    assert len(queries)==1 and len(pictures)==4 and len(controls)==13 and not ctx.machines
    assert [p['word'] for p in pictures]==[0x4820,0x4700,0x4800,0x4700]
    assert len(g['relative_fixups'])==8 and sum(len(r['cases']) for r in g['relocated_skip_cases'])==40
    terminal=g['all_target_commands'][-1];assert terminal['word']==0 and terminal['offset']+4==g['target_logical_end']
    ee=dict(end_case.__globals__);exec(compile(source['source_owned_seeded_end_adapter'],__file__+'::original-value-carry','exec'),ee)
    arm=image.read_file('/__arm9__.bin');ends=[ee['end_case'](arm,block,terminal['offset'],p,v) for p in [0,1,2,3,0xffffffff] for v in [0,1,2,3,0xffffffff]]
    assert all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends)
    require(catalogue==data['controls']['registered_current_catalogue_binding'],'complete current native catalogue binding')
    for key,actual in [('final_dispatches',dispatches),('original_nonrelative_nonspeech_nonmenu_control_maps',controls),('relocated_relative_cases',branches),('relocated_query_cases',queries),('relocated_picture_andhide_boundary_cases',pictures),('normal_seeded_ends',ends)]:
        require(data['controls'][key]==actual,'every independent stored control field:'+key)
    for dispatch in dispatches:
        boundary=next(b for b in dispatch['boundaries'] if b['kind']==('unexecuted-FE-modal-body' if dispatch['final_stored_hex'].startswith('fe') else 'unexecuted-progressive-body'))
        require(boundary['text_hex']==native['bodies']['revised_English'][dispatch['id']]['expanded_body'].hex(),'fresh independently computed native body expansion:'+dispatch['id'])
    context_temporary.cleanup()
    return dict(independent_final_dispatches=len(dispatches),original_null_FE_calls=1,relative_sites=len(branches),native_relative_cases=sum(len(r['cases']) for r in branches),raw_query_cases=len(queries),picture_hide_boundaries=len(pictures),nonrelative_nonspeech_nonmenu_controls=len(controls),normal_seeded_ends=len(ends),original_EV1_entries=len(events),opaque_structural_decode_pairs=len(opaque),no_new_actual_scene_effect_semantics_earned_inventory_orouter_eligibility_claim=True,new_emulator_runs=0)
