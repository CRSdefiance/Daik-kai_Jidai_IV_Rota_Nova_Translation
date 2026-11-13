"""Preserve the proven authoring schema with B182-specific decisions and controls."""
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    print(derive('scripts/author_lil_B181_v4841.py','scripts/author_lil_B182_v4888.py',{
        'B181':'B182','author_v4841':'author_v4888','prose_v4840':'prose_v4887',
        'comparison_v4839/all10':'comparison_v4886/all8',"len(gloss['records'])==10":"len(gloss['records'])==8",
        'voices_v4833/current207_catalog_eight_voices_and_three_source_selectors':'voices_v4879/current207_catalog_eight_voices_and_two_source_selectors',
        'dispatches_v4834/all10_source_current_dispatches_no_macros_and3_control_leaves':'dispatches_v4880/all8_source_current_dispatches_no_macros_and7_control_leaves',
        'controls_v4836/A000_C200_single_end_and_no_relative_or_predicate_contract':'controls_v4883/two_predicates_three_A000_C200_ten_relative_sites_and_single_end',
        'entry_v4835':'entry_v4882','names_v4837/six_original_Lady_name_consumers':'names_v4884/four_original_Lady_name_consumers',
        "branch_proof='work/analysis/lil_B181_controls_v4836/A000_C200_single_end_and_no_relative_or_predicate_contract.json'":
        "branch_proof='work/analysis/lil_B182_branches_v4881/original_relative_skip_operand_proof.json'",
        "counts=={'revise':5,'retain-wording':5}":"counts=={'revise':6,'retain-wording':2}",
        'records=rows,revised=5,retained=5,no_nobility_marriage_giver_identity_or_necklace_provenance_invented=True':
        'records=rows,revised=6,retained=2,source_explicit_princess_duke_and_son_preserved_without_inventing_names_or_marriage=True',
        'three_distinct_Lady_selectors_and_impersonal_FE_preserved=True,three_successive_source_sighs_preserved=True':
        'two_distinct_Lady_selectors_and_impersonal_FE_preserved=True,reported_engagement_ring_hyperbole_and_unknown_gem_joke_preserved=True',
        'source_all13_commands_no_predicates_or_relative_sites_preserved=True':
        'source_all25_commands_two500_predicates_ten_relative_sites_three_alternative_A000_C200_and_end_preserved=True',
        'all10_clean_first_contextual_decisions':'all8_clean_first_contextual_decisions',
        'all5_retentions_individually_justified':'all2_retentions_individually_justified',
        'all10_current_source_records_reviewed_as_one_exchange':'all8_current_source_records_reviewed_as_one_exchange',
        'Ten B181 decisions:5 revisions/5 justified retentions;explicit wish,three audible sighs and neutral Rubies forecast. Native approval pending;zero credit.':
        'Eight B182 decisions:6 revisions/2 justified retentions;reported engagement,explicit ranks/son,ring hyperbole and unknown gem joke. Native approval pending;zero credit.'
    }))
