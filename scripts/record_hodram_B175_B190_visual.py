"""Save the remaining directly reviewed speech pages and five phrase/page findings."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_formatting_20261102')
MANUSCRIPT = ROOT / 'formatting_input.json'
NATIVE = Path('work/analysis/Hodram_B171_B190_native_20261104/remaining/compiled_native_pages.json')
SCOPE = {
    'DK4_MES_B175_R0041': dict(coherent_pairs=[['say', 'it'], ['it', 'but']], reason='The opening phrase breaks after say and leaves a sparse first row. Keep say it together while using the available width.'),
    'DK4_MES_B175_R0048': dict(coherent_pairs=[['realize', 'it'], ['it', 'but']], reason='The opening phrase breaks between realize and it. Preserve phrase continuity rather than a sparse row before the pronoun.'),
    'DK4_MES_B175_R0139': dict(page_clause='I will not go easy on you simply because you are a woman.', reason='The page boundary strands because you are a woman. Keep the complete assurance together on page two.'),
    'DK4_MES_B177_R0024': dict(coherent_pairs=[['it', 'seems'], ['seems', 'to'], ['to', 'be'], ['be', 'in'], ['in', 'the']], reason='The first row contains only It seems. Reflow the opening phrase without breaking the established tomb name or shortening the sentence.'),
    'DK4_MES_B179_R0047': dict(coherent_pairs=[['since', 'when']], reason='The question splits the phrase since when. Keep the phrase together while retaining the preceding hesitant address.'),
}


if __name__ == '__main__':
    output = ROOT / 'B175_B190_direct_visual_review_20261104.json'
    preferences = ROOT / 'B175_B190_visual_preferences_20261104.json'
    assert not output.exists() and not preferences.exists()
    doc, native = map(load, [MANUSCRIPT, NATIVE])
    rows = {r['id']: r for r in doc['records']}
    sheets = [r for r in native['review_sheets'] if r['block'] >= 175]
    assert len(sheets) == 29
    for sheet in sheets:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    bound = {}
    for ident, finding in SCOPE.items():
        row = rows[ident]
        bound[ident] = {**finding, 'bindings': {key: sha(row[key].encode('utf-8')) for key in ['english', 'source_hex', 'current_hex']}}
    save(preferences, dict(records=bound, manuscript=str(MANUSCRIPT), manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        layout_only_no_prose_shortening_orauthored_breaks=True, new_credit=0))
    save(output, dict(reviewed_blocks=list(range(175, 191)), reviewed_pages=266, review_sheets=sheets,
        all29_sheets_directly_viewed=True, individual_findings=bound, acceptable_remaining_pages=True,
        B179_andB190_FE_corrected_rows_complete_andreadable=True,
        controls_andheaders_not_in_body_only_previews=True,
        font_consistent_complete_first_internal_andfinal_characters_observed=True,
        findings_require_new_native_andvisual_checks=True, actual_gameplay=False, new_credit=0))
    print('Viewed 29 more sheets / 266 pages; all initial 440 pages viewed. Five further layout findings, prose unchanged.')
