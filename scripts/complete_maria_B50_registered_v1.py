"""Add 16 source reviews once, preserving both registered panels under the one FE owner."""
import re
from scripts.complete_maria270_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'work/maria270_release_v1':'work/maria_B50_release_v1',
    'maria270_integrated_final_review_v1.json':'maria_B50_integrated_final_review_v1.json',
    'Maria_SC3_B37_B49_contextual_integrated_20261109':'Maria_SC3_B50_contextual_integrated_20261109',
    'Maria_SC3_B37_B49_display_20261109':'Maria_SC3_B50_FE_research_20261109',
    'all270_individual_five_gates_pass':'all16_individual_five_gates_pass',
    'actual_menu_cursor_states=[0],observed_menu_instances=2,observed_choice_labels=4':'actual_menu_cursor_states=[],observed_menu_instances=0,observed_choice_labels=0',
    'typed_labels=4':'typed_labels=0','justified_layout_retentions=6':'justified_layout_retentions=0,FE_blank_row_repairs=1,FE_pagination_owners=1,additional_native_FE_commands=1',
    "        assert len(row['review'])==5 and all(row['review'].values())":
        """        assert len(row['review'])==5 and all(row['review'].values())
        native_refs=bound['registered_native_pages']
        assert native_refs==row.get('planned_integrated_native_pages',[row['planned_integrated_reference']])
        assert len(native_refs)==(2 if row['id']=='DK4_MES_B50_R0043' else 1)""",
    'Maria B37–B49 contextual dialogue integrated once over the registered market-corrected cumulative release.':
        'Maria B50 contextual dialogue integrated once over the registered Maria270 cumulative release with exact-source FE continuation.',
    'editorial_review_current.Maria270_completion_v1.pending.json':'editorial_review_current.Maria_B50_completion_v1.pending.json',
    'Credited270 Maria reviews once;complete B50 remains active anduncredited.':'Credited16 B50 reviews once;17 physical panels are not17 source credits.',
})
counts={'270':'16','161':'9','109':'7','19462':'19732','19732':'19748','11871':'11880','7861':'7868','19735':'19751',
    '266':'16','272':'17','63':'16','69':'17','203':'0','711':'712','46':'47','28':'4','26':'2'}
pattern=re.compile(r'(?<![A-Za-z0-9_])(?:'+'|'.join(sorted(counts,key=len,reverse=True))+r')(?![A-Za-z0-9_])')
source=pattern.sub(lambda m:counts[m[0]],source)
if __name__=='__main__':exec(compile(source,__file__+'::same-once-only-credit-andearlier-ledger-prefix-preservation-two-native-refs','exec'),globals())
