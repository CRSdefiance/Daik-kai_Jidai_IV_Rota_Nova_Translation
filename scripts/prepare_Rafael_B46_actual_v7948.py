"""Derive complete actual body/name/FE audit for both ordinary menu choices and both languages."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B46_actual_tools_v7948');assert not root.exists()
    src=Path('scripts/audit_Rafael_B45_actual_v7895b.py').read_text('utf8')
    begin=src.index('    terminals=[]');end=src.index('    ROOT.mkdir(parents=True)',begin)
    old=src[begin:end]
    new="""    terminals=[];flow=read('work/analysis/Rafael_B46_menu_flow_v7925/two_choice_native_forwarding_four_relative_sites_accept22_decline7_source_scope.json')
    for choice in ['accept','decline']:
        for fixture in fixtures['fixtures']:
            folder=RUNS/f"route0_{fixture['version']}_{choice}";terminal=read(folder/'terminal.json')
            assert terminal['terminal'] and terminal['frames']==16001 and terminal['all_callbacks_readonly_andhost_slots_restored']
            assert terminal['choice']==choice
            terminals.append((fixture,folder,terminal))
"""
    b=src.index('        assert finished and len(pairs)==32')
    e=src.index('        exitframe=',b)
    checks="""        selected=0 if choice=='accept' else 1
        expected_source=flow['source_paths'][selected]
        expected_offsets=[c['offset'] for c in fixture['all_fixture_commands'][:10]]+[
            o['fixture_command_offset'] for i,o in enumerate(fixture['all_original_exchange_commands'])
            if current['groups'][0]['all_source_commands'][i]['offset'] in expected_source['visited_source_command_offsets']]
        assert finished and [p['fixture_offset'] for p in pairs]==expected_offsets
        assert pairs[-1]['native_result']==[0,selected]
        assert not trace['unreturned_at_capture_end'] and not unknown
        assert [s['id'] for s in speeches]==expected_source['source_speech_IDs'] and len(speeches)==(22 if selected==0 else 7)
        assert len({s['id'] for s in speeches})==len(speeches)
        observed={p['exchange_command_ordinal'] for p in pairs if p['exchange_command_ordinal'] is not None}
        skipped=[o for i,o in enumerate(fixture['all_original_exchange_commands']) if i not in observed]
        assert len(observed)==len(expected_source['visited_source_command_offsets'])
        menu_pair=next(p for p in pairs if p['word']==0x2100)
        assert menu_pair['native_result']==[2,selected]
        assert sum(s['source_selector']==254 for s in speeches)==(12 if selected==0 else 0)
"""
    groupcheck="""    assert len(groups)==4
    for choice in ['accept','decline']:
        source,english=[next(g for g in groups if g['choice']==choice and g['version']==v) for v in ['clean_Japanese','English']]
        assert source['input_schedule_sha256']==english['input_schedule_sha256']
    for version in ['clean_Japanese','English']:
        same=[g for g in groups if g['version']==version]
        assert {s['id'] for g in same for s in g['speech_observations']}=={r['id'] for r in current['records']}
        assert {p['exchange_command_ordinal'] for g in same for p in g['command_pairs'] if p['exchange_command_ordinal'] is not None}==set(range(37))
"""
    row=derive('scripts/audit_Rafael_B45_actual_v7895b.py','scripts/audit_Rafael_B46_actual_v7948.py',{
        'Complete actual source/English body/header/FE masks and unchanged original conditional execution.':'Complete actual B46 source/English body/header/FE masks andboth ordinary menu-controlled paths.',
        'Rafael_B45_actual_v7895b':'Rafael_B46_actual_v7948',
        'Rafael_B45_scene_fixtures_v7892':'Rafael_B46_scene_fixtures_v7944',
        'Rafael_B45_scene_runs_v7893':'Rafael_B46_scene_runs_v7945',
        'Rafael_B45_source_name_planes_v7894/12_complete_source_pages2_names8_literal_alignments_distinct_FE.json':'Rafael_B46_source_name_planes_v7946/24_complete_source_pages3_names12_literal_alignments12_FE.json',
        'Rafael_B45_native_review_v7883/12_exact_native_pages_rebound_with_individual_row_review.json':'Rafael_B46_pages_v7933/24_complete_native_pages96_compiled_alignments12_FE.json',
        'Rafael_B45_stored_v7885/all12_stored_bodies28_fresh20_reused_alignments_exact_viewed_planes.json':'Rafael_B46_stored_v7939/all24_stored_bodies44_fresh52_reused_alignments_exact_viewed_planes.json',
        'Rafael_B45_current_v7871/all12_complete_source_current_refs_before_new_English_manuscript.json':'Rafael_B46_current_v7927/all24_speeches2_choices_source_current_refs_before_new_English_manuscript.json',
        old:new,
        "version=fixture['version'];rp,tp=":"version=fixture['version'];choice=terminal['choice'];rp,tp=",
        "assert row['result_words']==[0,pairs[-2]['native_result'][1]]==[0,1]":"assert row['result_words']==[0,pairs[-2]['native_result'][1]]==[0,0 if choice=='accept' else 1]",
        src[b:e]:checks,
        "f'Rafael {version} R":"f'Rafael {version} {choice} R",
        "f'{version}_six_complete_panels_sheet":"f'{version}_{choice}_six_complete_panels_sheet",
        "next(s['complete_body_holds'][-1]['frame'] for s in speeches if s['source_selector']==254)":"next(s['complete_body_holds'][-1]['frame'] for s in speeches if (s['source_selector']==254 if choice=='accept' else s['id']=='DK4_MES_B46_R0105'))",
        "f'{version} frame":"f'{version} {choice} frame",
        "f'{version}_first_FE_return_final.png'":"f'{version}_{choice}_first_FE_orcaution_return_final.png'",
        "route_identity='Rafael',version=version,fixture=fixture":"route_identity='Rafael',version=version,choice=choice,fixture=fixture",
        'observed_original_exchange_commands=22':'observed_original_exchange_commands=len(observed)',
        'actual_unique_speeches=12':'actual_unique_speeches=len(speeches)',
        'native_terminal_result=[0,1]':'native_terminal_result=[0,selected],actual_menu_pair=menu_pair',
        "print(version,'speeches'":"print(version,choice,'speeches'",
        "    assert len(groups)==2 and groups[0]['input_schedule_sha256']==groups[1]['input_schedule_sha256']":groupcheck.rstrip(),
        'paired12_source_English_actual_body_name_FE_branch_andnormal_return_audit.json':'four_runs24_unique_speeches58_occurrences_two_choices_actual_body_name_FE_return_audit.json',
        'all24_pages_complete':'all58_speech_occurrences_complete',
        'all22_progressive_nameplates_andtwo_FE_absent_nameplates_preserved':'all34_progressive_occurrences24_FE_absent_nameplates_preserved',
        'actual_FE_condition_result1_preserved_without_result_orstate_forcing':'actual_menu0_accepts12_FE_menu1_declines_original_paths_without_result_orstate_forcing',
        'actual_normal_type0_value1_carry_both_languages':'actual_normal_type0_value0_accept_value1_decline_carry_both_languages',
        'original_unselected0400_outer0100_have_native_branch_proof_not_individual_gameplay_coverage':'all37_source_commands_observed_across_two_choices_each_language_other_native_result_cases_remain_offline',
        'original_ten_command_B44_ROM_entry_fixture_not_natural_B45_activation_Ceuta_location_orfull_route':'original_ten_command_B44_ROM_entry_fixture_not_natural_B46_activation_original_location_orfull_route',
    })
    root.mkdir(parents=True);save(root/'source_locked_derivation.json',row)
