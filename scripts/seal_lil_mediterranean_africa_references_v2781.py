"""Seal34 source/current target references and shared representative approval."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Mediterranean_Africa_reference_approval_v2781')
MAP=Path('translations/lil_mediterranean_africa_editorial_relocation_map_v1.json')
OLD=Path('translations/lil_mediterranean_africa_editorial_manuscript_v4.json')
DOC=Path('translations/lil_mediterranean_africa_editorial_manuscript_v5.json')
PLAN=Path('work/analysis/lil_Mediterranean_Africa_relocation_v2776/nested_source_relocation_research.json')
CENSUS=Path('work/analysis/lil_Mediterranean_Africa_reference_census_v2779/all353_commands124_relative_sites_and_shipped_entry_census.json')
SAMPLE=Path('work/analysis/lil_Mediterranean_Africa_sampling_v2780/relocated_predicates_and_representative_rule_reconciliation.json')
PADDING=Path('work/analysis/lil_Mediterranean_Africa_research_v2777/research_image_receipt.json')
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,MAP,DOC]);plan,census,sample,padding=map(read,[PLAN,CENSUS,SAMPLE,PADDING]);doc=deepcopy(read(OLD))
    assert census['all353_clean_current_target_commands_and124_relative_sites_reexecuted'] and census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_selected_Mediterranean_Africa_IDs']==[]
    assert sample['all28_relocated_original_predicates_preserve_source_operands_results_and_event_query_arguments']
    assert padding['all146_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==584
    historical_review=Path('work/analysis/lil_Seville_reference_approval_v2722/representative_sheet_review.json')
    prior_current_review=Path('work/analysis/lil_post_Seville_completion_v2754/current_six_frame_visual_review.json')
    for p in [historical_review,prior_current_review]:
        review=read(p);assert review['viewed'] and sha(Path(review['sheet']).read_bytes())==review['sha256']
    blocks=[]
    for original,checked in zip(plan['blocks'],census['blocks'],strict=True):
        assert original['block']==checked['block'] and checked['entry_point_offset']==8
        spec=deepcopy(original);spec['target_block_sha256']=spec.pop('research_block_sha256')
        spec.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],external_entry_and_actual_revised_paths_approval_pending=False,
            individual_selected_Mediterranean_Africa_gameplay_unobserved=True)
        blocks.append(spec)
    arm=NdsImage.open(plan['candidate']).read_file('/__arm9__.bin')
    mapping=dict(format='dk4-lil-mediterranean-africa-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(arm),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=blocks,
        all353_nested_command_boundaries_and124_relative_sites_verified=True,all620_relocated_relative_skip_cases_preserve_original_targets=True,
        all28_relocated_native_predicates_preserve_source_semantics_and_mapped_cursor=True,
        representative_shared_rules_approved=True,representative_proof=str(SAMPLE),historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(prior_current_review),
        source_plan=str(PLAN),source_census=str(CENSUS),final_padding_proof=str(PADDING),actual_selected_Mediterranean_Africa_IDs=[],
        individual_conditional_visits_not_required_under_user_policy=True,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(MAP,mapping)
    choice_old=Path('translations/lil_mediterranean_africa_choices_editorial_draft_v3.json');choice_out=Path('translations/lil_mediterranean_africa_choices_editorial_draft_v4.json');assert not choice_out.exists()
    choice=deepcopy(read(choice_old));choice.update(previous_manuscript=str(choice_old),previous_manuscript_sha256=sha(choice_old.read_bytes()),reference_map=str(MAP),representative_proof=str(SAMPLE),registered_integration_pending=True,status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for row in choice['records']:row.update(current_text_hex=row['current_hex'],status=choice['status'])
    save(choice_out,choice)
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),
        representative_proof=str(SAMPLE),representative_proof_sha256=sha(SAMPLE.read_bytes()),historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(prior_current_review),
        choices=str(choice_out),choices_sha256=sha(choice_out.read_bytes()),final_padding_proof=str(PADDING),reference_map_pending=False,registered_integration_pending=True,
        status='source-prose-native-references-representative-approved;registered-release-startup-pending')
    for row in doc['records']:
        row['status']=doc['status'];row['native_display_consumer']='original_FE_modal_5473C_mode1' if row['kind']=='system-FE' else 'original_progressive_54020'
    assert [r['english'] for r in doc['records']]==[r['english'] for r in read(OLD)['records']]
    save(DOC,doc)
    save(ROOT/'approval_receipt.json',dict(manuscript=str(DOC),reference_map=str(MAP),
        hashes={str(p):sha(p.read_bytes()) for p in [DOC,MAP,OLD,PLAN,CENSUS,SAMPLE,PADDING,historical_review,prior_current_review,choice_old,choice_out]},
        source_prose_English_unchanged=True,all152_source_native_reference_and_representative_rules_approved=True,
        actual_selected_Mediterranean_Africa_IDs=[],new_emulator_runs=0,registered_release_and_current_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Sealed152 source/native/reference/representative approvals:353commands,124spans/620cases,28relocated predicates,584final-padding calls. Registered release/startup pending.')
