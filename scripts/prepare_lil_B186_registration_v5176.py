"""Prepare cumulative B186 registration and meaningful conditional/metadata negatives."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B186_registration_tools_v5176')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/register_lil_B182_v4913.py');text=source.read_text(encoding='utf-8')
    a=text.index("        description='Complete V4867");b=text.index('        note=',a)
    description="        description='Complete V5122 plus12 B186 whole-exchange reviews:7 revisions/5 justified retentions. Owner174/Cook175 sweetness discussion,comic repeated sweet,self-authority and two perfunctory replies remain distinct;the Sweets/Alexandria notice stays tentative. Exact source/prose-bound R13 ordinary soft wraps use3 flowing rows without changing words,font,width or guards. All24 commands,one700 predicate,six relative operands,three alternative effects,C200,end and2 alignment zeros remain. Two9001-frame content cold boots show12 complete panels,47 holds,115 paired nontext samples and normal return. Ten timings,four later original A-indicator differences and unequal final PRNG remain disclosed;final RGB,five native groups and whole actor agree. One Japanese Alexandria alias remains a separate caller/display lead.',\n"
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
        ('lost-wrap-proof',doc['source_bound_wrap_refinement_proof'],lambda v:v.update(all12_words_controls_and_prose_unchanged=False)),
        ('concealed-other-wrap-changes',doc['source_bound_wrap_refinement_proof'],lambda v:v.update(eleven_other_compiled_targets_exact=False)),
        ('lost-boundary-reasons',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==13).pop('reviewed_ordinary_boundaries')),
        ('false-boundary-mutation-control',doc['source_bound_wrap_refinement_proof'],lambda v:v['exact_source_and_prose_mutation_controls'][0].update(rejected=False)),
        ('wrong-source-voice',doc['actor_voice_contract'],lambda v:next(r for r in v['fresh2_actor_names']['rows'] if r['actor_ID']==174).update(original_voice_class=1)),
        ('wrong-progressive-role',doc['source_nameplate_consumer_proof'],lambda v:v['progressive_nameplate_values'].update({'174':'Duchess'})),
        ('wrong-catalogue-role',doc['source_nameplate_consumer_proof'],lambda v:v['full_catalogue_values'].update({'175':'Servant'})),
        ('concealed-Japanese-city-alias',doc['actor_terminology_reconciliation'],lambda v:v['two_source_current_city_aliases'][0].update(text='Alexandria')),
        ('invented-trade-context',doc['actor_terminology_reconciliation'],lambda v:v.update(missing_sweetness_is_food_flavor_preparation_not_trade_advice=False)),
        ('invented-single-commodity',doc['actor_terminology_reconciliation'],lambda v:v.update(Sweets_is_broad_source_supported_collective_not_a_single_commodity_ID_or_new_UI_category=False)),
        ('concealed-FE-exposure',doc['actor_terminology_reconciliation'],lambda v:v.update(no_predecessor_English_exposed=True)),
        ('wrong-timing-disclosure',doc['postscene_native_state_proof'],lambda v:v['exact_timing_difference_counts'].update(total=0)),
        ('lost-FE',doc['native_font_proof'],lambda v:v.update(complete_FE_logical_and_physical_planes=0)),
        ('wrong-actual-unforced-flag',actual_proof,lambda v:v['versions'][0]['actual_predicate_transitions'][0].update(actual_unforced_original_LCG_transition=False)),
    ])
"""
    changes={
        text[a:b]:description,'B182':'B186','registration_v4913':'registration_v5176',
        'all-routes-unified-v4914':'all-routes-unified-v5177','combined_v4867':'combined_v5122',
        'all-routes-unified-v4867':'all-routes-unified-v5122','V4867':'V5122',
        'editorial_handoff_verification_v4911':'editorial_handoff_verification_v5174','editorial_manuscript_v4':'editorial_manuscript_v6',
        'lil_B182_layout_v1.py':'lil_B186_layout_v4.py',
        'reference_approval_v4909':'reference_approval_v5172','loader_v4899':'loader_v5162',
        'native_approval_v4892/all8':'native_approval_v5156/all12',
        'actual_v4906/actual_all8':'actual_v5169/actual_all12',
        'predicate500_v4896/all24_aligned_and_unaligned_original500':'predicate700_v5159/all12_aligned_and_unaligned_original700',
        "'postscene_native_state_proof','current_C200_source_ownership_proof'":"'postscene_native_state_proof','current_C200_source_ownership_proof','source_bound_wrap_refinement_proof'",
        "len(proof['changed_records'])==8":"len(proof['changed_records'])==12",
        "'{SPEAKER:A6}Hello.'":"'{SPEAKER:AE}Hello.'",
        'all25_source_and_relocated_structural_paths_identical':'all5_source_and_relocated_structural_paths_identical',
        'complete_matching_observations=7':'complete_matching_observations=11',
        "update(reviewed_English=[516])":"update(reviewed_English=[584])",
        'update(viewed=False)':'update(viewed_after_image_return=False)',
        'update(value=501)':'update(value=701)',
        "lambda v:v['cases'][0].update(roll=0)":"lambda v:v['cases'][0].update(roll=(v['cases'][0]['roll']+1)%1000)",
        '    for label,path,edit in mutations:reject(label,path,edit)':extras+'    for label,path,edit in mutations:reject(label,path,edit)',
        'build_integrated_release_v4913.tmp':'build_integrated_release_v5176.tmp',
        'expected_manifest_batches=564':'expected_manifest_batches=570','positive_records=8':'positive_records=12','expected_batches=564':'expected_batches=570',
    }
    row=derive(source,'scripts/register_lil_B186_v5176.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_registration.json',dict(derivation=row,
        parent_profile='all-routes-unified-v5122',profile='all-routes-unified-v5177',
        conditional_and_complete_metadata_wrap_role_exposure_negatives_required=True,
        no_ROM_registry_or_credit_change=True,full_goal_complete=False))
    print('Prepared B186 cumulative registration:complete V5122 ancestry and source-aware conditional/metadata/wrap negatives.')
