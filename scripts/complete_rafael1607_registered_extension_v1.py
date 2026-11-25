"""Credit the 183 exact records once after the registered patch and own startup."""
import re
from scripts.complete_rafael557_registered_extension_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    'Rafael1424_extended_release_verified_v2_20261105':'Rafael1607_extended_release_verified_v1_20261105',
    'rafael557_integrated_final_review_v1.json':'rafael_B177_B180_integrated_final_review_v1.json',
    'Rafael_SC0_B141_B160_contextual_integrated_20261105':'Rafael_SC0_B177_B180_contextual_integrated_20261105',
    'Rafael_SC0_B141_B160_clean_20261105':'Rafael_SC0_B177_B180_research_20261105',
    'Rafael1424_extended_release_verify_gc_v2_20261105':'Rafael1607_extended_release_verify_gc_v1_20261105',
    'Rafael1424_extended_startup_gc_v3_20261105':'Rafael1607_extended_startup_gc_v1_20261105',
    'Rafael1424_extended_Fernan_gc_v2_20261105':'Rafael1607_extended_Fernan_gc_v1_20261105',
    "==(682,114,26)":"==(683,114,26)",
    """        if row.get('FU_current_expansion_width_anddisplay_pending') is True:
            assert row['id'] in {'DK4_MES_B143_R0067','DK4_MES_B146_R0006'}
            assert row['actual_utterance_observed_in_disclosed_fixture'] and '{MACRO:FU}' in row['english']
            proof=load(conf['stored_native'])
            tested=next(r for r in proof['records'] if r['id']==row['id'])
            assert b'Rafael Castor' in bytes.fromhex(tested['expanded_hex'])
            assert tested['all_stored_planes_equal_directly_viewed_compiled_planes']
            row['FU_current_expansion_width_anddisplay_pending']=False""":
        """        if row['kind']=='typed-choice-label':
            proof=load(conf['stored_native'])
            tested=next(r for obj in proof['typed_objects'] for r in obj['label_references'] if r['id']==row['id'])
            assert row['actual_caption_default_cursor_state_observed']
            assert tested['offset']==bound['registered_reference']['offset'] and tested['stored_hex']==bound['registered_reference']['exact_stored_hex']
            row['complete_native_menu_binding_andformatting_pending']=False""",
    'source_variants=549,native_body_pages=558,typed_labels=8,observed_source_variants=188,':
        'source_variants=175,native_body_pages=186,typed_labels=8,observed_source_variants=104,',
    'observed_body_pages=193,offline_only_source_variants=361':'observed_body_pages=115,offline_only_source_variants=71',
    'editorial_review_current.Rafael557_completion_v1.pending.json':'editorial_review_current.Rafael1607_completion_v1.pending.json',
    "ledger['latest_checkpoint']='Rafael557 integrated once: 13269 complete, 7518 revisions and 5751 retentions. All 682 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue remaining Rafael and tutorial exchanges; main and full scope unchanged.'":
        "ledger['latest_checkpoint']='Rafael B177–B180 integrated once. All 683 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue the 67 clean-first B161–B165 drafts. Main and full scope preserved.'",
    'Credited 557 unique reviews once: 13269 complete, 7518 revisions and 5751 retentions. Main unchanged; full goal active.':
        'Credited 183 unique tutorial reviews once. Main preserved; full goal active.',
})
counts={'557':'183','235':'133','322':'50','12712':'13269','13269':'13452','7518':'7651','5751':'5801','13272':'13455'}
source=re.sub(r'(?<![A-Za-z0-9_])(?:557|235|322|12712|13269|7518|5751|13272)(?![0-9])',lambda m:counts[m[0]],source)
source=source.replace('all557_individual_five_gates_pass','all183_individual_five_gates_pass')
if __name__=='__main__':
    exec(compile(source,__file__+'::same-once-only-credit-with-exact-menu-receipts','exec'),globals())
