"""Bind six wrap/page refinements to exact prose after the first native/visual pass."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

DOC=Path('translations/rafael_B121_B140_formatting_manuscript_v4.json')
PLAN=Path('work/analysis/Rafael351_automatic_plans_v2_20261105/automatic_plans.json')
OUT=Path('translations/rafael_B121_B140_visual_preferences_v2.json')
if __name__=='__main__':
    assert not OUT.exists()
    doc,plan=map(load,[DOC,PLAN]);assert plan['manuscript_sha256']==sha(DOC.read_bytes())
    rows={r['id']:r for r in doc['records']};plans={r['id']:r for r in plan['records']}
    prefs={
        'DK4_MES_B121_R0100':dict(line_phrases=['give you'],reason='Keep give you together;the viewed first page had an unnecessarily early break after give.'),
        'DK4_MES_B123_R0048':dict(one_page=True,line_phrases=['out of dried mud'],reason='The viewed second page consisted only of of dried mud. Try a source-complete four-row plan before accepting that broken phrase/page turn.'),
        'DK4_MES_B123_R0171':dict(one_page=True,reason='The viewed second page consisted only of Or better. Preserve the whole confident response together if its exact prose fits.'),
        'DK4_MES_B128_R0089':dict(FE_planning_cells=36,reason='The first native run completed through R85,then the next FE R89 failed unchanged check_FE_rows. Its37-cell first line crosses native row membership after guard handling;reserve two planning cells only for this exact record. Physical228px/four-row geometry and all validators stay unchanged.'),
        'DK4_MES_B129_R0024':dict(one_page=True,reason='The automatic plan leaves and the New World alone on page2. Try fitting the complete existing paragraph without a page turn;no wording change.'),
        'DK4_MES_B140_R0012':dict(page_clause='with less military investment than other nations need.',reason='The automatic plan strands than other nations need on page2. Keep the full investment comparison together after the page turn;the complete153-character prose remains unchanged.'),
    }
    for ident,value in prefs.items():
        row=rows[ident]
        value['bindings']={k:sha(row[k].encode('utf-8')) for k in ['source_hex','current_hex','english']}
        value['previous_lines']=plans[ident]['lines']
    save(OUT,dict(records=prefs,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        original_plan=str(PLAN),original_plan_sha256=sha(PLAN.read_bytes()),
        source_prose_macros_andnative_geometry_unchanged=True,
        first_native_failure='work/analysis/Rafael351_native_gc_v1_20261105/failure_traceback.txt',
        all_refinements_need_fresh_native_andvisual_checks=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,Path(__file__)]}))
    print('Saved six exact-input wrap/page preferences;no prose shortened or native assertion relaxed.')
