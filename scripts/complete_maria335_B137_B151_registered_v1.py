"""Credit335 disjoint source objects once after registered release andown startup."""
import re
from scripts.complete_maria337_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'Credit216 unique contextual reviews':'Credit335 unique contextual reviews',
    'work/maria337_release_v1':'work/maria335_B137_B151_release_v1',
    'maria337_integrated_final_review_v1.json':'maria335_B137_B151_integrated_final_review_v1.json',
    'Maria_SC3_B125_B136_contextual_integrated_20261109':'Maria_SC3_B137_B151_contextual_integrated_20261109',
    'Maria_SC3_B125_B136_clean_20261109':'Maria_SC3_B137_B151_clean_20261109',
    'all337_individual_five_gates_pass':'all335_individual_five_gates_pass',
    'scope=dict(source_variants=335,native_body_pages=339,typed_labels=2,observed_source_variants=48,':
        'scope=dict(source_variants=333,native_body_pages=333,typed_labels=2,observed_source_variants=44,',
    'observed_body_pages=52,offline_only_source_variants=287,':'observed_body_pages=44,offline_only_source_variants=289,',
    "'current_story_gameplay_utterances':48,'current_story_gameplay_pages':52":"'current_story_gameplay_utterances':44,'current_story_gameplay_pages':44",
    'qualified_scoped_names=21,tutorial_page_boundary_fixes=4,additional_phrase_wrap_fixes=8,pages_reclaimed=0,':
        'qualified_scoped_names=26,scoped_FE_guard_fixes=6,additional_phrase_wrap_fixes=4,pages_reclaimed=3,',
    'current_batch_actual_gameplay_observations=48,current_batch_actual_gameplay_pages=52':
        'current_batch_actual_gameplay_observations=44,current_batch_actual_gameplay_pages=44',
    'Maria B125–B136 contextual dialogue,tutorial wrapping,glyph fixes and two repaired captions integrated once over registered Maria330.':
        'Maria B137–B151 contextual dialogue,tutorial wrapping,glyph andFE guard fixes,andtwo reviewed captions integrated once over registered Maria337.',
    'editorial_review_current.Maria337_completion_v1.pending.json':'editorial_review_current.Maria335_B137_B151_completion_v1.pending.json',
    'Credited337 Maria reviews once;224 revisions/113 retentions;original source membership preserved.':
        'Credited335 Maria reviews once;185 revisions/150 retentions;original source membership preserved.',
})
counts={'337':'335','224':'185','113':'150','717':'718','52':'53','21019':'21356','21356':'21691',
    '12861':'13046','8495':'8645','21359':'21694'}
pattern=re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source=pattern.sub(lambda m:counts[m[0]],source)
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-credit-andearlier-ledger-prefix-preservation','exec'),globals())
