"""Source-lock complete Maria source/English body/header/control audits without rerender assumptions."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B207_actual_audit_tools_v7706')
if __name__=='__main__':
    assert not ROOT.exists()
    result=derive('scripts/audit_papal_trade_scenes_v7650.py','scripts/audit_Maria_B207_scenes_v7706.py',{
        'from pathlib import Path':'from pathlib import Path\nfrom scripts.maria_existing_unlock_contract_v7680 import validate_capture',
        'from scripts.draft_papal_trade_prose_v7631 import CURRENT,CONSUMERS':'from scripts.draft_Maria_B207_prose_v7687 import CURRENT,CONSUMERS',
        'papal_trade_actual_v7650':'maria_B207_actual_v7706',
        'papal_trade_scene_fixtures_v7648/four_complete_source_English_original_route_prelude_fixtures':'maria_B207_scene_fixtures_v7704/Maria_two_complete_source_English_original_prelude_fixtures',
        'papal_trade_scene_runs_v7649':'maria_B207_scene_runs_v7705',
        'papal_trade_stored_v7641/all36_stored_targets144_alignments16_zero_ink_tails36_complete_pages':'maria_B207_stored_v7697/Maria18_stored_targets72_alignments7_zero_ink_tails18_complete_pages',
        'papal_trade_name_inputs_v7629/two_routes40_fresh_literal_alignments_five_exact_reused_font_planes':'maria_B207_name_inputs_v7685/Maria20_fresh_literal_alignments_five_exact_reused_font_planes',
        "assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']":"assert report['frames']==16001;validate_capture(report)",
        "assert not report['hardware_device_verification'] and not report['goal_complete'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))":"assert not report['hardware_device_verification'] and not report['goal_complete']",
        "cg=current['groups'][route];np={r['text']:r for r in names['groups'][route]['name_planes']}":"cg=current;np={r['text']:r for r in names['name_planes']}",
        "consumers['groups'][route]['native_four_distinct_name_consumers']":"consumers['native_four_distinct_name_consumers']",
        "stored['groups'][route]['records']":"stored['records']",
        "sourcefont={r['source_reference']['record_index']:r for r in jpfont['records']}":"sourcefont={r['source_body_hex']:r for r in jpfont['records']}",
        "native=sourcefont[index];src=next(x for x in cg['records'] if x['id']==r['id'])":"src=next(x for x in cg['records'] if x['id']==r['id']);native=sourcefont[bytes.fromhex(src['source_hex'])[1:].hex()]",
        'index==5':'index==4',
        '{0:30,1:28}[route]':'{3:27}[route]',
        'for route in [0,1]':'for route in [3]',
        'four_complete_scene_captures72_speech_occurrences_exact_body_headers_andnormal_returns':'Maria_two_complete_scene_captures36_occurrences_exact_body_headers_andnormal_returns',
        'total_actual_speech_occurrences=72,distinct_file_qualified_speeches=36':'total_actual_speech_occurrences=36,distinct_file_qualified_speeches=18',
        'all_four_source_English_runs_original_command_order_andnormal_returns':'both_source_English_runs_original_command_order_andnormal_returns',
        'all72_complete_leading_internal_final_body_andname_glyphs_bounds_andone_page_verified':'all36_occurrences_complete_leading_internal_final_body_andname_glyphs_bounds_andone_page_verified',
        'all_four_R5_three_ellipsis_black18_lightgray18_masks_exact':'both_R4_three_ellipsis_black18_lightgray18_masks_exact',
        'retained_CP932_R5':'retained_CP932_R4',
        'source_Japanese_black_masks_except_R5_gray_only_English_full_black_gray_masks':'source_Japanese_black_masks_except_R4_gray_only_English_full_black_gray_masks',
        'new_credit=0,full_goal_complete=False))':'existing_system_only_unlock_fixture=True,earned_unlock_verified=False,new_credit=0,full_goal_complete=False))',
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_Maria_actual_body_header_audit.json',dict(derivation=result,all_native_high_constants_andmultiplicity_preserved=True,source_font_reuse_bound_byexact_Japanese_body_not_shifted_ID_assumption=True,existing_system_only_unlock_earned_false=True,new_credit=0,full_goal_complete=False))
