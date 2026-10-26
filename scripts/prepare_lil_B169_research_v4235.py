"""Prepare the whole-loader, entry, end and relocated-dispatch probes for B169."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B169_research_tools_v4235')
PARENT = Path('out/all_routes_combined_v4204_candidate.nds')
ROM = Path('out/lil_B169_reference_v4236_RESEARCH_ONLY.nds')
PLAN = Path('work/analysis/lil_B169_relocation_v4233/nested_source_relocation_research.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    tools = [derive('scripts/create_lil_B168_reference_v4193.py','scripts/create_lil_B169_reference_v4236.py',{
        'V4160':'V4204','lil_B168_research_v4193':'lil_B169_research_v4236',
        'all_routes_combined_v4160':'all_routes_combined_v4204',
        'lil_B168_reference_v4193':'lil_B169_reference_v4236',
        'lil_B168_relocation_v4190':'lil_B169_relocation_v4233',
        'lil_B168_stored_v4191/all54_final_stored_targets216':'lil_B169_stored_v4234/all36_final_stored_targets144',
        'editorial_handoff_verification_v4189':'editorial_handoff_verification_v4209',
        'all54_final_targets':'all36_final_targets',
        "current_final_stored_macro_alignment_cases']==216":"current_final_stored_macro_alignment_cases']==144",
        'current_final_stored_macro_alignment_cases=216':'current_final_stored_macro_alignment_cases=144',
        '[168]':'[169]','actual_selected_B168_IDs':'actual_selected_B169_IDs',
    })]
    common = {'prepare_lil_B168_research_v4192':'prepare_lil_B169_research_v4235'}
    tools.append(derive('scripts/verify_lil_B168_loader_v4194.py','scripts/verify_lil_B169_loader_v4237.py',{
        **common,'lil_B168_research_v4193':'lil_B169_research_v4236',
        'lil_B168_loader_v4194':'lil_B169_loader_v4237','B168':'B169',
    }))
    tools.append(derive('scripts/verify_lil_B168_references_v4195.py','scripts/verify_lil_B169_references_v4238.py',{
        **common,'lil_B168_reference_census_v4195':'lil_B169_reference_census_v4238',
        'lil_B168_loader_v4194':'lil_B169_loader_v4237','B168':'B169','[168]':'[169]',
        'for r in result)==82':'for r in result)==53','all82_commands12_relative_sites':'all53_commands12_relative_sites',
        'all82_clean_current_target_commands_and12_relative_sites':'all53_clean_current_target_commands_and12_relative_sites',
        'native_commands_each=82':'native_commands_each=53','82-command/12-span':'53-command/12-span',
    }))
    tools.append(derive('scripts/prove_lil_B168_ends_v4196.py','scripts/prove_lil_B169_ends_v4239.py',{
        **common,'Decode both declared endwords per image,including both consecutive B168 endwords.':'Decode the single B169 tail endword per image with poisoned unread guards.',
        'lil_B168_ends_v4196':'lil_B169_ends_v4239',
        'assert n==168 and len(ends)==2':'assert n==169 and len(ends)==1',
        "len(cases)==4 and sum(not c['at_logical_tail'] for c in cases)==2":"len(cases)==2 and sum(not c['at_logical_tail'] for c in cases)==0",
        'four_declared_end_decodes':'two_declared_end_decodes',
        'all4_declared_end_decodes':'all2_declared_end_decodes',
        'B168_first_end_precedes_second_end_and_declared_logical_end':'B169_single_end_finishes_declared_logical_end',
        'second_B168_declared_word_decoder_probe_not_actual_reachability_claim':'single_B169_tail_word_decoder_probe_not_actual_reachability_claim',
        'Four declared current/target endwords pass with poisoned unread post-payload guards;B168 bothwords preserved.':'Two declared current/target tail ends pass with poisoned unread post-payload guards;B169 single end preserved.',
    }))
    tools.append(derive('scripts/prove_lil_B168_relocated_controls_v4197.py','scripts/prove_lil_B169_relocated_controls_v4240.py',{
        **common,'Bind relocated progressive/FE dispatch, substitutions, three predicates and all16 leaves.':'Bind36 relocated progressive dispatches, substitutions, three predicates and all five leaves.',
        'lil_B168_relocated_controls_v4197':'lil_B169_relocated_controls_v4240',
        'lil_B168_editorial_manuscript_v7':'lil_B169_editorial_manuscript_v4',
        'blocks[168]':'blocks[169]','block=168':'block=169',
        'len(dispatches) == 54 and len(leaves) == 16':'len(dispatches) == 36 and len(leaves) == 5',
        "sum(case['resolved_actor_ID'] is None for case in dispatches) == 3":"sum(case['resolved_actor_ID'] is None for case in dispatches) == 0",
        "sum(case['word'] == 0 for case in leaves) == 2":"sum(case['word'] == 0 for case in leaves) == 1",
        '== [0x6342, 0x630B, 0x6300, 0x6301]':'== []',
        'len(presentations) == 6':'len(presentations) == 0',
        'all54_progressive_FE_dispatches_three_predicates_and16_leaves':'all36_progressive_dispatches_three_predicates_and5_leaves',
        'all16_source_current_target_nonrelative_nonspeech_leaves':'all5_source_current_target_nonrelative_nonspeech_leaves',
        'all51_progressive_and3_null_actor_FE_consumers_FI7_FA1_FO1_exact':'all36_progressive_consumers_FI5_FO2_exact',
        'all40_resource_boundary_cases_reused_by_exact_words_runtime_and_dispatch':'no_source_resource_commands_in_this_block',
        'source_six_presentation_structural_results_reused_only_by_exact_whole_command_and_runtime':'no_source_presentation_commands_in_this_block',
        'source_resource_presentation_and_A000_callee_bodies_not_fully_executed_by_this_probe':'later_A000_callee_body_not_fully_executed_by_this_probe',
        'source_A000_after_touch_protest_yelp_sigh_and_before_FE_notices_preserved':'source_numeric29_0001_A000_after_final_give_and_take_and_before_end_preserved',
        'both_consecutive_endwords_and_all_relative_containers_preserved':'single_tail_endword_and_all_relative_containers_preserved',
        'actual_selected_B168_IDs':'actual_selected_B169_IDs',
        '54 relocated progressive/FE dispatches, three source-matched predicates and16 exact leaves pass.':'36 relocated progressive dispatches, three source-matched predicates and five exact leaves pass.',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=169,commands=53,relative_sites=12,
        tail_endwords=1,predicates=3,opaque_leaves=5,resources=0,presentations=0,A000=1,
        numeric_A000_operands=[29,1],no_recruitment_or_earned_flag_claim=True,no_registry_ledger_credit_change=True))
    print('B169 one-block reference, whole loader, entry census, single end and five-leaf probes prepared.')
