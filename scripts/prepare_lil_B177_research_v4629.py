"""Prepare B177 research/reference gates against the complete registered V4595 parent."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B177_research_tools_v4629')
PARENT=Path('out/all_routes_combined_v4595_candidate.nds')
ROM=Path('out/lil_B177_reference_v4630_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B177_relocation_v4625/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists()
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4541'
    assert len(registry['accepted_layers'])==114 and registry['profiles']['all-routes-unified-v4595']['status']=='experimental'
    tools=[derive('scripts/create_lil_B176_reference_v4580.py','scripts/create_lil_B177_reference_v4630.py',{
        'V4541':'V4595','lil_B176_research_v4580':'lil_B177_research_v4630',
        'all_routes_combined_v4541':'all_routes_combined_v4595','lil_B176_reference_v4580':'lil_B177_reference_v4630',
        'lil_B176_relocation_v4575':'lil_B177_relocation_v4625',
        'lil_B176_stored_v4576':'lil_B177_stored_v4626',
        'editorial_handoff_verification_v4578':'editorial_handoff_verification_v4628',
        '[176]':'[177]','actual_selected_B176_IDs':'actual_selected_B177_IDs',
    })]
    tools.append(derive('scripts/pin_lil_B176_reference_v4580.py','scripts/pin_lil_B177_reference_v4630.py',{
        'B176':'B177','lil_B176_reference_pin_v4580':'lil_B177_reference_pin_v4630',
        'lil_B176_research_v4580':'lil_B177_research_v4630','V4580':'V4630',
    }))
    tools.append(derive('scripts/verify_lil_B176_loader_v4581.py','scripts/verify_lil_B177_loader_v4631.py',{
        'work/analysis/lil_B175_loader_v4527/whole_SC2_and_B175_initial_entry_proof.json':
            'work/analysis/lil_B176_loader_v4581/whole_SC2_and_B176_initial_entry_proof.json',
        'prepare_lil_B176_research_v4579':'prepare_lil_B177_research_v4629',
        'lil_B176_loader_v4581':'lil_B177_loader_v4631','lil_B176_research_v4580':'lil_B177_research_v4630',
        'whole_SC2_and_B176_initial_entry_proof':'whole_SC2_and_B177_initial_entry_proof',
        'B176':'B177','V4541':'V4595',
    }))
    tools.append(derive('scripts/verify_lil_B176_references_v4582.py','scripts/verify_lil_B177_references_v4632.py',{
        'prepare_lil_B176_research_v4579':'prepare_lil_B177_research_v4629',
        'lil_B176_reference_census_v4582':'lil_B177_reference_census_v4632',
        'lil_B176_loader_v4581':'lil_B177_loader_v4631','B176':'B177','[176]':'[177]',
    }))
    tools.append(derive('scripts/prove_lil_B176_ends_v4583.py','scripts/prove_lil_B177_ends_v4633.py',{
        'prepare_lil_B176_research_v4579':'prepare_lil_B177_research_v4629',
        'lil_B176_ends_v4583':'lil_B177_ends_v4633','n==176':'n==177','B176':'B177',
    }))
    tools.append(derive('scripts/prove_lil_B176_relocated_controls_v4584.py','scripts/prove_lil_B177_relocated_controls_v4634.py',{
        'B176':'B177','lil_B176':'lil_B177',
        'prepare_lil_B176_research_v4579':'prepare_lil_B177_research_v4629',
        'relocated_controls_v4584':'relocated_controls_v4634','editorial_manuscript_v3':'editorial_manuscript_v5',
        'blocks[176]':'blocks[177]','block=176':'block=177','00a0ffff010a0da1':'00a0ffff01090fa1',
        '[(0xA000,8,8),(0xC200,384,398),(0,386,400)]':'[(0xA000,8,8),(0xC200,480,464),(0,482,466)]',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=177,structural_commands=13,
        relative_sites=0,target_cases=0,FE=1,A000=1,C200=1,endwords=1,
        registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),
        promoted_main='all-routes-unified-v4541',registered_parent='all-routes-unified-v4595',
        whole_ROM_exact_parent_loader_reuse=True,no_registry_ledger_credit_change=True,full_goal_complete=False))
