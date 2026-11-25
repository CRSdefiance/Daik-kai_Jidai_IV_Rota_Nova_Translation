"""Add the missing individual info reasons; retain all exact compiled/native results."""
from copy import deepcopy
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_confrontation_row_reasons_v7801b')
PLAN=Path('work/analysis/maria_confrontation_wrap_v7799/16_plans_one_sentence_coherence_refinement_no_prose_change.json')
FONT=Path('work/analysis/maria_confrontation_final_pages_v7800/16_final_compiled_pages4_fresh60_exact_reused_alignments.json')
NEW_PLAN=ROOT/'16_full_width_plans_nine_individual_row_reasons.json'
NEW_FONT=ROOT/'16_native_pages_exact_with_nine_individual_row_reasons.json'
REASONS={
    16:"The retained polite interruption and questioning admiral/name fit one English row. The source's staging break is not needed for meaning, voice or identity.",
    19:"Lil's startled question, complete acknowledgement and identity demand fit two ordinary English rows. Preserve the three speech acts and stammer, rather than the Japanese three-row staging.",
    23:"The complete company/name introduction and recognition challenge fit two English rows using the measured FO7/FI5 expansions. Source FO before FI remains exact; two natural clauses add no rank.",
    27:"The retained startled FI recognition and personal-arrival question fit a single full-width English row with measured FI5. Punctuation conveys the surprise without copying Japanese staging breaks.",
    31:"The retained sudden alarm and fear of being killed form a complete single-row question. Lil's suspicion remains attributed and is denied by the following Maria line.",
    34:"Maria's denial, tentative inference, explicit purpose and manipulation warning fit three English rows. All four ideas remain; ordinary wrapping replaces the four Japanese source rows.",
    37:"The complete defense preserves the attempted rescue, the people of Southeast Asia and praise of Kuhn as a merchant. Four native rows retain every word. A scoped ordinary soft-wrap preference keeps the short final sentence He's a great merchant! together; no narrower viewport or authored break is used.",
    52:"The frustrated question, life warning and remaining opportunity fit two English rows. Do not retain three Japanese staging rows or add an escape plan, deadline or guaranteed outcome.",
    56:"Lil's refusal to believe the abrupt allegation and dismissive snort fit two English rows. The idiomatic spring that on me preserves the sudden-claim meaning without literal person-location invention.",
}
if __name__=='__main__':
    assert not ROOT.exists();plan,font=map(read,[PLAN,FONT]);assert font['plan_sha256']==sha(PLAN.read_bytes())
    annotated=deepcopy(plan);infos=[]
    for row in annotated['records']:
        found=any(i['code']=='line-break-count' for i in row['base_QA']['issues'])
        if found:
            assert row['source_record_index'] in REASONS
            row['previous_row_count_reason']=row.get('row_count_reason')
            row['row_count_reason']=REASONS[row['source_record_index']]
            infos.append(row['source_record_index'])
    assert set(infos)==set(REASONS) and len(infos)==9
    assert [r['encoded_hex'] for r in annotated['records']]==[r['encoded_hex'] for r in plan['records']]
    assert [r['base_QA'] for r in annotated['records']]==[r['base_QA'] for r in plan['records']]
    ROOT.mkdir(parents=True)
    annotated.update(previous_plan=str(PLAN),previous_plan_sha256=sha(PLAN.read_bytes()),
        nine_exact_informational_row_count_reasons_now_explicit=True,no_prose_compiled_QA_orpixel_changes=True)
    save(NEW_PLAN,annotated)
    bound=deepcopy(font);bound.update(plan=str(NEW_PLAN),plan_sha256=sha(NEW_PLAN.read_bytes()),
        previous_native_proof=str(FONT),previous_native_proof_sha256=sha(FONT.read_bytes()),
        all16_native_rows_byte_exact_no_checks_replayed=True,
        original_7801_reason_assertion_failure_preserved_not_ROM_orfont_failure=True)
    assert bound['records']==font['records'];save(NEW_FONT,bound)
    derivative=derive('scripts/record_Maria_confrontation_native_view_v7801.py','scripts/record_Maria_confrontation_native_view_v7801b.py',{
        'maria_confrontation_native_view_v7801':'maria_confrontation_native_view_v7801b',
        str(PLAN).replace('\\','/'):str(NEW_PLAN).replace('\\','/'),
        str(FONT).replace('\\','/'):str(NEW_FONT).replace('\\','/'),
    })
    save(ROOT/'binding_receipt.json',dict(previous_plan=str(PLAN),previous_plan_sha256=sha(PLAN.read_bytes()),
        annotated_plan=str(NEW_PLAN),annotated_plan_sha256=sha(NEW_PLAN.read_bytes()),
        previous_native_proof=str(FONT),previous_native_proof_sha256=sha(FONT.read_bytes()),
        rebound_native_proof=str(NEW_FONT),rebound_native_proof_sha256=sha(NEW_FONT.read_bytes()),
        individual_source_bound_info_reasons=REASONS,all_original_compiled_body_lineplan_QA_andnative_pixels_exact=True,
        native_renders_oralignments_replayed=0,view_derivation=derivative,no_ROM_ledger_orcredit_change=True,full_goal_complete=False))
    print('Nine individual informational row-count reasons bound;all16 prose/compiled/QA/native rows exact.No native checks replayed.')
