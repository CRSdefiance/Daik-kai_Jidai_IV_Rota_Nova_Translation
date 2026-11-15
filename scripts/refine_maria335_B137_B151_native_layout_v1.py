"""Reuse the qualified scoped FE36 reserve for four concrete native-row risks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.meaning_maria335_B137_B151_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    out=ROOT/'continuity_preferences_v3_native.json';findings=ROOT/'native_layout_findings_v1.json'
    assert not out.exists() and not findings.exists()
    original=ROOT/'continuity_preferences_v2.json';pref=deepcopy(load(original))
    docpath=ROOT/'formatting_v1/formatting_input.json';doc=load(docpath);byid={r['id']:r for r in doc['records']}
    planpath=ROOT/'plan_continuity_v2/automatic_plans.json';plans={r['id']:r for r in load(planpath)['records']}
    diagpath=ROOT/'FE_B139_R199_diagnostic_v1/diagnostic.json';diag=load(diagpath)
    assert diag['planned_row_lengths']==[37,33] and [r['y'] for r in diag['actual_rows']]==[0,12,24]
    assert diag['actual_rows'][1]['ASCII']=='w '
    risks={r['id'] for r in plans.values() if r['kind']=='system-FE' and any(len(s.strip())>=37 for s in r['lines'])}
    assert risks=={'DK4_MES_B139_R0199','DK4_MES_B139_R0202','DK4_MES_B145_R0051','DK4_MES_B150_R0036'}
    notes=[]
    for ident in sorted(risks):
        reason=('Use the already qualified record-scoped FE36 guard reserve after B139R199 splits the last w of view into a new native row. '
            'This exact paragraph is either the observed failure or a matching37/38-cell row risk. Preserve physical228px geometry,all prose,font,controls andnative guards;fresh row/pixel checks remain required.')
        row=byid[ident];assert row['kind']=='system-FE' and ident not in pref['records']
        pref['records'][ident]=dict(FE_planning_cells=36,reason=reason,bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
        notes.append(dict(id=ident,source_reference=row['source_reference'],current_reference=row['current_reference'],initial_lines=plans[ident]['lines'],finding=reason))
    phrases={
        'DK4_MES_B138_R0070':(['only','if','you','want','to','of','course'],'Keep the complete short Only if you want to, of course. answer together instead of stranding to, of course. after the line break.'),
        'DK4_MES_B138_R0109':(['private','cabin'],'Keep the exact Private Cabin room name together in the recovery tutorial.'),
    }
    for ident,(words,reason) in phrases.items():
        row=byid[ident];assert ident not in pref['records']
        pref['records'][ident]=dict(required_pairs=[list(p) for p in zip(words,words[1:])],reason=reason,
            bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
        notes.append(dict(id=ident,source_reference=row['source_reference'],current_reference=row['current_reference'],initial_lines=plans[ident]['lines'],finding=reason))
    pref.update(previous_preferences=str(original),previous_preferences_sha256=digest(original),
        original_failed_native_output=str(ROOT/'native_pages_v1'),exact_failing_record='DK4_MES_B139_R0199',
        physical_FE_viewport_not_narrowed=True,native_guard_not_waived=True,no_prose_orfont_orengine_changes=True,new_credit=0)
    save(out,pref)
    save(findings,dict(records=notes,native_failure=str(diagpath),native_failure_sha256=digest(diagpath),
        qualified_FE36_recipe='scripts/prepare_maria310_FE_guard_trials_v1.py',
        qualified_FE36_recipe_sha256=digest('scripts/prepare_maria310_FE_guard_trials_v1.py'),
        reused_completed_receipts_still_require_exact_final_bytes=True,all_fifth_gates_still_pending=True,new_credit=0,
        evidence={str(p):digest(p) for p in [original,docpath,planpath,diagpath,Path(__file__)]}))
    print('Prepared4 scoped FE36 row repairs and2 phrase-wrap refinements;prose andphysical geometry unchanged.')


if __name__=='__main__':main()
