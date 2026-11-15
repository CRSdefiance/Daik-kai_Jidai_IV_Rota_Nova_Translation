"""Credit328 disjoint source objects once, preserving both registered FE child references."""
import re
from scripts.complete_maria303_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'work/maria303_release_v1':'work/maria328_release_v1',
    'maria303_integrated_final_review_v1.json':'maria328_integrated_final_review_v1.json',
    'Maria_SC3_B58_B70_contextual_integrated_20261109':'Maria_SC3_B73_B95_contextual_integrated_20261109',
    'Maria_SC3_B58_B70_clean_20261109':'Maria_SC3_B73_B95_clean_20261109',
    'all303_individual_five_gates_pass':'all328_individual_five_gates_pass',
    "        assert len(row['review'])==5 and all(row['review'].values())":
        """        assert len(row['review'])==5 and all(row['review'].values())
        native_refs=bound['registered_native_pages']
        assert native_refs==row.get('planned_integrated_native_pages',[row['planned_integrated_reference']])
        assert len(native_refs)==(2 if row['id']=='DK4_MES_B87_R0139' else 1)
        row['registered_native_pages']=native_refs""",
    'scope=dict(source_variants=299,native_body_pages=299,typed_labels=4,observed_source_variants=116,':
        'scope=dict(source_variants=313,native_body_pages=321,typed_labels=15,observed_source_variants=43,',
    'observed_body_pages=116,offline_only_source_variants=183,':'observed_body_pages=48,offline_only_source_variants=270,',
    'observed_menu_instances=2,observed_choice_labels=4,offline_only_captions=0':'observed_menu_instances=2,observed_choice_labels=6,offline_only_captions=9',
    "'current_story_gameplay_utterances':116,'current_story_gameplay_pages':116":"'current_story_gameplay_utterances':43,'current_story_gameplay_pages':48",
    'qualified_scoped_names=20,wrap_improvements=7,justified_layout_retentions=4,':
        'qualified_scoped_names=24,wrap_improvements=12,justified_layout_retentions=1,FE_pagination_owners=1,additional_native_FE_commands=1,',
    'current_batch_actual_gameplay_observations=116,current_batch_actual_gameplay_pages=116':
        'current_batch_actual_gameplay_observations=43,current_batch_actual_gameplay_pages=48',
    'Maria B58–B70 contextual dialogue andmenus integrated once over the registered cumulative Maria310 release.':
        'Maria B73–B95 contextual dialogue,menus,styles andsource-owned FE continuation integrated once over registered Maria303.',
    'editorial_review_current.Maria303_completion_v1.pending.json':'editorial_review_current.Maria328_completion_v1.pending.json',
    'Credited303 Maria reviews once;181 revisions/122 retentions.':'Credited328 Maria reviews once;143 revisions/185 retentions;FE children do not duplicate source credit.',
})
counts={'303':'328','181':'143','122':'185','714':'715','49':'50','20058':'20361','20361':'20689',
    '12245':'12388','8116':'8301','20364':'20692'}
pattern=re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source=pattern.sub(lambda m:counts[m[0]],source)
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-credit-andfull-earlier-ledger-prefix-preservation','exec'),globals())
