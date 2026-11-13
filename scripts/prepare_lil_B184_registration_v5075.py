"""Prepare meaningful pre-mutation controls and cumulative registration after V5030."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B184_registration_tools_v5075')
if __name__=='__main__':
    assert not ROOT.exists()
    text=Path('scripts/register_lil_B183_v4965.py').read_text(encoding='utf-8')
    a=text.index("        description='Complete V4914");b=text.index("        note=",a)
    description="        description='Complete V5030 plus9 B184 whole-exchange reviews:4 revisions/5 justified retentions,two clean couple roles,eight progressive and one prospective Tea/Sofala FE. Preserve all12 source commands,household request,A000,C200 and end. Exact source/prose-bound wrapping uses2 safe R14 rows without changing words. Paired9001-frame content cold boots cover every panel and normal return;8 timing and4 later A-indicator differences remain disclosed.115 nontext samples,final RGB,five native groups,whole actor and measured RNG agree.',\n"
    extras="""    mutations.extend([
        ('wrong-source-header-metadata',str(DOC),lambda v:v['records'][0]['source_reference'].update(header_offset=1)),
        ('wrong-current-header-metadata',str(DOC),lambda v:v['records'][0]['current_reference'].update(header_offset=1)),
        ('wrong-source-length-metadata',str(DOC),lambda v:v['records'][0]['source_reference'].update(bytes=1)),
        ('wrong-current-length-metadata',str(DOC),lambda v:v['records'][0]['current_reference'].update(bytes=1)),
        ('wrong-source-record-index',str(DOC),lambda v:v['records'][0]['source_reference'].update(record_index=1)),
        ('wrong-current-record-index',str(DOC),lambda v:v['records'][0].update(current_record_index=1)),
        ('wrong-source-block-metadata',str(DOC),lambda v:v['records'][0]['source_reference'].update(block=183)),
        ('wrong-source-extent-metadata',str(MAP),lambda v:v['blocks'][0].update(source_bytes=1)),
        ('wrong-source-logical-metadata',str(MAP),lambda v:v['blocks'][0].update(source_logical_end=1)),
        ('wrong-target-extent-metadata',str(MAP),lambda v:v['blocks'][0].update(research_bytes=1)),
        ('wrong-target-logical-metadata',str(MAP),lambda v:v['blocks'][0].update(research_logical_end=1)),
        ('inconsistent-command-map',str(MAP),lambda v:v['blocks'][0]['command_map'][0].update(new_extent=2)),
        ('lost-household-fact',doc['actor_terminology_reconciliation'],lambda v:v.update(household_tea_is_low_not_city_or_trade_cargo_shortage=False)),
        ('lost-boundary-mutation-control',doc['source_bound_wrap_refinement_proof'],lambda v:v['exact_source_and_prose_mutation_controls'].pop()),
    ])
"""
    changes={text[a:b]:description,
        'B183':'B184','lil_B183_editorial_v1':'lil_B184_editorial_v2','lil_B183_layout_v3':'lil_B184_layout_v2',
        'registration_v4965':'registration_v5075','all-routes-unified-v4966':'all-routes-unified-v5076','combined_v4914':'combined_v5030',
        'editorial_manuscript_v8':'editorial_manuscript_v5','editorial_handoff_verification_v4956':'editorial_handoff_verification_v5058',
        'reference_approval_v4963':'reference_approval_v5073','loader_v4951':'loader_v5063',
        'native_approval_v4946/all25':'native_approval_v5056/all9','actual_v4960/actual_all25':'actual_v5070/actual_all9',
        "len(proof['changed_records'])==25":"len(proof['changed_records'])==9",'all25_words_controls_and_prose_unchanged':'all9_words_controls_and_prose_unchanged',
        'all24_other_compiled_targets_and_native_planes_exact':'eight_other_compiled_targets_exact',
        "v['native_ten_consumer_cases']":"v['native_four_consumer_cases']",
        'complete_matching_observations=24':'complete_matching_observations=8',
        "('concealed-RNG-inequality',doc['postscene_native_state_proof'],lambda v:v.update(PRNG_equality=True))":"('false-RNG-inequality',doc['postscene_native_state_proof'],lambda v:v.update(PRNG_equality=False))",
        'postscene11001':'postscene9001',
        "next(r for r in v['fresh5_actor_names']['rows'] if r['actor_ID']==153).update(original_voice_class=0)":"next(r for r in v['fresh2_actor_names']['rows'] if r['actor_ID']==164).update(original_voice_class=1)",
        "('conflated-Sailor-Retainer',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'153':'Retainer'}))":"('wrong-progressive-couple-role',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'164':'Woman in a Couple'}))",
        "('lost-catalogue-distinction',doc['source_nameplate_consumer_proof'],lambda v:v['full_catalogue_values'].update({'153':'Sailor'}))":"('wrong-catalogue-couple-role',doc['source_nameplate_consumer_proof'],lambda v:v['full_catalogue_values'].update({'165':'Man in a Couple'}))",
        "('lost-second-FE',doc['native_font_proof'],lambda v:v.update(complete_FE_logical_and_physical_planes=1))":"('lost-FE',doc['native_font_proof'],lambda v:v.update(complete_FE_logical_and_physical_planes=0))",
        '    for label,path,edit in mutations:reject(label,path,edit)':extras+'    for label,path,edit in mutations:reject(label,path,edit)',
        'all-routes-unified-v4914':'all-routes-unified-v5030','V4914':'V5030','build_integrated_release_v4965.tmp':'build_integrated_release_v5075.tmp',
        'expected_manifest_batches=565':'expected_manifest_batches=568','positive_records=25':'positive_records=9','expected_batches=565':'expected_batches=568'}
    assert all(k in text for k in changes),[k for k in changes if k not in text]
    tool=derive('scripts/register_lil_B183_v4965.py','scripts/register_lil_B184_v5075.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'prepared.json',dict(tool=tool,atomic_compiler='dk4tool/patch/lil_B184_editorial_v2.py',
        meaningful_metadata_and_fact_boundary_controls_added=14,earlier_registry_builder_profiles_and_main_preserved=True,new_review_credit=0,full_goal_complete=False))
