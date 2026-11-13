"""Bind exact reviewed compiled bytes without changing prose or review gates."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_compiled_v8808')
OLD=Path('translations/hodram_B54_B60_editorial_manuscript_v1.json')
DOC=Path('translations/hodram_B54_B60_editorial_manuscript_v2.json')
VIEW=Path('work/analysis/Hodram_B54_B60_native_view_v8805/all82_native_English_direct_view_andboundary_review.json')

if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old,view=map(read,[OLD,VIEW]);pages_path=Path(view['native_pages']);plan_path=Path(view['plan']);pages,plan=map(read,[pages_path,plan_path])
    assert view['manuscript_sha256']==pages['manuscript_sha256']==plan['manuscript_sha256']==sha(OLD.read_bytes())
    assert view['all11_sheets85pages82utterances_directly_viewed'] and not plan['failures']
    rows=[]
    for original,p,n,v in zip(old['records'],plan['records'],pages['records'],view['records'],strict=True):
        assert original['id']==p['id']==n['id']==v['id'] and original['english']==n['logical_English']==' '.join(p['lines'])
        assert n['compiled_hex']==p['encoded_hex']==v['compiled_hex'] and not original['review']['formatting']
        assert not any(i['severity'] in ['error','warning'] for i in p['base_QA']['issues'])
        r=deepcopy(original);r.update(compiled_hex=p['encoded_hex'],compiled_bytes=len(bytes.fromhex(p['encoded_hex'])),formatted_markup=p['formatted_markup'],
            generated_lines=p['lines'],expected_native_pages=p['expected_native_pages'],qa_waivers=[],qa_waiver_scope=[],
            original_QA_issues=p['base_QA']['issues'],native_body_review_reason=v['wrap_review'],
            native_body_review_proof=str(VIEW),native_body_review_proof_sha256=sha(VIEW.read_bytes()),compiled_native_body_review=deepcopy(n),
            all_stored_controls_actual_headers_transitions_policy_andregistered_release_pending=True)
        assert all(r[k]==value for k,value in original.items());rows.append(r)
    doc=deepcopy(old);doc.update(records=rows,predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        compiled_plan=str(plan_path),compiled_plan_sha256=sha(plan_path.read_bytes()),native_body_pages=str(pages_path),native_body_pages_sha256=sha(pages_path.read_bytes()),
        native_body_view=str(VIEW),native_body_view_sha256=sha(VIEW.read_bytes()),all82_complete_native_English_bodies_directly_viewed=True,
        all82_formatting_gates_still_false=True,zero_original_QA_errors_warnings_andwaivers=True,
        status='82-prose-andnative-pages-reviewed-storage-actual-production-registered-release-pending')
    save(DOC,doc);ROOT.mkdir(parents=True)
    save(ROOT/'compiled_body_bindings.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        records=[dict(id=r['id'],compiled_hex=r['compiled_hex'],source_reference=r['source_reference'],current_reference=r['current_reference'],source_complete_preamble_hex=r['source_complete_preamble_hex'],original_QA_issues=r['original_QA_issues'],expected_native_pages=r['expected_native_pages']) for r in rows],
        all_original_record_values_exactly_preserved=True,compiled_bytes_and82_preambles_bound_to_viewed85_pages=True,formatting_gates_still_false=True,
        source_MACRO_counts=old['source_macro_counts'],no_ROM_registry_ledger_orcompletion_credit_change=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [OLD,DOC,VIEW,pages_path,plan_path,Path(__file__)]}))
    print('82 compiled records bound to reviewed85pages;all prior manuscript fields/gates exact;no completion credit.')
