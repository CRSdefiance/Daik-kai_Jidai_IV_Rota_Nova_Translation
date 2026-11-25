"""Credit359 disjoint reviews once, after the registered candidate's complete release gates."""
import re
from scripts.complete_maria363_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'maria363_B216_B252':'maria359_B253_B274',
    'Maria_SC3_B216_B252':'Maria_SC3_B253_B274',
    'all363_individual_five_gates_pass':'all359_individual_five_gates_pass',
    'scope=dict(source_variants=351,native_body_pages=353,typed_labels=12,observed_source_variants=252,':
        'scope=dict(source_variants=349,native_body_pages=350,typed_labels=10,observed_source_variants=164,',
    'observed_body_pages=254,observed_page_occurrences=273,offline_only_source_variants=99,':
        'observed_body_pages=165,observed_page_occurrences=165,offline_only_source_variants=185,',
    'actual_menu_cursor_states=[0,1,2],observed_menu_instances=9,observed_distinct_menu_objects=5,observed_choice_labels=12,offline_only_captions=0,physical_style_alternatives=85,observed_style_alternatives=10,offline_only_style_alternatives=75':
        'actual_menu_cursor_states=[0,1],observed_menu_instances=5,observed_distinct_menu_objects=5,observed_choice_labels=10,offline_only_captions=0,physical_style_alternatives=131,observed_style_alternatives=12,offline_only_style_alternatives=119',
    "'current_story_gameplay_utterances':252,'current_story_gameplay_pages':254":"'current_story_gameplay_utterances':164,'current_story_gameplay_pages':165",
    'qualified_scoped_names=29,scoped_FE_guard_reserves=3,additional_directly_viewed_page_repairs=1,pages_reclaimed=0,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=1,source_bound_layout_changes=15,observed_FE_blank_rows_repaired=1,proposed_revisions=202,justified_retentions=161,observed_current_batch_source_bodies=252,':
        'qualified_scoped_names=18,scoped_FE_guard_reserves=0,additional_directly_viewed_page_repairs=1,pages_reclaimed=1,owned_FE_padding_bytes_repaired=0,whole_exchange_retentions_reopened=0,source_bound_layout_changes=34,observed_FE_blank_rows_repaired=0,proposed_revisions=202,justified_retentions=161,observed_current_batch_source_bodies=164,',
    'current_batch_actual_gameplay_observations=252,current_batch_actual_gameplay_pages=254':'current_batch_actual_gameplay_observations=164,current_batch_actual_gameplay_pages=165',
    'Maria B216–B252 contextual town andguild quests,forest exchanges,source-faithful riddle instructions,wrapping,menus andscoped names integrated once over registered Maria321 B196-B215.':
        'Maria B253–B274 contextual town quests,scurvy medicine,jungle andforest exchanges,carronade research,wrapping,menus andscoped names integrated once over registered Maria363 B216-B252.',
    'editorial_review_current.Maria363_B216_B252_completion_v1.pending.json':'editorial_review_current.Maria359_B253_B274_completion_v1.pending.json',
    'Credit363 unique contextual reviews':'Credit359 unique contextual reviews',
    'Credited363 Maria reviews once;202 revisions/161 retentions;original source membership preserved.':'Credited359 Maria reviews once;219 revisions/140 retentions;original source membership preserved.',
    'final_cumulative_integration_complete=True,stored_andrepresentative_checks_pending=False':
        'current_English_not_read=False,contextual_comparison_pending=False,names_terms_consumers_pending=False,all_fifth_gates_pending=False,final_cumulative_integration_complete=True,stored_andrepresentative_checks_pending=False',
    "    assert not FINAL.exists() and not (ROOT/'completion_checkpoint.json').exists()":
        "    assert not FINAL.exists() and not (ROOT/'completion_checkpoint.json').exists()\n    delta_path=Path('work/Maria_B253_B274_clean_20261110/final_layout_delta_v1.json');delta=load(delta_path)\n    assert delta['final_changed_record_count']==34 and delta['pages_reclaimed']==1\n    for p,h in delta['evidence'].items():assert sha(Path(p).read_bytes())==h",
})
counts={'363':'359','202':'219','161':'140','722':'723','57':'58',
    '22707':'23070','23070':'23429','13778':'13997','9292':'9432','23073':'23432'}
pattern=re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source=pattern.sub(lambda m:counts[m[0]],source)

if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-credit-andexact-earlier-ledger-prefix-guards','exec'),globals())
