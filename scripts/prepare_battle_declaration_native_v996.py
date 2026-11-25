"""Record176 visual reviews,exact warning decisions and a macro-safe paragraph compiler."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from unittest.mock import patch

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.battle_declaration_layout_v996 import compiled, IDS, PROFILE
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_declaration_v996')
FONT = Path('work/analysis/battle_declaration_v995b/native_font_proof.json')
OLD = Path('translations/battle_declaration_editorial_manuscript_v2.json')
NEW = Path('translations/battle_declaration_editorial_manuscript_v3.json')


def rejects(row):
    try:
        compiled(row)
    except ValueError:
        return True
    raise AssertionError('Unsafe compiler input accepted')


def main():
    assert not NEW.exists() and not (ROOT/'visual_review.json').exists()
    doc, font = read(OLD), read(FONT)
    assert font['manuscript_sha256'] == sha(OLD.read_bytes())
    assert font['producer_sha256'] == sha(Path('scripts/probe_battle_declaration_fonts_v995b.py').read_bytes())
    assert len(font['cases']) == 176 and font['complete_native_font_canvases'] == 176
    assert font['all7_templates_all20_native_faction_label_expansions'] == 140
    assert font['all15_static_complete_native_font_cases'] == 15
    assert font['all22_input_templates_reject_authored_or_pregenerated_LF_before_macro_processing']
    sheets_path = ROOT/'all176_review_sheet_manifest.json'
    sheets = read(sheets_path)
    assert sheets['native_font_proof_sha256'] == sha(FONT.read_bytes())
    assert [i for row in sheets['sheets'] for i in row['case_indices']] == list(range(176))
    for row in sheets['sheets']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    by_id = {row['message_id']: row for row in doc['records']}
    for case in font['cases']:
        row = by_id[case['message_id']]
        assert compiled(row).hex() == case['compiled_template_hex']
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
        assert case['whole228x64_native_independent_font_and_input_bitmap_guards_pass']
        assert case['full_native_byte_consumption_and_all_leading_trailing_letters_pass']
        value = case['faction_name_case']
        expected = row['english'].replace('%s', value['label']) if value else row['english']
        assert ' '.join(case['generated_native_lines']) == expected
    warnings = []
    for finding in font['line_boundary_findings_requiring_review']:
        i = finding['case_index']
        case = font['cases'][i]
        value = finding['faction']
        assert case['message_id'] == finding['message_ID'] and value is not None
        assert case['generated_native_lines'] == finding['lines']
        if value['kind'] == 'native-company-label':
            assert finding['message_ID'] in (1897, 1901)
            assert finding['lines'][-1] == value['label']+'?'
            assert len(finding['lines']) == 2 and finding['weak_line_end_indices'] == [0]
            assert finding['lines'][0].endswith(' on')
            if finding['single_word_final_row']:
                assert len(value['label'].split()) == 1 and len(value['label']) >= 8
            reason = ('The complete source-verified faction name occupies its own automatically generated row after the confirmation predicate. This is a complete proper name,not an isolated letter,broken word or abbreviation tail. All glyphs and the uniform x6 cell origin pass. The on/name boundary is readable in this target-identification question;no authored staging or padding was added.')
        else:
            assert value['kind'] == 'synthetic-layout-stress-not-real-faction'
            assert value['label'] in ('ABCDEFGHIJKLMNOPQRSTUVW', 'Northern Compass Co.')
            assert finding['message_ID'] in (1897, 1898, 1899, 1900, 1901)
            reason = ('Synthetic long-name stress case,not a claim that this faction exists or that a player has earned an encounter. The unbroken complete name is allowed on a separate row;the native formatter retains every word within35 cells and four rows. The on/name boundary remains comprehensible. No real source label is shortened or substituted to satisfy this test.')
        warnings.append({'case_index': i, 'message_ID': case['message_id'], 'faction_name_case': value,
                         'generated_native_lines': finding['lines'],
                         'findings': (['single_word_final_row'] if finding['single_word_final_row'] else [])+
                                     (['weak_line_end'] if finding['weak_line_end_indices'] else []),
                         'disposition': 'reviewed-narrow-case-waiver', 'reason': reason,
                         'preview_sha256': case['preview_sha256']})
    assert len(warnings) == 27
    negatives = {}
    sample = deepcopy(by_id[1909])
    for key, english in {
        'pregenerated_literal_I_LF_macro_collision': "I don't know who they are. Should I\n  tell them we're going to attack?",
        'authored_alignment': 'Should  I tell them?',
        'authored_leading_space': ' Should I tell them?',
        'tab_control': 'Should\tI tell them?',
        'full_width_I': 'Ｉ will ask.',
        'native_pronoun_macro_without_source': 'IC will ask.',
        'native_faction_macro_without_source': 'FI will ask.',
        'unsupported_percent_command': 'We have 5% of the fleet.',
        'translator_control_markup': 'Wait.{LB}Ask them.',
        'oversized_scratch_input': 'A'*220,
    }.items():
        negatives[key] = rejects({**sample, 'english': english})
    named = deepcopy(by_id[1897])
    for key, fields in {
        'lost_real_faction_argument': {'english': 'May we declare war?'},
        'duplicated_real_faction_argument': {'english': 'May we declare war on %s and %s?'},
        'wrong_conversion': {'english': 'Declare war on %d?'},
        'declared_argument_count_mismatch': {'native_argument_count': 0},
        'unsupported_source_ID': {'message_id': 1911},
    }.items():
        negatives[key] = rejects({**named, **fields})
    assert len(negatives) == 15 and all(negatives.values())
    # Compilation itself must use neither an emulator nor any historical ROM.
    with patch('dk4tool.rom.nds.NdsImage.open', side_effect=AssertionError('Pure paragraph compilation cannot read ROMs')):
        assert all(compiled(row).hex() == font['generated_paragraph_templates'][str(row['message_id'])]['compiled_hex'] for row in doc['records'])
    review = ROOT/'visual_review.json'
    save(review, {'native_font_proof': str(FONT), 'native_font_proof_sha256': sha(FONT.read_bytes()),
        'all176_complete_previews_visually_reviewed_via8_full_canvas_sheets': True,
        'review_sheet_manifest': str(sheets_path), 'review_sheet_manifest_sha256': sha(sheets_path.read_bytes()),
        'all27_line_boundary_findings': warnings, 'blocking_errors': 0, 'unwaived_warnings': 0,
        'all15_compiler_rejection_controls': negatives,
        'all22_compilations_exact_with_all_ROM_open_calls_forbidden': True,
        'previous_failed_probe': 'work/analysis/battle_declaration_v995/successor_provenance.json',
        'scope': 'Complete original228x64 native text canvases and every real faction label plus odd/even/long/short stress variants. Actual RGB/modal rectangle/portrait/buttons/pagination/cancellation/acceptance/return and registered integration remain pending.',
        'compiler': 'scripts/battle_declaration_layout_v996.py',
        'compiler_sha256': sha(Path('scripts/battle_declaration_layout_v996.py').read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()), 'visual_review_pending': False,
        'completed_entries_added': 0, 'full_goal_complete': False})
    native = deepcopy(doc)
    native.update(consumer_layout_profile=PROFILE, formatting_review_pending=False,
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        status='22-native-font-and-case-scoped-layout-approved-copy-repack-release-actual-pending',
        reviewed_research_manuscript=str(OLD), reviewed_research_manuscript_sha256=sha(OLD.read_bytes()),
        native_font_proof=str(FONT), native_font_proof_sha256=sha(FONT.read_bytes()),
        visual_review_proof=str(review), visual_review_proof_sha256=sha(review.read_bytes()),
        native_runtime_proof='work/analysis/battle_declaration_v993c/native_runtime_verification.json',
        native_runtime_proof_sha256=sha(Path('work/analysis/battle_declaration_v993c/native_runtime_verification.json').read_bytes()),
        actual_UI_geometry_scene_controls_and_registered_release_pending=True)
    for row in native['records']:
        row['review']['formatting'] = True
        selected = [w for w in warnings if w['message_ID'] == row['message_id']]
        if selected:
            row['case_bound_qa_waivers'] = selected
            row['qa_waivers'] = sorted({f for w in selected for f in w['findings']})
            row['qa_waiver_reason'] = 'Only the exact name-expansion cases listed in case_bound_qa_waivers;complete proper names or synthetic long-name stress remain fully readable. No missing-letter,bounds,control,blank-page or unsupported real-name waiver.'
        row['compiled_hex'] = compiled(row).hex()
    validate_natural_dialogue_batch(native)
    assert tuple(row['message_id'] for row in native['records']) == IDS
    save(NEW, native)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1174 and ledger['records_with_source_and_prose_pass'] == 1199
    save(ROOT/'editorial_ledger_before_native_review.json', ledger)
    ledger['active_source_prose_drafts']['manuscripts'][-1] = str(NEW)
    ledger['battle_declaration_v996'] = {'status': native['status'], 'manuscript': str(NEW),
        'native_font_proof': str(FONT), 'visual_review_proof': str(review),
        'complete_native_font_cases': 176, 'real_faction_expansions': 140, 'static_cases': 15,
        'synthetic_layout_cases': 21, 'reviewed_case_bound_warnings': 27,
        'completed_entries_added': 0, 'source_prose_reviews_added': 0}
    rule = 'Before original COMMON speech macro expansion,compile new prose as one logical paragraph. A literal I immediately followed by LF can be a native pronoun command;do not prewrap before that consumer. Preserve real clean-source IC/control commands and use the mapped post-expansion formatter. Keep other consumers and historical batches on their independently verified contracts.'
    assert rule not in ledger['formatting_watchlist']['requirements']
    ledger['formatting_watchlist']['requirements'].append(rule)
    ledger['formatting_watchlist']['latest_battle_macro_boundary_proof'] = str(review)
    checkpoint = ('V996 approves22 battle/declaration paragraphs for native font/layout after all176 complete228x64 canvases and eight full-canvas sheets:140 real faction expansions,21 odd/even/short/long stress cases and15 static cases. All27 target-name/stress boundary findings have exact case-bound written decisions;15 unsafe compiler controls fail closed. A rejected prewrapped1909 probe exposed literal I followed by LF being parsed as a pronoun;the pure compiler now feeds all22 as one paragraph before native expansion/wrapping. The named-faction balancing membership remains useful to prevent tiny Co./Fleet tails;runtime footprints and prior54904x2 selector/3668 modal/140 status checks remain pinned. No ROM or patch built,no actual scene credit. Native repack/copies,registered integration/exact patch and actual confirmation/announcement/return verification remain pending. V987 current;1174 complete,1199 source/prose;global editorial goal and separate graphics/all18 plaques remain open.')
    ledger['latest_checkpoint'] = checkpoint
    ledger['research_checkpoints'].append({'id': 'V996-battle-declaration22-native-layout', 'proof': str(review),
        'manuscript': str(NEW), 'completed_entries_added': 0, 'source_prose_reviews_added': 0,
        'previous_goal_turn_classification': 'progress:22 source/prose reviews and exact fixed-footprint runtime matrices saved and archived',
        'this_goal_turn_classification': 'progress:176 complete font canvases reviewed;real macro-boundary defect caught and fixed in compiler;27 precise warning decisions and15 rejection controls',
        'full_goal_complete': False})
    before = read(ROOT/'editorial_ledger_before_native_review.json')
    for key in ('current_integrated_candidate', 'source_pins', 'current_native_relocation_reference', 'unresolved_graphics_work',
                'older_record_reaudit_after_full_editorial_goal', 'raw_source_coverage_revisit', 'approved_name_roles'):
        assert ledger[key] == before[key]
    save(ledger_path, ledger)
    doc_path = Path('docs/battle_declaration_v996_native_checkpoint.md')
    assert not doc_path.exists()
    with doc_path.open('x', encoding='utf-8') as f:
        f.write('# V996: battle/declaration complete native font review\n\n'+checkpoint+'\n\n')
        f.write('## Macro ordering rule\n\n'+rule+'\n\nThe failed probe and all its partial renders remain research-only.1909 actual gameplay must specifically verify the complete literal I at the generated line end. Candidate production compilation contains no generated LF;the native speech path inserts it after macro processing.\n\n')
        f.write('## Remaining required work\n\nNative full copies/cache sequencing,exact COMMON repack,registered full-stack ROM and clean-input patch,title/New Game regression and representative original known/unknown/ready questions and announcements. Verify speaker/portrait,full native and RGB text,bounds,choice cancellation/acceptance,dismissal and normal scene return before completion credit.\n')
    with Path('docs/natural_dialogue_workflow.md').open('a', encoding='utf-8') as f:
        f.write('\n\n## COMMON speech macro expansion before word wrapping\n\n'+rule+' Source-bound proof:V996 battle/declaration1889-1910. The live-glyph test catches a real ordering defect:prewrapped literal I plus LF became native pronoun bytes966C. Do not change the global I/IC guard to conceal this error;it preserves original executable controls. Compile one paragraph for this mapped speech consumer and verify the output of original expansion followed by wrapping. Embedded Deck comments,raw selectors and story profiles retain their own proven contracts. See [V996 native proof](battle_declaration_v996_native_checkpoint.md).\n')
    for p in map(Path, ('docs/translation_progress.md', 'docs/editorial_review_goal.md', 'docs/todo.md', 'docs/known_issues.md')):
        with p.open('a', encoding='utf-8') as f:
            f.write('\n\n## V996: battle/declaration native font and macro ordering\n\n'+checkpoint+' See [V996 native checkpoint](battle_declaration_v996_native_checkpoint.md).\n')
    archive = Path('E:/Rota Nova translations/Editorial review/V996 Battle declaration native font review')
    assert not archive.exists()
    files = [NEW, FONT, review, sheets_path, Path(__file__), Path('scripts/battle_declaration_layout_v996.py'),
        Path('scripts/probe_battle_declaration_fonts_v995.py'), Path('scripts/probe_battle_declaration_fonts_v995b.py'),
        Path('work/analysis/battle_declaration_v995/successor_provenance.json'), doc_path, ledger_path,
        Path('docs/natural_dialogue_workflow.md')]
    files += [Path(c['preview']) for c in font['cases']]+[Path(s['path']) for s in sheets['sheets']]
    copied = []
    for source in dict.fromkeys(files):
        target = archive/source.absolute().relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        assert not target.exists()
        copy2(source, target)
        assert source.read_bytes() == target.read_bytes()
        copied.append({'source': str(source), 'archive': str(target), 'sha256': sha(target.read_bytes())})
    save(ROOT/'archive_manifest.json', {'files': copied, 'all_hashes_verified': True,
        'complete_native_previews_archived': 176, 'actual_gameplay_screenshots_added': 0,
        'completed_entries_added': 0, 'full_goal_complete': False})
    print('V996:22 native-format-approved paragraphs;176 complete font canvases,27 exact warning decisions,15 rejection controls.1174 complete,1199 source/prose. ROM/copies/patch/actual scenes pending;goal active.')


if __name__ == '__main__':
    main()
