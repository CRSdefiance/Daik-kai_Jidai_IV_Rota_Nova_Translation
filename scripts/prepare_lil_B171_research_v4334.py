"""Prepare B171 research image, whole loaders, reference census and end decodes."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save, read
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B171_research_tools_v4334')
PARENT=Path('out/all_routes_combined_v4303_candidate.nds')
ROM=Path('out/lil_B171_reference_v4335_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B171_relocation_v4332/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists()
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4303'
    assert len(registry['accepted_layers'])==114
    tools=[derive('scripts/create_lil_B170_reference_v4284.py','scripts/create_lil_B171_reference_v4335.py',{
        'V4251':'V4303','lil_B170_research_v4284':'lil_B171_research_v4335',
        'all_routes_combined_v4251':'all_routes_combined_v4303',
        'lil_B170_reference_v4284':'lil_B171_reference_v4335',
        'lil_B170_relocation_v4281':'lil_B171_relocation_v4332',
        'lil_B170_stored_v4282/all33_final_stored_targets132':'lil_B171_stored_v4333/all37_final_stored_targets148',
        'work/analysis/editorial_handoff_verification_v4280/verified_handoff.json':'releases/all_routes_unified_v4303/promotion.json',
        "prior['candidate_sha256']":"prior['rom_sha256']",
        'all33_final_targets':'all37_final_targets',
        "current_final_stored_macro_alignment_cases']==132":"current_final_stored_macro_alignment_cases']==148",
        'current_final_stored_macro_alignment_cases=132':'current_final_stored_macro_alignment_cases=148',
        '[170]':'[171]','actual_selected_B170_IDs':'actual_selected_B171_IDs',
    })]
    common={'prepare_lil_B170_research_v4283':'prepare_lil_B171_research_v4334'}
    tools.append(derive('scripts/verify_lil_B170_loader_v4285.py','scripts/verify_lil_B171_loader_v4336.py',{
        **common,'lil_B170_research_v4284':'lil_B171_research_v4335',
        'lil_B170_loader_v4285':'lil_B171_loader_v4336','B170':'B171',
    }))
    tools.append(derive('scripts/verify_lil_B170_references_v4286.py','scripts/verify_lil_B171_references_v4337.py',{
        **common,'lil_B170_reference_census_v4286':'lil_B171_reference_census_v4337',
        'lil_B170_loader_v4285':'lil_B171_loader_v4336','B170':'B171','[170]':'[171]',
    }))
    tools.append(derive('scripts/prove_lil_B170_ends_v4287.py','scripts/prove_lil_B171_ends_v4338.py',{
        **common,'lil_B170_ends_v4287':'lil_B171_ends_v4338','B170':'B171',
        'assert n==170 and len(ends)==2':'assert n==171 and len(ends)==2',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=171,commands=45,relative_sites=0,
        pause=0,C200=1,endwords=2,nonrelative_leaves=8,source_resources=[0x6325],A000=0,
        registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),
        promoted_main='all-routes-unified-v4303',no_registry_ledger_credit_change=True,full_goal_complete=False))
    print('Prepared B171 one-block research image, whole loaders, census and both-end decoder producers.')
