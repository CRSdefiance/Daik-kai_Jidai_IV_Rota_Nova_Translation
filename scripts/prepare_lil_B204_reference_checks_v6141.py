"""Prepare whole reference,guarded end and exact relocated-control successors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B204_reference_check_tools_v6141')
if __name__=='__main__':
    assert not ROOT.exists()
    shared={'B203':'B204','prepare_lil_B203_references_v6034':'prepare_lil_B204_references_v6135'}
    tools=[derive('scripts/verify_lil_B203_references_v6039.py','scripts/verify_lil_B204_references_v6141.py',{
        **shared,'reference_census_v6039':'reference_census_v6141','loader_v6038':'loader_v6140','[203]':'[204]','31-command':'26-command',"sum(len(r['mapped_commands'])for r in result)==31":"sum(len(r['mapped_commands'])for r in result)==26",'all31':'all26','native_commands_each=31':'native_commands_each=26',
    })]
    tools.append(derive('scripts/prove_lil_B203_ends_v6040.py','scripts/prove_lil_B204_ends_v6142.py',{**shared,'ends_v6040':'ends_v6142','n==203':'n==204'}))
    tools.append(derive('scripts/prove_lil_B203_relocated_controls_v6041.py','scripts/prove_lil_B204_relocated_controls_v6143.py',{
        **shared,'relocated_controls_v6041':'relocated_controls_v6143','manuscript_v4':'manuscript_v7','blocks[203]':'blocks[204]',
        'scripts.current_build_native_context_v4774':'scripts.current_build_native_context_v6097',
        "dp,cp=map(read,[doc['control_contract'],doc['source_effect_and_predicate_contract']])":"cp_path=Path('work/analysis/lil_B204_controls_v6139/six_exact_leaves_picture47xx_two43xx_one_A000_structural_pairs_and_guarded_end.json');dp,cp=map(read,[doc['control_contract'],cp_path])",
        "Path(doc['source_effect_and_predicate_contract'])":"cp_path",'all9_source_current_nonspeech_leaves':'all6_source_current_nonspeech_leaves','all9_source_current_target_control_leaves':'all6_source_current_target_control_leaves',
        '[0x4820,0x4735]':'[0x4835,0x4735]','word==0x4820':'word==0x4835','len(dispatches)==22':'len(dispatches)==20',"sum(r['resolved_actor_ID'] is None for r in dispatches)==1":"sum(r['resolved_actor_ID'] is None for r in dispatches)==4",'len(leaves)==9':'len(leaves)==6',"sum(r['word']==0xA000 for r in leaves)==4":"sum(r['word']==0xA000 for r in leaves)==1",
        "assert len(cp['one_resource632E_ten_boundary_cases'])==10 and len(cp['source6003_ten_boundary_cases'])==10 and len(cp['source_four_A000_structural_pairs'])==4":"assert len(cp['source_one_picture_pair'])==len(cp['source_one_short47xx_pair'])==1 and len(cp['source_two43xx_and_one_A000_structural_pairs'])==3 and len(cp['ten_guarded_complete_end_cases'])==10",
        'all22_dispatches_one_picture_one47xx_pair_and9_exact_leaves':'all20_dispatches_one_picture_one47xx_pair_and6_exact_leaves','original10_resource632E10_6003_boundary_cases_and_four_A000_pairs_reused_by_exact_bytes_and_current_snapshot':'original_two43xx_one_A000_structural_pairs_and_ten_guarded_ends_reused_by_exact_bytes_and_current_snapshot',
        'all21_progressive_and_one_FE_object_preserved=True,one_original_FI_zero_FA_FO_preserved=True':'all16_progressive_and_four_FE_objects_preserved=True,no_FI_FA_FO_source_macros=True','original_names_and_Mikhail_progressive_catalogue_distinction_preserved':'original_names_and_Jam_progressive_full_signature_distinction_preserved',
        'Bind22 relocated B203 dispatches and all nine source-owned control leaves.':'Bind20 relocated B204 dispatches and all six source-owned control leaves.',
        '22 relocated dispatches,one picture/one47xx pair and9 exact leaves pass;one FE/FI,no2000 pause. English scene next.':'20 relocated dispatches,one picture/one47xx pair and6 exact leaves pass;four FE letters,no macros or2000 pause. English scene next.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_checks.json',dict(tools=tools,all_native_addresses_and_ABI_checks_preserved=True,fresh_current_control_contract_required=True,full_goal_complete=False));print('B204 reference census,guarded end and20 relocated dispatch/six-leaf checks prepared.')
