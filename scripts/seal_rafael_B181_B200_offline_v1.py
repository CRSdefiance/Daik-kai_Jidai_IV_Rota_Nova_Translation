"""Bind all viewed body and name planes, then reconstruct the exact 20-block batch."""
from pathlib import Path
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save
from scripts.plan_rafael_B181_B187_story_v1 import ROOT, CURRENT, NAMES
from scripts.rebuild_rafael_B166_B167_reviewed_v1 import source as prior_rebuild, TEMPLATE
from scripts.source_locked_derivation_v5118 import checked_text


OUT = ROOT / 'offline_display_package_v1'
STORY_MANUSCRIPT = ROOT / 'story_formatting_manuscript_v4.json'
TOWN_MANUSCRIPT = ROOT / 'town_formatting_manuscript_v3.json'
STORY_PLAN = ROOT / 'story_plans_v4/automatic_plans.json'
TOWN_PLAN = ROOT / 'town_plans_v3/automatic_plans.json'
TOWN_VISUAL = ROOT / 'town_offline_visual_v1.json'
NAME_NATIVE = ROOT / 'all_name_planes_v1/native_name_planes.json'
STORY_NATIVE = [ROOT/f'{n}/compiled_native_pages.json' for n in ('story_native_v1', 'story_native_delta_v1')]
TOWN_NATIVE = [ROOT/f'{n}/compiled_native_pages.json' for n in ('town_native_v1', 'town_native_delta_v1')]


def digest(path):
    return sha(Path(path).read_bytes())


def seal():
    assert not OUT.exists()
    sm, tm, sp, tp, tv, names, current = map(load,
        (STORY_MANUSCRIPT, TOWN_MANUSCRIPT, STORY_PLAN, TOWN_PLAN, TOWN_VISUAL, NAME_NATIVE, CURRENT))
    runtime = current['runtime']
    assert all(doc['runtime'] == runtime for doc in (sm,tm,names))
    assert sm['blocks'] + tm['blocks'] == [g['block'] for g in current['groups']] == list(range(181,201))
    assert all(c['word'] not in (0x2100,0x2200,0x4100) for g in current['groups'] for c in g['all_source_commands'])
    assert sp['manuscript_sha256'] == digest(STORY_MANUSCRIPT) and tp['manuscript_sha256'] == digest(TOWN_MANUSCRIPT)
    assert tv['final_all_body_pages_directly_viewed'] and tv['final_source_and_native_encodings_exact']
    assert tv['evidence'][str(TOWN_PLAN)] == digest(TOWN_PLAN)
    body_proofs = list(map(load, (*STORY_NATIVE,*TOWN_NATIVE)))
    assert [p['pages'] for p in body_proofs] == [227,26,157,16]
    assert len({p['font_sha256'] for p in body_proofs}) == 1
    body_sheets, chosen = [], {}
    for doc in body_proofs:
        assert doc['runtime'] == runtime and not doc['actual_gameplay']
        assert doc['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert doc['complete_consumption_andpagination_exact'] and doc['FE_actual_glyph_row_membership_checked']
        chosen.update({r['id']: r for r in doc['records']})
        body_sheets.extend(doc['review_sheets'])
    sheets = body_sheets + names['review_sheets']
    assert all(digest(s['path']) == s['sha256'] for s in sheets)
    assert (names['scoped_actors'], names['distinct_strings'], names['fresh_name_planes'], names['exact_reused_name_planes']) == (29,23,15,8)
    assert names['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    assert len(chosen) == len(sp['records']) + len(tp['records']) == 384
    assert not sp['failures'] and not tp['failures']
    rows, plans = sm['records'] + tm['records'], sp['records'] + tp['records']
    for row, plan in zip(rows, plans, strict=True):
        assert row['id'] == plan['id']
        assert all(i['severity'] not in ('warning','error') for i in plan['base_QA']['issues'])
        proof = chosen[row['id']]
        assert all(row[k] == proof[k] for k in ('source_reference','current_reference','kind'))
        assert plan['encoded_hex'] == proof['compiled_hex'] and plan['logical_English'] == proof['logical_English'] == row['english']
        display = proof['complete_native_English_display']
        pages = [display] if row['kind'] == 'system-FE' else display['pages']
        assert len(pages) == plan['expected_native_pages'] == 1
        assert all(digest(p['native_plane']) == p['native_plane_sha256'] for p in pages)
    aziza = chosen['DK4_MES_B187_R0015']
    assert b"Castor Co., aren't you?" in bytes.fromhex(aziza['expanded_native_hex']).replace(b'\n', b' ')
    assert bytes.fromhex(chosen['DK4_MES_B187_R0091']['expanded_native_hex']) == b'Rafael Castor'
    assert sum(r['source_selector'] == 254 for r in rows) == 27
    OUT.mkdir()
    mf, pl, na = [OUT/f'{name}.json' for name in ('formatting_manuscript','automatic_plans','compiled_native_pages')]
    evidence = {str(p):digest(p) for p in (STORY_MANUSCRIPT,TOWN_MANUSCRIPT,STORY_PLAN,TOWN_PLAN,TOWN_VISUAL,
        *STORY_NATIVE,*TOWN_NATIVE,NAME_NATIVE,NAMES,CURRENT,Path(__file__))}
    save(mf,{**sm,'blocks':sm['blocks']+tm['blocks'],'records':rows,'physical_speech_objects':384,
        'ordinary_speech_objects':384,'typed_choice_objects':0,'source_staged_FE_panels':0,
        'source_F_literal_token_counts':sm['source_F_literal_token_counts'],'evidence':evidence})
    save(pl,{**sp,'manuscript':str(mf),'manuscript_sha256':digest(mf),'records':plans,'pages':384,
        'complete_source_story_and_town_plan_evidence':evidence})
    save(na,{**body_proofs[0],'manuscript':str(mf),'manuscript_sha256':digest(mf),'plan':str(pl),'plan_sha256':digest(pl),
        'records':[chosen[r['id']] for r in rows],'pages':384,'review_sheets':body_sheets,
        'fresh_compiled_alignments':1536,'direct_visual_review_pending':False,'evidence':evidence})
    shared = dict(manuscript=str(mf),manuscript_sha256=digest(mf),plan=str(pl),plan_sha256=digest(pl),runtime=runtime,new_credit=0)
    save(OUT/'menu.json',{**shared,'offline_visual_approved':True,'direct_view_pending':False,'menus':[],'typed_labels':0,
        'complete_clean_current_census_proves_no_choice_objects':True})
    save(OUT/'styles.json',{**shared,'objects':[],'complete_clean_current_census_proves_no4100_objects':True})
    save(OUT/'visual_review.json',{**shared,'native':str(na),'native_sha256':digest(na),'body_pages':384,
        'scoped_name_count':29,'distinct_scoped_name_strings':23,'source_staged_FE_pages':0,'source_FE_pages':27,
        'all_body_and_name_sheets_directly_viewed':True,'all_final_direct_visual_findings_resolved':True,
        'actual_gameplay':False,'sheets':sheets,'story_fresh_refined_pages':26,'story_exact_prior_pages_reused':201,
        'stored_branch_loader_and_gameplay_checks_pending':True,
        'names':str(NAME_NATIVE),'names_sha256':digest(NAME_NATIVE),'evidence':evidence})
    print('384 exact viewed pages and 29 scoped labels sealed for stored and gameplay checks.')


rebuild = checked_text(prior_rebuild,{
    "len(doc['records'])==186": "len(doc['records'])==384",
    "==len(native['records'])==186": "==len(native['records'])==384",
    '==(186,0,0)': '==(384,0,0)',
    'len(changed)==2': 'len(changed)==20',
    'speech_count=186': 'speech_count=384',
    'ordinary_speeches=186': 'ordinary_speeches=384',
    'menu_labels=0,changed_blocks=2': 'menu_labels=0,changed_blocks=20',
    "visual['body_pages']==187": "visual['body_pages']==384",
    'Rafael B166–B167 complete 186-speech': 'Rafael B181–B200 complete 384-speech',
})

if __name__ == '__main__':
    if sys.argv[1:] == ['--seal']:
        seal()
    else:
        exec(compile(rebuild,__file__+'::same-exact-20-block-reconstruction', 'exec'), globals())
