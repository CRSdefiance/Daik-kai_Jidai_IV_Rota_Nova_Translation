"""Credit330 disjoint original objects once; preserve both FE child pairs."""
import re
from scripts.complete_maria328_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/maria328_release_v1':'work/maria330_release_v1','maria328_integrated_final_review_v1.json':'maria330_integrated_final_review_v1.json',
    'Maria_SC3_B73_B95_contextual_integrated_20261109':'Maria_SC3_B96_B124_contextual_integrated_20261109',
    'Maria_SC3_B73_B95_clean_20261109':'Maria_SC3_B96_B124_clean_20261109','all328_individual_five_gates_pass':'all330_individual_five_gates_pass',
    "row['id']=='DK4_MES_B87_R0139'":"row['id'] in {'DK4_MES_B116_R0041','DK4_MES_B116_R0051'}",
    'scope=dict(source_variants=313,native_body_pages=321,typed_labels=15,observed_source_variants=43,':'scope=dict(source_variants=328,native_body_pages=338,typed_labels=2,observed_source_variants=53,',
    'observed_body_pages=48,offline_only_source_variants=270,':'observed_body_pages=58,offline_only_source_variants=275,',
    'actual_menu_cursor_states=[0],observed_menu_instances=2,observed_choice_labels=6,offline_only_captions=9':'actual_menu_cursor_states=[0,1],observed_menu_instances=1,observed_choice_labels=2,offline_only_captions=0',
    "'current_story_gameplay_utterances':43,'current_story_gameplay_pages':48":"'current_story_gameplay_utterances':53,'current_story_gameplay_pages':58",
    'qualified_scoped_names=24,wrap_improvements=12,justified_layout_retentions=1,FE_pagination_owners=1,additional_native_FE_commands=1,':
        'qualified_scoped_names=26,closing_clause_boundary_fixes=7,orphan_See_repaired=True,pages_reclaimed=3,FE_pagination_owners=2,additional_native_FE_commands=2,',
    'current_batch_actual_gameplay_observations=43,current_batch_actual_gameplay_pages=48':'current_batch_actual_gameplay_observations=53,current_batch_actual_gameplay_pages=58',
    'Maria B73–B95 contextual dialogue,menus,styles andsource-owned FE continuation integrated once over registered Maria303.':'Maria B96–B124 contextual dialogue,menu,styles andtwo source-owned FE continuations integrated once over registered Maria328.',
    'editorial_review_current.Maria328_completion_v1.pending.json':'editorial_review_current.Maria330_completion_v1.pending.json',
    'Credited328 Maria reviews once;143 revisions/185 retentions;FE children do not duplicate source credit.':'Credited330 Maria reviews once;249 revisions/81 retentions;FE children do not duplicate source credit.',
})
counts={'328':'330','143':'249','185':'81','715':'716','50':'51','20361':'20689','20689':'21019','12388':'12637','8301':'8382','20692':'21022'}
pattern=re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source=pattern.sub(lambda m:counts[m[0]],source)
# The source-variant scope was already updated before numeric source-credit substitution.
source=checked_text(source,{'source_variants=330,native_body_pages=338':'source_variants=328,native_body_pages=338'}) if 'source_variants=330,native_body_pages=338' in source else source
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-ledger-credit-andall-prior-prefix-guards','exec'),globals())
