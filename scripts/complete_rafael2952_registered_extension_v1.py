"""Credit the 403 exact Rafael records once after final release and startup proofs."""
import re

from scripts.complete_rafael2549_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source=checked_text(previous,{
    'Rafael2549_extended_release_verified_v1_20261106':'Rafael2952_extended_release_verified_v1_20261106',
    'rafael_B181_B200_integrated_final_review_v1.json':'rafael_B201_B220_integrated_final_review_v1.json',
    'Rafael_SC0_B181_B200_contextual_integrated_20261106':'Rafael_SC0_B201_B220_contextual_integrated_20261106',
    'Rafael_SC0_B181_B200_research_20261106':'Rafael_SC0_B201_B220_clean_20261106',
    'Rafael2549_extended_release_verify_gc_v1_20261106':'Rafael2952_extended_release_verify_gc_v1_20261106',
    'Rafael2549_extended_startup_gc_v1_20261106':'Rafael2952_extended_startup_gc_v1_20261106',
    'Rafael2549_extended_Fernan_gc_v1_20261106':'Rafael2952_extended_Fernan_gc_v1_20261106',
    '==(688,114,26)':'==(689,114,26)',
    'all384_individual_five_gates_pass':'all403_individual_five_gates_pass',
    "{'progressive', 'system-FE'}":"{'progressive', 'system-FE', 'typed-choice-label'}",
    "scope=dict(source_variants=384,native_body_pages=384,typed_labels=0,observed_source_variants=148,\n        observed_body_pages=148,offline_only_source_variants=236,actual_review=conf['actual'],":
        "scope=dict(source_variants=382,native_body_pages=383,typed_labels=21,observed_source_variants=173,\n"
        "        observed_body_pages=174,offline_only_source_variants=209,actual_review=conf['actual'],",
    'actual_menu_cursor_states=[],\n        no_typed_menus_in_scope=True,original_story_branches_and_event_outcomes_unvisited=True,':
        "actual_menu_cursor_states=[0],observed_menu_instances=6,observed_choice_labels=13,offline_only_captions=8,\n"
        "        original_story_branches_and_event_outcomes_unvisited=True,",
    "ledger[BATCH]={**prior[BATCH],**completed,'new_credit':384":
        "ledger[BATCH]={**prior[BATCH],**completed,'full_intake_not_complete':False,'new_credit':384",
    'editorial_review_current.Rafael2549_completion_v1.pending.json':'editorial_review_current.Rafael2952_completion_v1.pending.json',
    'Rafael B181–B200 integrated once. All 688 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue the B201–B220 clean intake. Main and full scope preserved.':
        'Rafael B201–B220 integrated once. All 689 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue with the next complete Rafael exchanges.',
    'Credited 384 Rafael B181–B200 reviews once. Main preserved and full goal active.':
        'Credited 403 Rafael B201–B220 reviews once.',
})
counts={'384':'403','317':'299','67':'104','14010':'14394','14394':'14797',
    '8407':'8706','5987':'6091','14397':'14800'}
source=re.sub(r'(?<![A-Za-z0-9_])(?:384|317|67|14010|14394|8407|5987|14397)(?![0-9])',
    lambda match:counts[match[0]],source)
if __name__=='__main__':
    exec(compile(source,__file__+'::same-once-only-credit-with-exact-observed-mixed-menu-scope','exec'),globals())

