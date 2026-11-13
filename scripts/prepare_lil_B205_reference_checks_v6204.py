"""Derive current/reference loaders,25-command census,eight controls and complete English fixture."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B205_reference_check_tools_v6204')
if __name__=='__main__':
    assert not ROOT.exists();shared={'B204':'B205','prepare_lil_B204_references_v6135':'prepare_lil_B205_references_v6200'}
    tools=[derive('scripts/verify_lil_B204_loader_v6140.py','scripts/verify_lil_B205_loader_v6205.py',{**shared,'V6110':'V6160','loader_v6140':'loader_v6205','research_v6138':'research_v6203'})]
    tools.append(derive('scripts/verify_lil_B204_references_v6141.py','scripts/verify_lil_B205_references_v6206.py',{**shared,'reference_census_v6141':'reference_census_v6206','loader_v6140':'loader_v6205','[204]':'[205]','26-command':'25-command',"sum(len(r['mapped_commands'])for r in result)==26":"sum(len(r['mapped_commands'])for r in result)==25",'all26':'all25','native_commands_each=26':'native_commands_each=25'}))
    tools.append(derive('scripts/prove_lil_B204_ends_v6142.py','scripts/prove_lil_B205_ends_v6207.py',{**shared,'ends_v6142':'ends_v6207','n==204':'n==205'}))
    tools.append(derive('scripts/prove_lil_B204_relocated_controls_v6143.py','scripts/prove_lil_B205_relocated_controls_v6208.py',{
        **shared,'relocated_controls_v6143':'relocated_controls_v6208','manuscript_v7':'manuscript_v6','blocks[204]':'blocks[205]',
        'work/analysis/lil_B204_controls_v6139/six_exact_leaves_picture47xx_two43xx_one_A000_structural_pairs_and_guarded_end.json':'work/analysis/lil_B205_controls_v6179/eight_exact_leaves_picture147_47xx_two63xx_three_A000_and_guarded_end.json',
        'Bind20 relocated B204 dispatches and all six source-owned control leaves.':'Bind17 relocated B205 dispatches and all eight source-owned control leaves.','all6_source_current_nonspeech_leaves':'all8_source_current_nonspeech_leaves','all6_source_current_target_control_leaves':'all8_source_current_target_control_leaves',
        '[0x4835,0x4735]':'[0x4841,0x4721]','word==0x4835':'word==0x4841','len(dispatches)==20':'len(dispatches)==17',"sum(r['resolved_actor_ID'] is None for r in dispatches)==4":"sum(r['resolved_actor_ID'] is None for r in dispatches)==7",'len(leaves)==6':'len(leaves)==8',"sum(r['word']==0xA000 for r in leaves)==1":"sum(r['word']==0xA000 for r in leaves)==3", "len(cp['source_two43xx_and_one_A000_structural_pairs'])==3":"len(cp['source_two63xx_three_A000_structural_pairs'])==5",
        'all20_dispatches_one_picture_one47xx_pair_and6_exact_leaves':'all17_dispatches_one_picture_one47xx_pair_and8_exact_leaves',
        'original_two43xx_one_A000_structural_pairs_and_ten_guarded_ends_reused_by_exact_bytes_and_current_snapshot':'original_two63xx_three_A000_structural_pairs_and_ten_guarded_ends_reused_by_exact_bytes_and_current_snapshot',
        'all16_progressive_and_four_FE_objects_preserved':'all10_progressive_and_seven_FE_objects_preserved','original_names_and_Jam_progressive_full_signature_distinction_preserved':'original_names_Lil_Argot_Angelo_Puccini_and_FE_null_actor_distinction_preserved',
        '20 relocated dispatches,one picture/one47xx pair and6 exact leaves pass;four FE letters,no macros or2000 pause. English scene next.':'17 relocated dispatches,one picture/one47xx pair and8 exact leaves pass;seven FE sounds/echoes,no macros or2000 pause. English scene next.',
    }))
    tools.append(derive('scripts/research_lil_B204_English_fixture_v6144.py','scripts/research_lil_B205_English_fixture_v6209.py',{
        **shared,'English_fixture_v6144':'English_fixture_v6209','English_v6144':'English_v6209','English_fixture_v6145':'English_fixture_v6210','English_run_v6145':'English_run_v6210','English_v6145':'English_v6210',
        'work/analysis/shachihoko_item_menu_fixture_v6103/complete_B204_source_B22_fixture_with_coordinated_item_data.json':'work/analysis/lil_B205_source_fixture_v6180/complete_B205_source_B22_fixture.json',
        'loader_v6140':'loader_v6205','reference_census_v6141':'reference_census_v6206','all26_commands':'all25_commands','all26_clean':'all25_clean','relocated_controls_v6143':'relocated_controls_v6208','all20_dispatches_one_picture_one47xx_pair_and6_exact_leaves':'all17_dispatches_one_picture_one47xx_pair_and8_exact_leaves',
        "len(controls['relocated_dispatch_cases'])==20":"len(controls['relocated_dispatch_cases'])==17",'bank[204]':'bank[205]','len(native)==26 and len(commands)==35 and len(speeches)==20':'len(native)==25 and len(commands)==34 and len(speeches)==17',"sum(c['word']==0xA000 for c in commands)==5":"sum(c['word']==0xA000 for c in commands)==7",'source_block=204':'source_block=205','all35_stored_fixture_commands':'all34_stored_fixture_commands','all26_source_commands_plus9_initializers':'all25_source_commands_plus9_initializers','not_natural_event204_activation':'not_natural_event205_activation',
        'castle/four-letter/transition':'parrot/five-echo/two-sound/capture/transition',
        'scripts/run_lil_B204_source_fixture_v6071.py':'scripts/run_lil_B205_source_fixture_v6181.py','source_fixture_v6070':'source_fixture_v6180','source_run_v6071_clean_Japanese':'source_run_v6181_clean_Japanese','source_v6071_clean_Japanese':'source_v6181_clean_Japanese',
        '26 source+9 initializer commands,20 objects,four FE letters,current coordinated item data':'25 source+9 initializer commands,17 objects,five FE echoes/two sounds,unchanged current item data',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_reference_checks_and_English_fixture.json',dict(tools=tools,all_native_addresses_and_ABI_checks_preserved=True,exact_B205_controls_not_inherited_castle_letter_counts=True,new_review_credit=0,full_goal_complete=False));print('B205 complete reference/loader/entry/end/eight-control checks and34-command English fixture tools prepared.')
