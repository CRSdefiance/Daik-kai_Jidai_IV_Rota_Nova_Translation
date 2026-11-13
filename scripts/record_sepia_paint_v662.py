"""Archive controlled sepia painting and retain the full graphics audit scope."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/sepia_consumers_v662')
DOC = Path('docs/sepia_paint_v662_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V662 Sepia native painting')
KEY = 'all64_source_sepia_page_palette_native_paints_complete_destination_alpha_and_bounds_v662'


def main():
    proof_path = ROOT / 'native_paint_proof.json'
    proof, pre = read(proof_path), read(ROOT / 'preflight.json')
    assert proof['script_sha256'] == sha(Path('scripts/verify_sepia_paint_v662.py').read_bytes())
    assert len(proof['cases']) == 64 and proof['unique_complete_paintings'] == 56
    assert sum(r['source_opaque_pixels'] for r in proof['cases']) == 2498560
    assert sum(r['opaque_index0_pixels'] for r in proof['cases']) == 30200
    assert proof['isolated_native_palette_alpha_control']['complete_loaded_source_restored_exact']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    rom, clean = NdsImage.open(pre['candidate']), NdsImage.open('work/clean.nds')
    arm = rom.read_file('/__arm9__.bin')
    hits = []
    for section in MainCodeFile(arm, 0x02000000).sections:
        hits.extend(section.ramAddress + off for off in range(0, len(section.data) - 3, 4)
                    if struct.unpack_from('<I', section.data, off)[0] == 0x02313B8C)
    assert hits == [0x0210F328]
    legacy = IlnkContainer.parse(rom.read_file('/GRP/CMMNIMG.DK4')).blocks[3]
    assert legacy == IlnkContainer.parse(clean.read_file('/GRP/CMMNIMG.DK4')).blocks[3]
    old = next(r for r in read('work/analysis/common_raw_v194.json')['blocks'] if r['block_index'] == 3)
    assert sha(legacy) == old['source_block_sha256'] and len(legacy) == 243232
    save(ROOT / 'source_usage_bounds.json', {'current_ARM9_sha256': sha(arm),
        'aligned_owner_literals_in_all_loaded_ARM9_sections': hits,
        'registration_literal_not_gameplay_consumer': True,
        'computed_indirect_and_file_ID_readers_not_excluded': True,
        'original_legacy_CMMN_block3_sha256': sha(legacy),
        'legacy_complete243232_bytes_exact_clean_and_previous_source_review': True,
        'legacy_actual_display_not_proven': True,
        'eight_controlled_bank0_native_outputs_visually_reviewed': True,
        'all64_distinct_palette_case_visual_review_not_claimed': True})
    save(ROOT / 'rejected_contracts.json', {
        'destination_header_not_screen_selector': {'retained_difference_report': 'first_paint_difference.json',
            'correct_native_screen_base': 0x022E1794, 'correct_native_selector': 0},
        'every_page_has_index0': {'rejected': True, 'actual_pages_with_index0':
            sorted({r['page'] for r in proof['cases'] if r['opaque_index0_pixels']})}})
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    for source in (DOC, Path(__file__), Path('scripts/verify_sepia_paint_v662.py'),
                   *ROOT.glob('*.json'), *ROOT.glob('*.txt'), *ROOT.glob('*.png')):
        ARCHIVE.mkdir(parents=True, exist_ok=True)
        checked_copy(source, ARCHIVE / source.name)
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'all64_controlled_original_loader_cache_view_and_paint_cases': True,
        'all3145728_destination_words_including_border_exact_source_model': True,
        'all2498560_source_pixels_written_no_output_reads_no_outside_crop_writes': True,
        'forty_cases30200_opaque_index0_cells_reject_wrong_transparency_model': True,
        'separate_palette_bit15_control_restores_complete_loaded_source_exact': True,
        'all_executed_instructions_exact_original_ARM9_overlay': True,
        'actual_sepia_and_legacy_gameplay_consumers_not_established': True,
        'eight_native_output_PNGs_not_gameplay_screenshots_or_guide_candidates': True,
        'ROM_patch_manifest_registry_canonical_and_release_pointers_unchanged': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'other_graphics_gameplay_older_record_and_final_acceptance_gates_open': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V662: complete controlled native sepia-map page and palette painting'
    addition = ('All64 original sepia page/palette cases pass actual registration, SDK-file-bridged '
        'loading, native cache/view setup and complete original software painting. All3,145,728 '
        'destination words match independent source colors, including borders; all2,498,560 '
        'source pixels are written with no output reads or out-of-crop writes. Original palette '
        'bit15 semantics preserve30,200 opaque index0 pixels in40 cases. One isolated alpha '
        'control passes and restores the entire loaded source exactly. All executed code is '
        'original ARM9/overlay. Eight bank0 outputs visually inspected; controlled outputs '
        'are not emulator screenshots or guide candidates. Rejected destination/index0 '
        'assumptions retained. Actual sepia/legacy consumers, other graphics and acceptance '
        'remain open. V653/patch/registry/pointers unchanged; all18 plaques incomplete and22 '
        'historical scopes exact. Evidence on E; full goal active. See '
        '[V662 checkpoint](sepia_paint_v662_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'],
        'no_new_emulator_capture_guide_or_gameplay_parent_credit': True,
        'scripts': {str(p): sha(p.read_bytes()) for p in (Path(__file__), Path('scripts/verify_sepia_paint_v662.py'))},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print('V662 native proof and eight controlled outputs archived; three audits/four documents updated; full goal active.')


if __name__ == '__main__':
    main()
