"""Seal caller/name/font evidence while retaining all unimplemented runtime gates."""
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_postmacro_layout_v1119 import layout
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_name_scope_checkpoint_v1120')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V1120 Duel names native fonts and caller scope')


def main():
    assert not ROOT.exists() and not ARCHIVE.exists()
    scope_path = Path('work/analysis/duel_scope_names_v1117b/original_caller_ABI_scope.json')
    names_path = Path('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    fonts_path = Path('work/analysis/duel_full_name_fonts_v1119/native_all_source_names_font_proof.json')
    phase_path = Path('work/analysis/duel_full_name_fonts_v1119/all4160_source_name_layouts_corrected_phase.json')
    scope, names, fonts, phases = [read(path) for path in (scope_path, names_path, fonts_path, phase_path)]
    assert len(scope['cases']) == 53 and sum(row['selected_by_proposed_scope'] for row in scope['cases']) == 20
    assert all(row['full_stack_and_callee_saved_ABI_pass'] for row in scope['cases'])
    assert names['native_slots208_cover207_IDs_with_slot207_aliasing_current_captain']
    assert len(names['names']) == 208 and len(phases['layouts']) == 4160
    assert fonts['all2820_full_native_ASCII_CP932_planes_match_independent_complete_font_masks_and_shadows']
    assert len(fonts['cases']) == 2820
    for case in fonts['cases']:
        assert not case['glyphs_outside_final_visible_crop'] and not case['glyphs_crossing_source_rows']
        assert not case['glyph_ink_absent_from_final_crop']
        assert not case['first_glyph_damaged_by_later_stride_spill']
        assert case['whole_source_plane_exact_to_independently_laid_out_complete_words_and_font']
        assert case['native_font_consumes_complete_generated_string']
    for preview in fonts['research_previews']:
        assert sha(Path(preview['path']).read_bytes()) == preview['sha256']
    prior = read('work/analysis/duel_postmacro_v1115/native_postmacro_layout_prototype.json')
    for case in prior['cases']:
        generated, lines = layout(case['text'].encode('ascii'))
        assert generated.hex() == case['native_draw_context']['generated_postmacro_hex']
        assert lines == case['native_draw_context']['generated_lines']
    candidate = Path(fonts['candidate'])
    assert sha(candidate.read_bytes()) == fonts['candidate_sha256'] == scope['candidate_sha256']
    manuscript = read('translations/duel_editorial_manuscript_v3.json')
    assert all(not row['review']['formatting'] for row in manuscript['records'])
    current_arm = NdsImage.open(candidate).read_file('/__arm9__.bin')
    clean_arm = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    old_storage = read('work/analysis/tavern_storage_v764/retired_source_inventory.json')
    storage = []
    for row in old_storage['source_allocations']:
        lo, hi = row['lo'] - 0x02000000, row['hi'] - 0x02000000
        storage.append({'span': [row['lo'], row['hi']],
                        'current_exact_to_clean': current_arm[lo:hi] == clean_arm[lo:hi]})
    assert sum(row['current_exact_to_clean'] for row in storage) == 2
    ROOT.mkdir(parents=True)
    summary = (
        'V1120 verifies original duel caller scope and complete source-name font geometry. '
        'The208 source slots cover207 distinct actor IDs;slot207 aliases the current captain. '
        'Original EA1C selects the appropriate native getter. All4160 prospective name/paragraph '
        'layouts retain complete words and source name bytes.53 original CPU caller cases validate '
        '20 duel messages and exclude13 other-table plus20 direct-static calls,with full stack and '
        'callee-saved ABI checks. The full-name test exposed a real prototype break defect: '
        'double-byte characters reset ASCII batching,so whole-row byte parity could displace a '
        'continuation initial. SuccessorV1119 uses the trailing ASCII run. All2820 complete font '
        'cases for20 paragraphs and141 distinct source names now match independent ASCII/CP932 '
        'masks and shadows,with complete initials/endings and original144x36 crops. All41 earlier '
        'ASCII prototype outputs remain exact. Native selector,printf,macro,constructor,painters '
        'and crop paths execute in their declared research tests;loader,SDK/UI and Python-layout '
        'boundaries are explicit. This is not an assembled runtime or actual duel playback. '
        'All33 formatting gates remain false;no ROM,patch,registry or prose change. '
        'The historical retired-source census has34 changed allocations and two12-byte unchanged '
        'slots;none is newly approved free code storage. Runtime ownership/ABI integration,13 '
        'ordinary escape notices,original scene transitions and broader editorial/graphics work '
        'remain open.1196 complete,1267 source/prose-reviewed;no completion credit. V1105 remains '
        'experimental,V997 fully scene-verified,canonical unchanged;goal active.'
    )
    checkpoint_path = ROOT / 'checkpoint.json'
    save(checkpoint_path, {'summary': summary, 'scope_proof': str(scope_path),
        'source_name_catalogue': str(names_path), 'corrected_phase_layouts': str(phase_path),
        'full_native_name_font_proof': str(fonts_path), 'all41_prior_ASCII_outputs_exact': True,
        'representative_Fernando1931_and_Francisca1938_previews_visually_reviewed': True,
        'original_slot207_alias_is_not_an_extra_actor': True,
        'retired_source_current_byte_comparison_only_not_ownership_approval': storage,
        'all33_formatting_gates_false_no_ROM_or_completion_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1196 and ledger['records_with_source_and_prose_pass'] == 1267
    ledger['duel_prose_v1103'].update(name_scope_checkpoint=str(checkpoint_path),
        source_slot_identity_note='208 slots cover207 actor IDs;slot207 is the current captain alias',
        full_CP932_font_planes_and_assembled_runtime_and_fixed_storage_still_pending=False,
        CPU_full_CP932_font_planes_complete_runtime_fixed_storage_integration_actual_still_pending=True,
        mixed_phase_failed_predecessor='work/analysis/duel_full_name_failure_v1118/first_CP932_request_failure.json')
    # The old aggregate flag mixed a completed font gate with pending runtime work.
    # The explicit status keeps every remaining gate open.
    ledger['duel_prose_v1103']['formatting_status'] = 'all-source-name-CPU-fonts-and-original-caller-scope-pass;runtime-storage-integration-and-actual-open'
    ledger['formatting_watchlist']['duel_CP932_phase_followup'] = {
        'proof': str(fonts_path), 'counterexample': fonts['mixed_phase_counterexample_retained'],
        'status': 'corrected-CPU-prototype-only;production-runtime-and-actual-open',
        'rule': 'Double-byte glyphs end an ASCII batch;derive pre-LF padding from the trailing ASCII run.',
        'not_a_global_change_to_other_verified_consumer_profiles': True}
    ledger['latest_checkpoint'] = summary
    save(ledger_path, ledger)
    doc = Path('docs/duel_v1120_name_scope_checkpoint.md')
    doc.write_text('# V1120: duel source names,caller scope and mixed glyph phase\n\n' + summary +
        '\n\n## Counterexample and correction\n\n'
        'The rejected V1118 prototype rendered COMMON1933 with protected source name Fernando '
        '(CP9328265 fullwidth F). Its continuation L appeared atx132 on row0 while e began atx6 '
        'on row1. Original fullwidth name bytes were correct. Whole-row byte parity was the '
        'wrong model because the double-byte glyph ends the preceding ASCII batch. V1119 emits '
        'the pre-LF blank only when the trailing ASCII run is odd. The corrected full native '
        'painter and independent font reference agree for all source names. Failed evidence is '
        'retained and no predecessor proof is overwritten.\n\n'
        'At the original font boundary,LR is0200DAC4,private text isSP+10,context isSP+410, '
        'outer return isSP+47C,and saved voice table isSP+4A4. Only outer0200D4BC plus tables '
        '02117340/02117360/021174E0 selects the proposed duel scope. The direct-static parent '
        '0200D528 and other voice tables are excluded. These are measured original CPU caller '
        'facts;no assembled wrapper has yet been approved.\n\n'
        'The tests explicitly model native message loading when supplying reviewed CPU text, '
        'SDK clearing,widget registration and Python layout. They do not inject numeric '
        'messages into an emulator,modify actual actor IDs or force any battle outcome. Font '
        'previews are diagnostic research and must not be filed as guide gameplay screenshots.\n', encoding='utf-8')
    for name in ('docs/translation_progress.md', 'docs/todo.md', 'docs/known_issues.md'):
        with Path(name).open('a', encoding='utf-8') as stream:
            stream.write('\n\n## V1120: duel names and native caller scope\n\n' + summary +
                         ' See [V1120 evidence](duel_v1120_name_scope_checkpoint.md).\n')
    sources = [Path(__file__), ledger_path, doc, checkpoint_path,
               Path('translations/duel_editorial_manuscript_v3.json')]
    for pattern in ('*v1117*.py', '*v1118.py', '*v1119.py'):
        sources += list(Path('scripts').glob(pattern))
    for folder in ('duel_scope_names_v1117b', 'duel_full_name_failure_v1118', 'duel_full_name_fonts_v1119'):
        sources += list(Path('work/analysis', folder).rglob('*.json'))
        sources += list(Path('work/analysis', folder).rglob('*.png'))
    sources += [Path(name) for name in ('docs/translation_progress.md', 'docs/todo.md', 'docs/known_issues.md')]
    ARCHIVE.mkdir(parents=True)
    files, seen = [], set()
    for source in sources:
        source = source.absolute()
        if source in seen:
            continue
        seen.add(source)
        target = ARCHIVE / source.relative_to(Path.cwd())
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes()) == digest
        files.append({'source': str(source), 'archived': str(target), 'sha256': digest})
    save(ARCHIVE / 'archive_manifest.json', {'files': files, 'all_hashes_verified': True,
        'research_only_no_ROM_or_completion_credit': True, 'full_goal_complete': False})
    save(ROOT / 'archive_receipt.json', {'archive': str(ARCHIVE), 'files': len(files),
        'manifest_sha256': sha((ARCHIVE / 'archive_manifest.json').read_bytes())})
    print(f'V1120 archived {len(files)} verified files;53 caller cases,2820 native fonts,all41 prior outputs exact;runtime/actual open.')


if __name__ == '__main__':
    main()
