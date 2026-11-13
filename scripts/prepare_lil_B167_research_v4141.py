"""Derive the one-block reference image and source-bound loader, end and control probes."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B167_research_tools_v4141')
PARENT=Path('out/all_routes_combined_v4110_candidate.nds')
ROM=Path('out/lil_B167_reference_v4142_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B167_relocation_v4139/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists();tools=[]
    tools.append(derive('scripts/create_lil_B166_reference_v4096.py','scripts/create_lil_B167_reference_v4142.py',{
        'lil_B166_research_v4096':'lil_B167_research_v4142','lil_B166_reference_v4096':'lil_B167_reference_v4142',
        'lil_B166_relocation_v4093':'lil_B167_relocation_v4139',
        'lil_B166_stored_v4094/all42_final_stored_targets168':'lil_B167_stored_v4140/all27_final_stored_targets108',
        'all_routes_combined_v4046':'all_routes_combined_v4110','V4046':'V4110',
        'editorial_handoff_verification_v4091':'editorial_handoff_verification_v4137',
        'all42_final_targets':'all27_final_targets',"current_final_stored_macro_alignment_cases']==168":"current_final_stored_macro_alignment_cases']==108",
        'current_final_stored_macro_alignment_cases=168':'current_final_stored_macro_alignment_cases=108',
        '[166]':'[167]','actual_selected_B166_IDs':'actual_selected_B167_IDs'
    }))
    common={'prepare_lil_B166_research_v4095':'prepare_lil_B167_research_v4141','lil_B166_research_v4096':'lil_B167_research_v4142'}
    tools.append(derive('scripts/verify_lil_B166_loader_v4097.py','scripts/verify_lil_B167_loader_v4143.py',{
        **common,'lil_B166_loader_v4097':'lil_B167_loader_v4143','B166':'B167'}))
    tools.append(derive('scripts/verify_lil_B166_references_v4098.py','scripts/verify_lil_B167_references_v4144.py',{
        **common,'lil_B166_reference_census_v4098':'lil_B167_reference_census_v4144',
        'lil_B166_loader_v4097':'lil_B167_loader_v4143','B166':'B167','[166]':'[167]',
        'for r in result)==62':'for r in result)==46','for r in result)==8':'for r in result)==12','for r in result)==40':'for r in result)==60',
        'all62_commands8_relative_sites':'all46_commands12_relative_sites',
        'all62_clean_current_target_commands_and8_relative_sites':'all46_clean_current_target_commands_and12_relative_sites',
        'native_commands_each=62,relative_sites=8,target_native_skip_cases=40':'native_commands_each=46,relative_sites=12,target_native_skip_cases=60',
        '62-command/8-span':'46-command/12-span'}))
    tools.append(derive('scripts/prove_lil_B164_ends_v3991.py','scripts/prove_lil_B167_ends_v4145.py',{
        'advice endwords':'refusal and lecture endwords',
        'prepare_lil_B164_research_v3988':'prepare_lil_B167_research_v4141',
        'lil_B164_ends_v3991':'lil_B167_ends_v4145',
        'assert len(ends)==(2 if n==164 else 1)':'assert n==167 and len(ends)==2',
        'four_declared_end_decodes_and_all4':'four_declared_end_decodes_and_all12','B164':'B167'}))
    tools.append(derive('scripts/prove_lil_B166_relocated_controls_v4100.py','scripts/prove_lil_B167_relocated_controls_v4146.py',{
        **common,'Bind relocated speakers/FI3, Fernando membership, leaves and advice menu getters.':'Bind all relocated static speakers, two Cesare queries, six leaves and accept/refuse getters.',
        'lil_B166_relocated_controls_v4100':'lil_B167_relocated_controls_v4146',
        'lil_B166_editorial_manuscript_v5':'lil_B167_editorial_manuscript_v12',
        'lil_B166_choice_manuscript_v2':'lil_B167_choice_manuscript_v2',
        '[166]':'[167]','block=166':'block=167',
        'len(dispatches) == 42 and len(leaves) == 11 and len(predicates) == 1':'len(dispatches) == 27 and len(leaves) == 6 and len(predicates) == 2',
        "assert sum(c['word'] == 0xA000 for c in leaves) == sum(c['word'] == 0 for c in leaves) == 1":"assert sum(c['word'] == 0xA000 for c in leaves)==0 and sum(c['word'] == 0 for c in leaves)==2",
        '[0x632B, 0x632C]':'[0x6327, 0x632B]',"['Please do', 'Decline']":"['Okay', 'No thanks']",
        'all42_dispatches_Fernando_predicate11_leaves':'all27_dispatches_two_Cesare_predicates6_leaves',
        'all11_source_current_target':'all6_source_current_target',
        'all42_progressive_consumers_four_static_actors_FI3_exact':'all27_progressive_consumers_five_static_actors_no_macros_exact',
        'unforced_Fernando_result_matches_source_without_roster_fixture':'both_unforced_Cesare_results_match_source_without_roster_fixture',
        'menu_VM_and_complete_native_planes_reused_by_exact24byte_object':'menu_VM_and_complete_native_planes_reused_by_exact22byte_object',
        'resource_presentation_and_A000_bodies_not_fully_executed_by_this_probe':'resource_callee_bodies_not_fully_executed_by_this_probe_no_A000_or_other_presentation_commands',
        'both_advice_paths_rejoin_before_unchanged_recruitment_effect_and_single_end':'accept_and_refuse_paths_keep_separate_ends_and_later_query_result_not_menu_index',
        'actual_selected_B166_IDs':'actual_selected_B167_IDs',
        '42 relocated speakers/FI3,one source-matched Fernando query,11 exact leaves':'27 relocated static speakers,two source-matched Cesare queries,six exact leaves'
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,source_block=167,commands=46,relative_sites=12,separated_endwords=2,membership_queries=2,opaque_leaves=6,resource_words=[0x6327,0x632B],no_A000=True,no_registry_ledger_credit_change=True))
    print('B167 one-block reference,whole loader,census,two-end and control successors created.')
