"""Verify complete English masks, with exact R5 CP932 palette and measured later differences."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B234_English_audit_tools_v7600')
if __name__=='__main__':
    assert not ROOT.exists()
    common={'B233':'B234','English_actual_v7552':'English_actual_v7600','English_fixture_v7550':'English_fixture_v7598','English_run_v7551':'English_run_v7599','source_actual_v7535b/all11_source_speeches_complete_Japanese_name_masks22_commands':'source_actual_v7583/all18_source_speeches_complete_Japanese_name_masks29_commands','stored_v7545/all11_final_stored_targets44_alignments11_complete_pages':'stored_v7593/all18_final_stored_targets72_alignments18_complete_pages','name_planes_v7531/two_actors_four_getters_six_literal_planes24_alignments':'name_planes_v7579/two_actors_four_getters_five_literal_planes20_alignments','consumers_v7527/eleven_effective_bodies22_dispatches_two_actors_four_name_consumers':'consumers_v7575/eighteen_effective_bodies36_dispatches_two_actors_four_name_consumers','later_v7553':'later_v7601','later_pairs_v7553b':'later_pairs_v7601b','event233':'event234','all13':'all20','all11':'all18','all22':'all29','all11_English_speeches11_pages_complete_native_masks22_commands':'all18_English_speeches18_pages_complete_native_masks29_commands','original_A000_source950_target942':'original_A000_source1456_target1520',"p['source_offset']==950":"p['source_offset']==1456",'source_item97_card_getter_mechanics_other_consumers_unapproved':'source_item106_card_getter_mechanics_other_consumers_unapproved'}
    shadow="        assert len(models)==1\n        shadow=(197,198,197) if r['id']=='DK4_MES_B234_R0005' else (98,97,98)\n        if r['id']=='DK4_MES_B234_R0005':\n            palette=read(PALETTE);assert ref['final_target_hex']=='68816381638163' and palette['source_body_hex']=='816381638163' and palette['retained_CP932_shadow_RGB']==list(shadow) and len(models[0]['black'])==len(models[0]['gray'])==18\n"
    specs=[
      ('audit_lil_B233_English_v7552','audit_lil_B234_English_v7600',{
        'len(pairs)==22 and len(observations)==11 and len(pagepanels)==11':'len(pairs)==29 and len(observations)==18 and len(pagepanels)==18',
        'actual_unique_speeches=11,actual_native_pages=11':'actual_unique_speeches=18,actual_native_pages=18','speeches=11,pages=11':'speeches=18,pages=18',
        '        assert len(models)==1\n':shadow,
        'if im.getpixel((x,y))==(98,97,98)};matches=':'if im.getpixel((x,y))==shadow};matches=',
        '            assert len(matches)==1;m=matches[0]':"            if r['id']=='DK4_MES_B234_R0005':assert not any(im.getpixel((x,y))==(98,97,98) for y in range(296,360) for x in range(16,232))\n            assert len(matches)==1;m=matches[0]",
        'body_shadow_RGB=[98,97,98]':'body_shadow_RGB=list(shadow)',
        "if __name__=='__main__':":"PALETTE=Path('work/analysis/lil_B234_ellipsis_palette_v7583b/three_source_ellipsis_glyphs_lighter_gray_palette_and_complete_masks.json')\nif __name__=='__main__':",
        '[FIXTURE,RUN/':'[PALETTE,FIXTURE,RUN/',
        'ASCII_dark_gray_complete_masks_andall_name_masks_verified':'ASCII_dark_gray_andexact_R5_CP932_light_gray_complete_masks_andall_name_masks_verified',
        'both_source_personal_names_preserved':'source_Carlo_andshared_Trader_role_headers_preserved',
      }),
      ('measure_lil_B233_later_v7553','measure_lil_B234_later_v7601',{}),
      ('illustrate_lil_B233_later_v7553b','illustrate_lil_B234_later_v7601b',{}),
    ];jobs=[]
    for a,b,extra in specs:
        src=Path('scripts/'+a+'.py').read_text('utf8');changes={k:v for k,v in common.items() if k in src};changes.update(extra);assert not Path('scripts/'+b+'.py').exists();checked_text(src,changes);jobs.append(('scripts/'+a+'.py','scripts/'+b+'.py',changes))
    rows=[derive(*j) for j in jobs];ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_English_andlater_audits.json',dict(tools=rows,all18_actual_complete_body_masks_names_and29_commands_required=True,ASCII_black_dark_gray_andonly_exact_R5_source_CP932_black_light_gray_masks_checked_separately=True,R5_wrong_dark_gray_pixels_explicitly_rejected=True,following_resident_payloads_bound_to_actual_SC0_SC3_banks=True,no_assumed_timing_RNG_RGB_calendar_actors_components_orfuture_equality=True,no_full_item106_mechanic_card_other_consumer_approval=True,first_English_fixture_attempt_before_census_finish_failed_before_any_ROM_output_then_unchanged_script_resumed_after_terminal_census=True,missing_uncreated_runner_attempt_not_gameplay_orrejection_credit=True,no_input_retiming_state_forcing_orfull_route_claim=True,new_credit=0,full_goal_complete=False))
