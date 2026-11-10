"""Record direct review of every English sheet, retaining pending storage/gameplay gates."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_native_view_v8805')
PAGES=Path('work/analysis/Hodram_B54_B60_pages_v8804/compiled_native_pages.json')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v1.json')
NOTES={
 'DK4_MES_B54_R0014':'Two rows keep good luck together. The complete short sentence and chuckle remain one natural exchange; the shorter first row follows the conversational Well pause.',
 'DK4_MES_B55_R0006':'Four rows keep the military man, right? question tag together and retain the complete Veracruz guild message. This is a reviewed coherent-unit break at the original full width, not a copied Japanese break or a global width reduction.',
 'DK4_MES_B56_R0010':'The complete Foreign Girl caption and silence fit the distinct FE panel. The source FE null actor remains separate from ordinary speaker labels; no actor254 nameplate is invented.',
 'DK4_MES_B58_R0105':'Three rows retain the hesitant accusation, high price and destination in his country. No completed sale or homecoming is asserted. Simple fragments preserve language learning respectfully.',
 'DK4_MES_B58_R0120':'Three rows retain younger brother, companions, all killed and the repeated accusation. The ordinary complete-word boundary between others and with me does not alter the group reference or omit a glyph.',
 'DK4_MES_B58_R0239':'Three rows keep the tentative Iceland question whole. The clue and question remain legible; no fixed row count or maximum fill is imposed, and no destination is confirmed.',
 'DK4_MES_B59_R0023':'Two complete pages distinguish the fragment from the Proof. Fresh refined rendering keeps We\'d been praying together before the page transition; the second page starts the dependent clause with its native one-cell guard. The last hands... remains complete.',
 'DK4_MES_B59_R0026':'Two pages preserve the urgent wish and peace and prosperity. The second page continues bring peace and prosperity without an invented sentence or shortened facts. Native guard is visible before peace, with complete first and last characters.',
 'DK4_MES_B60_R0012':'Two pages preserve Sao Jorge, carpenter, Portuguese fleet, India, circulating illness and departure. The continuation with an illness follows came down naturally; its native guard does not drop the initial w.',
 'DK4_MES_B60_R0019':'All four rows preserve reported Portuguese mistreatment and care as if family. Complete-word sick/person and They/cared boundaries are readable in context and retain all words; these do not waive glyph, bounds or pagination checks.',
}

if __name__=='__main__':
    assert not ROOT.exists();pages,doc=map(read,[PAGES,DOC]);planpath=Path(pages['plan']);plan=read(planpath)
    assert pages['manuscript_sha256']==plan['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(doc['records'])==len(plan['records'])==len(pages['records'])==82 and len(pages['review_sheets'])==11 and pages['complete_native_English_pages']==85
    assert doc['revised']==46 and doc['retained']==36 and doc['source_macro_counts']==dict(FI=3,FA=4,FO=0)
    viewed=[]
    for s in pages['review_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256'];viewed.append(s)
    rows=[];boundaries=0
    for row,p,r in zip(doc['records'],plan['records'],pages['records'],strict=True):
        assert row['id']==p['id']==r['id'] and row['source_reference']==r['source_reference'] and row['current_reference']==r['current_reference']
        assert row['english']==r['logical_English']==p['logical_English'] and p['encoded_hex']==r['compiled_hex']
        assert not row['review']['formatting'] and all(row['review'][g] for g in ['source','context','localization','naturalness'])
        assert ' '.join(p['lines'])==row['english'] and not any(i['severity'] in ['warning','error'] for i in p['base_QA']['issues'])
        assert len(r['native_alignment']['cases'])==4 and all(c['output_hex']==r['expanded_native_hex'] for c in r['native_alignment']['cases'])
        note=NOTES.get(row['id'],'Every complete native row and its ordinary whole-word boundaries were viewed with this full exchange. All original words, punctuation, source substitutions, first/internal/final characters and source-bound reactions remain. No authored wrap, padding, font change or fit-driven prose shortening is approved.')
        boundaries+=len(p['automatic_boundaries'])
        rows.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],decision=row['decision'],
            retention_reason=row['retention_reason'],finding=row['finding'],logical_English=row['english'],compiled_hex=p['encoded_hex'],
            generated_lines=p['lines'],automatic_boundaries=p['automatic_boundaries'],native_pages=p['expected_native_pages'],wrap_review=note,
            all_native_page_previews_directly_viewed=True,original_QA_issues=p['base_QA']['issues'],formatting_gate_still_false_pending_stored_andactual=True))
    ROOT.mkdir(parents=True)
    save(ROOT/'all82_native_English_direct_view_andboundary_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),plan=str(planpath),plan_sha256=sha(planpath.read_bytes()),
        native_pages=str(PAGES),native_pages_sha256=sha(PAGES.read_bytes()),records=rows,viewed_sheets=viewed,all11_sheets85pages82utterances_directly_viewed=True,
        all_generated_word_boundaries_reviewed=boundaries,revisions=46,justified_retentions=36,
        three_two_page_records_andFE_panel_reviewed_withnative_metrics=True,all_complete_glyphs_bounds_pagination_anddefault_substitutions_pass=True,
        actual_gameplay_new_runs=0,no_new_natural_activation_orfullroute_claim=True,
        preserve_8802_syntax_failure_8803_page_origin_failure_andall_prior_outputs=True,
        Geronimo_Alonso_shared_de_field_fullname_consumers_anddeployment_still_open=True,
        stored_complete_controls_relocation_inverses_independentreferences_actual_policy_atomic_registeredintegration_pending=True,
        all82_formatting_gates_remain_false=True,new_credit=0,no_ROM_registry_orcompleted_ledger_change=True,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,planpath,PAGES,Path(__file__)]}))
    print('Direct view recorded:82 utterances/85 pages/11 sheets;',boundaries,'automatic word boundaries reviewed;46 revisions/36 retentions;storage/actual/release pending.')
