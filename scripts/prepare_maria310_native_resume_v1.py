"""Preserve65 whole-block and19 journaled records; scope only the unproved remaining226."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.meaning_maria_B51_B52_clean_v1 import ROOT

def main():
    out=ROOT/'native_resume_selection_v1.json';pref_path=ROOT/'formatting_v1/preferences_v4_FE_guards.json'
    assert not out.exists() and not pref_path.exists()
    doc_path=ROOT/'formatting_v1/formatting_input.json';plan_path=ROOT/'plan_v1/automatic_plans.json'
    doc,plan=map(load,[doc_path,plan_path]);byid={r['id']:r for r in doc['records']};oldplans={r['id']:r for r in plan['records']}
    completed=[];bindings=[]
    for block in [51,52,53]:
        path=ROOT/f'initial_native_v1/B{block}_checked.json';receipt=load(path)
        assert len(receipt['records'])=={51:26,52:2,53:37}[block]
        for row in receipt['records']:completed.append(row);bindings.append(dict(id=row['id'],path=str(path),sha256=digest(path),kind='completed-whole-block'))
    journals=sorted((ROOT/'remaining_native_v1').glob('complete_*.json'));assert len(journals)==19
    for path in journals:
        proof=load(path);inputs=load(proof['native_run_inputs'])
        assert digest(proof['native_run_inputs'])==proof['native_run_inputs_sha256']
        assert inputs['runtime']==doc['runtime'] and inputs['all_v1_native_assertions_preserved']
        assert proof['all_original_native_glyph_pixels_consumption_canaries_bounds_androw_assertions_pass']
        row=proof['record'];completed.append(row);bindings.append(dict(id=row['id'],path=str(path),sha256=digest(path),kind='append-only-completed-record'))
    assert len(completed)==len({r['id'] for r in completed})==84
    for row in completed:
        original=byid[row['id']]
        assert row['source_reference']==original['source_reference'] and row['current_reference']==original['current_reference']
        assert row['compiled_hex']==oldplans[row['id']]['encoded_hex'] and row['logical_English']==original['english']
        assert len(row['native_alignment']['cases'])==4
        pages=row['complete_native_English_display']['pages'] if row['kind']=='progressive' else [row['complete_native_English_display']]
        for page in pages:assert digest(page['preview'])==page['preview_sha256'] and digest(page['native_plane'])==page['native_plane_sha256']
    ids=[r['id'] for r in doc['records'] if r['id'] not in {r['id'] for r in completed}];assert len(ids)==226
    save(out,dict(ids=ids,completed_records_reused=84,completed_alignment_cases=336,bindings=bindings,
        completed_B54_images_without_complete_native_receipts_not_claimed_as_reusable=True,
        unchanged_prose_andall_five_gate_state=True,new_credit=0,
        evidence={str(p):digest(p) for p in [doc_path,plan_path,Path(__file__)]}))
    previous=ROOT/'formatting_v1/preferences_v3_FE37_trial.json';pref=deepcopy(load(previous))
    for ident in ['DK4_MES_B55_R0091','DK4_MES_B55_R0155','DK4_MES_B55_R0179']:
        row=byid[ident];assert row['kind']=='system-FE'
        pref['records'][ident]=dict(FE_planning_cells=36,
            reason='Use the existing scoped FE36 guard reserve for the concrete R91 unintended row and the same consumer\'s37-cell R155/R179 risks. Preserve full prose,physical228px geometry andall native guards;fresh checks remain mandatory.',
            bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
    pref.update(previous_preferences=str(previous),previous_preferences_sha256=digest(previous),
        prior_native_FE_row_failure='DK4_MES_B55_R0091',no_prose_orengine_changes=True,new_credit=0)
    save(pref_path,pref)
    print('Bound84 completed native records/336 alignments forreuse;226 remain;five scoped FE guard trials preserve prose.')
if __name__=='__main__':main()
