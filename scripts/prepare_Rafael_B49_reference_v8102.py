"""Bind B49's reviewed block to a preserved full reference and original native entry checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/Rafael_B49_reference_tools_v8102')
if __name__=='__main__':
    assert not ROOT.exists()
    common={
        'Rafael_B48_reference_v8046':'Rafael_B49_reference_v8102',
        'Rafael_B48_relocation_v8041/one_block91_speeches28_relative_fixups140_cases_exact_full_inverse.json':'Rafael_B49_relocation_v8096/one_block61_speeches56_relative_fixups280_cases_exact_full_inverse.json',
        'Rafael_B48_stored_v8042/all91_stored_bodies192_fresh172_reused_alignments92_exact_viewed_pages.json':'Rafael_B49_stored_v8097/all61_stored_bodies124_fresh120_reused_alignments61_exact_viewed_pages.json',
        'Rafael_B48_relocated_controls_v8043/91_stored_dispatches5_raw_predicates2_queries140_relative_cases25_seeded_ends.json':'Rafael_B49_relocated_controls_v8098/61_stored_dispatches13_raw_predicates1_query280_relative_cases25_seeded_ends.json',
        'Rafael_B48_native_review_v8040/91_paragraphs92_native_pages9_names_two_scoped_warnings37_infos_wrap_review.json':'Rafael_B49_native_review_v8095/61_native_pages7_names_three_scoped_warnings22_infos_wrap_review.json',
        'all_routes_combined_v8013':'all_routes_combined_v8066','all-routes-unified-v8013':'all-routes-unified-v8066',
    }
    receipt=derive('scripts/create_Rafael_B48_reference_v8046.py','scripts/create_Rafael_B49_reference_v8102.py',{
        **common,"len(manifest['batches'])==636":"len(manifest['batches'])==637",
        'all91_native_ink_planes_exact_to_already_viewed':'all61_native_ink_planes_exact_to_already_viewed',
        "len(view['directly_viewed_sheets'])==17":"len(view['directly_viewed_sheets'])==12",
        "len(controls['final_dispatches'])==91":"len(controls['final_dispatches'])==61",
        '==[48]':'==[49]','sha(b[48])':'sha(b[49])','only_changed_blocks=[48]':'only_changed_blocks=[49]',
        'Rafael B48 complete91-speech/92-page research reference from currentV8013,exact inverses/28 relocated spans/all stored/native checks. OnlyB48 changes.':'Rafael B49 complete61-speech/61-page research reference from currentV8066,exact inverses/56 relocated spans/all stored/native checks. OnlyB49 changes.',
        'Pinned B48 research reference. OnlySC0 B48 changes;342others/allotherfiles/components exact. CurrentV8013/mainV4701 unchanged.':'Pinned B49 research reference. OnlySC0 B49 changes;342others/allotherfiles/components exact. CurrentV8066/mainV4701 unchanged.',
    })
    loaders=derive('scripts/verify_Rafael_B48_loaders_v8047.py','scripts/verify_Rafael_B49_loaders_v8103.py',{
        'scripts.create_Rafael_B48_reference_v8046':'scripts.create_Rafael_B49_reference_v8102',
        'Rafael_B48_loaders_v8047':'Rafael_B49_loaders_v8103',
        'Rafael_B48_reference_v8046':'Rafael_B49_reference_v8102',
        'exact_B48_header_andall_mapped_targets_fit_original_0x2400_cache':'exact_B49_header_andall_mapped_targets_fit_original_0x2400_cache',
    })
    callers=derive('scripts/verify_Rafael_B48_references_v8048.py','scripts/verify_Rafael_B49_references_v8104.py',{
        'scripts.create_Rafael_B48_reference_v8046':'scripts.create_Rafael_B49_reference_v8102',
        'Rafael_B48_reference_census_v8048':'Rafael_B49_reference_census_v8104',
        'Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json':'Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B48_loaders_v8047':'Rafael_B49_loaders_v8103',
        'Rafael_B47_reference_census_v7996/all48_commands24_relative_sites15_speeches_EV0_entry_shipped_callers.json':'Rafael_B48_reference_census_v8048/all163_commands28_relative_sites91_speeches4_FE_EV0_entry_shipped_callers.json',
        'Rafael_B48_relocated_controls_v8043/91_stored_dispatches5_raw_predicates2_queries140_relative_cases25_seeded_ends.json':'Rafael_B49_relocated_controls_v8098/61_stored_dispatches13_raw_predicates1_query280_relative_cases25_seeded_ends.json',
        'block=bank[48]':'block=bank[49]',"cg['block']==tg['block']==48":"cg['block']==tg['block']==49",
        'len(rows)==163':'len(rows)==154',"tg['target_logical_end']==4948":"tg['target_logical_end']==3792",
        "len(tg['relative_fixups'])==28":"len(tg['relative_fixups'])==56",
        "sum(len(r['cases']) for r in tg['relocated_skip_cases'])==140":"sum(len(r['cases']) for r in tg['relocated_skip_cases'])==280",
        "len(controls['final_dispatches'])==91":"len(controls['final_dispatches'])==61",
        "len(controls['relocated_predicates_andqueries'])==7":"len(controls['relocated_predicates_andqueries'])==14",
        '[(48,49,48,[])]':'[(49,50,49,[39])]','block=48':'block=49',
        'all163_commands28_relative_sites91_speeches4_FE_EV0_entry_shipped_callers.json':'all154_commands56_relative_sites61_speeches_C281_EV0_entry_shipped_callers.json',
        'all91_text_records':'all61_text_records',
        'all163_source_current_target_commands28_relative_sites_bound_to_research_ROM':'all154_source_current_target_commands56_relative_sites_bound_to_research_ROM',
        'all91_preambles_source00_4B71_five_raw_predicates_two_queries_fourFE_andcomplete_end_preserved':'all61_preambles_source00_02_09_thirteen_raw_predicates_one_query_sevenA000_C281_andcomplete_end_preserved',
        'source_event48_action49_no_explicit_dependency_list_not_natural_eligibility':'source_event49_action50_requires39_not_natural_eligibility',
        'four_FE_andno_typed_menu_source_consumers_preserved':'no_FE_or_typed_menu_source_consumers',
        'actual_body_headers_R347_page_turn_four_FE_joining_transitions_policy_production_andrelease_pending':'actual_body_seven_headers_C281_transitions_return_policy_production_andrelease_pending',
        'Bind163commands,28relative spans,four FEpanels andoriginal EV0entry to a fresh shipped caller census.':'Bind154commands,56relative spans,C281 andoriginal EV0entry to a fresh shipped caller census.',
        "print('B48 full reference:163commands/28relative sites/91speeches/fourFE,originalEV0entry/shippedcallers bound.Actual scenes/policy/production/release pending.')":"print('B49 full reference:154commands/56relative sites/61speeches/C281,originalEV0entry/shippedcallers bound.Actual scenes/policy/production/release pending.')",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[receipt,loaders,callers])
    print('Prepared B49 full-reference, loader and caller tools; no emulator run or credit.')
