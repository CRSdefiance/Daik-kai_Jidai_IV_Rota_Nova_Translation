"""Freeze individual approval andwhole-inverse reference sealing forB36."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/maria_B36_approval_tools_v7816b')
if __name__=='__main__':
    assert not ROOT.exists();results=[]
    old="Complete whole-exchange English isautomatically formatted under the exact file/record/selector scoped216px,four-row profile;FI5/FA2/FO7 measured fromown Maria context. All first/internal/final native glyphs,guarded linebreaks,bounds,canaries,consumption andstored zero-ink tails pass. All67 areone page;22 individual row-count infos,no warnings orwaivers. Paired source/finalEnglish fixtures cover65 distinct speeches each,130complete panes,528complete body+name holds;two Julian conditional speeches remainexplicitly offline. Original branches,setup,witnessed previous-result extents,normal type0 valuecarry andreturns preserved. Native/source-only R65 nineteenth-cell finding isnot anEnglish width change. All measured timing,RNG,actor/component/calendar andlater RGB differences remainbound;no broad simulation/full-effects/everyframe/future claim. Existing system-only unlock isdisclosed,earned=false;initialized background isnot natural optional activation/location. Shared actor155 semantic wording,full207 names/catalogueUI andother consumers remainopen. Atomic production,registered reconstruction,clean-input patch andown-ROM startup remainpending."
    new="Complete English uses the exact source-bound 216px/four-row profile with measured FI5/FA2/FO7. All16 single pages,complete glyphs,bounds,canaries,consumption and11 zero-ink parity tails pass. Nine individually justified row-count infos andall baseQA remain;no warnings orwaivers. Original FO-before-FI order ispreserved in two natural introductory clauses. A scoped ordinary soft-wrap preference keeps the short closing praise together without authored breaks,width change orprose alteration. Paired source/English fixtures playall16 speeches each:32complete panes,132complete body/name holds,zero partials/unknowns,all29 fixturecommands andnormal type0 valuecarry. Allsource andEnglish black/ASCII-gray/CP932-gray/name masks match;all16 upperRGBpairs andresults/UI agree. Preserve18command/sixduration rows,exits8213/8216,108/131lateRGBdifferences,allrawRNG/actors/components/calendars andfollowingcommands. InitializedHangzhou/return8300 isnot originaloptional location oractivation;existing system-only unlock isdisclosed,earned=false. No fullmechanics/routes/hardware/everyframe/future/causalclaim. Lil/Maria/Xien headers areobserved;fullcatalogueUI/full207/shared151-159 semantics remainopen. Atomic registered production,exact patch andown-ROM startup remainpending."
    results.append(derive('scripts/approve_Maria_story_native_v7771.py','scripts/approve_Maria_B36_native_v7816b.py',{
        'maria_story_profile_v1':'maria_B36_profile_v1','Maria_story_final_paths_v7771':'Maria_B36_final_paths_v7816b',
        "policy['positive_count']==67 and policy['negative_count']==200":"policy['positive_count']==16 and policy['negative_count']==81",
        "stored['stored_alignment_coverage']==268 and stored['zero_ink_parity_tails']==33 and stored['final_complete_native_pages']==67":
        "stored['stored_alignment_cases']==64 and stored['zero_ink_parity_tail_count']==11 and stored['complete_stored_native_pages']==16",
        "view['all130_final_actual_panes_viewed_with_exact_reuse'] and view['complete_body_andheader_holds']==528":
        "view['all9_actual_transition_late_sheets_individually_viewed'] and view['complete_body_andheader_holds']==132",
        "actual['total_actual_speech_occurrences']==actual['complete_actual_page_panels']==130":
        "actual['total_actual_speech_occurrences']==actual['complete_actual_page_panels']==32",
        'len(panels)==65':'len(panels)==16',
        "offline={'DK4_MES_B108_R0020','DK4_MES_B108_R0125'}":"offline=set()",
        old:new,
        "'revise':48,'retain-wording':19":"'revise':9,'retain-wording':7",
        'all67_formatting_gates_false':'all16_formatting_gates_false','all67_five_individual_gates_true':'all16_five_individual_gates_true',
        'actual_objects=65,offline_only_objects=2':'actual_objects=16,offline_only_objects=0',
        '67 individual gates approved':'16 individual gates approved',
        'all67_individual_five_gates_approved':'all16_individual_five_gates_approved',
        'revision_count=48,retention_count=19,actual_final_pages=130':'revision_count=9,retention_count=7,actual_final_pages=32',
        'actual_speeches_each_language=65':'actual_speeches_each_language=16',
        'complete_body_andheader_holds=528':'complete_body_andheader_holds=132',
        'all67_native_stored_pages_complete_andall_original_controls_preserved':'all16_native_stored_pages_complete_andall_original_controls_preserved',
        '67individual five-gate decisions approved:48revisions/19retentions;65actual+2offline perlanguage.':
        '16individual five-gate decisions approved:9revisions/7retentions;16actual/0offline perlanguage.',
    }))
    results.append(derive('scripts/seal_Maria_story_references_v7772.py','scripts/seal_Maria_B36_references_v7817b.py',{
        'Maria_story_final_paths_v7771':'Maria_B36_final_paths_v7816b',
        'all67':'all16','all116_commands20_relative_sites_source_bound':'all22_commands_no_relative_sites_source_bound',
        'all_three_clean':'complete_clean','complete_three_source_predecessor_blocks':'complete_source_predecessor_block',
        'three_clean':'complete_clean','three-block':'one-block',
        'two_Julian_conditionals_explicitly_offline':'all16_original_speeches_actually_observed',
        'two_Julian_conditionals_offline':'no_unplayed_speeches',
        'final_actual65_eachlanguage_two_Julian_conditionals_offline':'final_actual16_eachlanguage_no_unplayed_speeches',
        'view[\'all130_final_actual_panes_viewed_with_exact_reuse\']':'view[\'all9_actual_transition_late_sheets_individually_viewed\']',
        '==[34,35,108]':'==[36]',
        "'dk4-Maria67-source-relocation-map-v1'":"'dk4-Maria16-B36-source-relocation-map-v1'",
        "read(VIEW)['final_late_limits']":"dict(source_English_exits=read(VIEW)['source_English_exits'],command_difference_rows=read(VIEW)['command_difference_rows'],duration_difference_rows=read(VIEW)['duration_difference_rows'],later_RGB_differences=read(VIEW)['later_RGB_differences'],later_samples=read(VIEW)['later_samples'],five_component_equality=read(VIEW)['five_component_equality'],whole_actor_equality=read(VIEW)['whole_actor_equality'],final_PRNG_seeds=read(VIEW)['final_PRNG_seeds'])",
        '67 exact decisions':'16 exact decisions',
        '67decisions/three blocks sealed;116commands/20relative sites;full clean+predecessor inverse/all300otherblocks exact.':
        '16decisions/B36 sealed;22commands/no relative sites;full clean+predecessor inverse/all302otherblocks exact.',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'provenance.json',dict(derivations=results,
        all_original_native_numeric_constants_individual_gates_macro_preambles_andfull_inverse_guards_preserved=True,
        all16_actual_source_English_speeches_no_unplayed_conditionals=True,
        all_measured_late_differences_andbroad_name_goal_preserved=True,new_credit=0,full_goal_complete=False))
