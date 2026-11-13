"""Record the CPU-only duel layout investigation without granting release credit."""
from pathlib import Path
from shutil import copy2

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save


ROOT = Path('work/analysis/duel_layout_checkpoint_v1116')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V1116 Duel native layout research')


def main():
    assert not ROOT.exists() and not ARCHIVE.exists()
    native_path = Path('work/analysis/duel_text_surface_v1113b/native_duel_surface_proof.json')
    prototype_path = Path('work/analysis/duel_postmacro_v1115/native_postmacro_layout_prototype.json')
    prototype = read(prototype_path)
    assert len(prototype['cases']) == 41
    assert prototype['CPU_only_postmacro_boundary_transformation_not_assembled_runtime_or_actual_gameplay']
    assert prototype['new_33_formatting_gates_remain_false_and_no_ROM_or_gameplay_change']
    for case in prototype['cases']:
        assert case['whole_source_plane_exact_to_independently_laid_out_complete_words_and_font']
        assert case['CPU_prototype_has_complete_correct_visible_layout']
        assert case['native_font_consumes_complete_generated_string']
        assert not case['glyph_ink_absent_from_final_crop']
        assert not case['first_glyph_damaged_by_later_stride_spill']
        assert not case['glyphs_crossing_source_rows']
        assert not case['glyphs_outside_final_visible_crop']
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
    candidate = Path(prototype['candidate'])
    assert sha(candidate.read_bytes()) == prototype['candidate_sha256']
    manuscript_path = Path('translations/duel_editorial_manuscript_v3.json')
    manuscript = read(manuscript_path)
    assert len(manuscript['records']) == 33
    assert all(not record['review']['formatting'] for record in manuscript['records'])
    assert sum(record['editorial_decision'] == 'revise' for record in manuscript['records']) == 23
    shop_path = Path('work/analysis/sighting_checkpoint_v1097/photographed_shop_formatting.json')
    shop = read(shop_path)
    assert all(row['no_authored_indent_internal_gap_or_stray_Discover'] for row in shop['entries'])
    assert sha(Path(shop['earlier_actual_V747_capture']).read_bytes()) == shop['capture_sha256']
    preservation_path = Path('work/analysis/sighting_grammar_release_v1104/registered_release_verification.json')
    preservation = read(preservation_path)
    assert preservation['candidate_sha256'] == prototype['candidate_sha256']
    assert preservation['all3653_unselected_message_strings_including_user676_677_and_inherited_event_prose_exact']
    assert preservation['entire_renderer_selector_previous_runtime_and_all_native_name_labels_exact']
    ROOT.mkdir(parents=True)
    summary = (
        'V1116 records the distinct duel widget geometry and a CPU-only post-expansion layout prototype. '
        'Its backing surface is208x36,but the original renderer displays three144x12 crops:24 ASCII cells '
        'per row,three rows. Native automatic wrapping can write past the backing row before advancing, '
        'damage earlier glyph pixels and hide text beyond the final crop despite consuming the entire string. '
        'The41-case prototype covers20 duel paragraphs with Clifford and a legal16-character ASCII name, '
        'plus a current-text control. Complete independent font planes and native crop submissions match '
        'without lost letters or overflow. These are CPU research results with explicit SDK-clear and '
        'widget-registration boundary models;they are not assembled runtime fixes or gameplay screenshots. '
        'ManuscriptV3 preserves formal1938 name recognition and duel proposal;23 revisions,10 retentions. '
        'All33 formatting gates remain false. Real CP932 names,scoped wrapper ABI,owned fixed storage, '
        '13 ordinary escape notices,registered integration and original scene transitions remain pending. '
        'No ROM or patch changed. V1105 remains experimental,V997 fully scene-verified,canonical unchanged. '
        '1196 completed and1267 source/prose-reviewed;no completion credit. The photographed shop676/677 '
        'repair remains preserved in V1105;the actual V747 capture was visually rechecked,not rerun. '
        'Full editorial scope,global formatting and separate graphics audit remain open.'
    )
    proof_path = ROOT / 'checkpoint.json'
    save(proof_path, {
        'summary': summary,
        'native_surface_diagnostic': str(native_path),
        'CPU_postmacro_prototype': str(prototype_path),
        'candidate': str(candidate), 'candidate_sha256': prototype['candidate_sha256'],
        'all41_prototype_planes_crops_complete_letters_and_preview_hashes_pass': True,
        'representative1931_native_and1938_max16_previews_visually_reviewed': True,
        'SDK_clear_and_widget_registration_modeled_not_full_native_GPU_execution': True,
        'not_assembled_runtime_or_actual_gameplay': True,
        'all33_manuscript_formatting_gates_still_false': True,
        'unused_zero_bytes_in_owned_caption_buffer_are_not_free_code_storage': True,
        'photographed_shop_reference': str(shop_path),
        'V1105_exact_preservation_proof': str(preservation_path),
        'actual_V747_shop_capture_visually_reviewed_no_fresh_shop_activation': True,
        'no_ROM_patch_registry_or_build_changes': True,
        'completed_entry_credit': 0, 'full_goal_complete': False,
        'producer_sha256': sha(Path(__file__).read_bytes()),
    })
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert ledger['records_editorially_completed'] == 1196
    assert ledger['records_with_source_and_prose_pass'] == 1267
    duel = ledger['duel_prose_v1103']
    duel['native_surface_proof'] = str(native_path)
    duel['native_postmacro_prototype'] = str(prototype_path)
    duel['layout_checkpoint'] = str(proof_path)
    duel['formatting_status'] = 'CPU-prototype-only;real-CP932-names-runtime-ABI-fixed-storage-integration-and-actual-open'
    ledger['latest_checkpoint'] = summary
    save(ledger_path, ledger)
    doc = Path('docs/duel_v1116_native_layout_checkpoint.md')
    doc.write_text('# V1116: duel native geometry and layout research\n\n' + summary + '\n\n'
        'The original152x64 widget has three display rows20 pixels apart. Each submission reads144x12 '
        'from the208x36 backing image. Treating the entire backing width as visible was rejected. '
        'The diagnostic executes the original constructor,measurement,macro expansion,glyph painter and '
        'crop-submission path. It models only the missing SDK clear and widget registration boundaries. '
        'The independent complete pixel reference includes native odd-byte blank-pair flushes.\n\n'
        'The proposed correction operates after original macro expansion,keeps ordinary prose as one '
        'paragraph,and generates balanced complete-word rows with no leading indentation. It adjusts '
        'only the private vertical origin for multiline text. No font,palette,border,width flag or live '
        'actor identity changes. A Python boundary prototype passing41 cases does not prove a production '
        'wrapper. Original caller/table guards,register/stack preservation,all real name encodings and '
        'owned existing storage must be proven before integration. The zero span in the existing caption '
        'buffer is owned mutable data and must not be repurposed as code. No section,BSS,cache,arena or '
        'staged-payload growth is allowed.\n\n'
        'The user photograph concerns COMMON676/677,already repaired in V747. Its saved in-game frame '
        'shows two aligned lines without the internal padding gap or stray Discover. The registered '
        'V1105 preservation proof keeps those strings and their complete renderer exact. This is '
        'preserved prior targeted gameplay evidence,not a new shop-scene run or a whole-game guarantee.\n', encoding='utf-8')
    for filename in ('docs/translation_progress.md', 'docs/todo.md', 'docs/known_issues.md'):
        with Path(filename).open('a', encoding='utf-8') as stream:
            stream.write('\n\n## V1116: duel layout research and formatting watch\n\n' + summary +
                         ' See [V1116 evidence](duel_v1116_native_layout_checkpoint.md).\n')
    sources = [Path(__file__), ledger_path, manuscript_path, doc, proof_path, native_path,
               prototype_path, shop_path, preservation_path, Path(shop['earlier_actual_V747_capture'])]
    sources += [Path(case['preview']) for case in prototype['cases']]
    for pattern in ('*v1112.py', '*v1113*.py', '*v1114.py', '*v1115.py'):
        sources += list(Path('scripts').glob(pattern))
    for folder in ('duel_text_surface_v1113b', 'duel_layout_v1114'):
        sources += list(Path('work/analysis', folder).rglob('*.json'))
        sources += list(Path('work/analysis', folder).rglob('*.png'))
    sources += [Path(name) for name in ('docs/translation_progress.md', 'docs/todo.md', 'docs/known_issues.md')]
    ARCHIVE.mkdir(parents=True)
    generated = Path('E:/Rota Nova translations/Generated')
    files, seen = [], set()
    for source in sources:
        source = source.absolute()
        if source in seen:
            continue
        seen.add(source)
        relative = (source.relative_to(Path.cwd()) if source.is_relative_to(Path.cwd()) else
                    Path('Generated') / source.relative_to(generated))
        target = ARCHIVE / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        copy2(source, target)
        digest = sha(source.read_bytes())
        assert sha(target.read_bytes()) == digest
        files.append({'source': str(source), 'archived': str(target), 'sha256': digest})
    save(ARCHIVE / 'archive_manifest.json', {'files': files, 'all_hashes_verified': True,
         'research_previews_are_not_guide_gameplay_screenshots': True, 'full_goal_complete': False})
    save(ROOT / 'archive_receipt.json', {'archive': str(ARCHIVE), 'files': len(files),
         'manifest_sha256': sha((ARCHIVE / 'archive_manifest.json').read_bytes())})
    print(f'V1116 research checkpoint archived: {len(files)} hash-verified files; no ROM changes or completion credit.')


if __name__ == '__main__':
    main()
