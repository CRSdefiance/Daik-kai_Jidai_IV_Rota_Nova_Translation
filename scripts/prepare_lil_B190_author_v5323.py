"""Prepare all seventeen clean-first contextual decisions after conditional proofs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B190_author_tools_v5323')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/author_lil_B189_v5282.py');text=source.read_text(encoding='utf-8')
    a=text.index('    doc.update(records=rows');b=text.index('    ROOT.mkdir',a)
    semantic="""    doc.update(records=rows,revised=10,retained=7,
        source_Port_Worker119_and_progressive_Sailor159_catalogue_Retainer159_voices0_4_preserved=True,
        source_unknown_cause_retail_medicine_reported_one_go_cure_explicit_doubt_and_panacea_reputation_preserved=True,
        source_owner_not_invented_rank_kinship_or_employment_and_wish_not_joint_recommendation=True,
        source_common_knowledge_hyperbole_and_apparent_truth_are_character_claims=True,
        source_shopping_proposal_not_completed_purchase_use_or_recovery=True,
        source_Medicine13_full_and_compact_Med_Havana_binding_preserved=True,
        source29_commands_one500_predicate_six_relatives_three_A000_C200_end_and_two_tailzeros_preserved=True,
        FE_prospective_Medicine_Havana_notice_distinct_from_reported_efficacy_and_earlier_location=True,full_goal_complete=False)
"""
    row=derive(source,'scripts/author_lil_B190_v5323.py',{
        text[a:b]:semantic,'B189':'B190','lil_B189_prose_v5281':'lil_B190_prose_v5322','author_v5282':'author_v5323','comparison_v5280':'comparison_v5321',
        'voices_v5274b/current207_catalog_eight_voices_and_four_source_selectors':'voices_v5315/current207_catalog_eight_voices_and_two_source_selectors',
        'dispatches_v5275b/all17_source_current_dispatches_no_macros_and3_control_leaves':'dispatches_v5316/all17_source_current_dispatches_no_macros_and6_control_leaves',
        "        branch_proof='work/analysis/lil_B189_controls_v5277b/A000_C200_single_end_and_no_relative_or_predicate_contract.json',":
        "        branch_proof='work/analysis/lil_B190_branches_v5318/original_relative_skip_operand_proof.json',",
        'controls_v5277b/A000_C200_single_end_and_no_relative_or_predicate_contract':'controls_v5318/one_predicate_three_A000_C200_six_relative_sites_and_single_end',
        'entry_v5276b':'entry_v5317','names_v5278b/eight_original':'names_v5319/four_original',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_contextual_author.json',dict(derivation=row,all17_clean_glosses_and_source_roles_voices_conditional_paths_terms_before_comparison=True,
        no_credit_or_ROM_change=True,full_goal_complete=False))
