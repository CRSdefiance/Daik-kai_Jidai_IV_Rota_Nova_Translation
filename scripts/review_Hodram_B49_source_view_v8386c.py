"""Record direct review of all fourteen complete Japanese native body pages before current English."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B49_source_view_v8386c')
SOURCE=Path('work/analysis/Hodram_B49_source_display_v8386b/source_display.json')
if __name__=='__main__':
    assert not ROOT.exists();proof=read(SOURCE);assert len(proof['records'])==14 and proof['current_English_dialogue_bodies_unconsulted'];sheet=proof['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'];rows=[]
    for row in proof['records']:
        display=row['complete_native_source_display'];FE=row['source_selector']==254
        if FE:
            assert display['pages']==1 and sha(Path(display['native_physical_plane']).read_bytes())==display['native_physical_plane_sha256'] and sha(Path(display['native_logical_plane']).read_bytes())==display['native_logical_plane_sha256']
        else:
            assert len(display['pages'])==1
            for page in display['pages']:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
        rows.append(dict(id=row['id'],source_reference=row['source_reference'],source_selector=row['source_selector'],pages=1,directly_viewed_complete_first_internal_final_characters=True,source_manual_lines_retained_as_evidence_not_future_English_layout_instructions=True))
    ROOT.mkdir(parents=True);save(ROOT/'source_view.json',dict(source_native_proof=str(SOURCE),source_native_proof_sha256=sha(SOURCE.read_bytes()),directly_viewed_sheet=sheet,records=rows,all14_source_pages_directly_viewed=True,source_R43_four_rows_andcomplete_bow_trade_offer_visible=True,source_R67_silence_andnegated_denial_complete=True,source_R74_distinct_cheer_andfarewell_not_collapsed_with_R43=True,source_FE_outgoing_wristband_title_andfinal_characters_complete=True,approved_Hodram_Joakim_fields_anddistinct_full_getter_preserved_no_name_change=True,not_actual_scene_orFE_palette_geometry_transition_observation=True,current_B49_English_bodies_still_unconsulted=True,native_choice_UI_geometry_glyphs_selection_current_editorial_andactual_tests_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Directly viewed14clean nativepages:completeglyphs/4-row offer/qualifiedHodram reply/distinct farewell/outgoingwristbandFE;native/offline only.CurrentEnglish still unread;zero credit.')
