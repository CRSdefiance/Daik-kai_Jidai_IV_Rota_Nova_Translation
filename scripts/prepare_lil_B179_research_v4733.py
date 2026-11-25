"""Prepare B179 research gates against complete main V4701; no C200 probe."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B179_research_tools_v4733')
PARENT=Path('out/all_routes_combined_v4701_candidate.nds')
ROM=Path('out/lil_B179_reference_v4734_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B179_relocation_v4729/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists()
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert len(registry['accepted_layers'])==114 and registry['profiles']['all-routes-unified-v4701']['status']=='experimental'
    tools=[derive('scripts/create_lil_B178_reference_v4686.py','scripts/create_lil_B179_reference_v4734.py',{
        'V4655':'V4701','lil_B178_research_v4686':'lil_B179_research_v4734',
        'all_routes_combined_v4655':'all_routes_combined_v4701','lil_B178_reference_v4686':'lil_B179_reference_v4734',
        'lil_B178_relocation_v4681':'lil_B179_relocation_v4729',
        'lil_B178_stored_v4682/all13_final_stored_targets52':'lil_B179_stored_v4730/all14_final_stored_targets56',
        'editorial_handoff_verification_v4684':'editorial_handoff_verification_v4732',
        '[178]':'[179]','actual_selected_B178_IDs':'actual_selected_B179_IDs','all13_final_targets':'all14_final_targets',
        "['current_final_stored_macro_alignment_cases']==52":"['current_final_stored_macro_alignment_cases']==56",
        'current_final_stored_macro_alignment_cases=52':'current_final_stored_macro_alignment_cases=56',
    })]
    tools.append(derive('scripts/pin_lil_B178_reference_v4686.py','scripts/pin_lil_B179_reference_v4734.py',{
        'B178':'B179','lil_B178_reference_pin_v4686':'lil_B179_reference_pin_v4734',
        'lil_B178_research_v4686':'lil_B179_research_v4734','V4686':'V4734',
    }))
    tools.append(derive('scripts/verify_lil_B178_loader_v4687.py','scripts/verify_lil_B179_loader_v4735.py',{
        'work/analysis/lil_B177_loader_v4631/whole_SC2_and_B177_initial_entry_proof.json':
            'work/analysis/lil_B178_loader_v4687/whole_SC2_and_B178_initial_entry_proof.json',
        'prepare_lil_B178_research_v4685':'prepare_lil_B179_research_v4733',
        'lil_B178_loader_v4687':'lil_B179_loader_v4735','lil_B178_research_v4686':'lil_B179_research_v4734',
        'whole_SC2_and_B178_initial_entry_proof':'whole_SC2_and_B179_initial_entry_proof',
        'B178':'B179','V4655':'V4701',
    }))
    tools.append(derive('scripts/verify_lil_B178_references_v4688b.py','scripts/verify_lil_B179_references_v4736.py',{
        'prepare_lil_B178_research_v4685':'prepare_lil_B179_research_v4733',
        'lil_B178_reference_census_v4688b':'lil_B179_reference_census_v4736',
        'lil_B178_loader_v4687':'lil_B179_loader_v4735','B178':'B179','[178]':'[179]',
    }))
    tools.append(derive('scripts/prove_lil_B178_ends_v4689.py','scripts/prove_lil_B179_ends_v4737.py',{
        'prepare_lil_B178_research_v4685':'prepare_lil_B179_research_v4733',
        'lil_B178_ends_v4689':'lil_B179_ends_v4737','n==178':'n==179','B178':'B179',
    }))
    source=Path('scripts/prove_lil_B178_relocated_controls_v4690.py');text=source.read_text(encoding='utf-8')
    start=text.index("        if command['word']==0xC200:");end=text.index("        if command['word']==0xA000:",start)
    tools.append(derive(source,'scripts/prove_lil_B179_relocated_controls_v4738.py',{
        text[start:end]:'','from scripts.prove_lil_B139_C200_v3461e import C200\n':'',
        'prepare_lil_B178_research_v4685':'prepare_lil_B179_research_v4733',
        'lil_B178_relocated_controls_v4690':'lil_B179_relocated_controls_v4738',
        'lil_B178_editorial_manuscript_v3':'lil_B179_editorial_manuscript_v3',
        'blocks[178]':'blocks[179]','block=178':'block=179','00a0ffff010002a1':'00a0ffff01221da1',
        '[(0xA000,8,8),(0xC200,488,450),(0,490,452)]':'[(0xA000,8,8),(0,508,492)]',
        'len(dispatches)==13':'len(dispatches)==14',
        'len(leaves)==3 and len(uis)==len(effects)==1':'len(leaves)==2 and len(uis)==0 and len(effects)==1',
        'all3_source_current_nonrelative_nonspeech_leaves':'all2_source_current_nonrelative_nonspeech_leaves',
        'all3_source_current_target_nonrelative_nonspeech_leaves':'all2_source_current_target_nonrelative_nonspeech_leaves',
        'all13_progressive_FE_dispatches_A000_C200_pairs_and3_leaves':'all14_progressive_FE_dispatches_A000_pairs_and2_leaves',
        'all12_progressive_static_actors':'all13_progressive_static_actors','actual_selected_B178_IDs':'actual_selected_B179_IDs',
        'Bind thirteen relocated dispatches, three exact leaves and paired original control paths.':
            'Bind fourteen relocated dispatches,two exact leaves,A000 and end;no C200 exists.',
        'Thirteen relocated dispatches,twelve progressive/one impersonal FE;three exact leaves,paired A000 structural/C200 paths and single end pass. Actual scene pending.':
            'Fourteen relocated dispatches,thirteen progressive/one impersonal FE;two exact leaves,paired A000 structural paths and single end pass. No C200. Actual scene pending.',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=179,structural_commands=16,relative_sites=0,target_cases=0,
        FE=1,A000=1,C200=0,endwords=1,registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),
        promoted_main='all-routes-unified-v4701',registered_parent='all-routes-unified-v4701',
        whole_ROM_exact_parent_loader_reuse_requires_hash_proof=True,no_registry_ledger_credit_change=True,full_goal_complete=False))
