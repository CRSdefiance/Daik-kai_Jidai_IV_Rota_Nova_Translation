"""Repair the observed guarded FE blank row and two short question wraps."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.meaning_maria335_B137_B151_v1 import ROOT
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def main():
    out=ROOT/'continuity_preferences_v4_native.json'
    finding=ROOT/'native_layout_findings_v2.json'
    assert not out.exists() and not finding.exists()
    previous=ROOT/'continuity_preferences_v3_native.json'
    pref=deepcopy(load(previous))
    manuscript=ROOT/'formatting_v1/formatting_input.json'
    rows={r['id']:r for r in load(manuscript)['records']}
    planpath=ROOT/'plan_native_v3/automatic_plans.json'
    plans={r['id']:r for r in load(planpath)['records']}
    diagpath=ROOT/'FE_B145_R57_diagnostic_v1/diagnostic.json'
    diag=load(diagpath)
    assert diag['planned_row_lengths']==[36,21]
    assert [r['y'] for r in diag['actual_rows']]==[0,12,24]
    assert diag['actual_rows'][1]['ASCII']=='  '
    remaining_risks={r['id'] for r in plans.values() if r['kind']=='system-FE' and any(len(s.strip())>=36 for s in r['lines'])}
    assert remaining_risks=={'DK4_MES_B145_R0057','DK4_MES_B145_R0077'}
    notes=[]
    for ident in sorted(remaining_risks):
        row=rows[ident]
        reason=('Use the qualified record-scoped FE36 planning reserve: B145R57 produces an extra native blank row after its36-character planned row; B145R77 has the same36-character risk. Keep physical228px width, complete prose, native font and all row/pixel/canary guards; fresh native checks required.')
        assert ident not in pref['records']
        pref['records'][ident]=dict(FE_planning_cells=36,reason=reason,bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
        notes.append(dict(id=ident,source_reference=row['source_reference'],current_reference=row['current_reference'],old_lines=plans[ident]['lines'],finding=reason))
    for ident in ['DK4_MES_B139_R0134','DK4_MES_B140_R0116']:
        row=rows[ident]
        reason='Keep the short complete question What is your name (contracted in the unchanged prose) together rather than splitting What\'s / your name across rows.'
        assert ident not in pref['records']
        pref['records'][ident]=dict(required_pairs=[["what's","your"],["your","name"]],reason=reason,
            bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
        notes.append(dict(id=ident,source_reference=row['source_reference'],current_reference=row['current_reference'],old_lines=plans[ident]['lines'],finding=reason))
    pref.update(previous_preferences=str(previous),previous_preferences_sha256=digest(previous),
        original_failed_native_output=str(ROOT/'native_resume_pages_v1'),exact_failing_record='DK4_MES_B145_R0057',
        native_guard_not_waived=True,physical_FE_viewport_not_narrowed=True,no_prose_orfont_orengine_changes=True,new_credit=0)
    save(out,pref)
    save(finding,dict(records=notes,diagnostic=str(diagpath),diagnostic_sha256=digest(diagpath),
        all_fifth_gates_still_pending=True,new_credit=0,evidence={str(p):digest(p) for p in [previous,manuscript,planpath,diagpath,Path(__file__)]}))
    print('Prepared two scoped FE36 guards and two short-question refinements; no prose changes.')


if __name__=='__main__':main()
