"""Bind91 stored speech dispatches,all44 nonrelative controls,seven queries andnormal carry."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B49_relocated_controls_v8098')
MAP=Path('work/analysis/Rafael_B49_relocation_v8096/one_block61_speeches56_relative_fixups280_cases_exact_full_inverse.json')
CURRENT=Path('work/analysis/Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json')
EFFECTIVE=Path('work/analysis/Rafael_B49_effective_v8087/all61_effective_English_templates122_original_dispatches_no_FE.json')
SOURCE=Path('work/analysis/Rafael_B49_source_controls_v8081/source_EV0_56_relative_sites280_cases13_raw_predicates1_query25_seeded_ends.json')
STORED=Path('work/analysis/Rafael_B49_stored_v8097/all61_stored_bodies124_fresh120_reused_alignments61_exact_viewed_pages.json')
INPUT=Path('work/analysis/current_V8066_Rafael_native_v8069/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists()
    mapping,current,effective,source,stored=map(read,[MAP,CURRENT,EFFECTIVE,SOURCE,STORED])
    assert stored['relocation_sha256']==sha(MAP.read_bytes()) and effective['source_packet_sha256']==sha(CURRENT.read_bytes())
    image=NdsImage.open(current['current_ROM']);assert sha(Path(current['current_ROM']).read_bytes())==mapping['candidate_sha256']==source['candidate_sha256']
    g=mapping['groups'][0];block=IlnkContainer.parse(Path(mapping['target_archive']).read_bytes()).blocks[49]
    assert sha(block)==g['target_block_sha256']==stored['research_block_sha256'] and len(block)==3792
    names=read(source['names']);assert sha(Path(source['names']).read_bytes())==source['names_sha256']
    voices={r['source_selector']:r['original_voice_class'] for r in names['native_static_selector_andvoice_resolution']['rows']}
    ns={**inherited.__dict__,'SOURCE':CURRENT,'route':0,'route_mask':1,'CATALOG_LOOKUP':{}}
    for name,text in effective['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),ns)
    exec(compile(effective['source_owned_measured_macro_body_adapter'],__file__+'::measured-defaults','exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    dispatches=[];predicates=[];controls=[]
    for ref in g['text_records']:
        raw=bytes.fromhex(ref['target_hex']);at=ref['new_offset'];assert block[at:at+len(raw)+1]==raw+b'\0'
        result=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop();is_FE=raw[0]==254
        expected=next(r for r in stored['records'] if r['id']==ref['id'])['expanded_stored_hex']
        boundary=next(r for r in result['boundaries'] if r['kind']==('unexecuted-FE-modal-body' if is_FE else 'unexecuted-progressive-body'))
        assert boundary['text_hex']==expected and result['resolved_actor_ID']==(None if is_FE else raw[0])
        assert result['source_voice_class']==(None if is_FE else voices[raw[0]])
        if is_FE:assert len(result['FE_original_null_actor_calls'])==1 and result['FE_original_null_actor_calls'][0]['args'][2]==0
        else:assert not result['FE_original_null_actor_calls']
        dispatches.append(dict(id=ref['id'],final_offset=at,final_stored_hex=raw.hex(),**result))
    for a,b,m in zip(current['groups'][0]['all_source_commands'],g['all_target_commands'],g['command_map'],strict=True):
        assert a['word']==b['word']==m['word']
        if a['word'] in [0x4000,0x100,0x200,0x300,0x400]:continue
        assert a['whole_command_hex']==b['whole_command_hex']
        controls.append(dict(source_offset=a['offset'],target_offset=b['offset'],word=a['word'],source_command_hex=a['whole_command_hex']))
        if a['word'] in [0x8000,0x8100]:
            result=ctx.execute(probe,block,b);ctx.machines.pop()
            original=next(r for r in source['source_raw_predicates_andqueries'] if r['offset']==a['offset'])
            assert result['native_result']==original['native_result'] and result['source_command_hex']==original['source_command_hex']
            predicates.append(dict(source_offset=a['offset'],target_offset=b['offset'],original=original,relocated=result))
    assert len(dispatches)==61 and sum(r['resolved_actor_ID'] is None for r in dispatches)==0
    assert len(predicates)==14 and sum(p['relocated']['word']==0x8100 for p in predicates)==1
    assert len(controls)==37 and sum(r['word']==0xA000 for r in controls)==7 and not ctx.machines
    assert len(g['relative_fixups'])==56 and sum(len(r['cases']) for r in g['relocated_skip_cases'])==280
    terminal=g['all_target_commands'][-1];assert terminal['word']==0 and terminal['offset']==3788 and terminal['offset']+4==g['target_logical_end']==3792
    adapter=source['source_owned_seeded_end_adapter'];env=dict(end_case.__globals__)
    exec(compile(adapter,__file__+'::relocated-normal-end-carry','exec'),env);arm=image.read_file('/__arm9__.bin')
    ends=[env['end_case'](arm,block,3788,p,s) for p in [0,1,2,3,0xFFFFFFFF] for s in [0,1,2,3,0xFFFFFFFF]]
    assert len(ends)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in ends)
    save(ROOT/'61_stored_dispatches13_raw_predicates1_query280_relative_cases25_seeded_ends.json',dict(
        candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],relocation=str(MAP),relocation_sha256=sha(MAP.read_bytes()),
        stored_proof=str(STORED),stored_proof_sha256=sha(STORED.read_bytes()),final_dispatches=dispatches,
        original_nontext_control_maps=controls,relocated_relative_cases=g['relocated_skip_cases'],
        relocated_predicates_andqueries=predicates,normal_seeded_ends=ends,
        all61_final_actors_voices_complete_stored_bodies_exact_no_FE_objects=True,
        all13_raw_predicates_andone_completion_query_current_unforced_values_andunaligned_scratch_restore_preserved=True,
        all37_nonrelative_controls_sevenA000_C281_andcomplete_end_bytes_exact=True,
        original_source_structural_pairs_reused_by_exact_command_andruntime_bytes=True,
        full_scene_camera_resource_A000_effect_bodies_not_explained_orclaimed_executed=True,
        registered_current_catalogue_binding=catalogue,R311_R388_final_effective_bytes_include_exact_two_FI_default_expansions=True,
        no_typed_menu_added_no_invented_printf_orstate_result_seed_forcing=True,
        actual_B49_paths_nameplates_C281_transition_andnormal_value_carry_still_pending=True,
        fullreference_loaders_callers_frozen_policy_atomic_andregistered_release_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(Path(p).read_bytes()) for p in [MAP,CURRENT,EFFECTIVE,SOURCE,STORED,INPUT,Path(__file__)]},
        new_emulator_runs=0,new_credit=0,full_goal_complete=False))
    print('61stored dispatches/noFE,13raw predicates/onecompletionquery,37opaque controls,56sites280cases/25normalcarry ends pass.Actual full-scene execution pending.')
