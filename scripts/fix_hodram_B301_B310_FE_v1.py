"""Exclude one observed overlong guarded FE row without changing prose or native geometry."""
from copy import deepcopy
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_hodram_B301_B310_formatting_v1 import ROOT,FORMATTING
from dk4tool.patch.grand_race_menu_release import sha

OUT=ROOT/'formatting_v1/FE_guard_preferences_v2.json'

def main():
    assert not OUT.exists()
    failure=ROOT/'FE_departure_row_failure_v1.json';proof=load(failure)
    assert proof['record']=='DK4_MES_B309_R0294' and proof['actual_row_membership_failed']
    assert proof['complete_nonspace_glyph_sequence_preserved']
    assert [r['y'] for r in proof['actual_rows']]==[0,12,24] and proof['actual_rows'][1]['text'].strip()=='r'
    row=next(r for r in load(FORMATTING)['records'] if r['id']==proof['record'])
    p=deepcopy(load(ROOT/'formatting_v1/initial_preferences.json'))
    p['records'][row['id']]=dict(FE_planning_cells=36,
        reason='The37-character first row broke appear into appea and a lone r before the protected LF. Exclude that observed guarded row while preserving both sentences, full228px native geometry and all source controls.',
        bindings={k:sha(row[k].encode()) for k in ['source_hex','current_hex','english']})
    save(OUT,p)
    save(ROOT/'FE_departure_formatting_fix_v2.json',dict(record=row['id'],diagnostic=str(failure),diagnostic_sha256=digest(failure),
        preferences=str(OUT),preferences_sha256=digest(OUT),observed_broken_word='appear',
        no_prose_font_engine_orviewport_change=True,all_other_record_preferences_unchanged=True,
        fresh_plan_andnative_checks_required=True,new_credit=0))
    print('Saved one source-bound FE36 preference for the observed split-word row.')

if __name__=='__main__':main()
