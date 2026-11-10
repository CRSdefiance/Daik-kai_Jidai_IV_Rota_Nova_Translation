"""Prepare the complete42-command English fixture and five ordinary-input same-code runs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B206_English_fixture_tools_v6312')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/research_lil_B205_English_fixture_v6209.py').read_text('utf-8');start=source.index("    runner=derive(");end=source.index("    save(ROOT/'pin_and_runner_receipt.json'",start);runner_section=source[start:end]
    tools=[derive('scripts/research_lil_B205_English_fixture_v6209.py','scripts/research_lil_B206_English_fixture_v6312.py',{
      'B205':'B206','scripts.prepare_lil_B205_references_v6200':'scripts.create_lil_B206_reference_v6307','lil_B205_English_fixture_v6209':'lil_B206_English_fixture_v6312','lil_B205_English_v6209':'lil_B206_English_v6312',
      'work/analysis/lil_B205_source_fixture_v6180/complete_B205_source_B22_fixture.json':'work/analysis/shady_man_source_fixture_v6260/complete_B206_source_B22_fixture.json',
      'lil_B205_loader_v6205':'lil_B206_loader_v6308','lil_B205_reference_census_v6206':'lil_B206_reference_census_v6309','all25_commands_no_relative_sites':'all42_commands_eight_relative_sites','all25_clean_current_target_commands_and_no_relative_sites':'all42_clean_current_target_commands_and_eight_relative_sites',
      'work/analysis/lil_B205_relocated_controls_v6208/all17_dispatches_one_picture_one47xx_pair_and8_exact_leaves.json':'work/analysis/lil_B206_relocated_controls_v6311/all24_dispatches_picture_three47xx_three_A000_and10_guarded_ends.json',
      "len(controls['relocated_dispatch_cases'])==17":"len(controls['relocated_dispatch_cases'])==24",'bank[205]':'bank[206]','source_block=205':'source_block=206','len(native)==25 and len(commands)==34 and len(speeches)==17':'len(native)==42 and len(commands)==51 and len(speeches)==24','all34_stored':'all51_stored','all25_source_commands':'all42_source_commands','event205_activation':'event206_activation',
      'parrot/five-echo/two-sound/capture/transition':'ceramic-earring/pitch/purchase/two-refusals/transition',
      '25 source+9 initializer commands,17 objects,five FE echoes/two sounds':'42 source+9 initializer commands,24 speeches/four labels,two choices/eight spans',
      runner_section:"    runner=dict(prepared_separately_by='scripts/prepare_lil_B206_English_fixture_v6312.py',five_same_code_source_English_paths_with_ordinary_inputs=True)\n",
    })]
    base='scripts/run_shady_man_source_buy_v6262.py'
    for version,case,down in [(6313,'buy',None),(6314,'high_price',7300),(6315,'pitch_refusal',6300),(6316,'high_price',7300),(6317,'pitch_refusal',6300)]:
        english=version<=6315;root=f'lil_B206_English_run_v{version}_{case}' if english else f'lil_B206_current_source_run_v{version}_{case}';cap=f'lil_B206_English_v{version}_{case}' if english else f'lil_B206_current_source_v{version}_{case}'
        changes={'shady_man_source_run_v6262_buy':root,'shady_man_source_v6262_buy':cap}
        if english:changes.update({'work/analysis/shady_man_source_fixture_v6260/complete_B206_source_B22_fixture.json':'work/analysis/lil_B206_English_fixture_v6312/complete_B206_English_B22_fixture.json',"selected['case']=='clean_Japanese'":"selected['case']=='reviewed_English'"})
        if down:changes['[dict(start=f,duration=5,buttons=[\'A\']) for f in range(2600,15501,240)]']='[dict(start=f,duration=5,buttons=[\'A\']) for f in range(2600,15501,240)]+[dict(start='+str(down)+",duration=5,buttons=['DOWN'])]"
        name=f'scripts/run_lil_B206_English_{case}_v{version}.py' if english else f'scripts/run_lil_B206_current_source_{case}_v{version}.py';tools.append(derive(base,name,changes))
    ROOT.mkdir(parents=True);save(ROOT/'complete_English_fixture_and_five_same_code_ordinary_runs.json',dict(tools=tools,complete42_commands24_speeches4_labels2_menus8_spans=True,new_same_code_Japanese_buy_reuses_existing_terminal_v6262=True,two_old_source_refusals_require_new_name_data_baseline_for_strict_paired_comparison=True,capture_schedule_all_runs_same_every60_plus4000=True,ordinary_A_every240_and_DOWN6300_or7300_inputs_not_runtime_state_fixtures=True,no_source_command_effect_roster_funds_RNG_or_result_omission_or_forcing=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('Complete English fixture and3 English/2 necessary same-code source-refusal runs prepared. Existing new-code source-buy is reused;all native addresses preserved.')
