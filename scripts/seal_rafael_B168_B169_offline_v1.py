"""Seal directly viewed final pages and materialize only the two owned story blocks."""
from pathlib import Path
import sys

from dk4tool.patch.grand_race_menu_release import sha
from scripts import check_rafael_B168_pages_on1860_v1 as b168
from scripts import plan_rafael_B168_B169_display_v1 as display
from scripts import refine_rafael_B169_intervention_v1 as final
from scripts.audit_story_glyph_consistency import load, save
from scripts.rebuild_rafael_B166_B167_reviewed_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = display.ROOT
OUT = ROOT / 'offline_display_v1'
NATIVE = OUT / 'compiled_native_pages.json'
NAMES = OUT / 'native_name_planes.json'
VISUAL = OUT / 'visual_review.json'
CURRENT = display.CURRENT
TEMPLATE = Path('scripts/rebuild_reviewed_editorial_batch_v4.py')


def digest(path):
    return sha(Path(path).read_bytes())


def seal():
    assert not OUT.exists()
    proofs = [
        b168.ROOT / 'native_v1/compiled_native_pages.json',
        ROOT / 'native_delta_v1/compiled_native_pages.json',
        ROOT / 'native_visual_delta_v1/compiled_native_pages.json',
        ROOT / 'native_intervention_v1/compiled_native_pages.json',
    ]
    compiled = list(map(load, proofs))
    plan, doc, current = map(load, (final.PLAN, final.MANUSCRIPT, CURRENT))
    runtime = doc['runtime']
    assert runtime == current['runtime'] and not plan['failures']
    assert plan['manuscript_sha256'] == digest(final.MANUSCRIPT)
    assert [(len(d['records']), d['pages']) for d in compiled] == [(47, 49), (69, 69), (4, 4), (1, 1)]
    selected, sheets = {}, []
    for proof in compiled:
        assert proof['runtime'] == runtime and not proof['actual_gameplay']
        assert proof['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
        assert proof['complete_consumption_andpagination_exact']
        sheets.extend(proof['review_sheets'])
        selected.update({r['id']: r for r in proof['records']})
    assert len(sheets) == 14 and all(digest(s['path']) == s['sha256'] for s in sheets)
    assert len(selected) == len(plan['records']) == len(doc['records']) == 115
    for row, layout in zip(doc['records'], plan['records'], strict=True):
        assert row['id'] == layout['id']
        proof = selected[row['id']]
        assert row['english'] == proof['logical_English'] == layout['logical_English']
        assert proof['compiled_hex'] == layout['encoded_hex']
        assert all(proof[k] == row[k] for k in ('source_reference', 'current_reference'))
        pages = proof['complete_native_English_display']['pages']
        assert len(pages) == layout['expected_native_pages']
        assert all(digest(p['native_plane']) == p['native_plane_sha256'] for p in pages)
    assert sum(r['expected_native_pages'] for r in plan['records']) == 117
    names_path = ROOT / 'name_planes_v1/native_name_planes.json'
    prior_path = b168.A / 'Rafael_B166_B167_current1674_20261105/name_planes_v1/native_name_planes.json'
    names, prior_names = map(load, (names_path, prior_path))
    assert names['scoped_actors'] == 9 and names['runtime'] == runtime
    assert names['all_scoped_progressive_names_ASCII_complete_andfit_native216px']
    assert prior_names['runtime']['ARM9_sha256'] == runtime['ARM9_sha256']
    angelo = next(r for r in prior_names['planes'] if r['text'] == 'Angelo Puccini')
    assert angelo['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
    name_sheets = names['review_sheets']
    assert len(name_sheets) == 1 and digest(name_sheets[0]['path']) == name_sheets[0]['sha256']
    assert digest(angelo['preview']) == angelo['preview_sha256'] and digest(angelo['native_plane']) == angelo['native_plane_sha256']
    assert all(c['word'] not in (0x2100, 0x2200, 0x4100) for g in current['groups'] for c in g['all_source_commands'])
    evidence = {str(p): digest(p) for p in [final.MANUSCRIPT, final.PLAN, CURRENT, *proofs, names_path, prior_path, Path(__file__)]}
    OUT.mkdir()
    shared = dict(manuscript=str(final.MANUSCRIPT), manuscript_sha256=digest(final.MANUSCRIPT),
                  plan=str(final.PLAN), plan_sha256=digest(final.PLAN), runtime=runtime, new_credit=0)
    save(NATIVE, {**compiled[0], **shared, 'records': [selected[r['id']] for r in doc['records']],
                  'pages': 117, 'fresh_compiled_alignments': 460, 'review_sheets': sheets,
                  'direct_visual_review_pending': False, 'evidence': evidence})
    save(NAMES, {**names, 'actors': sorted({*names['actors'], 15}), 'scoped_actors': 10,
                 'distinct_strings': 10, 'planes': [*names['planes'], angelo],
                 'exact_reused_name_planes': names['exact_reused_name_planes']+1,
                 'direct_visual_review_pending': False, 'prior_Angelo_font_and_ARM9_dependency_exact': True,
                 'evidence': {**names['evidence'], **evidence}})
    save(OUT / 'menu.json', {**shared, 'offline_visual_approved': True, 'direct_view_pending': False,
                             'menus': [], 'typed_labels': 0, 'complete_clean_current_census_proves_no_choice_objects': True})
    save(OUT / 'styles.json', {**shared, 'objects': [], 'complete_clean_current_census_proves_no4100_objects': True})
    save(VISUAL, {**shared, 'native': str(NATIVE), 'native_sha256': digest(NATIVE),
                  'names': str(NAMES), 'names_sha256': digest(NAMES), 'body_pages': 117, 'scoped_names': 10,
                  'all_body_and_name_sheets_directly_viewed': True, 'all_final_direct_visual_findings_resolved': True,
                  'selected_body_previews': sheets, 'name_sheets': name_sheets,
                  'reused_Angelo_name_preview': dict(path=angelo['preview'], sha256=angelo['preview_sha256']),
                  'actual_gameplay': False, 'stored_and_focused_gameplay_pending': True, 'evidence': evidence})
    print('Sealed 117 directly viewed final pages and ten scoped nameplates for exact reconstruction.')


source = checked_text(previous, {
    "len(doc['records'])==186": "len(doc['records'])==115",
    "==len(native['records'])==186": "==len(native['records'])==115",
    '==(186,0,0)': '==(115,0,0)',
    'speech_count=186': 'speech_count=115',
    'ordinary_speeches=186': 'ordinary_speeches=115',
    'visual=load(OUT/': 'visual=load(OUT/',
    "visual['body_pages']==187": "visual['body_pages']==117",
    'Rafael B166–B167 complete 186-speech source-bound reconstruction': 'Rafael B168–B169 complete 115-speech source-bound reconstruction',
})


if __name__ == '__main__':
    if sys.argv[1:] == ['--seal']:
        seal()
    else:
        exec(compile(source, __file__+'::complete-two-block-reconstruction', 'exec'), globals())
