"""Prepare a one-block B175 reference, exact-parent loader reuse and entry/end tests."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B175_research_tools_v4525')
PARENT=Path('out/all_routes_combined_v4496_candidate.nds')
ROM=Path('out/lil_B175_reference_v4526_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B175_relocation_v4521/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists()
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4496'
    assert len(registry['accepted_layers'])==114 and 'all-routes-unified-v4496' in registry['profiles']
    tools=[derive('scripts/create_lil_B174_reference_v4482.py','scripts/create_lil_B175_reference_v4526.py',{
        'V4445':'V4496','lil_B174_research_v4482':'lil_B175_research_v4526',
        'all_routes_combined_v4445':'all_routes_combined_v4496','lil_B174_reference_v4482':'lil_B175_reference_v4526',
        'lil_B174_relocation_v4477':'lil_B175_relocation_v4521',
        'lil_B174_stored_v4478/all33_final_stored_targets132':'lil_B175_stored_v4522/all32_final_stored_targets128',
        'editorial_handoff_verification_v4480':'editorial_handoff_verification_v4524',
        "prior['candidate_sha256']":"prior['preserved_release_files'][PARENT.as_posix()]",
        'all33_final_targets':'all32_final_targets',
        "current_final_stored_macro_alignment_cases']==132":"current_final_stored_macro_alignment_cases']==128",
        'current_final_stored_macro_alignment_cases=132':'current_final_stored_macro_alignment_cases=128',
        '[174]':'[175]','actual_selected_B174_IDs':'actual_selected_B175_IDs',
    })]
    tools.append(derive('scripts/verify_lil_B174_loader_v4483.py','scripts/verify_lil_B175_loader_v4527.py',{
        'work/analysis/lil_B173_loader_v4432/whole_SC2_and_B173_initial_entry_proof.json':
            'work/analysis/lil_B174_loader_v4483/whole_SC2_and_B174_initial_entry_proof.json',
        'prepare_lil_B174_research_v4481':'prepare_lil_B175_research_v4525',
        'lil_B174_loader_v4483':'lil_B175_loader_v4527','lil_B174_research_v4482':'lil_B175_research_v4526',
        'whole_SC2_and_B174_initial_entry_proof':'whole_SC2_and_B175_initial_entry_proof',
        'B174':'B175','V4445':'V4496',
    }))
    tools.append(derive('scripts/verify_lil_B174_references_v4484.py','scripts/verify_lil_B175_references_v4528.py',{
        'prepare_lil_B174_research_v4481':'prepare_lil_B175_research_v4525',
        'lil_B174_reference_census_v4484':'lil_B175_reference_census_v4528',
        'lil_B174_loader_v4483':'lil_B175_loader_v4527','B174':'B175','[174]':'[175]',
        'for r in result)==45':'for r in result)==39','all45':'all39','native_commands_each=45':'native_commands_each=39',
        'typed_relative_span_count\']for r in result)==4':"typed_relative_span_count']for r in result)==0",
        'target_native_skip_cases\']for r in result)==20':"target_native_skip_cases']for r in result)==0",
        'all39_commands_four_relative_sites_and_shipped_entry_census':'all39_commands_no_relative_sites_and_shipped_entry_census',
        'all39_clean_current_target_commands_and_four_relative_sites_reexecuted':'all39_clean_current_target_commands_and_no_relative_sites_reexecuted',
        'relative_sites=4,target_native_skip_cases=20':'relative_sites=0,target_native_skip_cases=0',
    }))
    tools.append(derive('scripts/prove_lil_B174_ends_v4485.py','scripts/prove_lil_B175_ends_v4529.py',{
        'Decode the single B174 tail endword per image':'Decode both B175 declared endwords per image',
        'prepare_lil_B174_research_v4481':'prepare_lil_B175_research_v4525',
        'lil_B174_ends_v4485':'lil_B175_ends_v4529','n==174 and len(ends)==1':'n==175 and len(ends)==2',
        'len(cases)==2 and sum(not c[\'at_logical_tail\'] for c in cases)==0':
            "len(cases)==4 and sum(not c['at_logical_tail'] for c in cases)==2",
        'two_declared_end_decodes_and_four_relative_sites':'four_declared_end_decodes_no_relative_sites',
        'all2_declared_end_decodes':'all4_declared_end_decodes',
        'B174_single_end_finishes_declared_logical_end':'B175_second_end_finishes_declared_logical_end',
        'single_B174_tail_word_decoder_probe_not_actual_reachability_claim':'both_B175_endword_decoder_probes_not_actual_reachability_claim',
        'Two declared current/target tail endwords pass with poisoned unread post-payload guards;B174 single end preserved.':
            'Four current/target declared endwords pass with poisoned unread post-payload guards;both B175 ends preserved.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_derivation.json',dict(tools=tools,source_block=175,
        structural_commands=39,relative_sites=0,target_cases=0,FE=9,C200=1,endwords=2,
        registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),
        promoted_main='all-routes-unified-v4496',whole_ROM_exact_parent_loader_reuse=True,
        no_registry_ledger_credit_change=True,full_goal_complete=False))
    print('Prepared B175 reference,exact V4496 parent reuse,39-command census and four endword decodes.')
