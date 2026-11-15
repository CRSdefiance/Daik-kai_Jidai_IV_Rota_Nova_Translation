"""Execute relocated stored dispatches/query/picture boundaries and preserve complete native controls."""
from pathlib import Path
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

if __name__=='__main__':
    assert not ROOT.exists();mapping,current,source,display,stored=map(read,[MAP,CURRENT,SOURCE,DISPLAY,STORED])
    assert stored['relocation_sha256']==sha(MAP.read_bytes())
    image=NdsImage.open(current['current_ROM']);assert sha(Path(current['current_ROM']).read_bytes())==mapping['candidate_sha256']
    g=mapping['groups'][0];block=Path(g['target_block']).read_bytes();assert sha(block)==g['target_block_sha256']==stored['research_block_sha256']
    assert image.read_file('/__arm9__.bin')==NdsImage.open(display['candidate']).read_file('/__arm9__.bin')
    ns={**inherited.__dict__,'SOURCE':INPUT,'route':1,'route_mask':2,'CATALOG_LOOKUP':{}}
    for name,text in display['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::exact-'+name,'exec'),ns)
    exec(compile(display['source_owned_macro_body_adapter'],__file__+'::measured-defaults','exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    pe=dict(picture.__globals__);exec(compile(source['source_owned_picture_adapter'],__file__+'::original-two-layouts-andhide','exec'),pe)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
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
            result=ctx.execute(probe,block,after);ctx.machines.pop()
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
    save(ROOT/'stored_controls.json',dict(candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],relocation=str(MAP),relocation_sha256=sha(MAP.read_bytes()),stored=str(STORED),stored_sha256=sha(STORED.read_bytes()),final_dispatches=dispatches,original_nonrelative_nonspeech_nonmenu_control_maps=controls,relocated_relative_cases=g['relocated_skip_cases'],relocated_query_cases=queries,relocated_picture_andhide_boundary_cases=pictures,normal_seeded_ends=ends,all14_source_actors_voices_full_preambles_stored_bodies_andoriginal_null_FE_exact=True,original_item148_descriptors_distinct_layouts_andhide_boundaries_exact=True,seven_opaque_effects_preserved_without_claiming_gameplay_semantics=True,source_query_raw_result_not_boolean_orinventory_award=True,registered_current_catalogue_binding=catalogue,all8_relative_sites40_cases_and25_normal_value_carries_pass=True,actual_scene_resource_effect_bodies_eligibility_menu_selection_andFE_transition_pending=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [MAP,CURRENT,SOURCE,DISPLAY,STORED,INPUT,Path(__file__)]}))
    print('B49 stored controls:14 dispatches/one null FE,40 relocated branch cases,one unchanged raw query,four picture/hide boundaries,25 normal value-carry cases pass.No actual effect oractivation claim.')
