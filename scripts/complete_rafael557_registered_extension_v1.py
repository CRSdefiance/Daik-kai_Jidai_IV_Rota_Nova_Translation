"""Credit the 557 unique reviewed records only after exact patch and own startup."""
from pathlib import Path
import re
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE=Path('scripts/complete_rafael351_registered_extension_v2.py')
source=checked_text(TEMPLATE.read_text(encoding='utf-8'),{
    'Rafael867_extended_release_verified_v3_20261105':'Rafael1424_extended_release_verified_v2_20261105',
    'rafael351_integrated_final_review_v2.json':'rafael557_integrated_final_review_v1.json',
    'Rafael_SC0_B121_B140_contextual_integrated_20261105':'Rafael_SC0_B141_B160_contextual_integrated_20261105',
    'Rafael_SC0_B121_B140_clean_20261105':'Rafael_SC0_B141_B160_clean_20261105',
    'Rafael867_extended_release_verify_gc_v3_20261105':'Rafael1424_extended_release_verify_gc_v2_20261105',
    'Rafael867_extended_startup_gc_v3_20261105':'Rafael1424_extended_startup_gc_v3_20261105',
    'Rafael867_extended_Fernan_gc_v3_20261105':'Rafael1424_extended_Fernan_gc_v2_20261105',
    "    assert (release['complete_stack_entries'],release['accepted_layers'],release['passing_release_checks'])==(681,114,26)":
        "    assert (release['complete_stack_entries'],release['accepted_layers'],release['passing_release_checks'])==(682,114,26)",
    "        assert not any(v is True and 'pending' in k for k,v in row.items() if k!='registered_release_andcompletion_credit_pending')":
        """        if row.get('FU_current_expansion_width_anddisplay_pending') is True:
            assert row['id'] in {'DK4_MES_B143_R0067','DK4_MES_B146_R0006'}
            assert row['actual_utterance_observed_in_disclosed_fixture'] and '{MACRO:FU}' in row['english']
            proof=load(conf['stored_native'])
            tested=next(r for r in proof['records'] if r['id']==row['id'])
            assert b'Rafael Castor' in bytes.fromhex(tested['expanded_hex'])
            assert tested['all_stored_planes_equal_directly_viewed_compiled_planes']
            row['FU_current_expansion_width_anddisplay_pending']=False
        assert not any(v is True and 'pending' in k for k,v in row.items() if k!='registered_release_andcompletion_credit_pending')""",
    'source_variants=341,native_body_pages=344,typed_labels=10,observed_source_variants=132,':'source_variants=549,native_body_pages=558,typed_labels=8,observed_source_variants=188,',
    'observed_body_pages=134,offline_only_source_variants=209':'observed_body_pages=193,offline_only_source_variants=361',
    """    combined='Rafael867_qualified_cumulative_research_20261105'
    ledger[combined]={**prior[combined],**completed,'new_credit':0,'remaining_new_source_credit':0,
        'registered_integration_andclean_input_patch_pending':False,'all867_registered_andcredited_in_two_disjoint_families':True}
""":"",
    "BATCH,FAMILY,combined,'current_integrated_candidate'":"BATCH,FAMILY,'current_integrated_candidate'",
    "ledger['latest_checkpoint']='Rafael351 integrated once after516:12712 complete/7283 revisions/5429 retentions;681 entries/114 accepted layers/eight stages/exact clean patch/own startup/Fernan getters pass. All867 research reviews are integrated. Continue Rafael early story/tutorial priority;main/full scope unchanged.'":
        "ledger['latest_checkpoint']='Rafael557 integrated once: 13269 complete, 7518 revisions and 5751 retentions. All 682 entries, 114 accepted layers, eight final stages, exact patch and own startup pass. Continue remaining Rafael and tutorial exchanges; main and full scope unchanged.'",
    'editorial_review_current.Rafael351_completion_v2.pending.json':'editorial_review_current.Rafael557_completion_v1.pending.json',
    "Credited351 unique source reviews once:12712 complete/7283 revisions/5429 retentions. All867 nowintegrated;main unchanged/full goal active.":
        "Credited 557 unique reviews once: 13269 complete, 7518 revisions and 5751 retentions. Main unchanged; full goal active.",
})
counts={'351':'557','201':'235','150':'322','12361':'12712','12712':'13269','7283':'7518','5429':'5751','12715':'13272'}
source=re.sub(r'(?<![A-Za-z0-9_])(?:351|201|150|12361|12712|7283|5429|12715)(?![0-9])',lambda m:counts[m[0]],source)
source=source.replace('all351_individual_five_gates_pass','all557_individual_five_gates_pass')
if __name__=='__main__':exec(compile(source,__file__+'::same-atomic-credit-with-two-qualified-FU-flags','exec'),globals())
