"""Credit390 disjoint original objects once after registration andown startup."""
import re
from scripts.complete_maria335_B137_B151_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'Credit335 unique contextual reviews':'Credit390 unique contextual reviews',
    'work/maria335_B137_B151_release_v1':'work/maria390_B152_B175_release_v1',
    'maria335_B137_B151_integrated_final_review_v1.json':'maria390_B152_B175_integrated_final_review_v1.json',
    'Maria_SC3_B137_B151_contextual_integrated_20261109':'Maria_SC3_B152_B175_contextual_integrated_20261110',
    'Maria_SC3_B137_B151_clean_20261109':'Maria_SC3_B152_B175_clean_20261109',
    'all335_individual_five_gates_pass':'all390_individual_five_gates_pass',
    'scope=dict(source_variants=333,native_body_pages=333,typed_labels=2,observed_source_variants=44,':
        'scope=dict(source_variants=373,native_body_pages=373,typed_labels=17,observed_source_variants=83,',
    'observed_body_pages=44,offline_only_source_variants=289,':'observed_body_pages=83,offline_only_source_variants=290,',
    'actual_menu_cursor_states=[0,1],observed_menu_instances=1,observed_choice_labels=2,offline_only_captions=0':
        'actual_menu_cursor_states=[0,1,2],observed_menu_instances=2,observed_choice_labels=5,offline_only_captions=12',
    "'current_story_gameplay_utterances':44,'current_story_gameplay_pages':44":"'current_story_gameplay_utterances':83,'current_story_gameplay_pages':83",
    'qualified_scoped_names=26,scoped_FE_guard_fixes=6,additional_phrase_wrap_fixes=4,pages_reclaimed=3,':
        'qualified_scoped_names=47,scoped_FE_guard_reserves=8,additional_phrase_wrap_fixes=11,pages_reclaimed=1,owned_FE_padding_bytes_repaired=1,whole_exchange_retentions_reopened=1,proposed_revisions=154,justified_retentions=236,observed_current_batch_source_bodies=83,',
    'current_batch_actual_gameplay_observations=44,current_batch_actual_gameplay_pages=44':
        'current_batch_actual_gameplay_observations=83,current_batch_actual_gameplay_pages=83',
    "row.update(planned_integrated_reference=bound['registered_reference'],registered_integration_pending=False,":
        "row.update(no_proposal_may_ship_orreceive_completion_credit_yet=False,planned_integrated_reference=bound['registered_reference'],registered_integration_pending=False,",
    'Maria B137–B151 contextual dialogue,tutorial wrapping,glyph andFE guard fixes,andtwo reviewed captions integrated once over registered Maria337.':
        'Maria B152–B175 contextual town/random dialogue,source-faithful wine reply,wrapping,menus andowned FE padding repair integrated once over registered Maria335 B137-B151.',
    'editorial_review_current.Maria335_B137_B151_completion_v1.pending.json':'editorial_review_current.Maria390_B152_B175_completion_v1.pending.json',
    'Credited335 Maria reviews once;185 revisions/150 retentions;original source membership preserved.':
        'Credited390 Maria reviews once;154 revisions/236 retentions;original source membership preserved.',
})
counts={'335':'390','185':'154','150':'236','718':'719','53':'54','21356':'21691','21691':'22081',
    '13046':'13200','8645':'8881','21694':'22084'}
pattern=re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source=pattern.sub(lambda m:counts[m[0]],source)
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-source-credit-andcomplete-earlier-ledger-prefix-guards','exec'),globals())
