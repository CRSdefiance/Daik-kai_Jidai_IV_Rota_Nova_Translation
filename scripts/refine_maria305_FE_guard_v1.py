"""Apply the qualified record-specific FE guard reserve to concrete row risks."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B176_B195_clean_20261110')


def main():
    output=ROOT/'formatting_v1/page_preferences_v7_FE.json';assert not output.exists()
    before=ROOT/'formatting_v1/page_preferences_v6.json';docpath=ROOT/'formatting_v1/formatting_input.json'
    diagnostic=ROOT/'FE_B177_R66_diagnostic_v1.json';proof=load(diagnostic)
    assert proof['actual_row_membership_failed'] and proof['complete_nonspace_glyph_sequence_preserved']
    assert proof['actual_rows'][2]==dict(y=24,text='  ') and len(proof['actual_rows'])==4
    prefs=load(before);rows={r['id']:r for r in load(docpath)['records']}
    plans={r['id']:r for r in load(ROOT/'plan_v5/automatic_plans.json')['records']}
    expected={'DK4_MES_B177_R0066','DK4_MES_B184_R0016'}
    assert len(plans['DK4_MES_B184_R0016']['lines'][0].strip())==37
    for key in sorted(expected):
        row=rows[key];assert row['kind']=='system-FE' and row['source_selector']==254 and key not in prefs['records']
        prefs['records'][key]=dict(FE_planning_cells=36,
            reason='Use the qualified record-scoped FE36 guard reserve after the actual B177R66 extra blank native row. B184R16 has the matching long FE row risk. Retain physical228px width,all prose,source controls,font andnative assertions;fresh native alignment/row/pixel proof remains required.',
            bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
    prefs.update(previous_preferences=str(before),previous_preferences_sha256=digest(before),
        concrete_native_failure=str(diagnostic),concrete_native_failure_sha256=digest(diagnostic),
        qualified_existing_recipe='scripts/prepare_maria310_FE_guard_trials_v1.py',
        no_prose_physical_geometry_font_orengine_changes=True,
        evidence={str(p):digest(p) for p in [docpath,diagnostic,before,Path(__file__)]})
    save(output,prefs);print('Prepared two exact FE guard-reserve refinements; all prose andphysical228px width unchanged.')


if __name__=='__main__':main()
