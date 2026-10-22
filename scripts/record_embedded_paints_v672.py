"""Archive exact native component/color evidence, preserving actual-context gaps."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_embedded_paints_v672 import ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V672 Embedded caption painting')
DOC = Path('docs/embedded_paints_v672_checkpoint.md')
KEY = 'embedded_five_captions664_controlled_native_paints83_banks_and_exact_palette_correspondence_v672'
SCRIPTS = ('scripts/verify_embedded_paints_v672.py', 'scripts/relate_common_palette_v672.py',
           'scripts/record_embedded_paints_v672.py', 'scripts/verify_embedded_archive_v672.py')


def copy(source, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, target)


def main():
    pp, relation_path = ROOT / 'native_embedded_paint_proof.json', ROOT / 'palette_correspondence.json'
    proof, relation, pre = read(pp), read(relation_path), read(ROOT / 'preflight.json')
    assert proof['script_sha256'] == sha(Path(SCRIPTS[0]).read_bytes())
    assert relation['script_sha256'] == sha(Path(SCRIPTS[1]).read_bytes())
    assert len(proof['cases']) == 664 and len(proof['previews']) == 16
    assert len(relation['counterparts']) == 4
    assert relation['portrait_control_same_mapping_only_matches_pixels'] == 39817
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'palette_relation': str(relation_path), 'palette_relation_sha256': sha(relation_path.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'complete_controlled_legacy_palette_paints_verified_actual_consumers_still_open',
        'all664_original_current83_bank_two_mode_two_background_native_calls_exact': True,
        'all32636928_destination_words_and_full_source_guards_exact': True,
        'all307_current_complete_font_pixels_and_five_caption_cells_exact': True,
        'original_antialias_shades_retained_in_source_model_not_equated_to_monochrome_font': True,
        'complete512x256_both_atlas_halves_exact_original_and_current': True,
        'all1328_modern_words_reproduced_by_explicit_observed_color_map_with42_held_out_banks': True,
        'mapping_not_executed_as_original_runtime_conversion_or_applied_to_ROM': True,
        'source_portrait_control_rejects_global_converter_generalization': True,
        'six_actual_control_contexts_legacy_loader_setup_and_GPU_selection_open': True,
        'no_new_emulator_screenshot_gameplay_or_unused_art_credit': True,
        'all18_plaques_incomplete22_historical_requirements_exact': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name, scope in frozen.items():
        target = Path('translations') / name
        data = read(target)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(target, data)
    heading = '## V672: embedded captions, full native palette crops and exact color relationship'
    addition = ('All664 explicit scratch-descriptor native paints pass: original/current captions, '
        '83 original banks, two original drawing modes and two backgrounds. All32,636,928 '
        'destination words, source bytes, guards and write coverage match; complete307 English '
        'font pixels and both512x256 atlas halves pass. Original antialias shades are modeled '
        'from exact source indices. A32-entry observed channel map derived from41 banks verifies '
        '42 held-out banks and all1328 modern palette words for Marker/Frame, original/current. '
        'The same map fails full portrait equivalence; no global/runtime converter is invented. '
        'Sixteen controlled outputs and paired sheet visually reviewed; no gameplay captures '
        'or guide credit. Failed two-index source assumption retained. Original legacy loader, '
        'descriptor/mode/palette selection, GPU and six actual control contexts stay open. '
        'V666/patch/registry/pointers unchanged; all18 plaques incomplete and22 scopes exact. '
        'See [V672 checkpoint](embedded_paints_v672_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        target = Path('docs') / name
        text = target.read_text(encoding='utf-8')
        if heading not in text:
            target.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for source in (DOC, *map(Path, SCRIPTS)):
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'],
        'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'controlled_native_output_not_emulator_or_guide': True,
        'actual_consumers_and_full_graphics_goal_still_open': True, 'full_goal_complete': False})
    print('V672 native/color evidence archived; three audits/four docs updated;18/22 scope retained.')


if __name__ == '__main__':
    main()
