"""Archive original village backdrop evidence without closing unrelated gates."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_backgrounds_v643 import CAP, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/village_backgrounds_v643_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V643 Village backgrounds')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V640 Narvik location fixture')
KEY = 'all24_original_village_coast_background_selectors_and_actual_Narvik_native_painter_v643'


def main():
    pp = ROOT / 'native_background_proof.json'
    p, pre = read(pp), read(ROOT / 'preflight.json')
    assert p['candidate_sha256'] == pre['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(p['all24_original_village_background_selectors']) == 24
    assert len(p['all54_complete_current_and_historical_two_screen_comparisons']) == 54
    assert not p['full_goal_complete']
    for path, digest in p['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    files = [DOC, pp, ROOT / 'preflight.json', ROOT / 'complete_replay_inputs.json',
        ROOT / 'fixture_guards.json', ROOT / 'visual_review.json',
        ROOT / 'village_source_backgrounds_NATIVE_SCALE.png',
        ROOT / 'actual_image_callback_diagnostic.json', ROOT / 'background_callback_probe.json',
        ROOT / 'complete_chain_diagnostic.json', ROOT / 'expanded_chain_diagnostic.json',
        ROOT / 'font_chain_failure_detail.json', ROOT / 'current_vs_V618_whole_frame_diagnostic.json',
        CAP / 'capture_report.json', CAP / 'navigation_command_journal.json',
        ROM.with_suffix('.manifest.json'), Path(__file__)]
    files.extend(Path(path) for path in p['scripts'])
    for source in files:
        checked_copy(source, ARCHIVE / source.name)
    screenshots, guides = [], []
    for row in p['all54_complete_current_and_historical_two_screen_comparisons']:
        shot = row['current_PNG']
        target = ARCHIVE / f"CURRENT_V640_frame{row['frame']:06d}_UNMODIFIED_NATIVE.png"
        checked_copy(shot['path'], target)
        record = {'path': str(target), 'frame': row['frame'], 'sha256': shot['PNG_sha256'],
                  'unmodified_capture': True, 'coordinate_only_fixture_at5200_disclosed': True}
        screenshots.append(record)
        if row['frame'] in (8400, 15700):
            guide = GUIDE / ('LOCATION_FIXTURE_' + target.name)
            checked_copy(shot['path'], guide)
            guides.append({**record, 'path': str(guide)})
    save(GUIDE / 'provenance.json', {'candidate_sha256': p['candidate_sha256'],
        'screenshots': guides, 'source_report': p['report'], 'source_report_sha256': p['report_sha256'],
        'only_ship_coordinates_injected_not_discovery_development_inventory_or_dialogue': True,
        'original_Svartisen_acceptance_and_development_sequence_verified': True,
        'ordinary_long_distance_travel_or_item_acquisition_not_claimed': True,
        'publication_approved': False})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': p['candidate_sha256'],
        'screenshots': screenshots, 'guide_candidates': guides, 'full_goal_complete': False,
        'all_original_RAM_VRAM_and_run_files_remain_on_E': True,
        'files': {q.name: sha(q.read_bytes()) for q in ARCHIVE.iterdir()
                  if q.is_file() and q.name != 'provenance.json'}})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': p['candidate_sha256'],
        'all24_village_IDs12_supplied_contexts_original_town_background_selection_verified': True,
        'selected_original_coast_files': [43, 44, 48],
        'original_ROM_metadata_flag20_zero_not_mutable_development_verified': True,
        'actual_Narvik_original_password_development0_to2_and_return_verified': True,
        'whole49152_index_source_plane512_palette_bytes_and_native16bit_painter_words_verified': True,
        'actual_registered_Town_context_sprite_getter_source_crop_bank_and_destination_verified': True,
        '54_whole_current_V618_two_screen_frames5308416_pixels_exact': True,
        'all49152_physical_lower_VRAM_pixels_exact_to_capture': True,
        'whole_chain_attempts_not_counted_as_complete': True,
        'next_actual_CPU_VRAM_mapping_dependency': p['next_concrete_chain_dependency'],
        'all8_caption_card_ordinary_contexts_miniature_Confirm_and_wider_goal_still_open': True,
        'all18_original_plaques_incomplete_all22_historical_scopes_exact': True,
        'ROM_patch_registry_canonical_and_all_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'guide_candidates': str(GUIDE),
        'full_goal_complete': False, 'canonical_promoted': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY] = entry
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        assert all(read(path)[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V643: original village coast selection and actual Narvik backdrop'
    addition = """

Current V640 repeats the original Narvik password/development0-to2 sequence with
only8 source-terrain-checked coordinate bytes changed. All54 shared two-screen
frames5308416 pixels match V618 without exclusions.288 original native selector
calls cover24 village IDs/all12 supplied contexts,selecting original coastal
files43/44/48;metadata flag20 is source-ROM zero,not village development. Actual
Narvik loads whole towngrp48 and exact512-byte palette/49152-index canvas. Its
registered original painter emits49152 complete source palette words,including
bit15,over a poisoned isolated destination with guards/ABI/clean code intact.
Actual lower VRAM matches all49152 captured pixels. Whole-chain attempts remain
uncredited:a later font callback needs actual CPU VRAM alias0601BFC8 at01FF9470.
54 unmodified screenshots and2 clearly labeled location-fixture guide candidates
are saved on E. No ROM/patch/registry/pointer changes. All18 plaques and22 scopes
remain exact;white cards,miniature/Confirm and broader gates stay open. See
[V643 checkpoint](village_backgrounds_v643_checkpoint.md).
"""
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n' + addition, encoding='utf-8')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('Archived54 current screenshots/2 disclosed-location guide candidates;3 additive audits;all18/22 scopes and release artifacts preserved.')


if __name__ == '__main__':
    main()
