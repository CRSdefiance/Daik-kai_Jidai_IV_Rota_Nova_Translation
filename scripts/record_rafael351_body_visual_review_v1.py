"""Record direct review of every final native body page, with exact reuse and exceptions."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/Rafael351_body_visual_review_v1_20261105')
NATIVE=Path('work/analysis/Rafael351_native_final_v3_20261105/compiled_native_pages.json')
PLAN=Path('work/analysis/Rafael351_automatic_plans_v6_20261105/automatic_plans.json')
FIRST=Path('work/analysis/Rafael351_automatic_plans_v2_20261105/automatic_plans.json')
PREFS=Path('translations/rafael_B121_B140_visual_preferences_v5.json')

if __name__=='__main__':
    assert not ROOT.exists()
    native,plan,first,prefs=map(load,[NATIVE,PLAN,FIRST,PREFS])
    assert len(native['records'])==341 and native['pages']==344
    assert native['plan_sha256']==sha(PLAN.read_bytes())
    original_root=Path('work/analysis/Rafael351_native_v1_20261105')
    sheets=[original_root/f'B{b}_part{n}.png' for b,count in [(121,3),(122,1),(123,5),(124,1),(125,2),(126,1),(127,2)] for n in range(1,count+1)]
    sheets += [Path('work/analysis/Rafael351_native_v2_20261105')/f'B{b}_part1.png' for b in [121,123]]
    contacts=[Path('work/analysis/Rafael351_remaining_native_sheets_v1_20261105/contact_manifest.json'),
        Path('work/analysis/Rafael351_delta_native_sheets_v3_20261105/contact_manifest.json')]
    for path in contacts:
        contact=load(path)
        for item in contact['sheets']:
            p=Path(item['path']);assert sha(p.read_bytes())==item['sha256'];sheets.append(p)
    assert len(sheets)==30 and len(set(sheets))==30
    prior=load('work/analysis/Rafael351_native_baseline344_v1_20261105/compiled_native_pages.json')
    known_previews={p['preview_sha256'] for r in prior['records'] for p in (r['complete_native_English_display']['pages'] if r['kind']=='progressive' else [r['complete_native_English_display']])}
    duplicate_partial=sorted(original_root.glob('*B128*.png'))
    assert duplicate_partial and all(sha(p.read_bytes()) in known_previews for p in duplicate_partial)
    old={r['id']:r for r in first['records']};details=[]
    for r in plan['records']:
        changed=r['encoded_hex']!=old[r['id']]['encoded_hex']
        preference=prefs['records'].get(r['id'],{})
        details.append(dict(id=r['id'],logical_English=r['logical_English'],final_lines=r['lines'],
            source_reference=next(x['source_reference'] for x in native['records'] if x['id']==r['id']),
            changed_from_first_plan=changed,
            finding=preference.get('reason','Retain the complete readable paragraph and natural clause/phrase flow;no additional wrap or page-boundary change is needed.'),
            documented_dramatic_opening_reason=preference.get('documented_dramatic_opening_reason'),
            direct_native_body_visual_review=True,source_prose_not_shortened=True,new_credit=0))
    ROOT.mkdir(parents=True)
    save(ROOT/'body_visual_review.json',dict(native=str(NATIVE),native_sha256=sha(NATIVE.read_bytes()),
        final_plan=str(PLAN),final_plan_sha256=sha(PLAN.read_bytes()),records=details,
        body_records=341,final_body_pages=344,all344_final_body_pages_directly_viewed=True,
        directly_opened_readable_sheets=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in sheets],
        duplicate_unsealed_B128_previews_reused_by_exact_later_viewed_PNG_identity=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in duplicate_partial],
        no_failed_partial_B128_record_orassertion_reused_as_complete_proof=True,
        observed_guard_failure_fixed_only_for_exact_R128_R89_input=True,
        rejected_tavern_address_only_row=prefs['rejected_address_only_row'],
        automatic_opening_beat_exception=prefs['records']['DK4_MES_B136_R0147']['documented_dramatic_opening_reason'],
        fifth_gates_stored_allocations_typed_captions_names_representative_gameplay_andrelease_still_pending=True,
        offline_native_checks_not_observed_gameplay=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [NATIVE,PLAN,FIRST,PREFS,*contacts,Path(__file__)]}))
    print('Recorded341 native bodies/344 directly viewed final pages,30 opened sheets,exact duplicate partial-page reuse. Body review only;full fifth gates,stored/menu/name/gameplay/release work remain.')
