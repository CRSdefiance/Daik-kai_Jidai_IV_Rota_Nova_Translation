"""Prepare disclosed B178 research/reference gates against the complete V4655 parent."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B178_research_tools_v4685')
PARENT=Path('out/all_routes_combined_v4655_candidate.nds')
ROM=Path('out/lil_B178_reference_v4686_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B178_relocation_v4681/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists()
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4595'
    assert len(registry['accepted_layers'])==114 and registry['profiles']['all-routes-unified-v4655']['status']=='experimental'
    tools=[derive('scripts/create_lil_B177_reference_v4630.py','scripts/create_lil_B178_reference_v4686.py',{
        'V4595':'V4655','lil_B177_research_v4630':'lil_B178_research_v4686',
        'all_routes_combined_v4595':'all_routes_combined_v4655','lil_B177_reference_v4630':'lil_B178_reference_v4686',
        'lil_B177_relocation_v4625':'lil_B178_relocation_v4681',
        'lil_B177_stored_v4626/all10_final_stored_targets40':'lil_B178_stored_v4682/all13_final_stored_targets52',
        'editorial_handoff_verification_v4628':'editorial_handoff_verification_v4684',
        '[177]':'[178]','actual_selected_B177_IDs':'actual_selected_B178_IDs',
        'all10_final_targets':'all13_final_targets',"['current_final_stored_macro_alignment_cases']==40":"['current_final_stored_macro_alignment_cases']==52",
        'current_final_stored_macro_alignment_cases=40':'current_final_stored_macro_alignment_cases=52',
    })]
    tools.append(derive('scripts/pin_lil_B177_reference_v4630.py','scripts/pin_lil_B178_reference_v4686.py',{
        'B177':'B178','lil_B177_reference_pin_v4630':'lil_B178_reference_pin_v4686',
        'lil_B177_research_v4630':'lil_B178_research_v4686','V4630':'V4686',
    }))
    tools.append(derive('scripts/verify_lil_B177_loader_v4631.py','scripts/verify_lil_B178_loader_v4687.py',{
        'work/analysis/lil_B176_loader_v4581/whole_SC2_and_B176_initial_entry_proof.json':
            'work/analysis/lil_B177_loader_v4631/whole_SC2_and_B177_initial_entry_proof.json',
        'prepare_lil_B177_research_v4629':'prepare_lil_B178_research_v4685',
        'lil_B177_loader_v4631':'lil_B178_loader_v4687','lil_B177_research_v4630':'lil_B178_research_v4686',
        'whole_SC2_and_B177_initial_entry_proof':'whole_SC2_and_B178_initial_entry_proof',
        'B177':'B178','V4595':'V4655',
    }))
    tools.append(derive('scripts/verify_lil_B177_references_v4632.py','scripts/verify_lil_B178_references_v4688.py',{
        'prepare_lil_B177_research_v4629':'prepare_lil_B178_research_v4685',
        'lil_B177_reference_census_v4632':'lil_B178_reference_census_v4688',
        'lil_B177_loader_v4631':'lil_B178_loader_v4687','B177':'B178','[177]':'[178]',
        '13-command':'16-command','all13_commands':'all16_commands','all13_clean_current_target_commands':'all16_clean_current_target_commands',
    }))
    tools.append(derive('scripts/prove_lil_B177_ends_v4633.py','scripts/prove_lil_B178_ends_v4689.py',{
        'prepare_lil_B177_research_v4629':'prepare_lil_B178_research_v4685',
        'lil_B177_ends_v4633':'lil_B178_ends_v4689','n==177':'n==178','B177':'B178',
    }))
    tools.append(derive('scripts/prove_lil_B177_relocated_controls_v4634.py','scripts/prove_lil_B178_relocated_controls_v4690.py',{
        'prepare_lil_B177_research_v4629':'prepare_lil_B178_research_v4685',
        'lil_B177_relocated_controls_v4634':'lil_B178_relocated_controls_v4690',
        'lil_B177_editorial_manuscript_v5':'lil_B178_editorial_manuscript_v3',
        'blocks[177]':'blocks[178]','block=177':'block=178','00a0ffff01090fa1':'00a0ffff010002a1',
        '[(0xA000,8,8),(0xC200,480,464),(0,482,466)]':'[(0xA000,8,8),(0xC200,488,450),(0,490,452)]',
        'len(dispatches)==10':'len(dispatches)==13',"len(spec['command_map'])==13":"len(spec['command_map'])==16",
        'all10_progressive_FE_dispatches':'all13_progressive_FE_dispatches',
        'all9_progressive_static_actors':'all12_progressive_static_actors','actual_selected_B177_IDs':'actual_selected_B178_IDs',
        'Bind ten relocated':'Bind thirteen relocated',
        'Ten relocated dispatches,nine progressive':'Thirteen relocated dispatches,twelve progressive',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=178,structural_commands=16,relative_sites=0,target_cases=0,
        FE=1,A000=1,C200=1,endwords=1,registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),
        promoted_main='all-routes-unified-v4595',registered_parent='all-routes-unified-v4655',
        whole_ROM_exact_parent_loader_reuse=True,no_registry_ledger_credit_change=True,full_goal_complete=False))
