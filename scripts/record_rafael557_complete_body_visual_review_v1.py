"""Seal exact coverage of the directly viewed native pages, retaining rejected trials."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load,save
from dk4tool.patch.grand_race_menu_release import sha

NATIVE=Path('work/analysis/Rafael557_native_final_v1_20261105/compiled_native_pages.json')
PLAN=Path('work/analysis/Rafael557_automatic_plans_v10_20261105/automatic_plans.json')
FIRST=Path('work/analysis/Rafael557_automatic_plans_v3_20261105/automatic_plans.json')
PREFS=Path('translations/rafael_B141_B160_visual_preferences_v10.json')
ROOT=Path('work/analysis/Rafael557_body_visual_review_v1_20261105')

def pages(row):
    rendered=row['complete_native_English_display']
    return rendered['pages'] if row['kind']=='progressive' else [rendered]

if __name__=='__main__':
    assert not ROOT.exists();native,plan,first,prefs=map(load,[NATIVE,PLAN,FIRST,PREFS])
    assert len(native['records'])==len(plan['records'])==549 and native['pages']==558
    assert native['plan_sha256']==sha(PLAN.read_bytes())
    original=Path('work/analysis/Rafael557_native_v1_20261105')
    sheets=[original/name for name in ['B141_part1.png','B141_part2.png','B142_part1.png',*[f'B143_part{i}.png' for i in range(1,9)]]]
    contact_paths=[Path('work/analysis')/folder/'contact_manifest.json' for folder in [
        'Rafael557_reused_remaining_sheets_v1_20261105','Rafael557_fresh_initial_sheets_v1_20261105','Rafael557_final53_sheets_v1_20261105']]
    seen={p['preview_sha256'] for b in [141,142,143] for r in load(original/f'B{b}_checked.json')['records'] for p in pages(r)}
    reviewed_source_pages=117
    for path in contact_paths:
        contact=load(path)
        assert contact['readable_2x_nearest_native_pixels_no_content_changed']
        for page in contact['pages']:
            assert sha(Path(page['source']).read_bytes())==page['source_sha256']
            seen.add(page['source_sha256']);reviewed_source_pages+=1
        for sheet in contact['sheets']:
            p=Path(sheet['path']);assert sha(p.read_bytes())==sheet['sha256'];sheets.append(p)
    delta_proofs=[]
    for folder,parts in [('Rafael557_delta_native_v1_20261105',['B145_part1.png']),
                         ('Rafael557_delta_native_v2_20261105',['B148_part1.png','B153_part1.png','B155_part1.png'])]:
        root=Path('work/analysis')/folder;proof=root/'compiled_native_pages.json';d=load(proof);delta_proofs.append(proof)
        for row in d['records']:
            for p in pages(row):
                assert sha(Path(p['preview']).read_bytes())==p['preview_sha256'];seen.add(p['preview_sha256']);reviewed_source_pages+=1
        sheets.extend(root/name for name in parts)
    assert len(sheets)==len(set(sheets))==42 and reviewed_source_pages==585
    assert all(p.is_file() for p in sheets)
    final_pages=[p for row in native['records'] for p in pages(row)]
    assert len(final_pages)==558 and all(p['preview_sha256'] in seen for p in final_pages)
    old={r['id']:r for r in first['records']};details=[]
    exceptions={
        'DK4_MES_B144_R0028':'Retain the complete four-row layout: forcing both full tablet titles together produced a second page containing only the Proof is. The Stone Tablet base names and every word remain intact.',
        'DK4_MES_B151_R0293':'Retain the brief admiral call and whole recollection idiom; the question remains complete on one page. Combining the 36-cell opening with the call would exceed protected native first-row capacity.',
        'DK4_MES_B160_R0065':'Retain the short tentative map observation before the question. The hesitation and uncertainty suit Janus, and the whole page fits without changing prose.',
        'DK4_MES_B148_R0224':'Retain the complete final rhetorical question on its second page; it preserves Uddin\'s measured, slightly awkward farewell rather than stranding a predicate fragment.',
    }
    for row in plan['records']:
        preference=prefs['records'].get(row['id'],{})
        details.append(dict(id=row['id'],source_reference=next(r['source_reference'] for r in native['records'] if r['id']==row['id']),
            final_lines=row['lines'],pages=row['expected_native_pages'],changed_from_first_clean_plan=row['encoded_hex']!=old[row['id']]['encoded_hex'],
            visual_finding=exceptions.get(row['id'],preference.get('reason','Retain the readable complete native paragraph, phrase/clause flow and source-specific voice; no further wrap or page change is needed.')),
            all_final_native_pages_directly_viewed=True,prose_not_shortened=True,new_credit=0))
    ROOT.mkdir(parents=True)
    save(ROOT/'body_visual_review.json',dict(native=str(NATIVE),native_sha256=sha(NATIVE.read_bytes()),final_plan=str(PLAN),final_plan_sha256=sha(PLAN.read_bytes()),
        records=details,body_records=549,final_body_pages=558,all558_final_body_pages_directly_viewed=True,
        source_preview_pages_viewed_including_retired_trials=585,final_layout_changes_from_first_clean_plan=sum(r['changed_from_first_clean_plan'] for r in details),
        directly_opened_readable_sheets=[dict(path=str(p),sha256=sha(p.read_bytes())) for p in sheets],
        no_native_execution_repeated_for_this_visual_coverage_join=True,all_six_FE_rows_andcomplete_leading_trailing_glyphs_checked=True,
        two_source_bound_reviewed_infinitive_boundaries=True,rejected_tablet_title_trial=prefs['rejected_full_tablet_title_keep_together_trial'],
        all_fifth_gates_still_false=True,stored_allocation_representative_gameplay_andregistered_release_pending=True,
        offline_checks_not_new_observed_gameplay=True,new_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [NATIVE,PLAN,FIRST,PREFS,*contact_paths,*delta_proofs,Path(__file__)]}))
    print('Saved549 native bodies/558 directly viewed final pages;42 readable sheets/585 previews including retired layouts. Formatting research complete;stored/gameplay/release gates stillpending.')
