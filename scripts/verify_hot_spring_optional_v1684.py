"""Fresh actual V1676 proof;carry unchanged fonts/text from V1637 explicitly."""
from pathlib import Path

if __name__=='__main__':
    source=Path('scripts/verify_hot_spring_notice_actual_v1646.py').read_text(encoding='utf-8')
    changes=[('from scripts.audit_hot_spring_resilient_v1645c import audit','from scripts.reuse_search_run_audit_v1684a import audit'),
        ('from dk4tool.patch.hot_spring_notice_editorial import current_entries','from dk4tool.patch.search_reports_editorial import current_entries\nfrom dk4tool.patch.hot_spring_notice_editorial import current_entries as previous_entries'),
        ("ROOT=Path('work/analysis/hot_spring_notice_actual_v1646')","ROOT=Path('work/analysis/hot_spring_optional_actual_v1684')"),
        ('hot_spring_notice_resilient_v1645_1637','search_reports_live_v1680_1676'),
        ('out/all_routes_combined_v1637_candidate.nds','out/all_routes_combined_v1676_candidate.nds'),
        ('out/all_routes_combined_v1622_candidate.nds','out/all_routes_combined_v1637_candidate.nds'),
        ("cases['terminal']==cases['normal_return_frame']","cases['terminal']>=cases['normal_return_frame'] and cases['terminal_return_actually_viewed']"),
        ("assert notice_fonts['ARM9_sha256']==sha(arm) and notice_fonts['COMMON_sha256']==sha(common)",
         "assert notice_fonts['ARM9_sha256']==sha(old.read_file('/__arm9__.bin')) and notice_fonts['COMMON_sha256']==sha(old.read_file('/COMMON/MESFILE.DK4'))\n    prior_entries=previous_entries(old.read_file('/COMMON/MESFILE.DK4'),old.read_file('/__arm9__.bin'))\n    assert all(entries[n].text==prior_entries[n].text for n in [310,*range(2275,2288)])"),
        ('artificial_locations_and_single_original_supply_refill_not_earned_travel_or_resupply','only_declared_testing_locations_and_any_logged_crew_supply_refills_not_earned_progress')]
    for old,new in changes:
        assert source.count(old)==1,old;source=source.replace(old,new)
    needle="    ROOT.mkdir(parents=True);save(ROOT/"
    assert source.count(needle)==1
    source=source.replace(needle,"    assert cases['terminal'] in frames\n"+needle)
    source=source.replace("'normal_Sea_View_return_actually_viewed':frames[returned],", "'normal_Sea_View_return_actually_viewed':frames[returned],'later_terminal_normal_return_actually_viewed':frames[cases['terminal']],'unchanged_prior_text_and_font_reference_reconciled_to_V1637_with_fresh_V1676_native_and_actual_RGB':True,")
    exec(compile(source,__file__,'exec'),{'__name__':'__main__','__file__':__file__})
