"""Record directly viewed complete source pages;keep native/offline andactual gameplay separate."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B50_source_view_v8487b')
DISPLAY=Path('work/analysis/Hodram_B50_source_display_v8487/source_display.json')
CONTROLS=Path('work/analysis/Hodram_B50_source_controls_v8486/source_controls.json')
if __name__=='__main__':
    assert not ROOT.exists();display,controls=map(read,[DISPLAY,CONTROLS]);sheet=display['review_sheet']
    assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'] and len(display['records'])==3 and controls['item148_native_layout0_andoriginal_hide_boundary_pass']
    assert display['current_English_dialogue_bodies_unconsulted'] and controls['current_English_dialogue_bodies_still_unconsulted']
    assert [r['source_selector'] for r in display['records']]==[2,2,254] and sum(len(r['original_four_alignments']['cases']) for r in display['records'])==12
    assert all(r['complete_native_source_display']['pages']==1 if r['source_selector']==254 else len(r['complete_native_source_display']['pages'])==1 for r in display['records'])
    ROOT.mkdir(parents=True);save(ROOT/'source_view.json',dict(display=str(DISPLAY),display_sha256=sha(DISPLAY.read_bytes()),controls=str(CONTROLS),controls_sha256=sha(CONTROLS.read_bytes()),directly_viewed_sheet=sheet,all3_complete_source_pages_directly_viewed=True,source_arrival_request_then_explicit_gift_cheer_farewell_then_outgoing_notice_preserved=True,source_Lil_original_voice3_andFE_original_null_actor_bound_offline=True,source_item148_layout0_andhide_boundaries_are_not_executed_UI_oractual_trade_eligibility=True,source_FI_FA_FO_counts_zero=True,source_four_rows_R10_complete_without_extra_page=True,no_current_English_exposure_prose_formatting_actual_orregistered_approval=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Viewed all3complete B50Japanese nativepages;twoLil/bodypages andnullFE/outgoingnotice. CurrentEnglish unread;no actualgameplay orcredit.')
