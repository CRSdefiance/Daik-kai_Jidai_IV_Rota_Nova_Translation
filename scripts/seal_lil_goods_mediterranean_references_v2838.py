"""Seal34 source/current target references and shared representative approval."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Goods_Mediterranean_reference_approval_v2838')
MAP=Path('translations/lil_goods_mediterranean_editorial_relocation_map_v1.json')
OLD=Path('translations/lil_goods_mediterranean_editorial_manuscript_v5.json')
DOC=Path('translations/lil_goods_mediterranean_editorial_manuscript_v6.json')
PLAN=Path('work/analysis/lil_Goods_Mediterranean_relocation_v2833b/nested_source_relocation_research.json')
CENSUS=Path('work/analysis/lil_Goods_Mediterranean_reference_census_v2836/all273_commands128_relative_sites_and_shipped_entry_census.json')
SAMPLE=Path('work/analysis/lil_Goods_Mediterranean_sampling_v2837b/relocated_predicates_and_representative_rule_reconciliation.json')
PADDING=Path('work/analysis/lil_Goods_Mediterranean_research_v2834b/research_image_receipt.json')
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,MAP,DOC]);plan,census,sample,padding=map(read,[PLAN,CENSUS,SAMPLE,PADDING]);doc=deepcopy(read(OLD))
    assert census['all273_clean_current_target_commands_and128_relative_sites_reexecuted'] and census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_selected_India_Polder_IDs']==[]
    assert sample['all32_relocated_original_predicates_preserve_source_operands_results_and_event_query_arguments']
    assert padding['all90_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==360
    historical_review=Path('work/analysis/lil_Seville_reference_approval_v2722/representative_sheet_review.json')
    prior_current_review=Path('work/analysis/lil_India_Polder_completion_v2818/current_six_frame_visual_review.json')
    for p in [historical_review,prior_current_review]:
        review=read(p);assert review['viewed'] and sha(Path(review['sheet']).read_bytes())==review['sha256']
    blocks=[]
    for original,checked in zip(plan['blocks'],census['blocks'],strict=True):
        assert original['block']==checked['block'] and checked['entry_point_offset']==8
        spec=deepcopy(original);spec['target_block_sha256']=spec.pop('research_block_sha256')
        spec.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],external_entry_and_actual_revised_paths_approval_pending=False,
            individual_selected_India_Polder_gameplay_unobserved=True)
        blocks.append(spec)
    arm=NdsImage.open(plan['candidate']).read_file('/__arm9__.bin')
    mapping=dict(format='dk4-lil-goods-mediterranean-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(arm),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=blocks,
        all273_nested_command_boundaries_and128_relative_sites_verified=True,all640_relocated_relative_skip_cases_preserve_original_targets=True,
        all32_relocated_native_predicates_preserve_source_semantics_and_mapped_cursor=True,
        representative_shared_rules_approved=True,representative_proof=str(SAMPLE),historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(prior_current_review),
        source_plan=str(PLAN),source_census=str(CENSUS),final_padding_proof=str(PADDING),actual_selected_India_Polder_IDs=[],
        individual_conditional_visits_not_required_under_user_policy=True,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(MAP,mapping)
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        representative_proof=str(SAMPLE),representative_proof_sha256=sha(SAMPLE.read_bytes()),historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(prior_current_review),
        final_padding_proof=str(PADDING),reference_map_pending=False,registered_integration_pending=True,
        status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for row in doc['records']:row['status']=doc['status']
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(OLD)['records']]
    save(DOC,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),reference_map=str(MAP),
        hashes={str(p):sha(p.read_bytes()) for p in [DOC,MAP,OLD,PLAN,CENSUS,SAMPLE,PADDING,historical_review,prior_current_review]},
        source_prose_English_unchanged=True,all90_source_native_reference_and_representative_rules_approved=True,
        actual_selected_India_Polder_IDs=[],new_emulator_runs=0,registered_release_and_current_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Sealed90source/native/reference/representative approvals:273commands,128spans/640cases,32relocatedpredicates,360finalparitymacro cases. Registeredrelease/startup pending.')
