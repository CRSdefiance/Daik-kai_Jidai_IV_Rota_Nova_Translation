"""Keep one complete short aside and reuse scoped guards for eight matching FE risks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    out=ROOT/'continuity_preferences_v1.json';findings=ROOT/'continuity_findings_v1.json'
    assert not out.exists() and not findings.exists()
    docpath=ROOT/'formatting_v1/formatting_input.json';planpath=ROOT/'plan_initial_v1/automatic_plans.json'
    doc,plan=map(load,[docpath,planpath]);rows={r['id']:r for r in doc['records']};plans={r['id']:r for r in plan['records']}
    priorpath=ROOT/'formatting_v1/initial_preferences.json';preferences=deepcopy(load(priorpath));notes=[]
    ident='DK4_MES_B169_R0073';row=rows[ident]
    assert plans[ident]['expected_native_pages']==2 and len(row['english'])==124 and plans[ident]['lines'][-1]=='twice more.)'
    reason='Trial the complete124-character private bargaining aside at the validated216px width instead of stranding twice more on page2. Keep at least twice more coherent; preserve every word, parenthesis, control andmacro. Fresh native/visual proof remains required.'
    preferences['records'][ident]=dict(one_page=True,required_pairs=[['at','least'],['least','twice'],['twice','more']],reason=reason,
        bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
    notes.append(dict(id=ident,source_reference=row['source_reference'],current_reference=row['current_reference'],initial_lines=plans[ident]['lines'],finding=reason))
    risks={r['id'] for r in plan['records'] if r['kind']=='system-FE' and any(len(s.strip())>=36 for s in r['lines'])}
    assert risks=={'DK4_MES_B152_R0053','DK4_MES_B153_R0072','DK4_MES_B154_R0038','DK4_MES_B156_R0094',
        'DK4_MES_B158_R0028','DK4_MES_B162_R0064','DK4_MES_B164_R0099','DK4_MES_B167_R0055'}
    old=Path('work/Maria_B137_B151_clean_20261109/native_layout_findings_v2.json')
    assert load(old)['all_fifth_gates_still_pending']
    for ident in sorted(risks):
        row=rows[ident]
        reason='Reuse the qualified record-scopedFE36 planning reserve for this exact36–38-character guarded-row risk, matching prior native word-split/extra-row failures. Keep physical228px geometry, prose, font, consumer andall native guards unchanged. Fresh record checks are still required; do not apply the reserve to other FE records.'
        preferences['records'][ident]=dict(FE_planning_cells=36,reason=reason,
            bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
        notes.append(dict(id=ident,source_reference=row['source_reference'],current_reference=row['current_reference'],initial_lines=plans[ident]['lines'],finding=reason))
    preferences.update(previous_preferences=str(priorpath),previous_preferences_sha256=digest(priorpath),
        qualified_matching_FE_guard_findings=str(old),qualified_matching_FE_guard_findings_sha256=digest(old),
        prose_font_viewport_andengine_unchanged=True,native_andvisual_checks_pending=True,new_credit=0)
    save(out,preferences)
    save(findings,dict(records=notes,source_objects=390,body_candidates=373,ordinary_one_page_trials=1,scoped_FE_reserves=8,
        physical_widths_216_and228_unchanged=True,no_words_shortened=True,new_credit=0,
        evidence={str(p):digest(p) for p in [docpath,planpath,priorpath,old,Path(__file__)]}))
    print('Prepared one full-width short-aside trial andeight exact matching FE guard reserves;fresh native/visual checks pending.')


if __name__=='__main__':main()
