"""Record viewed complete English pages; keep formatting approval pending storage/gameplay."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B31_B53_native_review_v8727')
OLD=Path('translations/hodram_B31_B53_editorial_manuscript_v1.json')
DOC=Path('translations/hodram_B31_B53_editorial_manuscript_v2.json')
PAGES=Path('work/analysis/Hodram_B31_B53_pages_v8726/compiled_native_pages.json')
REASONS={
 'DK4_MES_B31_R0013':'Two complete automatically wrapped rows keep the irritated rhetorical tag will you? together and the complete first-person challenge together. The native full216px view shows the first Y, all contractions and punctuation and the final period. No blank or extra page, authored break, narrowing or shortening is used.',
 'DK4_MES_B31_R0018':'The four complete native rows preserve every word and punctuation mark, including the first Y, the entire challenge and the final fear. The ordinary complete-word boundary really / ought to fear. continues the same relative clause across rows. It is readable in the full sentence and fits the unchanged full216px native consumer without a fifth row, blank page, split word, lost character or shortened prose. No wider viewport or altered font is used.',
 'DK4_MES_B53_R0007':'Three complete native rows keep the report of wanted status and the final caution as complete phrases. The ordinary complete-word boundary ended up / wanted by the Ottoman Empire. preserves the single reported-status construction, rather than introducing a deliberate pause. The first L, apostrophes, Ottoman Empire spelling and final period are complete. All words remain, with full216px automatic wrapping and no extra page or authored staging break.',
}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old,pages=map(read,[OLD,PAGES]);planpath=Path(pages['plan']);plan=read(planpath)
    assert pages['manuscript_sha256']==plan['manuscript_sha256']==sha(OLD.read_bytes()) and pages['plan_sha256']==sha(planpath.read_bytes())
    assert sha(Path(pages['review_sheet']['path']).read_bytes())==pages['review_sheet']['sha256']
    assert not plan['failures'] and not old['typed_choice_records'];rows=[]
    for original,p,n in zip(old['records'],plan['records'],pages['records'],strict=True):
        assert original['id']==p['id']==n['id'] and original['english']==n['logical_English']==' '.join(p['lines']) and len(n['pages'])==1
        assert not p['base_QA']['issues'] and not original['review']['formatting']
        for page in n['pages']:
            for key in ['native_plane','preview']:assert sha(Path(page[key]).read_bytes())==page[key+'_sha256']
        row=deepcopy(original);row.update(compiled_hex=p['encoded_hex'],compiled_bytes=len(bytes.fromhex(p['encoded_hex'])),formatted_markup=p['formatted_markup'],
            planned_English_markup=p['planning_record']['english'],generated_lines=p['lines'],expected_native_pages=1,qa_waivers=[],qa_waiver_scope=[],
            native_body_review_reason=REASONS[row['id']],native_body_review_proof=str(PAGES),native_body_review_proof_sha256=sha(PAGES.read_bytes()),
            compiled_native_body_review=deepcopy(n),all_stored_controls_actual_branch_context_headers_policy_andregistered_release_pending=True)
        assert all(row[k]==original[k] for k in ['english','source_hex','current_hex','source_reference','current_reference','review','decision','localization_note']);rows.append(row)
    doc=deepcopy(old);doc.update(records=rows,predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),compiled_plan=str(planpath),compiled_plan_sha256=sha(planpath.read_bytes()),
        native_body_pages=str(PAGES),native_body_pages_sha256=sha(PAGES.read_bytes()),all_three_complete_native_English_pages_directly_viewed=True,
        all_three_formatting_gates_still_false=True,zero_original_QA_issues_zero_warnings_waivers=True,
        status='contextual-prose-native-pages-viewed-relocation-stored-actual-names-policy-release-pending')
    save(DOC,doc);ROOT.mkdir(parents=True)
    save(ROOT/'native_body_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        directly_viewed_sheet=pages['review_sheet'],reviewed_body_pages=3,fresh_logical_alignment_cases=12,fresh_compiled_alignment_cases=12,
        individual_body_reviews=[dict(id=r['id'],reason=r['native_body_review_reason'],generated_lines=r['generated_lines'],compiled_hex=r['compiled_hex']) for r in rows],
        original_QA_issues=[],no_qa_waivers=True,all_three_complete_bodies_visually_read=True,
        all_words_compiled_bytes_source_current_refs_individual_review_gates_andnative_planes_preserved=True,
        full216px_original_metrics_guards_pairphase_macro_rules_preserved=True,
        source_names_actor34_fullmiddle_finding_stored_actual_policy_atomic_registered_release_andcredit_pending=True,
        no_ROM_registry_orcredit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,DOC,PAGES,planpath,Path(__file__)]}))
    print('All3 English native pages directly reviewed;unchanged prose,zero QAissues/warnings/waivers. Storage,actual,names andregistered workflow remain pending.')
