"""Prepare one-block B170 research image,whole loader,census and guarded ends."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B170_research_tools_v4283')
PARENT=Path('out/all_routes_combined_v4251_candidate.nds')
ROM=Path('out/lil_B170_reference_v4284_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B170_relocation_v4281/nested_source_relocation_research.json')
if __name__=='__main__':
    assert not ROOT.exists()
    tools=[derive('scripts/create_lil_B169_reference_v4236.py','scripts/create_lil_B170_reference_v4284.py',{
        'V4204':'V4251','lil_B169_research_v4236':'lil_B170_research_v4284',
        'all_routes_combined_v4204':'all_routes_combined_v4251',
        'lil_B169_reference_v4236':'lil_B170_reference_v4284',
        'lil_B169_relocation_v4233':'lil_B170_relocation_v4281',
        'lil_B169_stored_v4234/all36_final_stored_targets144':'lil_B170_stored_v4282/all33_final_stored_targets132',
        'editorial_handoff_verification_v4209':'editorial_handoff_verification_v4280',
        'all36_final_targets':'all33_final_targets',
        "current_final_stored_macro_alignment_cases']==144":"current_final_stored_macro_alignment_cases']==132",
        'current_final_stored_macro_alignment_cases=144':'current_final_stored_macro_alignment_cases=132',
        '[169]':'[170]','actual_selected_B169_IDs':'actual_selected_B170_IDs',
    })]
    common={'prepare_lil_B169_research_v4235':'prepare_lil_B170_research_v4283'}
    tools.append(derive('scripts/verify_lil_B169_loader_v4237.py','scripts/verify_lil_B170_loader_v4285.py',{
        **common,'lil_B169_research_v4236':'lil_B170_research_v4284',
        'lil_B169_loader_v4237':'lil_B170_loader_v4285','B169':'B170',
    }))
    tools.append(derive('scripts/verify_lil_B169_references_v4238.py','scripts/verify_lil_B170_references_v4286.py',{
        **common,'lil_B169_reference_census_v4238':'lil_B170_reference_census_v4286',
        'lil_B169_loader_v4237':'lil_B170_loader_v4285','B169':'B170','[169]':'[170]',
        'for r in result)==53':'for r in result)==45','all53_commands12_relative_sites':'all45_commands_zero_relative_sites',
        'all53_clean_current_target_commands_and12_relative_sites':'all45_clean_current_target_commands_and_zero_relative_sites',
        'native_commands_each=53':'native_commands_each=45','53-command/12-span':'45-command/zero-span',
        "sum(r['typed_relative_span_count']for r in result)==12":"sum(r['typed_relative_span_count']for r in result)==0",
        "sum(r['target_native_skip_cases']for r in result)==60":"sum(r['target_native_skip_cases']for r in result)==0",
        'relative_sites=12,target_native_skip_cases=60':'relative_sites=0,target_native_skip_cases=0',
    }))
    tools.append(derive('scripts/prove_lil_B169_ends_v4239.py','scripts/prove_lil_B170_ends_v4287.py',{
        **common,'Decode the single B169 tail endword per image with poisoned unread guards.':'Decode both B170 consecutive endwords per image with poisoned unread guards.',
        'lil_B169_ends_v4239':'lil_B170_ends_v4287',
        'assert n==169 and len(ends)==1':'assert n==170 and len(ends)==2',
        "len(cases)==2 and sum(not c['at_logical_tail'] for c in cases)==0":"len(cases)==4 and sum(not c['at_logical_tail'] for c in cases)==2",
        'two_declared_end_decodes_and_all12_in_block_relative_destinations':'four_declared_end_decodes_and_zero_relative_sites',
        'all2_declared_end_decodes':'all4_declared_end_decodes',
        'B169_single_end_finishes_declared_logical_end':'B170_first_end_precedes_second_end_and_declared_logical_end',
        'single_B169_tail_word_decoder_probe_not_actual_reachability_claim':'second_B170_declared_word_decoder_probe_not_actual_reachability_claim',
        'Two declared current/target tail ends pass with poisoned unread post-payload guards;B169 single end preserved.':'Four declared current/target endwords pass with poisoned unread post-payload guards;B170 both ends preserved.',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=170,commands=45,relative_sites=0,pause=1,
        C200=1,endwords=2,nonrelative_leaves=12,source_resources=[0x6342,0x632D],A000_hex='00a0ffff19100120',
        no_registry_ledger_credit_change=True,full_goal_complete=False))
    print('B170 research image,whole loader,census and both-end decode producers prepared;no release approval.')
