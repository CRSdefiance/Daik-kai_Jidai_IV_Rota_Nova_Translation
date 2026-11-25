"""Reuse 610 exact plans, replace one apology wrap, retain the measured fleet-name clause."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.profiles import get_dialogue_profile
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Hodram_B151_B170_formatting_20261102')
if __name__=='__main__':
    target=ROOT/'ordinary_plans_v2/automatic_plans.json';assert not target.exists()
    original_path=ROOT/'ordinary_plans/automatic_plans.json';single_path=ROOT/'apology_replan_v2/automatic_plans.json'
    old,new=load(original_path),load(single_path);source=Path(old['manuscript']);doc=load(source)
    assert old['manuscript_sha256']==new['manuscript_sha256']==sha(source.read_bytes()) and not old['failures'] and not new['failures']
    assert len(old['records'])==611 and len(new['records'])==1
    alias=Path('scripts/plan_hodram_B151_B170_ordinary.py')
    for path,digest in old['evidence'].items():
        actual=alias if path.endswith('plan_editorial_scene_prose_v14.py') else Path(path)
        assert sha(actual.read_bytes())==digest,(path,actual)
    for path,digest in new['evidence'].items():assert sha(Path(path).read_bytes())==digest,path
    replacement=new['records'][0];assert replacement['id']=='DK4_MES_B159_R0112'
    assert replacement['lines']==["I'm sorry,","but I'll have to let you go."]
    old_by={r['id']:r for r in old['records']};bound={r['id']:r for r in doc['records']}
    assert replacement['logical_English']==old_by[replacement['id']]['logical_English']==bound[replacement['id']]['english']
    rows=[deepcopy(replacement if r['id']==replacement['id'] else r) for r in old['records']]
    gerhard=next(r for r in rows if r['id']=='DK4_MES_B168_R0166')
    warnings=[i for i in gerhard['base_QA']['issues'] if i['severity']=='warning']
    assert warnings==[dict(severity='warning',code='orphan-final-line',message="final line is unusually short: 'of <FO>.'")]
    assert gerhard['lines']==['My apologies. Gerhard Adernkatz,','of {MACRO:FO}.']
    profile=get_dialogue_profile('hodram-story-live');assert profile.macro_ascii_lengths['FO']==15 and profile.macro_widths['FO']==90
    reason=('The raw QA counts the seven-character placeholder of <FO>., while the route-bound FO expands to '
            'Bergstrom Fleet (15 ASCII cells). The clause is 19 visible cells/114px before its 6px guard. '
            'Keep Gerhard Adernkatz together and the complete faction phrase on row two. The original warning remains recorded; '
            'fresh native macro and pixel checks must still confirm it.')
    gerhard['unmodified_base_QA']=deepcopy(gerhard['base_QA'])
    for issue in gerhard['base_QA']['issues']:
        if issue['severity']=='warning':issue.update(severity='info',reviewed_retention_reason=reason)
    gerhard['QA_exact_macro_placeholder_retention']=dict(original_issue=warnings[0],reason=reason,expanded_visible_cells=19,profile_macro_cells=15)
    replacement_reason=('Source 悪いが、辞めてもらうよ introduces a complete apology before the dismissal. '
                        'Allow the automatic boundary after sorry, to keep but I\'ll have to let you go. together, '
                        'instead of stranding you go. No prose or authored line break was added.')
    rows_by={r['id']:r for r in rows};rows_by[replacement['id']]['automatic_clause_boundary_reason']=replacement_reason
    assert all(rows_by[i]==r for i,r in old_by.items() if i not in [replacement['id'],gerhard['id']])
    assert not any(i['severity'] in ['warning','error'] for r in rows for i in r['base_QA']['issues'])
    result={**old,'records':rows,'source_owned_planner_for_one_replacement':new['source_owned_planner'],
        'original_plans':str(original_path),'original_plans_sha256':sha(original_path.read_bytes()),
        'replacement_plans':str(single_path),'replacement_plans_sha256':sha(single_path.read_bytes()),
        'exact_unchanged_layouts_reused':610,'fresh_layouts':1,'raw_QA_warning_retention_records':1,
        'ordinary_apology_boundary_reason':replacement_reason,'macro_placeholder_warning_reason':reason,
        'historical_filename_collision_producer_alias':dict(original='scripts/plan_editorial_scene_prose_v14.py',exact_source_now=str(alias),sha256=sha(alias.read_bytes())),
        'evidence':{str(p):sha(p.read_bytes()) for p in [source,original_path,single_path,alias,ROOT/'historical_helper_restoration.json',Path(__file__)]}}
    target.parent.mkdir(parents=True);save(target,result)
    geometry=Path('work/analysis/Hodram_B156_cinematic_geometry_20261102/observed_cinematic_geometry.json');g=load(geometry)
    assert g['cinematic_FE_records']==23 and g['all23_source_FE_typed_geometry_228x48_288stride_6x12_current_vtables_exact']
    assert len(g['review_sheets'])==2
    for sheet in g['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    save(geometry.with_name('source_cinematic_visual_review.json'),dict(geometry=str(geometry),geometry_sha256=sha(geometry.read_bytes()),
        directly_viewed_sheets=g['review_sheets'],source_FE_panels_viewed=23,
        finding='Alternating left/right positions, blank first rows, silent ellipses and embedded Sera/Hodram headings are deliberate source scene staging. Preserve speaker/emotional progression with individually justified English layout; do not copy Japanese full-width spacing or flatten this into ordinary prose-only FE layout.',
        original_source_body_complete_andbounds_visually_confirmed=True,English_formatting_visual_andgameplay_pending=True,
        content_fixture_not_natural_endgame=True,guide_photos=False,new_credit=0))
    print('611 ordinary plans/627 pages: one wrap fixed,610 layouts reused; exact placeholder warning retained with measured reason. 23 source cinematic panels visually reviewed; English/native/stored gates pending.')
