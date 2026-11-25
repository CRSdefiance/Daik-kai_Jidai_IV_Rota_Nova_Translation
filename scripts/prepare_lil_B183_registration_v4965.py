"""Prepare cumulative registration and meaningful atomic B183 rejection cases."""
from pathlib import Path
from scripts.prepare_lil_B181_compiler_v4865 import alter
from scripts.verify_village_wrap_v608 import save

EXTRA="""    mutations.extend([
        ('lost-wrap-question-proof',doc['source_bound_wrap_refinement_proof'],lambda v:v.update(all25_words_controls_and_prose_unchanged=False)),
        ('concealed-other-wrap-changes',doc['source_bound_wrap_refinement_proof'],lambda v:v.update(all24_other_compiled_targets_and_native_planes_exact=False)),
        ('wrong-source-voice',doc['actor_voice_contract'],lambda v:next(r for r in v['fresh5_actor_names']['rows'] if r['actor_ID']==153).update(original_voice_class=0)),
        ('conflated-Sailor-Retainer',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'153':'Retainer'})),
        ('lost-catalogue-distinction',doc['source_nameplate_consumer_proof'],lambda v:v['full_catalogue_values'].update({'153':'Sailor'})),
        ('wrong-commodity',doc['actor_terminology_reconciliation'],lambda v:v.update(commodity='Paintings')),
        ('wrong-city-alias',doc['actor_terminology_reconciliation'],lambda v:v['two_source_current_city_aliases'][0].update(text='Amsterdam')),
        ('wrong-timing-disclosure',doc['postscene_native_state_proof'],lambda v:v['exact_timing_difference_counts'].update(total=0)),
        ('lost-second-FE',doc['native_font_proof'],lambda v:v.update(complete_FE_logical_and_physical_planes=1)),
    ])
"""
if __name__=='__main__':
    root=Path('work/analysis/lil_B183_registration_tools_v4965');out=Path('scripts/register_lil_B183_v4965.py');assert not root.exists() and not out.exists()
    text=Path('scripts/register_lil_B181_v4866.py').read_text(encoding='utf-8')
    text=alter(text,{
        'B181':'B183','V4821':'V4914','registration_v4866':'registration_v4965','all-routes-unified-v4867':'all-routes-unified-v4966',
        'all_routes_combined_v4821':'all_routes_combined_v4914','all-routes-unified-v4821':'all-routes-unified-v4914',
        'editorial_manuscript_v4':'editorial_manuscript_v8','editorial_handoff_verification_v4850':'editorial_handoff_verification_v4956',
        'lil_B181_layout_v1':'lil_B183_layout_v3','reference_approval_v4864':'reference_approval_v4963','loader_v4853':'loader_v4951',
        'native_approval_v4845':'native_approval_v4946','all10_source_prose':'all25_source_prose','actual_v4861':'actual_v4960','actual_all10':'actual_all25',
        "'postscene_native_state_proof','current_C200_source_ownership_proof'":"'postscene_native_state_proof','current_C200_source_ownership_proof','source_bound_wrap_refinement_proof'",
        "len(proof['changed_records'])==10":"len(proof['changed_records'])==25",'positive_records=10':'positive_records=25',
        'native_six_consumer_cases':'native_ten_consumer_cases','complete_matching_observations=10':'complete_matching_observations=24',
        "('false-RNG-equality',doc['postscene_native_state_proof'],lambda v:v.update(PRNG_equality=False))":"('concealed-RNG-inequality',doc['postscene_native_state_proof'],lambda v:v.update(PRNG_equality=True))",
        'postscene9001':'postscene11001','build_integrated_release_v4866.tmp':'build_integrated_release_v4965.tmp',
        'expected_manifest_batches=563':'expected_manifest_batches=565','expected_batches=563':'expected_batches=565',
        "description='Complete V4821 stack plus10 B181 whole-exchange reviews:5 revisions/5 justified retentions,nine progressive Lady166/167/168 and one prospective Athens Rubies notice. All13 commands,A000/C200/end and distinct three sighs preserved. Two actual9001-frame content cold boots show10 panels and normal return;115 nontext samples,all postscene RGB,five state groups,whole actor and PRNG agree without forced outcomes.'":
        "description='Complete V4914 stack plus25 B183 whole-exchange reviews:16 revisions/9 justified retentions,five progressive roles and two impersonal FE objects. All28 source commands,A000/C200/end preserved. Source-bound wrap-v3 keeps the fitting question intact and complete locative over there together without word or width changes. Two11001-frame content cold boots show25 complete panels and normal return;11 timing differences and unequal final RNG remain disclosed.149 nontext samples,all sampled postscene RGB,five state groups and whole actor agree.'",
    })
    text=text.replace('    for label,path,edit in mutations:reject(label,path,edit)',EXTRA+'    for label,path,edit in mutations:reject(label,path,edit)')
    compile(text,str(out),'exec');out.write_text(text,encoding='utf-8',newline='\n');root.mkdir(parents=True)
    save(root/'prepared_tools.json',dict(registration=str(out),expected_manifest_batches=565,no_registry_mutation_yet=True,full_goal_complete=False))
