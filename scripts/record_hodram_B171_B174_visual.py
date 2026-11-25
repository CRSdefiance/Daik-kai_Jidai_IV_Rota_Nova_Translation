"""Save direct contact-sheet findings and byte-bound layout preferences."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Hodram_B171_B190_formatting_20261102')
MANUSCRIPT = ROOT / 'formatting_input.json'
SCOPE = {
    'DK4_MES_B171_R0075': dict(one_page=True, reason='The second page contains only the final headwind phrase. Try the complete 128-character paragraph on one native-width page.'),
    'DK4_MES_B171_R0095': dict(page_clause="and it won't fit a small ship.", reason='The second page contains only a small ship. Keep the complete size restriction together.'),
    'DK4_MES_B171_R0098': dict(page_clause='so only large ships can carry it.', reason='The second page contains only ships can carry it. Start the complete ship-size consequence on page two.'),
    'DK4_MES_B171_R0101': dict(one_page=True, reason='The 120-character question strands behind them? on page two. Use the available native width for the whole question.'),
    'DK4_MES_B173_R0058': dict(page_clause='This would be a great undertaking for us!', reason='The final sentence breaks between great and undertaking. Keep that complete sentence together on page two.'),
    'DK4_MES_B173_R0138': dict(page_clause="It's simply a way to win a woman's heart... Heh heh.", reason='The page boundary separates a woman\'s from heart. Keep the complete final explanation and chuckle together.'),
}


if __name__ == '__main__':
    output = ROOT / 'B171_B174_direct_visual_review_20261104.json'
    preferences = ROOT / 'B171_B174_visual_preferences_20261104.json'
    assert not output.exists() and not preferences.exists()
    doc = load(MANUSCRIPT)
    rows = {r['id']: r for r in doc['records']}
    sheets = []
    for block, count in [(171, 3), (172, 6), (173, 4), (174, 4)]:
        folder = Path('work/analysis/Hodram_B171_B190_native_20261102/initial' if block == 171 else 'work/analysis/Hodram_B171_B190_native_20261104/remaining')
        for part in range(1, count + 1):
            path = folder / f'B{block}_part{part}.png'
            sheets.append(dict(path=str(path), sha256=sha(path.read_bytes()), directly_viewed=True))
    bound = {}
    for ident, finding in SCOPE.items():
        row = rows[ident]
        bound[ident] = {**finding, 'bindings': {key: sha(row[key].encode('utf-8')) for key in ['english', 'source_hex', 'current_hex']}}
    save(preferences, dict(records=bound, manuscript=str(MANUSCRIPT), manuscript_sha256=sha(MANUSCRIPT.read_bytes()),
        layout_only_no_prose_shortening_orauthored_breaks=True, new_credit=0))
    save(output, dict(reviewed_blocks=[171, 172, 173, 174], reviewed_pages=174, review_sheets=sheets,
        individual_findings=bound, acceptable_remaining_pages=True,
        B172_FE_corrected_rows_complete_andreadable=True, controls_andheaders_not_in_body_only_previews=True,
        font_consistent_complete_first_internal_andfinal_characters_observed=True,
        findings_require_new_native_andvisual_checks=True, actual_gameplay=False, new_credit=0))
    print('Viewed 17 sheets / 174 pages; six layout findings, prose unchanged.')
