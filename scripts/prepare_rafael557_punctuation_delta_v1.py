"""Isolate the two changed plans and seal observed capture scope before rechecking them."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

A=Path('work/analysis')
ROOT=A/'Rafael557_company_punctuation_v1_20261105'
DOC=Path('translations/rafael_B141_B160_formatting_manuscript_v4.json')
PLAN=A/'Rafael557_automatic_plans_v11_20261105/automatic_plans.json'
OLD=A/'Rafael557_storage_inputs_v1_20261105/plans.json'

if __name__=='__main__':
    assert not (ROOT/'delta_manuscript.json').exists()
    doc,plan,old=map(load,[DOC,PLAN,OLD]);assert plan['manuscript_sha256']==sha(DOC.read_bytes())
    assert len(plan['records'])==len(old['records'])==549 and not plan['failures']
    ids=set(doc['observed_runtime_punctuation_corrections'])
    assert {a['id'] for a,b in zip(plan['records'],old['records'],strict=True) if a!=b}==ids
    selected=[r for r in doc['records'] if r['id'] in ids];target=[r for r in plan['records'] if r['id'] in ids]
    assert len(selected)==len(target)==2 and all(r['expected_native_pages']==1 for r in target)
    subset=ROOT/'delta_manuscript.json';subplan=ROOT/'delta_plans.json'
    save(subset,{**doc,'records':selected,'blocks':[154],'source_objects':2,'physical_speech_objects':2,'ordinary_speech_objects':2,
        'typed_choice_objects':0,'typed_choice_commands':0,'full_manuscript':str(DOC),'full_manuscript_sha256':sha(DOC.read_bytes())})
    save(subplan,{**plan,'records':target,'manuscript':str(subset),'manuscript_sha256':sha(subset.read_bytes()),
        'complete_plan':str(PLAN),'complete_plan_sha256':sha(PLAN.read_bytes())})
    contacts=[A/f'Rafael557_{p}_actual_sheets_v1_20261105/receipt.json' for p in ['tutorial','story']]
    menus=[A/f'Rafael557_{p}_menu_pixels_v1_20261105/menu_actual_pixels.json' for p in ['tutorial','story']]
    sheets=[];bodies=[];refs=[]
    for path in contacts:
        c=load(path);ref=Path(c['actual_pixel_proof']);assert sha(ref.read_bytes())==c['actual_pixel_proof_sha256'];refs.append(ref)
        proof=load(ref);assert proof['all_complete_native_body_andheader_planes_andblank_guards_match']
        bodies.extend(proof['ordered_selected_source_calls']);sheets+=c['bottom_screen_sheets']+c['full_scene_sheets']
    for path in menus:
        p=load(path);assert p['all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches']
        assert len(p['menus'])==2 and all(m['observed_selected_options']==[0] for m in p['menus'])
        sheets.append(p['review_sheet'])
    assert len(sheets)==21 and len(bodies)==193 and len({p['id'] for p in bodies})==188
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    approved=[p for p in bodies if p['id'] not in ids];assert len(approved)==191 and len({p['id'] for p in approved})==186
    save(ROOT/'direct_actual_visual_review_before_delta.json',dict(directly_opened_readable_sheets=sheets,
        both_initial_cold_boot_runs_observed=True,all193_initial_body_pages_directly_viewed=True,
        accepted_unchanged_actual_pages=approved,retired_actual_pages=[p for p in bodies if p['id'] in ids],
        four_complete_menu_captions_anddefault_cursor_states_directly_viewed=True,
        no_original_conditional_location_chronology_hardware_orfull_route_coverage=True,
        whole_exchange_retention_notes={
            'B143_R0380':'Keep the second page as the complete market-share consequence rather than breaking that instruction across pages.',
            'B143_R0403':'Keep the complete advice to build up funds on the second page; it is the next step in the lesson.',
            'B150_R0013':'The exact one-page attempt failed the validated planning limits. Retain the complete purpose phrase on page two instead of an isolated fragment, with the original wording and width intact.',
            'B145':'Keep the public Arcadius header; Eirene is revealed in the private speech, followed by a request for discretion.',
            'B148_R0121':'The two notice rows render consecutively without the prior blank row or lost letters.',
        },final_delta_visual_review_pending=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PLAN,OLD,subset,subplan,*contacts,*menus,*refs,Path(__file__)]}))
    print('547 speech plans are byte-for-byte unchanged; two one-page plans need fresh checks. Sealed 191 unaffected viewed pages and four menus.')
