"""Seal the compiled formatter and font evidence;leave release gates open."""
from pathlib import Path
from shutil import copy2
from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_compiled_checkpoint_v1139')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V1139 Compiled duel formatter native fonts')


def main():
    assert not ROOT.exists() and not ARCHIVE.exists()
    compiler_path = Path('work/analysis/duel_layout_native_v1133/compiler_provenance.json')
    matrix_path = Path('work/analysis/duel_native_layout_v1134/compiled_native_DP_matrix.json')
    fonts_path = Path('work/analysis/duel_compiled_fonts_v1136c/compiled_native_complete_fonts.json')
    isa_path = Path('work/analysis/duel_native_ISA_v1137b/exact_binary_ISA_and_reproduction.json')
    compiler, matrix, fonts, isa = [read(path) for path in (compiler_path, matrix_path, fonts_path, isa_path)]
    assert compiler['binary_bytes'] == 1432
    assert sha(Path(compiler['binary']).read_bytes()) == compiler['binary_sha256'] == isa['verified_binary_SHA256']
    assert matrix['all4700_native_outputs_match_independent_physical_phase_DP'] and len(matrix['cases']) == 4700
    assert len(matrix['all13_invalid_inputs_reject_without_changing_input_or_guards']) == 13
    assert matrix['native_memory_write_bounds']['input_high'] <= 1024
    assert matrix['native_memory_write_bounds']['deepest_stack_bytes'] == 144
    assert fonts['unique_complete_font_cases'] == len(fonts['cases']) == 1356
    assert fonts['native_compiled_layout_and_private_Y_execute_without_Python_replacement']
    for case in fonts['cases']:
        assert case['whole_source_plane_exact_to_independently_laid_out_complete_words_and_font']
        assert case['compiled_native_formatter_has_complete_correct_visible_layout']
        assert case['native_font_consumes_complete_generated_string']
        assert not case['glyph_ink_absent_from_final_crop']
        assert not case['glyphs_crossing_source_rows'] and not case['glyphs_outside_final_visible_crop']
        assert not case['first_glyph_damaged_by_later_stride_spill']
    assert isa['same1432byte_code_with_and_without_debug_symbols']
    assert isa['all_code_Thumb1_or_ARMv5_BL_BLX_no_Thumb2_or_ARMv6_NOP']
    assert len(isa['instructions']) == 656
    candidate = Path(fonts['candidate'])
    assert sha(candidate.read_bytes()) == fonts['candidate_sha256'] == '64b1da09fe0f75007af73b0f44a39ce9d2d3c6dedbb70cf6c0ca20223a7f1c29'
    manuscript_path = Path('translations/duel_editorial_manuscript_v3.json')
    assert all(not row['review']['formatting'] for row in read(manuscript_path)['records'])
    ROOT.mkdir(parents=True)
    previews = fonts['research_previews']
    assert len(previews) == 12
    sheet = Image.new('RGB', (1728, 6 * 198), '#263238')
    for index, preview in enumerate(previews):
        path = Path(preview['path'])
        assert sha(path.read_bytes()) == preview['sha256']
        sheet.paste(Image.open(path).convert('RGB'), ((index % 2) * 864, (index // 2) * 198))
    sheet_path = ROOT / 'compiled_native_font_research_sheet.png'
    sheet.save(sheet_path)
    summary = (
        'V1139 implements the dedicated duel24x3 word-layout algorithm as readable freestanding C, '
        'compiled reproducibly for ARM946 Thumb with project-local pinned Zig0.13.0. The1432-byte '
        'native formatter matches independent dynamic programming for4700 cases:4160 source-slot '
        'combinations and540 legal-name stress cases. All prior source outputs remain exact. '
        'Physical pair-flush cells are included in the24-column bound. Thirteen malformed/overlong '
        'inputs reject without text or guard changes;native writes stay inside the caller-owned '
        '1024-byte buffer and144-byte private stack depth. A real overlong-workspace alias was '
        'caught and corrected by length preflight. Native compiled code now runs after original '
        'macro expansion and before the original ASCII/CP932 painters,without Python text or Y '
        'replacement. All1356 distinct expanded-message/font cases have complete independent '
        '4bit pixel planes,uniform margins,full first/last letters and exact original144x36 crops. '
        'The4700 matrix projects to1140 distinct source inputs plus216 additional stress inputs; '
        'nonargument messages are not counted repeatedly as new font coverage. Two compiler builds '
        'with/without debug symbols produce identical1432 bytes;ELF code/data mapping identifies656 '
        'Thumb1/ARMv5 instructions and only two internal functions,no library calls. Research '
        'trampoline/code addresses are CPU-only and are not approved ROM storage. Production '
        'caller filtering,existing owned placement,relink/native verification,13 ordinary escape '
        'notices,registered combined ROM/exact patch and original duel scenes remain pending. '
        'No playable ROM,patch,registry or prose changed. All33 formatting gates remain false; '
        '1196 complete,1267 source/prose-reviewed,no completion credit. V1105 experimental,V997 '
        'fully scene-verified,canonical unchanged. Full editorial and separate graphics scopes '
        'stay active;the global uppercase weak-word audit is not replaced by this scoped formatter.'
    )
    checkpoint_path = ROOT / 'checkpoint.json'
    save(checkpoint_path, {'summary': summary, 'compiler_provenance': str(compiler_path),
        'native_DP_matrix': str(matrix_path), 'complete_native_font_proof': str(fonts_path),
        'exact_binary_ISA': str(isa_path), 'research_sheet': str(sheet_path),
        'research_sheet_sha256': sha(sheet_path.read_bytes()),
        'research_previews_not_actual_emulator_or_guide_screenshots': True,
        'CPU_only_trampoline_not_production_hook_or_owned_ROM_placement': True,
        'no_ROM_patch_or_completion_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1196 and ledger['records_with_source_and_prose_pass'] == 1267
    ledger['duel_prose_v1103'].update(compiled_formatter_checkpoint=str(checkpoint_path),
        compiled_formatter_source=compiler['source'], compiled_formatter_source_sha256=compiler['source_sha256'],
        compiled_formatter_binary_bytes=1432, compiled_formatter_binary_sha256=compiler['binary_sha256'],
        compiled_formatter_ISA=str(isa_path),
        formatter_next_action='Place and relink native code in verified existing owned storage;install exact caller filter;verify fonts/integration/exact patch and original duel scenes.',
        formatting_status='compiled-layout-and-original-native-fonts-pass;production-filter-owned-placement-integration-and-actual-open')
    ledger['formatting_watchlist']['duel_compiled_native24x3'] = {
        'layout_proof': str(matrix_path), 'font_proof': str(fonts_path), 'ISA_proof': str(isa_path),
        'status': 'native-code-CPU-font-proven;production-hook-ROM-and-original-scenes-open',
        'all33_formatting_gates_still_false': True}
    ledger['latest_checkpoint'] = summary
    save(ledger_path, ledger)
    doc = Path('docs/duel_v1139_compiled_formatter_checkpoint.md')
    doc.write_text('# V1139: compiled native duel formatter and complete fonts\n\n' + summary +
        '\n\n## Runtime contract and provenance\n\n'
        'The formatter consumes one canonical paragraph after original macro expansion. It '
        'preserves all text and substitutions,uses complete words,and scores punctuation,weak '
        'word endings,kept phrases and orphaned final words. It budgets the actual24x3 view '
        'and the trailing ASCII batch after the last double-byte glyph. Workspace begins at '
        'expanded-buffer+128 and remains before the original private font context at+1024. '
        'Source calls use a bounded32-word contract;all source/default and1-16byte legal-name '
        'stress expansions are covered. Invalid paragraphs return zero unchanged.\n\n'
        'The compiler is pinned and project-local,with exact executable/source/linker/ELF/binary '
        'hashes and argument lists in compiler_provenance.json. The symbol build reproduces '
        'the exact release-style binary and supplies explicit code/literal boundaries. A '
        '16bit RSBS immediate-zero decode is the Thumb1 NEG alias,validated by its opcode; '
        'no unsupported ISA was waived. Source debug paths do not alter native bytes. Final '
        'ROM addresses require relinking and another native check,not blind rebasing.\n\n'
        'The CPU font trampoline calls compiled native layout,sets private vertical origin '
        'from its native row result,then calls the unmodified original painter. Python only '
        'reads and compares. SDK clear and UI registration are explicit models,and GPU crop '
        'submissions are captured rather than displayed. The first font run reached the '
        '100K instruction ceiling in the original painter;its terminal successor uses the '
        'declared3M bound. Native completion,full register/stack ABI,pixels and crops then pass. '
        'This is not emulator playback,hardware verification or a playable build.\n\n'
        'All18 plaques and the broader graphics audit remain unfinished. The older-record '
        're-audit follows the full editorial goal. No progress credit was awarded for these '
        'runtime tests;the source/prose and completion counts remain unchanged.\n', encoding='utf-8')
    for filename in ('docs/translation_progress.md', 'docs/todo.md', 'docs/known_issues.md'):
        with Path(filename).open('a', encoding='utf-8') as stream:
            stream.write('\n\n## V1139: compiled duel formatter and native fonts\n\n' + summary +
                         ' See [V1139 evidence](duel_v1139_compiled_formatter_checkpoint.md).\n')
    sources = [Path(__file__), ledger_path, manuscript_path, doc, checkpoint_path, sheet_path,
               Path('scripts/duel_layout_native_v1128.ld')]
    for pattern in ('*v1128.c', '*v1131.c', '*v1133.c', '*v1131.py', '*v1132.py', '*v1133.py',
                    '*v1134.py', '*v1135.py', '*v1136*.py', '*v1137*.py', '*v1138.py'):
        sources += list(Path('scripts').glob(pattern))
    for folder in ('duel_layout_native_v1131', 'duel_native_preflight_v1132', 'duel_layout_native_v1133',
                   'duel_native_layout_v1134', 'duel_layout_native_v1135', 'duel_compiled_fonts_v1136c', 'duel_native_ISA_v1137b'):
        for pattern in ('*.json', '*.bin', '*.elf', '*.png', '*.txt'):
            sources += list(Path('work/analysis', folder).rglob(pattern))
    sources += [Path(filename) for filename in ('docs/translation_progress.md', 'docs/todo.md', 'docs/known_issues.md')]
    sources += list(Path('work/analysis/duel_toolchain_v1128/ziglang-0.13.0.dist-info').glob('*'))
    ARCHIVE.mkdir(parents=True)
    files, seen = [], set()
    for source in sources:
        source = source.absolute()
        if not source.is_file() or source in seen:
            continue
        seen.add(source)
        target = ARCHIVE / source.relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes()) == digest
        files.append({'source': str(source), 'archived': str(target), 'sha256': digest})
    save(ARCHIVE / 'archive_manifest.json', {'files': files, 'all_hashes_verified': True,
        'compiler_installation_retained_at_pinned_project_local_path_not_duplicated_wholesale': True,
        'no_playable_ROM_or_completion_credit': True, 'full_goal_complete': False})
    save(ROOT / 'archive_receipt.json', {'archive': str(ARCHIVE), 'files': len(files),
        'manifest_sha256': sha((ARCHIVE / 'archive_manifest.json').read_bytes())})
    print(f'V1139 archived{len(files)} verified files;4700 native layouts,1356 complete fonts,1432 reproducible bytes. Placement/filter/integration/actual remain open.')


if __name__ == '__main__':
    main()
