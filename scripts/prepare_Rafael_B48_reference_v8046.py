"""Prepare immutable full B48 reference,all343 loaders andfresh163-command caller binding."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B48_reference_tools_v8046')
if __name__=='__main__':
    assert not ROOT.exists()
    registry=read('translations/release_stack.json');assert len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert registry['profiles']['all-routes-unified-v8013']['rafael_B47_editorial']=='translations/rafael_B47_editorial_release_v1.json'
    results=[derive('scripts/create_Rafael_B47_reference_v7994.py','scripts/create_Rafael_B48_reference_v8046.py',{
        'Rafael_B47_reference_v7994':'Rafael_B48_reference_v8046',
        'Rafael_B47_relocation_v7989/one_block15_speeches24_relative_fixups120_cases_exact_full_inverse.json':
            'Rafael_B48_relocation_v8041/one_block91_speeches28_relative_fixups140_cases_exact_full_inverse.json',
        'Rafael_B47_stored_v7990/all15_stored_bodies32_fresh28_reused_alignments16_exact_viewed_pages.json':
            'Rafael_B48_stored_v8042/all91_stored_bodies192_fresh172_reused_alignments92_exact_viewed_pages.json',
        'Rafael_B47_relocated_controls_v7991/15_stored_dispatches6_raw_predicates120_relative_cases25_seeded_ends.json':
            'Rafael_B48_relocated_controls_v8043/91_stored_dispatches5_raw_predicates2_queries140_relative_cases25_seeded_ends.json',
        'Rafael_B47_native_review_v7988/15_paragraphs16_native_pages4_names_two_scoped_warnings_individual_wrap_review.json':
            'Rafael_B48_native_review_v8040/91_paragraphs92_native_pages9_names_two_scoped_warnings37_infos_wrap_review.json',
        'all_routes_combined_v7964':'all_routes_combined_v8013','all-routes-unified-v7964':'all-routes-unified-v8013',
        "len(manifest['batches'])==635":"len(manifest['batches'])==636",
        'all15_native_ink_planes_exact_to_already_viewed':'all91_native_ink_planes_exact_to_already_viewed',
        "len(view['directly_viewed_sheets'])==4":"len(view['directly_viewed_sheets'])==17",
        "len(controls['final_dispatches'])==15":"len(controls['final_dispatches'])==91",
        '==[47]':'==[48]','sha(b[47])':'sha(b[48])','only_changed_blocks=[47]':'only_changed_blocks=[48]',
        'Rafael B46 complete15-speech/16-page research reference from currentV7964,exact inverses/24 relocated spans/all stored/native checks. OnlyB47 changes.':
            'Rafael B48 complete91-speech/92-page research reference from currentV8013,exact inverses/28 relocated spans/all stored/native checks. OnlyB48 changes.',
        'Pinned B47 research reference. OnlySC0 B47 changes;342others/allotherfiles/components exact. CurrentV7964/mainV4701 unchanged.':
            'Pinned B48 research reference. OnlySC0 B48 changes;342others/allotherfiles/components exact. CurrentV8013/mainV4701 unchanged.',
    })]
    results.append(derive('scripts/verify_Rafael_B47_loaders_v7995.py','scripts/verify_Rafael_B48_loaders_v8047.py',{
        'scripts.create_Rafael_B47_reference_v7994':'scripts.create_Rafael_B48_reference_v8046',
        'Rafael_B47_loaders_v7995':'Rafael_B48_loaders_v8047',
        'Rafael_B47_reference_v7994':'Rafael_B48_reference_v8046',
        'exact_B47_header_andall_mapped_targets_fit_original_0x2400_cache':'exact_B48_header_andall_mapped_targets_fit_original_0x2400_cache',
    }))
    source=Path('scripts/verify_Rafael_B47_references_v7996.py').read_text('utf8')
    results.append(derive('scripts/verify_Rafael_B47_references_v7996.py','scripts/verify_Rafael_B48_references_v8048.py',{
        'scripts.create_Rafael_B47_reference_v7994':'scripts.create_Rafael_B48_reference_v8046',
        'Rafael_B47_reference_census_v7996':'Rafael_B48_reference_census_v8048',
        'Rafael_B47_current_v7980/all15_complete_source_current_refs_before_new_English_manuscript.json':
            'Rafael_B48_current_v8028/all91_complete_source_current_refs_before_new_English_manuscript.json',
        'Rafael_B47_loaders_v7995':'Rafael_B48_loaders_v8047',
        'Rafael_B46_reference_census_v7943/all37_commands_four_relative_sites_two_choices_EV0_entry_shipped_callers.json':
            'Rafael_B47_reference_census_v7996/all48_commands24_relative_sites15_speeches_EV0_entry_shipped_callers.json',
        'Rafael_B47_relocated_controls_v7991/15_stored_dispatches6_raw_predicates120_relative_cases25_seeded_ends.json':
            'Rafael_B48_relocated_controls_v8043/91_stored_dispatches5_raw_predicates2_queries140_relative_cases25_seeded_ends.json',
        'block=bank[47]':'block=bank[48]',"cg['block']==tg['block']==47":"cg['block']==tg['block']==48",
        'len(rows)==48':'len(rows)==163', "tg['target_logical_end']==1344":"tg['target_logical_end']==4948",
        "len(tg['relative_fixups'])==24":"len(tg['relative_fixups'])==28",
        "sum(len(r['cases']) for r in tg['relocated_skip_cases'])==120":"sum(len(r['cases']) for r in tg['relocated_skip_cases'])==140",
        "len(controls['final_dispatches'])==15":"len(controls['final_dispatches'])==91",
        "len(controls['relocated_predicates'])==6":"len(controls['relocated_predicates_andqueries'])==7",
        '[(47,48,47,[37])]':'[(48,49,48,[])]','block=47':'block=48',
        'all48_commands24_relative_sites15_speeches_EV0_entry_shipped_callers.json':
            'all163_commands28_relative_sites91_speeches4_FE_EV0_entry_shipped_callers.json',
        'all15_text_records':'all91_text_records',
        'all48_source_current_target_commands24_relative_sites_bound_to_research_ROM':
            'all163_source_current_target_commands28_relative_sites_bound_to_research_ROM',
        'all15_sixbyte_preambles_including_source00_six_predicates_andcomplete_end_preserved':
            'all91_preambles_source00_4B71_five_raw_predicates_two_queries_fourFE_andcomplete_end_preserved',
        'source_event47_action48_requires37_not_natural_eligibility':
            'source_event48_action49_no_explicit_dependency_list_not_natural_eligibility',
        'no_menu_orFE_objects_in_source':'four_FE_andno_typed_menu_source_consumers_preserved',
        'actual_body_headers_R53_page_transition_policy_production_andregistered_release_pending':
            'actual_body_headers_R347_page_turn_four_FE_joining_transitions_policy_production_andrelease_pending',
        'Bind all48 commands,24 relative spans andoriginal EV0 entry to a fresh shipped caller census.':
            'Bind163commands,28relative spans,four FEpanels andoriginal EV0entry to a fresh shipped caller census.',
        source.splitlines()[-1]:"    print('B48 full reference:163commands/28relative sites/91speeches/fourFE,originalEV0entry/shippedcallers bound.Actual scenes/policy/production/release pending.')",
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_derivations.json',results)
    print('Prepared B48 reference/loaders/callers tools;no ROM created until reference producer runs.')
