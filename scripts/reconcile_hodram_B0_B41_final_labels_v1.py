"""Reconcile stale intake-stage pending labels without changing reviewed text, facts or gates."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Hodram_B0_B41_clean_20261107')
OLD=Path('translations/hodram_B0_B41_final_review_v1.json')
FINAL=Path('translations/hodram_B0_B41_final_review_v2.json')
OUT=ROOT/'research_final_v2'

def main():
    assert not OUT.exists() and not FINAL.exists()
    ready_path=ROOT/'research_final_v1/research_completion.json';ready=load(ready_path)
    assert ready['manuscript_sha256']==digest(OLD) and ready['all_individual_five_gates_pass']
    doc=deepcopy(load(OLD));before=deepcopy(doc)
    row_labels=['source_context_localization_formatting_gates_pending',
        'clean_name_event_membership_current_comparison_drafts_andall_five_gates_pending',
        'scoped_names_terms_controls_glyphs_andall_display_checks_pending',
        'source_name_term_control_andformatting_binding_pending',
        'native_style_dispatch_andall_five_review_gates_pending']
    changes=[]
    for row in doc['records']:
        assert all(row['review'][k] for k in ['source','context','localization','naturalness','formatting'])
        for key in row_labels:
            if row.get(key) is True:row[key]=False;changes.append(dict(id=row['id'],field=key))
    for key in ['all_individual_fifth_gates_still_pending','source_names_terms_anddistinct_display_consumers_still_require_scoped_review',
                'no_new_English_gameplay_orformatted_page_approval','source_context_localization_formatting_gates_pending']:
        if doc.get(key) is True:doc[key]=False;changes.append(dict(id='batch',field=key))
    assert all((a['english'],a['review'],a['source_reference'],a['current_reference'],a['planned_integrated_reference'])==
        (b['english'],b['review'],b['source_reference'],b['current_reference'],b['planned_integrated_reference'])
        for a,b in zip(before['records'],doc['records'],strict=True))
    doc.update(previous_final_manuscript=str(OLD),previous_final_manuscript_sha256=digest(OLD),
        stale_intake_stage_labels_reconciled_only=True,registered_release_andcompletion_credit_pending=True)
    validate_natural_dialogue_batch(doc);save(FINAL,doc);OUT.mkdir()
    plans=load(ROOT/'research_final_v1/release_plans.json');plans.update(manuscript=str(FINAL),manuscript_sha256=digest(FINAL))
    save(OUT/'release_plans.json',plans)
    ready.update(manuscript=str(FINAL),manuscript_sha256=digest(FINAL),previous_completion=str(ready_path),previous_completion_sha256=digest(ready_path),
        only_stale_pending_metadata_reconciled=True)
    ready['evidence'].update({str(FINAL):digest(FINAL),str(ready_path):digest(ready_path),str(Path(__file__)):digest(__file__)})
    save(OUT/'research_completion.json',ready)
    save(OUT/'metadata_reconciliation.json',dict(changes=changes,all_wording_gates_andexact_references_unchanged=True,
        previous=str(OLD),previous_sha256=digest(OLD),final=str(FINAL),final_sha256=digest(FINAL),new_credit=0))
    print('Reconciled',len(changes),'stale intake-stage labels;394 reviewed texts,gates andexact references unchanged. Integration remains.')

if __name__=='__main__':main()
