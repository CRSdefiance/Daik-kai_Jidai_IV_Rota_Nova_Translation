"""Bind five stored dispatches, unchanged nontext controls, raw evaluators and complete normal ends."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Lil_current_route_context_v8198 import RouteCurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as inherited
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.prove_lil_B196_6003_ends_v5597 import end_case
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_final_controls_v8214')
MAP=Path('work/analysis/Gerhard_sparse_relocation_v8208b/two_blocks_five_sparse_revisions_all_commands_native_relative_cases_full_predecessor_inverse.json')
CURRENT=Path('work/analysis/Gerhard_surname_five_v8199/five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json')
EFFECTIVE=Path('work/analysis/Gerhard_surname_effective_v8201/all5_effective_English_templates10_original_dispatches_no_FE.json')
STORED=Path('work/analysis/Gerhard_stored_v8209/5_stored_bodies4_fresh16_reused_alignments5_exact_viewed_pages.json')
NAMES=Path('work/analysis/Gerhard_before_names_v8200/four_identities8_getters3_source_voices16_synthetic_Lil_alignments.json')
ENDS=Path('work/analysis/lil_B218_controls_v6878/two_A000_structural_cases50_normal_seeded_ends_no_relative_or_predicate.json')
INPUT=Path('work/analysis/current_V8172_Lil_native_v8198/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();mapping,current,effective,stored,names,end_source=map(read,[MAP,CURRENT,EFFECTIVE,STORED,NAMES,ENDS])
    assert stored['relocation_sha256']==sha(MAP.read_bytes()) and effective['source_packet_sha256']==sha(CURRENT.read_bytes())
    image=NdsImage.open(current['current_ROM']);assert sha(Path(current['current_ROM']).read_bytes())==mapping['candidate_sha256']==names['candidate_sha256']
    archive=Path(mapping['target_archive']).read_bytes();assert sha(archive)==mapping['target_archive_sha256']
    container=IlnkContainer.parse(archive);arm=image.read_file('/__arm9__.bin')
    voices={r['source_selector']:r['original_voice_class'] for r in names['native_static_selector_andvoice_resolution']['rows']}
    ns={**inherited.__dict__,'SOURCE':CURRENT,'route':2,'route_mask':4,'CATALOG_LOOKUP':{}}
    for name,text in effective['source_owned_dispatch_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),ns)
    exec(compile(effective['source_owned_measured_macro_body_adapter'],__file__+'::measured-Lil-defaults','exec'),ns)
    ns['CATALOG_LOOKUP'],catalogue=ns['bind_current_catalog'](image)
    adapter=end_source['source_owned_seeded_end_adapter'];env=dict(end_case.__globals__);exec(compile(adapter,__file__+'::original-normal-value-carry','exec'),env)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    dispatches=[];controls=[];predicates=[];ends=[]
    for g in mapping['groups']:
        number=g['block'];spec=next(s for s in current['groups'] if s['block']==number)
        clean,old,target=bytes.fromhex(spec['clean_block_hex']),bytes.fromhex(spec['current_block_hex']),container.blocks[number]
        assert sha(target)==g['target_block_sha256']
        for ref in g['text_records']:
            raw=bytes.fromhex(ref['target_hex']);at=ref['new_offset'];assert target[at:at+len(raw)+1]==raw+b'\0' and raw[0] in [1,9,16]
            result=ctx.execute(ns['dispatch'],raw[0],raw[1:]);ctx.machines.pop()
            expected=next(r for r in stored['records'] if r['id']==ref['id'])['expanded_stored_hex']
            boundary=next(r for r in result['boundaries'] if r['kind']=='unexecuted-progressive-body')
            assert boundary['text_hex']==expected and result['resolved_actor_ID']==raw[0] and result['source_voice_class']==voices[raw[0]]
            assert not result['FE_original_null_actor_calls'] and result['registered_catalog_match'] is None
            dispatches.append(dict(id=ref['id'],block=number,final_offset=at,final_stored_hex=raw.hex(),**result))
        for source,previous,final,m in zip(spec['all_source_commands'],spec['all_current_commands'],g['all_target_commands'],g['command_map'],strict=True):
            assert source['word']==previous['word']==final['word']==m['word'];word=final['word']
            if word in [0x4000,0x100,0x200,0x300,0x400]:continue
            assert previous['whole_command_hex']==final['whole_command_hex']
            controls.append(dict(block=number,source_offset=source['offset'],previous_offset=previous['offset'],target_offset=final['offset'],word=word,
                clean_hex=source['whole_command_hex'],previous_andtarget_hex=final['whole_command_hex'],
                source_difference_only_prior_reviewed_translated_choice=source['whole_command_hex']!=final['whole_command_hex']))
            if word in [0x8000,0x8100]:
                assert source['whole_command_hex']==final['whole_command_hex']
                values=[]
                for label,block,command in [('clean',clean,source),('current',old,previous),('target',target,final)]:
                    value=ctx.execute(probe,block,command);ctx.machines.pop();values.append(dict(version=label,**value))
                assert values[0]['native_result']==values[1]['native_result']==values[2]['native_result']
                predicates.append(dict(block=number,source_offset=source['offset'],target_offset=final['offset'],cases=values,
                    raw_native_results_not_assumed_boolean_menu_orpath_attainability=True))
        for label,block,commands in [('clean',clean,spec['all_source_commands']),('current',old,spec['all_current_commands']),('target',target,g['all_target_commands'])]:
            terminal=commands[-1];assert terminal['word']==0 and terminal['native_extent']==4 and block[terminal['offset']:terminal['offset']+4]==bytes(4)
            cases=[env['end_case'](arm,block,terminal['offset'],p,v) for p in [0,1,2,3,0xFFFFFFFF] for v in [0,1,2,3,0xFFFFFFFF]]
            assert len(cases)==25 and all(r['native_result'][0]==0 and r['native_result'][1]==r['initial_value_word'] for r in cases)
            ends.append(dict(block=number,version=label,terminal=terminal,cases=cases,normal_value_carry_not_zero_assumption=True))
    assert len(dispatches)==5 and len(controls)==51 and len(predicates)==10 and len(ends)==6 and not ctx.machines
    assert sum(r['source_difference_only_prior_reviewed_translated_choice'] for r in controls)==1
    save(ROOT/'5_final_dispatches51_controls30_raw_evaluations150_seeded_ends.json',dict(
        candidate=current['current_ROM'],candidate_sha256=current['current_ROM_sha256'],relocation=str(MAP),relocation_sha256=sha(MAP.read_bytes()),
        stored_proof=str(STORED),stored_proof_sha256=sha(STORED.read_bytes()),final_dispatches=dispatches,original_nontext_control_maps=controls,
        raw_predicates_andqueries=predicates,raw_native_evaluations=30,normal_seeded_ends=ends,normal_seeded_end_cases=150,
        all5_final_actor_voice_complete_stored_body_dispatches_exact_no_FE=True,
        all51_nonrelative_nontext_controls_current_target_byte_exact=True,only_clean_difference_is_exact_prior_reviewed_typed_choice=True,
        relative_native_cases_reused_from_exact_relocation=660,all130_preambles225_commands44_relative_scopes_bound=True,
        source_andtarget_four_byte_normal_ends_preserve_value_word_for25_seeds_each=True,source_owned_seeded_end_adapter=adapter,
        registered_current_catalogue_binding=catalogue,source_FI1_measured_Lil_expansion_preserved=True,
        ordinary_opening_evaluator_results_not_natural_eligibility_orforced_gameplay_states=True,
        full_opaque_effect_picture_resource_andchoice_UI_bodies_unexecuted_bythis_native_dispatch_probe=True,
        name_data_target_is_separate_owned_CPU_input_proof_not_implicitly_applied_here=True,
        actual_scenes_fullreference_loaders_callers_frozen_policy_atomic_registered_release_pending=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [MAP,CURRENT,EFFECTIVE,STORED,NAMES,ENDS,INPUT,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('5 stored dispatches/51 exact nontext controls/30 raw evaluators/150 seeded normal ends pass;no new gameplay or ROM.')
