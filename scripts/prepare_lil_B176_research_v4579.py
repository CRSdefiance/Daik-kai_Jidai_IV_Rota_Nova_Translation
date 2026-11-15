"""Prepare B176 one-block research, exact-parent loaders, census and guarded tail probes."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/lil_B176_research_tools_v4579')
PARENT=Path('out/all_routes_combined_v4541_candidate.nds')
ROM=Path('out/lil_B176_reference_v4580_RESEARCH_ONLY.nds')
PLAN=Path('work/analysis/lil_B176_relocation_v4575/nested_source_relocation_research.json')

if __name__=='__main__':
    assert not ROOT.exists()
    registry=read('translations/release_stack.json')
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4541'
    assert len(registry['accepted_layers'])==114 and registry['profiles']['all-routes-unified-v4541']['status']=='experimental'
    tools=[derive('scripts/create_lil_B175_reference_v4526.py','scripts/create_lil_B176_reference_v4580.py',{
        'V4496':'V4541','lil_B175_research_v4526':'lil_B176_research_v4580',
        'all_routes_combined_v4496':'all_routes_combined_v4541','lil_B175_reference_v4526':'lil_B176_reference_v4580',
        'lil_B175_relocation_v4521':'lil_B176_relocation_v4575',
        'lil_B175_stored_v4522/all32_final_stored_targets128':'lil_B176_stored_v4576/all10_final_stored_targets40',
        'editorial_handoff_verification_v4524/verified_handoff.json':'editorial_handoff_verification_v4578/independent_verified_handoff.json',
        'all32_final_targets':'all10_final_targets',
        "current_final_stored_macro_alignment_cases']==128":"current_final_stored_macro_alignment_cases']==40",
        'current_final_stored_macro_alignment_cases=128':'current_final_stored_macro_alignment_cases=40',
        '[175]':'[176]','actual_selected_B175_IDs':'actual_selected_B176_IDs',
    })]
    tools.append(derive('scripts/pin_lil_B175_reference_v4526.py','scripts/pin_lil_B176_reference_v4580.py',{
        'B175':'B176','lil_B175_reference_pin_v4526':'lil_B176_reference_pin_v4580',
        'lil_B175_research_v4526':'lil_B176_research_v4580','V4526':'V4580',
    }))
    tools.append(derive('scripts/verify_lil_B175_loader_v4527.py','scripts/verify_lil_B176_loader_v4581.py',{
        'work/analysis/lil_B174_loader_v4483/whole_SC2_and_B174_initial_entry_proof.json':
            'work/analysis/lil_B175_loader_v4527/whole_SC2_and_B175_initial_entry_proof.json',
        'prepare_lil_B175_research_v4525':'prepare_lil_B176_research_v4579',
        'lil_B175_loader_v4527':'lil_B176_loader_v4581','lil_B175_research_v4526':'lil_B176_research_v4580',
        'whole_SC2_and_B175_initial_entry_proof':'whole_SC2_and_B176_initial_entry_proof',
        'B175':'B176','V4496':'V4541',
    }))
    tools.append(derive('scripts/verify_lil_B175_references_v4528.py','scripts/verify_lil_B176_references_v4582.py',{
        'Fresh shipped entry census and45-command/four-span one-block mapping.':'Fresh shipped entry census and13-command/no-relative-site one-block mapping.',
        'prepare_lil_B175_research_v4525':'prepare_lil_B176_research_v4579',
        'lil_B175_reference_census_v4528':'lil_B176_reference_census_v4582',
        'lil_B175_loader_v4527':'lil_B176_loader_v4581','B175':'B176','[175]':'[176]',
        'for r in result)==39':'for r in result)==13','all39':'all13','native_commands_each=39':'native_commands_each=13',
    }))
    tools.append(derive('scripts/prove_lil_B175_ends_v4529.py','scripts/prove_lil_B176_ends_v4583.py',{
        'Decode both B175 declared endwords per image':'Decode the single B176 tail endword per image',
        'prepare_lil_B175_research_v4525':'prepare_lil_B176_research_v4579',
        'lil_B175_ends_v4529':'lil_B176_ends_v4583','n==175 and len(ends)==2':'n==176 and len(ends)==1',
        "len(cases)==4 and sum(not c['at_logical_tail'] for c in cases)==2":
            "len(cases)==2 and sum(not c['at_logical_tail'] for c in cases)==0",
        'four_declared_end_decodes_no_relative_sites':'two_declared_tail_end_decodes_no_relative_sites',
        'all4_declared_end_decodes':'all2_declared_end_decodes',
        'B175_second_end_finishes_declared_logical_end':'B176_single_end_finishes_declared_logical_end',
        'both_B175_endword_decoder_probes_not_actual_reachability_claim':'single_B176_tail_word_decoder_probe_not_actual_reachability_claim',
        'Four current/target declared endwords pass with poisoned unread post-payload guards;both B175 ends preserved.':
            'Two current/target tail endwords pass with poisoned unread post-payload guards;B176 single end preserved.',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_block=176,structural_commands=13,
        relative_sites=0,target_cases=0,FE=1,A000=1,C200=1,endwords=1,
        registry_sha256=sha(Path('translations/release_stack.json').read_bytes()),
        promoted_main='all-routes-unified-v4541',whole_ROM_exact_parent_loader_reuse=True,
        no_registry_ledger_credit_change=True,full_goal_complete=False))
