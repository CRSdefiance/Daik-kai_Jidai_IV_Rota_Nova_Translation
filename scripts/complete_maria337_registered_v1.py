"""Credit337 disjoint source objects once, preserving every earlier review and release."""
import re
from scripts.complete_maria330_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/maria330_release_v1':'work/maria337_release_v1','maria330_integrated_final_review_v1.json':'maria337_integrated_final_review_v1.json',
    'Maria_SC3_B96_B124_contextual_integrated_20261109':'Maria_SC3_B125_B136_contextual_integrated_20261109',
    'Maria_SC3_B96_B124_clean_20261109':'Maria_SC3_B125_B136_clean_20261109','all330_individual_five_gates_pass':'all337_individual_five_gates_pass',
    "row['id'] in {'DK4_MES_B116_R0041','DK4_MES_B116_R0051'}":"False",
    'scope=dict(source_variants=328,native_body_pages=338,typed_labels=2,observed_source_variants=53,':'scope=dict(source_variants=335,native_body_pages=339,typed_labels=2,observed_source_variants=48,',
    'observed_body_pages=58,offline_only_source_variants=275,':'observed_body_pages=52,offline_only_source_variants=287,',
    "'current_story_gameplay_utterances':53,'current_story_gameplay_pages':58":"'current_story_gameplay_utterances':48,'current_story_gameplay_pages':52",
    'qualified_scoped_names=26,closing_clause_boundary_fixes=7,orphan_See_repaired=True,pages_reclaimed=3,FE_pagination_owners=2,additional_native_FE_commands=2,':
        'qualified_scoped_names=21,tutorial_page_boundary_fixes=4,additional_phrase_wrap_fixes=8,pages_reclaimed=0,FE_pagination_owners=0,additional_native_FE_commands=0,',
    'current_batch_actual_gameplay_observations=53,current_batch_actual_gameplay_pages=58':'current_batch_actual_gameplay_observations=48,current_batch_actual_gameplay_pages=52',
    'Maria B96–B124 contextual dialogue,menu,styles andtwo source-owned FE continuations integrated once over registered Maria328.':
        'Maria B125–B136 contextual dialogue,tutorial wrapping,glyph fixes and two repaired captions integrated once over registered Maria330.',
    'editorial_review_current.Maria330_completion_v1.pending.json':'editorial_review_current.Maria337_completion_v1.pending.json',
    'Credited330 Maria reviews once;249 revisions/81 retentions;FE children do not duplicate source credit.':'Credited337 Maria reviews once;224 revisions/113 retentions;original source membership preserved.',
})
counts={'330':'337','249':'224','81':'113','716':'717','51':'52','20689':'21019','21019':'21356','12637':'12861','8382':'8495','21022':'21359'}
pattern=re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source=pattern.sub(lambda m:counts[m[0]],source)
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-credit-andfull-earlier-ledger-prefix-preservation','exec'),globals())
