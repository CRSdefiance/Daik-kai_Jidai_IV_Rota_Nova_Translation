"""Seal scoped cache execution and both native text consumers; no scene credit."""
from pathlib import Path
from shutil import copy2
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_resident_checkpoint_v1161')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V1161 Resident duel and escape native verification')


def main():
    assert not ROOT.exists() and not ARCHIVE.exists()
    paths = {
        'copy': Path('work/analysis/duel_cache_copies_v1145/all_native_copies_and_prefix_cache_sequence.json'),
        'scope': Path('work/analysis/duel_cache_scope_v1150/original_loader_scoped_cache_component.json'),
        'resident_fonts': Path('work/analysis/duel_resident_fonts_v1151/cache_resident_complete_fonts.json'),
        'escape_runtime': Path('work/analysis/duel_escape_runtime_v1154/native_runtime_verification.json'),
        'escape_fonts': Path('work/analysis/duel_escape_fonts_v1157/native_escape_fonts.json'),
        'visual': Path('work/analysis/duel_resident_review_v1158/visual_review_packet.json'),
        'ISA': Path('work/analysis/duel_native_ISA_v1160b/exact_binary_ISA_and_reproduction.json'),
        'PIC': Path('work/analysis/duel_PIC_positions_v1143/PIC_native_position_matrix.json'),
    }
    proofs = {key: read(path) for key, path in paths.items()}
    assert proofs['scope']['all20_original_voice_selections_enter_correct_native_PIC_component']
    assert proofs['scope']['all13_other_tables_and20_direct_numeric_controls_skip_component']
    assert len(proofs['scope']['cases']) == 53
    assert len(proofs['resident_fonts']['cases']) == 1356
    assert len(proofs['escape_fonts']['cases']) == 1417
    assert proofs['escape_fonts']['unique_font_planes'] == 1015
    assert proofs['escape_runtime']['old_and_new_full_scope_cases_each'] == 56696
    assert proofs['PIC']['all14100_positioned_native_cases_pass']
    assert len(proofs['ISA']['instructions']) == 677
    visual = proofs['visual']
    assert len(visual['all_review_sheets']) == 6
    for row in visual['all_review_sheets']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    for row in proofs['escape_fonts']['findings_requiring_review']:
        assert row['message_ID'] == 1954 and row['weak_line_end_indices'] == [0]
        assert row['lines'][0].endswith('Come on,') and row['lines'][1] == 'lads, cover them!'
        assert not row['short_or_orphan_final_row']
    manuscript_path = Path('translations/duel_editorial_manuscript_v3.json')
    assert all(not r['review']['formatting'] for r in read(manuscript_path)['records'])
    ROOT.mkdir(parents=True)
    visual_path = ROOT/'visual_review.json'
    save(visual_path, {'packet': str(paths['visual']), 'packet_sha256': sha(paths['visual'].read_bytes()),
        'all_six_sheets_visually_inspected': visual['all_review_sheets'],
        'full_first_last_letters_uniform_margins_complete_words_and_bounds_accepted': True,
        'contextual_weak_word_warning_retained': visual['contextual_boundary_warning'],
        'all_other_records_and_global_weak_word_audit_not_waived': True,
        'source_fullwidth_F_names_preserved_not_rewritten_for_visual_similarity': True,
        'synthetic_names_are_declared_stress_not_actual_player_capture': True,
        'not_actual_gameplay_or_guide_screenshots': True, 'visual_review_pending': False,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    summary = (
        'V1161 verifies the dedicated duel formatter in the existing COMMON input cache, '
        'with a 1,480-byte position-independent component stored before mapped strings and '
        'a 104-byte caller filter inside the original renderer\'s proven 108-byte code tail. '
        'No section, BSS, cache allocation, arena or 123,040-byte staged payload grows. '
        'All 14,100 position tests, 7,336 message-copy checks and 180 cache-sequence cases '
        'pass. All 53 original caller controls pass: 20 selected duel messages enter the '
        'component, while 13 other-table and 20 direct-call controls bypass it. The '
        'native cache-maintenance loops cover all 47 affected lines. All 1,356 distinct '
        'expanded duel inputs run through the original loader, printf, macro path, '
        'scoped component, ASCII/CP932 painters and three 144x12 crop submissions. '
        'Complete independent glyph planes match; no missing initials, endings or crop '
        'pixels occur. Two escape-speech memberships fit the existing 212-byte bank; '
        '56,696 source and 56,696 target selector cases, 3,668 modal outputs, 238 parent '
        'controls, five integer edges and 140 whole-memory status contracts pass. '
        'The 13 escape paragraphs pass 1,417 name/layout/font cases, including 208 '
        'original compact-name getters and 27 additional legal-name stress variants. '
        'The catalog includes nonparticipating NPC labels as extra stress, not proven '
        'duel participants. All 161 boundary warnings are the same natural break after '
        'the complete interjection Come on, before lads, cover them!; a narrow '
        'contextual retention is documented. Six research sheets were visually reviewed. '
        'Independent compiler builds reproduce the exact component; all 677 mapped '
        'instructions are Thumb1/ARMv5 with one bound original D5404 call and no library '
        'dependency. These are CPU tests with explicit file, SDK/UI, GPU and MCR hardware '
        'boundaries, not actual duel playback or hardware cache verification. The source '
        'snapshot\'s old resident file-offset table initially caused a failing test; '
        'reopening through the original loader correctly refreshed it. All 33 manuscript '
        'formatting gates remain false. Final compiler-owned escape state, combined '
        'payload, registered release audit, exact patch, cold boot and original duel '
        'scenes/dismissal/transitions remain pending. No new playable ROM, registry '
        'or completion credit. Counts remain 1,196 complete and 1,267 source/prose '
        'reviewed. V1105 remains experimental, V997 fully scene-verified, and the '
        'canonical base unchanged. The full editorial goal, general formatting audit '
        'and separate unfinished graphics audit remain active.'
    )
    checkpoint = ROOT/'checkpoint.json'
    save(checkpoint, {'summary': summary,
        'completed_proofs': {key: {'path': str(path), 'sha256': sha(path.read_bytes())} for key, path in paths.items()},
        'visual_review': str(visual_path), 'visual_review_sha256': sha(visual_path.read_bytes()),
        'previous_goal_turn_classification': 'no progress: formatting status answered using existing evidence',
        'current_goal_turn_classification': 'progress: scoped resident native execution, complete fonts for both consumers, preservation regressions and reproducible ISA proof',
        'no_live_processes_or_verified_wait_claim': True,
        'no_ROM_registry_patch_or_completed_record_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1196 and ledger['records_with_source_and_prose_pass'] == 1267
    ledger['duel_prose_v1103'].update(resident_native_checkpoint=str(checkpoint),
        resident_native_visual_review=str(visual_path),
        formatter_next_action='Compile all33 through duel_editorial_layout_v1155; preserve the opaque carrier prefix; apply escape memberships; verify final copies and full native consumer audit; register and build combined ROM/exact patch; cold-boot original duel scenes and normal transitions.',
        formatting_status='scoped-existing-cache-PIC-and-both-native-font-consumers-verified;final-combined-payload-registration-and-original-scenes-open')
    ledger['formatting_watchlist']['duel_compiled_native24x3'].update(
        resident_checkpoint=str(checkpoint), resident_fonts=str(paths['resident_fonts']),
        escape_fonts=str(paths['escape_fonts']), visual_review=str(visual_path),
        status='resident-code-native-font-proven;combined-release-original-duel-scenes-and-transitions-open',
        all33_formatting_gates_still_false=True)
    ledger['latest_checkpoint'] = summary
    save(ledger_path, ledger)
    doc = Path('docs/duel_v1161_resident_native_checkpoint.md')
    doc.write_text('# V1161: resident duel formatter and escape-speech verification\n\n'+summary+
        '\n\n## Storage and lifetime contract\n\n'
        'COMMON block21 contains 1,480 executable bytes and four NUL bytes before '
        'the first mapped string, ID1931. Every mapped span stays below the original '
        '512-byte output capacity; the block stays below 8KiB. The original getter '
        'loads the carrier block before the component runs. It executes synchronously '
        'through the original static painter; no COMMON lookup, file I/O, or component '
        'write occurs while its bytes are active. Each entry flushes data and invalidates '
        'instruction-cache lines through the original SDK range routines. Actual '
        'emulator/hardware behavior remains a required gate. Later repackers must '
        'preserve and hash-lock this opaque prefix and carrier binding. It is owned '
        'code, not expendable padding. The generic single-cache repacker rejects '
        'nonblank prefixes rather than discarding them.\n\n'
        'The front accepts only original parent0200D4BC and tables02117340, '
        '02117360 or021174E0. Other callers retain the original renderer. The '
        'separate escape notices use portrait speech and compiler-owned leading '
        'presentation state. scripts/duel_editorial_layout_v1155.py distinguishes '
        'these consumers. The earlier V1144 payload is research input, not the '
        'final compiled 33-entry payload.\n\n'
        'The CPU snapshot contains source-ROM resident ILNK offsets. V1148/V1149 '
        'correctly rejected stale source offsets while testing the new COMMON file. '
        'V1150 clears only its CPU resource-open/cache-tag state and runs the original '
        'reopen/header/offset-table reads into the existing resident allocation; it '
        'does not replace the table with an invented directory or change a ROM loader. '
        'V1147 also exposed a missing output bound in the host file-provider object. '
        'Those terminal predecessors remain preserved.\n\n'
        'Escape font cases invoke the native printf/macro/wrap entry with explicit '
        'original caller-frame/table ABI inputs; separate source proofs cover voice '
        'selection. They do not execute the defeat branch or establish event eligibility. '
        'The 53 caller test and 1,356 resident-font cases execute original D458. '
        'File open/read, unavailable SDK clear, UI registration, GPU submission '
        'and hardware effects of cache instructions are declared boundaries. '
        'No numeric message is injected into an emulator.\n\n'
        'All 18 plaques remain open; accepted texture/borders do not complete their '
        'graphics audit. The four low-resolution Online bodies stay excluded. '
        'The older-record re-audit and full remaining shared/route/raw-source review '
        'are not satisfied by these targeted checks.\n', encoding='utf-8')
    for name in ('docs/translation_progress.md', 'docs/todo.md', 'docs/known_issues.md'):
        with Path(name).open('a', encoding='utf-8') as stream:
            stream.write('\n\n## V1161: resident duel and escape verification\n\n'+summary+
                         ' See [V1161 evidence](duel_v1161_resident_native_checkpoint.md).\n')
    sources = [Path(__file__), manuscript_path, ledger_path, checkpoint, visual_path, doc,
               Path('docs/translation_progress.md'), Path('docs/todo.md'), Path('docs/known_issues.md')]
    for path in Path('scripts').iterdir():
        if path.is_file() and any(f'v{n}' in path.name for n in range(1140, 1162)):
            sources.append(path)
    for folder in ('duel_prefix_storage_v1140', 'duel_layout_native_v1141b', 'duel_cache_front_v1142',
        'duel_PIC_positions_v1143', 'duel_cache_payload_v1144', 'duel_cache_copies_v1145',
        'duel_cache_scope_v1150', 'duel_resident_fonts_v1151', 'duel_escape_runtime_v1153',
        'duel_escape_runtime_v1154', 'duel_escape_fonts_v1157', 'duel_resident_review_v1158',
        'duel_layout_native_v1159', 'duel_native_ISA_v1160b'):
        for path in (Path('work/analysis')/folder).rglob('*'):
            if path.is_file():
                sources.append(path)
    ARCHIVE.mkdir(parents=True)
    files, seen = [], set()
    for source in sources:
        source = source.absolute()
        if source in seen or not source.is_file():
            continue
        seen.add(source)
        target = ARCHIVE/source.relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes()) == digest
        files.append({'source': str(source), 'archived': str(target), 'sha256': digest})
    save(ARCHIVE/'archive_manifest.json', {'files': files, 'all_hashes_verified': True,
        'no_new_playable_ROM_or_completion_credit': True, 'full_goal_complete': False})
    save(ROOT/'archive_receipt.json', {'archive': str(ARCHIVE), 'files': len(files),
        'manifest_sha256': sha((ARCHIVE/'archive_manifest.json').read_bytes())})
    print(f'V1161: {len(files)} archived files verified; 1356 resident duel and1417 escape fonts; integration/actual scenes remain open.', flush=True)


if __name__ == '__main__':
    main()
