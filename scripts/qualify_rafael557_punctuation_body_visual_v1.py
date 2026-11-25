"""Bind the two fresh viewed native pages and the exact 547 previous body reviews."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

A=Path('work/analysis')
ROOT=A/'Rafael557_body_visual_review_v2_20261105'
OLD=A/'Rafael557_body_visual_review_v1_20261105/body_visual_review.json'
NATIVE=A/'Rafael557_native_final_v2_20261105/compiled_native_pages.json'
PLAN=A/'Rafael557_automatic_plans_v11_20261105/automatic_plans.json'
FRESH=A/'Rafael557_punctuation_native_v1_20261105/compiled_native_pages.json'
SHEET=FRESH.with_name('B154_part1.png')

if __name__=='__main__':
    assert not ROOT.exists();old,native,plan,fresh=map(load,[OLD,NATIVE,PLAN,FRESH]);origin=Path(old['native'])
    assert old['native_sha256']==sha(origin.read_bytes()) and old['all558_final_body_pages_directly_viewed']
    assert native['plan_sha256']==sha(PLAN.read_bytes()) and native['pages']==558
    old_by_id={r['id']:r for r in load(origin)['records']};changed={r['id']:r for r in fresh['records']}
    assert len(changed)==2 and fresh['pages']==2 and fresh['fresh_compiled_alignments']==8
    assert {r['id'] for r in native['records'] if r!=old_by_id[r['id']]}==set(changed)
    assert all(r==changed[r['id']] for r in native['records'] if r['id'] in changed)
    by_id={r['id']:r for r in plan['records']};rows=[]
    for row in old['records']:
        ident=row['id'];target=by_id[ident]
        if ident in changed:
            row={**row,'final_lines':target['lines'],'pages':1,'changed_from_first_clean_plan':True,
                'visual_finding':'Fresh paragraph wraps and native preview were directly viewed. Complete first/last characters and the single Castor Co. abbreviation are clear; no duplicate sentence stop remains.'}
        else:assert row['final_lines']==target['lines'] and row['pages']==target['expected_native_pages']
        rows.append(row)
    sheets=[*old['directly_opened_readable_sheets'],dict(path=str(SHEET),sha256=sha(SHEET.read_bytes()))]
    assert len(sheets)==43 and all(sha(Path(s['path']).read_bytes())==s['sha256'] for s in sheets)
    ROOT.mkdir(parents=True)
    save(ROOT/'body_visual_review.json',{**old,'native':str(NATIVE),'native_sha256':sha(NATIVE.read_bytes()),
        'final_plan':str(PLAN),'final_plan_sha256':sha(PLAN.read_bytes()),'records':rows,
        'source_preview_pages_viewed_including_retired_trials':587,'directly_opened_readable_sheets':sheets,
        'final_layout_changes_from_first_clean_plan':sum(r['changed_from_first_clean_plan'] for r in rows),
        'fresh_punctuation_pages_viewed':2,'prior_exact_native_page_visual_reuse':556,
        'previous_visual_review':str(OLD),'previous_visual_review_sha256':sha(OLD.read_bytes()),
        'evidence':{str(p):sha(p.read_bytes()) for p in [OLD,NATIVE,PLAN,FRESH,SHEET,Path(__file__)]}})
    print('All 558 final pages are directly reviewed: 556 exact prior views and two freshly viewed punctuation pages.')
