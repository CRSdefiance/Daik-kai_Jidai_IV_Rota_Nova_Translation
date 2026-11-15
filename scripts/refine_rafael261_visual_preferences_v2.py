"""Save the complete 256-page visual pass and exact phrase/page findings."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from dk4tool.patch.grand_race_menu_release import sha

DOC = Path('translations/rafael_B85_B100_contextual_editorial_manuscript_v2.json')
NATIVE = Path('work/analysis/Rafael261_native_v1_20261105/compiled_native_pages.json')
OUT = Path('translations/rafael_B85_B100_visual_preferences_v2.json')

if __name__ == '__main__':
    assert not OUT.exists()
    doc, native = map(load, [DOC, NATIVE])
    assert len(native['records']) == 255 and native['pages'] == 256 and native['fresh_compiled_alignments'] == 1020
    assert native['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass']
    assert native['complete_consumption_andpagination_exact']
    for sheet in native['review_sheets']:
        assert sha(Path(sheet['path']).read_bytes()) == sheet['sha256']
    rows = {r['id']: r for r in doc['records']}
    phrases = {(86, 248): ["'What happens if I do this?'"],
        (86, 272): ['Just thinking about it is marvelous!'],
        (87, 206): ["You're welcome to,"],
        (88, 39): ['Nice to meet you.'], (88, 82): ['help you out...'],
        (88, 140): ['Come on,'], (90, 14): ["wonderful, aren't they?"],
        (90, 23): ['a fleet of my own,'], (91, 98): ["Let's get moving."],
        (93, 54): ['Some of these seeds']}
    records, findings = {}, []
    for pair in sorted(set(phrases) | {(86, 75)}):
        ident = f'DK4_MES_B{pair[0]}_R{pair[1]:04d}'
        row = rows[ident]
        entry = dict(bindings={k: sha(row[k].encode('utf-8')) for k in ['source_hex', 'current_hex', 'english']})
        if pair == (86, 75):
            entry['page_clause'] = 'Every so often, he makes that infernal racket.'
            reason = 'The viewed second page contains only the object that infernal racket. Keep the complete final sentence together across the page turn, preserving every prose character.'
        else:
            entry['line_phrases'] = phrases[pair]
            reason = 'The viewed wrap splits a short question tag, greeting, phrasal verb or connected clause, or leaves a sparse opening. Keep this exact phrase together; ordinary breaks remain formatter-owned.'
        records[ident] = entry
        findings.append(dict(id=ident, source_reference=row['source_reference'], current_reference=row['current_reference'], finding=reason, preference=entry))
    assert len(findings) == 11
    save(OUT, dict(format='dk4-source-scoped-visual-preferences-v1', records=records,
        previous_preferences='translations/rafael_B85_B100_visual_preferences_v1.json',
        visual_basis=str(NATIVE), visual_basis_sha256=sha(NATIVE.read_bytes()), findings=findings,
        all_prose_source_controls_andmacros_unchanged=True, new_credit=0))
    save(NATIVE.parent/'direct_visual_review_with_findings.json', dict(native_proof=str(NATIVE), native_proof_sha256=sha(NATIVE.read_bytes()),
        all256_native_pages_andall_readable_sheets_directly_viewed=True, sheets=native['review_sheets'],
        complete_glyphs_bounds_consumption_andpagination_pass=True, layout_findings=findings,
        final_layout_approval_pending_for11_records=True,
        justified_layout_retentions='Complete expressive reactions may be short. Retain natural sentence boundaries, full names and item names; the remaining paragraphs read cleanly without missing glyphs or artificial legacy breaks.',
        fullwidth_Latin_andEnglish_questionmark_artifacts_now_normal_ASCII=True,
        offline_only_not_gameplay=True, all_fifth_gates_still_false=True, new_credit=0))
    print('Viewed all256 native pages;11 scoped layout findings saved without changing prose.')
