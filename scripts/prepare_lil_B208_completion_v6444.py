"""Prepare a frozen completion successor with B208-specific gates and exact ledger inverse."""
import re
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text,derive
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B208_completion_tools_v6444')
if __name__=='__main__':
    assert not ROOT.exists();sourcepath=Path('scripts/complete_lil_B207_v6385.py');original=sourcepath.read_text('utf-8')
    a,b=original.index('def gates():'),original.index('\ndef restore(')
    source=original[:a]+'from scripts.lil_B208_completion_gates_v6444 import gates\n'+original[b:]
    ROOT.mkdir(parents=True);frozen=ROOT/'frozen_B207_completion_without_scene_specific_gates.py';frozen.write_text(source,encoding='utf-8')
    changes={
        'thirteen':'twenty-four','B207':'B208','B208_clean_review_pending':'B209_clean_review_pending',
        'completion_v6385':'completion_v6444','verification_v6386':'verification_v6445',
        'manuscript_v6.json':'manuscript_v7.json','release_v6381':'release_v6440','startup_v6384':'startup_v6443',
        'actual_v6374/all13_English_panels_complete_native_holds24_commands_and_source_comparison.json':'actual_v6431/all24_English_panels_complete_native_holds38_commands_and_source_comparison.json',
        'actual_review_v6376/viewed13_panels51_native_holds_and_honest_timing_RNG_prompt_scope.json':'actual_review_v6433/viewed24_panels95_holds_thought_FE_and_honest_broader_later_scope.json',
        'verification_v6364':'verification_v6436','registration_v6379':'registration_v6438','retention_v6382':'retention_v6441',
        'Lil-B207-Minotaur-Axe-uncertain-island-clue-conditional-search-and-undecided-gift13':'Lil-B208-pirate-sword-hearsay-intuition-private-thought-and-Charm-notice24',
        'unfinished_editorial_scope_v6385':'unfinished_editorial_scope_v6444',
        'Lil_B207_v6385':'Lil_B208_v6444','lil_B207_completion_text_v6385':'lil_B208_completion_text_v6444',
        "Counter(r['editorial_decision'] for r in rows)=={'revise':6,'retain-wording':7}":"Counter(r['editorial_decision'] for r in rows)=={'revise':15,'retain-wording':9}",
        "blocks[207]":"blocks[208]","block=207":"block=208",
        "revised=6,retained=7":"revised=15,retained=9",'revised_count=6,retained_count=7,fresh_revisions=6,fresh_retentions=7':'revised_count=15,retained_count=9,fresh_revisions=15,fresh_retentions=9',
        'new_revisions=6,justified_retentions=7':'new_revisions=15,justified_retentions=9',
        'blocks=[207]':'blocks=[208]',
        'actual_matching_holds=51':'actual_matching_holds=95','complete_text_nameplate_holds=51':'complete_text_nameplate_holds=95',
        'source207':'source208','event207':'event208','selected_source207':'selected_source208',
        'source_English_content_frames=22002,new_English_content_runs=1,new_English_content_frames=11001,reused_source_frames=11001':'source_English_content_frames=32002,new_English_content_runs=1,new_English_content_frames=16001,reused_source_frames=16001',
        'reused_verified_source_frames=11001':'reused_verified_source_frames=16001',
        'goal_turn_new_emulator_runs=3,goal_turn_new_frames=32403':'goal_turn_new_emulator_runs=2,goal_turn_new_frames=21402',
        "old['unfinished_editorial_scope_v6363']":"old['unfinished_editorial_scope_v6435']",
        "all15_commands13_preambles_one_A000_complete_end_and_original_results_preserved=True,one_exact_source_ordinary_boundary_three_rowcount_reasons=True":"all29_commands24_preambles_five_leaves_complete_end_and_original_results_preserved=True,one_exact_source_ordinary_boundary_four_rowcount_reasons=True,exact_preLF_reservation_source_bound_with_original_codec=True",
        'all15_source_commands_and9_initializers_observed=True':'all29_source_commands_and9_initializers_observed=True',
        'all13timing3RNG6promptRGB_and_different_final_PRNG_limits_preserved=True':'all16timing18RNG44broaderRGB_eight_duration_and_different_final_state_limits_preserved=True',
        "dict(file_path='/data/SC2.DK4',block=208,clean_inventory_and_full_exchange_gloss_before_prior_English=True,reviewed_objects=0,new_completion_credit=0,no_B207_actor_macro_item_conditional_search_effect_or_end_assumptions_inherited=True)":"dict(file_path='/data/SC2.DK4',block=209,clean_inventory_and_full_exchange_gloss_before_prior_English=True,clean_inventory='work/analysis/lil_B209_clean_inventory_v6446/all_clean_B209_speeches_before_predecessor_comparison.json',reviewed_objects=0,new_completion_credit=0,no_B208_actor_macro_item_FE_effect_or_end_assumptions_inherited=True)",
        "assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory":"assert 'speaker_names_and_role_labels_localization_review_v5708' in inventory and 'retrospective_exact_preLF_reservation_editorial_lead_v6435' in inventory",
        'next_Lil_B208_clean_review_pending=True':'next_Lil_B209_clean_review_pending=True',
        'source207_natural_activation':'source208_natural_activation',
        'measured13timing3RNG6promptRGB_and_different_final_PRNG_limits_preserved=True':'measured16timing18RNG44broaderRGB_eight_duration_and_different_final_state_limits_preserved=True',
        'startup31_frames_and_five_actor_controls_match_V6327':'startup31_frames_and_five_actor_controls_match_V6380',
        'all598_manifest_batches114_accepted18_checks_verified':'all599_manifest_batches114_accepted18_checks_verified',
        '## V6385: B207 complete exchange integrated once in cumulative V6380':'## V6444: B208 complete exchange integrated once in cumulative V6439',
        '# Current editorial handoff - V6385':'# Current editorial handoff - V6444',
        'V6380 verified:6428 completed/6431 source-prose. B208':'V6439 verified:6452 completed/6455 source-prose. B209',
        '6428 contextual rereads integrated;source/prose6431. All13 B207 records counted once.':'6452 contextual rereads integrated;source/prose6455. All24 B208 records counted once.',
        "formatting_reason='Historical native-only proof/UI limits preserved. Separate actual evidence verifies all13 complete English/current-style11-name panels,51 holds,all24 fixture command paths/results and town return. One exact it/if ordinary boundary and three rowcount reasons remain;no glyph,bounds,pagination or control waiver.'":"formatting_reason='Historical native-only proof/UI limits preserved. Actual evidence verifies24 complete English panels,95 holds,91 style11 nameplates and4 portraitless FE literal-notice holds,all38 fixture commands,town/B120/sailing return. Exact it/during ordinary boundary,four rowcount reasons and source-bound actual preLF reservation remain;no glyph,bounds,pagination or control waiver.'",
        "previous_B207_objects_uncredited=True":"previous_B208_objects_uncredited=True",
        "natural_event207_not_selected=True":"natural_event208_not_selected=True",
        "full_goal_complete=False));print('Six targets staged;13 disjoint reviews proposed once.":"full_goal_complete=False));print('Six targets staged;24 disjoint reviews proposed once.",
    }
    # Number-token replacement in the frozen reconstruction/ledger core only; no native constants.
    numeric={13:24,6415:6428,6428:6452,6431:6455,4011:4026,2417:2426,4529:4542,4542:4566,4828:4852}
    # Incorporate numeric substitutions as simultaneous exact word-boundary rewrites in a new frozen stage.
    # checked_text cannot apply regex keys; preserve and hash both stages explicitly.
    first=checked_text(source,changes)
    import io,tokenize
    tokens=[]
    for t in tokenize.generate_tokens(io.StringIO(first).readline):
        if t.type==tokenize.NUMBER and t.string.isdecimal() and int(t.string) in numeric:
            t=t._replace(string=str(numeric[int(t.string)]))
        tokens.append(t)
    target=tokenize.untokenize(tokens)
    # Remaining string fields are documentary IDs/counters, changed explicitly after code-token numbers.
    strings={'all13_':'all24_','13 disjoint':'24 disjoint','13 new':'24 new','exactly13_':'exactly24_',
        'new_completed_records=13':'new_completed_records=24','integrates13':'integrates24'}
    for a,b in strings.items():target=target.replace(a,b)
    compile(target,'complete_lil_B208_v6444.py','exec')
    from scripts.source_locked_derivation_v5118 import native_numbers
    assert native_numbers(target)==native_numbers(source)
    output=Path('scripts/complete_lil_B208_v6444.py');assert not output.exists();output.write_text(target,encoding='utf-8')
    save(ROOT/'prepared_completion.json',dict(source=str(sourcepath),source_sha256=sha(sourcepath.read_bytes()),frozen=str(frozen),frozen_sha256=sha(frozen.read_bytes()),output=str(output),output_sha256=sha(output.read_bytes()),scene_specific_gates_replaced_by_independently_authored_B208_module=True,native_high_integer_constants_and_multiplicities_preserved=True,full_goal_complete=False))
    print('B208 completion producer prepared;no ledger mutation.')
