"""Credit the 67 exact source records once after their patch and own startup."""
import re

from scripts.complete_rafael1607_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous, {
    'Rafael1607_extended_release_verified_v1_20261105': 'Rafael1674_extended_release_verified_v1_20261105',
    'rafael_B177_B180_integrated_final_review_v1.json': 'rafael_B161_B165_integrated_final_review_v1.json',
    'Rafael_SC0_B177_B180_contextual_integrated_20261105': 'Rafael_SC0_B161_B165_contextual_integrated_20261105',
    'Rafael_SC0_B177_B180_research_20261105': 'Rafael_SC0_B161_B165_research_20261105',
    'Rafael1607_extended_release_verify_gc_v1_20261105': 'Rafael1674_extended_release_verify_gc_v1_20261105',
    'Rafael1607_extended_startup_gc_v1_20261105': 'Rafael1674_extended_startup_gc_v1_20261105',
    'Rafael1607_extended_Fernan_gc_v1_20261105': 'Rafael1674_extended_Fernan_gc_v1_20261105',
    '==(683,114,26)': '==(684,114,26)',
    """        if row['kind']=='typed-choice-label':
            proof=load(conf['stored_native'])
            tested=next(r for obj in proof['typed_objects'] for r in obj['label_references'] if r['id']==row['id'])
            assert row['actual_caption_default_cursor_state_observed']
            assert tested['offset']==bound['registered_reference']['offset'] and tested['stored_hex']==bound['registered_reference']['exact_stored_hex']
            row['complete_native_menu_binding_andformatting_pending']=False""":
        """        assert row['kind'] in {'progressive', 'system-FE'}""",
    'registered_release_andcompletion_credit_pending': 'registered_release_and_completion_credit_pending',
    'source_variants=175,native_body_pages=186,typed_labels=8,observed_source_variants=104,':
        'source_variants=67,native_body_pages=68,typed_labels=0,observed_source_variants=55,',
    'observed_body_pages=115,offline_only_source_variants=71':
        'observed_body_pages=56,offline_only_source_variants=12',
    'actual_menu_cursor_states=[0]': 'actual_menu_cursor_states=[]',
    'other_menu_states_returns_branches_andcancellation_offline_only=True,':
        'no_typed_menus_in_scope=True,original_story_branches_and_event_outcomes_unvisited=True,',
    'editorial_review_current.Rafael1607_completion_v1.pending.json':
        'editorial_review_current.Rafael1674_completion_v1.pending.json',
    "ledger['latest_checkpoint']='Rafael B177–B180 integrated once. All 683 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue the 67 clean-first B161–B165 drafts. Main and full scope preserved.'":
        "ledger['latest_checkpoint']='Rafael B161–B165 integrated once. All 684 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue the complete clean-first B166 and B167 drafts. Main and full scope preserved.'",
    'Credited 183 unique tutorial reviews once. Main preserved; full goal active.':
        'Credited 67 Rafael B161–B165 reviews once. Main preserved and full goal active.',
})
counts = {'183':'67','133':'51','50':'16','13269':'13452','13452':'13519','7651':'7702','5801':'5817','13455':'13522'}
source = re.sub(r'(?<![A-Za-z0-9_])(?:183|133|50|13269|13452|7651|5801|13455)(?![0-9])', lambda m: counts[m[0]], source)
source = source.replace('all183_individual_five_gates_pass', 'all67_individual_five_gates_pass')
if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-once-only-credit-for-the-five-speech-blocks', 'exec'), globals())
