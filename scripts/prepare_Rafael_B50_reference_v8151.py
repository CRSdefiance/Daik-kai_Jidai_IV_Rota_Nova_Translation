"""Derive B50 full reference/load/caller tools from preserved B49 producers."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/Rafael_B50_reference_tools_v8151')
if __name__=='__main__':
    assert not ROOT.exists()
    controls='Rafael_B50_relocated_controls_v8148/28_stored_dispatches_nine_controls_zero_relatives_relocated4821_25_seeded_ends.json'
    current='Rafael_B50_current_v8136/all28_complete_source_current_refs_before_new_English_manuscript.json'
    common={
        'Rafael_B49_reference_v8102':'Rafael_B50_reference_v8151',
        'Rafael_B49_relocation_v8096/one_block61_speeches56_relative_fixups280_cases_exact_full_inverse.json':'Rafael_B50_relocation_v8146/one_block28_speeches_zero_relative_cases_exact_full_inverse.json',
        'Rafael_B49_stored_v8097/all61_stored_bodies124_fresh120_reused_alignments61_exact_viewed_pages.json':'Rafael_B50_stored_v8147/all28_stored_bodies_full_native_alignment_and28_exact_viewed_pages.json',
        'Rafael_B49_relocated_controls_v8098/61_stored_dispatches13_raw_predicates1_query280_relative_cases25_seeded_ends.json':controls,
        'Rafael_B49_native_review_v8095/61_native_pages7_names_three_scoped_warnings22_infos_wrap_review.json':'Rafael_B50_native_review_v8145/28_native_pages3_names_two_scoped_warnings18_infos_wrap_review.json',
        'all_routes_combined_v8066':'all_routes_combined_v8122','all-routes-unified-v8066':'all-routes-unified-v8122',
    }
    reference=derive('scripts/create_Rafael_B49_reference_v8102.py','scripts/create_Rafael_B50_reference_v8151.py',{
        **common,"len(manifest['batches'])==637":"len(manifest['batches'])==638",
        'all61_native_ink_planes_exact_to_already_viewed':'all28_native_ink_planes_exact_to_already_viewed',
        "len(view['directly_viewed_sheets'])==12":"len(view['directly_viewed_sheets'])==6",
        "len(controls['final_dispatches'])==61":"len(controls['final_dispatches'])==28",
        '==[49]':'==[50]','sha(b[49])':'sha(b[50])','only_changed_blocks=[49]':'only_changed_blocks=[50]',
        'Rafael B49 complete61-speech/61-page research reference from currentV8066,exact inverses/56 relocated spans/all stored/native checks. OnlyB49 changes.':'Rafael B50 complete28-speech/28-page research reference from currentV8122,exact inverses/zero relative sites/all stored/native checks. OnlyB50 changes.',
        'Pinned B49 research reference. OnlySC0 B49 changes;342others/allotherfiles/components exact. CurrentV8066/mainV4701 unchanged.':'Pinned B50 research reference. OnlySC0 B50 changes;342others/allotherfiles/components exact. CurrentV8122/mainV4701 unchanged.',
    })
    loaders=derive('scripts/verify_Rafael_B49_loaders_v8103.py','scripts/verify_Rafael_B50_loaders_v8152.py',{
        'scripts.create_Rafael_B49_reference_v8102':'scripts.create_Rafael_B50_reference_v8151',
        'Rafael_B49_loaders_v8103':'Rafael_B50_loaders_v8152',
        'Rafael_B49_reference_v8102':'Rafael_B50_reference_v8151',
        'exact_B49_header_andall_mapped_targets_fit_original_0x2400_cache':'exact_B50_header_andall_mapped_targets_fit_original_0x2400_cache',
    })
    callers=derive('scripts/verify_Rafael_B49_references_v8104.py','scripts/verify_Rafael_B50_references_v8153.py',{
        'scripts.create_Rafael_B49_reference_v8102':'scripts.create_Rafael_B50_reference_v8151',
        'Rafael_B49_reference_census_v8104':'Rafael_B50_reference_census_v8153',
        'Rafael_B49_current_v8086/all61_complete_source_current_refs_before_new_English_manuscript.json':current,
        'Rafael_B49_loaders_v8103':'Rafael_B50_loaders_v8152',
        'Rafael_B48_reference_census_v8048/all163_commands28_relative_sites91_speeches4_FE_EV0_entry_shipped_callers.json':'Rafael_B49_reference_census_v8104/all154_commands56_relative_sites61_speeches_C281_EV0_entry_shipped_callers.json',
        'Rafael_B49_relocated_controls_v8098/61_stored_dispatches13_raw_predicates1_query280_relative_cases25_seeded_ends.json':controls,
        'block=bank[49]':'block=bank[50]',"cg['block']==tg['block']==49":"cg['block']==tg['block']==50",
        'len(rows)==154':'len(rows)==37',"tg['target_logical_end']==3792":"tg['target_logical_end']==1374",
        "len(tg['relative_fixups'])==56":"len(tg['relative_fixups'])==0",
        "sum(len(r['cases']) for r in tg['relocated_skip_cases'])==280":"sum(len(r['cases']) for r in tg['relocated_skip_cases'])==0",
        "len(controls['final_dispatches'])==61":"len(controls['final_dispatches'])==28",
        "len(controls['relocated_predicates_andqueries'])==14":"len(controls['relocated_predicates_andqueries'])==0",
        '[(49,50,49,[39])]':'[(50,51,50,[])]','block=49':'block=50',
        'all154_commands56_relative_sites61_speeches_C281_EV0_entry_shipped_callers.json':'all37_commands_zero_relative_sites28_speeches_4821_EV0_entry_shipped_callers.json',
        'all61_text_records':'all28_text_records',
        'all154_source_current_target_commands56_relative_sites_bound_to_research_ROM':'all37_source_current_target_commands_zero_relative_sites_bound_to_research_ROM',
        'all61_preambles_source00_02_09_thirteen_raw_predicates_one_query_sevenA000_C281_andcomplete_end_preserved':'all28_preambles_source00_02_09_FA2_FI1_nine_nontext_4821_4720_4681_oneA000_andcomplete_end_preserved',
        'source_event49_action50_requires39_not_natural_eligibility':'source_event50_action51_no_explicit_dependencies_not_natural_eligibility',
        'actual_body_seven_headers_C281_transitions_return_policy_production_andrelease_pending':'actual_body_three_headers_4821_4720_4681_transitions_return_policy_production_andrelease_pending',
        'Bind154commands,56relative spans,C281 andoriginal EV0entry to a fresh shipped caller census.':'Bind37commands,zero relative sites,4821 andoriginal EV0entry to a fresh shipped caller census.',
        "print('B49 full reference:154commands/56relative sites/61speeches/C281,originalEV0entry/shippedcallers bound.Actual scenes/policy/production/release pending.')":"print('B50 full reference:37commands/zero relative sites/28speeches/4821,originalEV0entry/shippedcallers bound.Actual scenes/policy/production/release pending.')",
    })
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',[reference,loaders,callers])
    print('Prepared B50 full reference,343 loaders/686 parent modes andcaller census tools;zero credit.')
