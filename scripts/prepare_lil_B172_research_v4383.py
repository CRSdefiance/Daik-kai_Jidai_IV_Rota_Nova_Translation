"""Prepare one-block B172 research image,whole loaders,census and guarded single end."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save,read
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B172_research_tools_v4383')
PARENT=Path('out/all_routes_combined_v4353_candidate.nds')
ROM=Path('out/lil_B172_reference_v4384_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B172_relocation_v4381/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists()
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4303' and len(registry['accepted_layers'])==114
    assert 'all-routes-unified-v4353' in registry['profiles']
    tools=[derive('scripts/create_lil_B171_reference_v4335.py','scripts/create_lil_B172_reference_v4384.py',{
        'V4303':'V4353','lil_B171_research_v4335':'lil_B172_research_v4384',
        'all_routes_combined_v4303':'all_routes_combined_v4353','lil_B171_reference_v4335':'lil_B172_reference_v4384',
        'lil_B171_relocation_v4332':'lil_B172_relocation_v4381',
        'lil_B171_stored_v4333/all37_final_stored_targets148':'lil_B172_stored_v4382/all27_final_stored_targets108',
        'releases/all_routes_unified_v4303/promotion.json':'work/analysis/editorial_handoff_verification_v4380/verified_handoff.json',
        "prior['rom_sha256']":"prior['candidate_sha256']",'all37_final_targets':'all27_final_targets',
        "current_final_stored_macro_alignment_cases']==148":"current_final_stored_macro_alignment_cases']==108",
        'current_final_stored_macro_alignment_cases=148':'current_final_stored_macro_alignment_cases=108',
        '[171]':'[172]','actual_selected_B171_IDs':'actual_selected_B172_IDs',
    })]
    common={'prepare_lil_B171_research_v4334':'prepare_lil_B172_research_v4383'}
    tools.append(derive('scripts/verify_lil_B171_loader_v4336.py','scripts/verify_lil_B172_loader_v4385.py',{
        **common,'lil_B171_research_v4335':'lil_B172_research_v4384','lil_B171_loader_v4336':'lil_B172_loader_v4385','B171':'B172',
    }))
    tools.append(derive('scripts/verify_lil_B171_references_v4337.py','scripts/verify_lil_B172_references_v4386.py',{
        **common,'lil_B171_reference_census_v4337':'lil_B172_reference_census_v4386',
        'lil_B171_loader_v4336':'lil_B172_loader_v4385','B171':'B172','[171]':'[172]',
        'for r in result)==45':'for r in result)==38','all45':'all38','native_commands_each=45':'native_commands_each=38',
        '45-command/zero-span':'38-command/zero-span',
    }))
    tools.append(derive('scripts/prove_lil_B171_ends_v4338.py','scripts/prove_lil_B172_ends_v4387.py',{
        **common,'Decode both B171 consecutive endwords per image':'Decode the single B172 tail endword per image',
        'lil_B171_ends_v4338':'lil_B172_ends_v4387','assert n==171 and len(ends)==2':'assert n==172 and len(ends)==1',
        "len(cases)==4 and sum(not c['at_logical_tail'] for c in cases)==2":"len(cases)==2 and sum(not c['at_logical_tail'] for c in cases)==0",
        'four_declared_end_decodes_and_zero_relative_sites':'two_declared_end_decodes_and_zero_relative_sites',
        'all4_declared_end_decodes':'all2_declared_end_decodes',
        'B171_first_end_precedes_second_end_and_declared_logical_end':'B172_single_end_finishes_declared_logical_end',
        'second_B171_declared_word_decoder_probe_not_actual_reachability_claim':'single_B172_tail_word_decoder_probe_not_actual_reachability_claim',
        'Four declared current/target endwords pass with poisoned unread post-payload guards;B171 both ends preserved.':'Two declared current/target tail endwords pass with poisoned unread post-payload guards;B172 single end preserved.',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=172,commands=38,relative_sites=0,pause=0,C200=1,endwords=1,
        nonrelative_leaves=11,source_resources=[0x6329,0x6340,0x632A],A000_hex='00a0ffff010cc960',source_C200_before_A000=True,
        registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),promoted_main='all-routes-unified-v4303',
        research_parent='all-routes-unified-v4353',no_registry_ledger_credit_change=True,full_goal_complete=False))
    print('Prepared B172 research image,whole loaders,38-command census and single-end decoder producers;main V4303 preserved.')
