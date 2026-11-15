"""Seal source/target reference approval under the user's representative policy."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Seville_reference_approval_v2722')
MAP=Path('translations/lil_seville_editorial_relocation_map_v1.json')
PROSE=Path('translations/lil_seville_encounter_editorial_manuscript_v4.json')
CHOICES=Path('translations/lil_seville_choices_editorial_draft_v3.json')
PLAN=Path('work/analysis/lil_Seville_relocation_v2716/nested_source_relocation_research.json')
CENSUS=Path('work/analysis/lil_Seville_reference_census_v2720/all69_commands28_relative_sites_and_shipped_entry_census.json')
SAMPLE=Path('work/analysis/lil_Seville_sampling_v2721b/representative_rule_reconciliation.json')

if __name__=='__main__':
    assert not any(p.exists() for p in [ROOT,MAP,PROSE,CHOICES])
    plan,census,sample=read(PLAN),read(CENSUS),read(SAMPLE)
    assert census['all69_clean_current_target_commands_and28_relative_sites_reexecuted']
    assert census['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    assert sample['no_open_translation_specific_display_or_control_finding'] and sample['actual_Seville_IDs']==[]
    assert sample['all4_historical_progressive_holds_freshly_match_current_full_ink_gray_blank_masks']
    sheet=Path(sample['review_sheet']);assert sha(sheet.read_bytes())==sample['review_sheet_sha256']
    # The complete four-panel representative sheet was viewed in this turn.
    ROOT.mkdir(parents=True)
    review=ROOT/'representative_sheet_review.json'
    save(review,dict(sheet=str(sheet),sha256=sha(sheet.read_bytes()),viewed=True,
        findings='Complete Lil and Gerhard text and nameplates, centered two-choice menu, and separate FE tutorial paper are legible. Historical shared consumer evidence only; no Seville activation.',
        source_reconciliation=str(SAMPLE),source_sha256=sha(SAMPLE.read_bytes())))
    blocks=[]
    for prior,checked in zip(plan['blocks'],census['blocks'],strict=True):
        assert prior['block']==checked['block'] and checked['entry_point_offset']==8
        block=deepcopy(prior);block['target_block_sha256']=block.pop('research_block_sha256')
        block.update(external_references_complete=True,entry_point_offset=8,mapped_native_commands=checked['mapped_commands'])
        block['external_entry_and_actual_revised_paths_approval_pending']=False
        block['individual_Seville_gameplay_unobserved']=True
        blocks.append(block)
    clean=NdsImage.open('work/clean.nds');canonical=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    arm=NdsImage.open(plan['candidate']).read_file('/__arm9__.bin')
    mapping=dict(format='dk4-lil-seville-source-relocation-map-v1',required_runtime_ARM9_sha256=sha(arm),
        source_SC2_sha256=plan['source_SC2_sha256'],target_SC2_sha256=plan['target_SC2_sha256'],
        clean_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),canonical_SC2_sha256=sha(canonical.read_file('/data/SC2.DK4')),
        entry_point_offset=8,preserve_record_parity=True,external_references_complete=True,blocks=blocks,
        all69_nested_command_boundaries_and28_relative_sites_verified=True,
        all140_relocated_relative_skip_cases_preserve_original_targets=True,
        representative_shared_rules_approved=True,representative_proof=str(SAMPLE),representative_sheet_review=str(review),
        actual_Seville_IDs=[],individual_conditional_visits_not_required_under_user_policy=True,
        source_plan=str(PLAN),source_census=str(CENSUS),full_goal_complete=False)
    save(MAP,mapping)
    for previous,target in [(Path('translations/lil_seville_encounter_editorial_manuscript_v3.json'),PROSE),
                            (Path('translations/lil_seville_choices_editorial_draft_v2.json'),CHOICES)]:
        doc=read(previous);doc.update(previous_manuscript=str(previous),previous_manuscript_sha256=sha(previous.read_bytes()),
            reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),representative_proof=str(SAMPLE),
            representative_sheet_review=str(review),reference_map_pending=False,registered_integration_pending=True,
            status='source-prose-native-references-representative-approved;registered-release-startup-pending')
        for row in doc['records']:
            row['status']=doc['status']
            if 'source_record_index' in row:
                row['record_index']=row['current_record_index'];row['current_text_hex']=row['current_hex']
                row['native_display_consumer']='original_FE_modal_5473C_mode1' if row['source_presentation_prefix_hex']=='fe' else 'original_progressive_54020'
            else:row['current_text_hex']=row['current_hex']
        assert all(r['review']['formatting'] for r in doc['records'])
        save(target,doc)
    save(ROOT/'approval_receipt.json',dict(reference_map=str(MAP),manuscript=str(PROSE),choices=str(CHOICES),
        hashes={str(p):sha(p.read_bytes()) for p in [MAP,PROSE,CHOICES,PLAN,CENSUS,SAMPLE,review]},
        source_prose_English_unchanged=True,all20_source_native_and_reference_rules_approved=True,
        actual_Seville_IDs=[],new_emulator_runs=0,registered_release_and_startup_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Sealed20 source/prose/native/reference approvals;69 commands,28relative sites,140cases;representative policy explicit. Registered release/startup pending.')
