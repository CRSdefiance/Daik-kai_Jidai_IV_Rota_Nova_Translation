"""Seal145 source/current target references and shared representative approval."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Christina_Mivor_reference_approval_v3064')
MAP=Path('translations/lil_christina_mivor_editorial_relocation_map_v1.json')
OLD=Path('translations/lil_christina_mivor_editorial_manuscript_v7.json')
DOC=Path('translations/lil_christina_mivor_editorial_manuscript_v8.json')
PLAN=Path('work/analysis/lil_Christina_Mivor_relocation_v3059/nested_source_relocation_research.json')
CENSUS=Path('work/analysis/lil_Christina_Mivor_reference_census_v3062/all236_commands12_relative_sites_and_shipped_entry_census.json')
SAMPLE=Path('work/analysis/lil_Christina_Mivor_sampling_v3063/relocated_predicates_and_representative_rule_reconciliation.json')
PADDING=Path('work/analysis/lil_Christina_Mivor_research_v3060/research_image_receipt.json')
if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,MAP,DOC]);plan,census,sample,padding=map(read,[PLAN,CENSUS,SAMPLE,PADDING]);doc=deepcopy(read(OLD))
    assert census['all236_clean_current_target_commands_and12_relative_sites_reexecuted'] and census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_selected_Christina_Mivor_IDs']==[]
    assert sample['all3_relocated_original_predicates_preserve_source_operands_results_and_event_query_arguments']
    assert padding['all145_final_targets_complete_native_planes_equal_reviewed_planes'] and padding['current_final_padded_macro_alignment_cases']==580
    historical_review=Path('work/analysis/lil_Seville_reference_approval_v2722/representative_sheet_review.json')
    prior_current_review=Path('work/analysis/lil_Homecoming_Ian_completion_v3033/current_six_frame_visual_review.json')
    for p in [historical_review,prior_current_review]:
        review=read(p);assert review['viewed'] and sha(Path(review['sheet']).read_bytes())==review['sha256']
    blocks=[]
    for original,checked in zip(plan['blocks'],census['blocks'],strict=True):
        assert original['block']==checked['block'] and checked['entry_point_offset']==8
        spec=deepcopy(original);spec['target_block_sha256']=spec.pop('research_block_sha256')
        spec.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'],external_entry_and_actual_revised_paths_approval_pending=False,
            individual_selected_Christina_Mivor_gameplay_unobserved=True)
        blocks.append(spec)
    arm=NdsImage.open(plan['candidate']).read_file('/__arm9__.bin')
    mapping=dict(format='dk4-lil-christina-mivor-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(arm),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')),
        canonical_SC2_sha256=sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=blocks,
        all236_nested_command_boundaries_and12_relative_sites_verified=True,all60_relocated_relative_skip_cases_preserve_original_targets=True,
        all3_relocated_native_predicates_preserve_source_semantics_and_mapped_cursor=True,
        all3_FE_source_Boy_labels_preserved=True,
        representative_shared_rules_approved=True,representative_proof=str(SAMPLE),historical_representative_sheet_review=str(historical_review),prior_current_sheet_review=str(prior_current_review),
        source_plan=str(PLAN),source_census=str(CENSUS),final_padding_proof=str(PADDING),actual_selected_Christina_Mivor_IDs=[],
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
        source_prose_English_unchanged=True,all145_source_native_reference_and_representative_rules_approved=True,
        actual_selected_Christina_Mivor_IDs=[],new_emulator_runs=0,registered_release_and_current_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Sealed145 source/native/reference/representative approvals:236commands,12spans/60cases,3predicates/noqueries,580finalparity macro cases. Registeredrelease/startup pending.')
