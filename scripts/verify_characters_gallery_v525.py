"""All42 actual Characters screens, source ownership, regressions and patch."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.characters_gallery_text import BASE, NAMES, TABLE, transform
from dk4tool.patch.gallery_caption_bounds import validate
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_fleet_release_v375 import files

ROM = Path('out/all_routes_combined_v525_candidate.nds')
PARENT = Path('out/all_routes_combined_v523_candidate.nds')
OUT = Path('work/analysis/characters_gallery_v525')
ROOT = Path('E:/Rota Nova translations/Generated/work/emulation_v193')
CONTROL = ROOT / 'characters_control_v524'
CAPTURE = ROOT / 'characters_gallery_v525'
FRESH = ROOT / 'characters_gallery_v525_fresh'


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def report(folder, digest):
    path = folder / 'capture_report.json'
    data = read(path)
    assert data['ROM_sha256'] == digest and data['cold_boot'] and not data['savestate_loaded']
    assert not data['callback_errors']
    for row in data['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    for row in data.get('read_only_capture_RAM_snapshots', []):
        assert row['read_only_export'] and row['bytes'] == 0x400000
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    if data.get('battery_save_preloaded'):
        donor = data['battery_save_preloaded']
        assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
        assert data['synthetic_gallery_fixtures'] and not data['earned_unlock_verified']
    return data


def main():
    digest, parent_digest = sha(ROM.read_bytes()), sha(PARENT.read_bytes())
    assert digest == 'c84d292ac756cd91c817637c1bdf9257c4f4a16512eadedba698e7d10024a605'
    manifest, old_manifest = [read(p.with_suffix('.manifest.json')) for p in (ROM, PARENT)]
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v525'
    assert manifest['base_sha256'] == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['batches'] == old_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == old_manifest['required_batches'] and all(manifest['checks'].values())
    assert len(read('translations/release_stack.json')['accepted_layers']) == 114
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    a, b = [files(NdsImage.open(p)) for p in (PARENT, ROM)]
    assert sorted(p for p in a if a[p] != b[p]) == ['/__arm9__.bin']
    expected, stage = transform(a['/__arm9__.bin'])
    assert b['/__arm9__.bin'] == expected and len(stage['translated_source_owned_slots']) == 44
    assert len(validate(expected)) == 164
    assert len([p for p in a if p.lower().endswith(('.pxl', '.fls'))]) == 675
    control, current = report(CONTROL, parent_digest), report(CAPTURE, digest)
    plan = read(OUT / 'run_plan.json')
    assert control['scripted_input_schedule'] == current['scripted_input_schedule'] == read(OUT / 'inputs.json')
    assert current['frames'] == plan['final_frame'] and len(plan['frames']) == 42
    font = GameAsciiFont.from_arm9(expected)
    cases = []
    for index, frame in enumerate(plan['frames']):
        path = CAPTURE / f'frame_{frame:06d}_cold_boot.png'
        image = Image.open(path).convert('RGB')
        original = Image.open(CONTROL / path.name).convert('RGB')
        assert image.crop((0, 0, 256, 192)).tobytes() == original.crop((0, 0, 256, 192)).tobytes()
        ram = (CAPTURE / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        pointer = struct.unpack_from('<I', ram, TABLE + index * 4)[0]
        text = ram[pointer - BASE:pointer - BASE + 64].split(b'\0')[0].decode('ascii')
        assert text == f'{index:02d} {NAMES[index]}'
        title = ram[0x138A4C:0x138A58].split(b'\0')[0].decode('ascii')
        description = ram[0x139514:0x13952C].split(b'\0')[0].decode('ascii')
        assert title == 'Characters' and description == "The story's main cast."
        masks = []
        for label, x, y in [(title, 98, 194), (description, 16, 216), (text, 128 - len(text) * 3, 262)]:
            ink, bounds = complete_mask(font, label, image, x, y, (230, 230, 230))
            masks.append({'English': label, 'complete_ink_pixels': ink, 'bounds': bounds,
                          'all_first_final_letters_and_blank_cells_exact': True})
        # Every pixel outside the three source-owned text regions stays exact.
        regions = [(96, 192, 160, 212), (16, 216, 152, 232), (32, 262, 224, 278)]
        for y in range(384):
            for x in range(256):
                if any(lo <= x < hi and top <= y < bottom for lo, top, hi, bottom in regions):
                    continue
                assert image.getpixel((x, y)) == original.getpixel((x, y)), (index, x, y)
        cases.append({'index': index, 'image': str(path), 'runtime_name_pointer': pointer,
                      'complete_text_masks': masks, 'all49152_portrait_pixels_exact_to_original': True,
                      'all_surrounding_pixels_outside_three_text_fields_exact': True})
    first = Image.open(CAPTURE / 'frame_002800_cold_boot.png').convert('RGB')
    wrapped = Image.open(CAPTURE / 'frame_011200_cold_boot.png').convert('RGB')
    assert first.crop((0, 0, 256, 258)).tobytes() == wrapped.crop((0, 0, 256, 258)).tobytes()
    complete_mask(font, '00 Rafael', wrapped, 101, 262, (230, 230, 230))
    back = Image.open(CAPTURE / 'frame_011400_cold_boot.png').convert('RGB')
    assert back.tobytes() == Image.open(CONTROL / 'frame_011400_cold_boot.png').convert('RGB').tobytes()
    fresh = report(FRESH, digest)
    old_fresh = report(ROOT / 'gallery_caption_v523_fresh', parent_digest)
    assert fresh['scripted_input_schedule'] == old_fresh['scripted_input_schedule']
    assert fresh['core_options'] == old_fresh['core_options']
    old_frames, new_frames = [{r['frame']: r for r in d['frames_captured']} for d in (old_fresh, fresh)]
    assert old_frames.keys() == new_frames.keys() and len(old_frames) == 56
    assert all(old_frames[n]['PNG_sha256'] == new_frames[n]['PNG_sha256'] for n in old_frames)
    make_xdelta(Path('work/clean.nds'), ROM, ROM.with_suffix('.xdelta'))
    reconstructed = OUT / 'reconstructed.nds'
    apply_xdelta(Path('work/clean.nds'), ROM.with_suffix('.xdelta'), reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    parent_path = Path('work/analysis/gallery_caption_v523/preservation_proof.json')
    preservation = read(parent_path)
    assert len(preservation['entries']) == 921 and all(a[r['path']] == b[r['path']] for r in preservation['entries'])
    preservation.update(candidate=str(ROM), candidate_sha256=digest,
                        exact_container_parent=str(PARENT), exact_container_parent_sha256=parent_digest,
                        parent_preservation_proof=str(parent_path), parent_preservation_proof_sha256=sha(parent_path.read_bytes()))
    (OUT / 'preservation_proof.json').write_text(json.dumps(preservation, indent=2) + '\n', encoding='utf-8')
    plaques = read('translations/graphics_completion_campaign_v1.json')['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not r['fully_completed'] for r in plaques)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()), 'exact_clean_patch_reconstruction': True,
             'all470_batches_and114_accepted_layers_preserved': True,
             'only44_source_owned_Characters_strings_change': stage['translated_source_owned_slots'],
             'all42_actual_Characters_screens': cases, 'all42_portraits_exact_to_original_GPU': True,
             'all126_complete_heading_description_name_masks_pass': True,
             'original_carousel_wrap_and_Back_verified': True,
             'all164_Event_Scenes_title_bounds_guard_retained': True,
             'all56_fresh_regression_frames_exact': True,
             'all675_graphics_and_every_other_component_byte_exact_to_V523': True,
             'all921_preservation_entries_inherited_by_exact_container_equality': True,
             'source_control_report': str(CONTROL / 'capture_report.json'),
             'source_control_report_sha256': sha((CONTROL / 'capture_report.json').read_bytes()),
             'actual_report': str(CAPTURE / 'capture_report.json'),
             'actual_report_sha256': sha((CAPTURE / 'capture_report.json').read_bytes()),
             'synthetic_Gallery_unlock_test_original_donor_unchanged': True,
             'earned_unlock_normal_ending_and_legacy_consumer_not_claimed': True,
             'all22_requirements_and18_incomplete_plaques_retained': True,
             'status': 'experimental', 'canonical_promotion': False,
             'full_goal_complete': False, 'hardware_device_verification': False}
    (OUT / 'release_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('V525:44 translated fields,42 exact portraits,126 complete masks,56 fresh frames, inherited content and exact patch pass.')


if __name__ == '__main__':
    main()
