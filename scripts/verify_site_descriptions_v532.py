"""All nineteen actual photos/prose and relocated name consumers, plus release."""

import json
import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.characters_gallery_text import NAMES
from dk4tool.patch.characters_gallery_text import TABLE as CHARACTERS_TABLE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.historic_site_names import BASE
from dk4tool.patch.historic_site_names import TABLE as SITE_TABLE
from dk4tool.patch.site_descriptions import DESCRIPTION_TABLE, formatted, transform
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_characters_gallery_v525 import report
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_fleet_release_v375 import files

ROM = Path('out/all_routes_combined_v532_candidate.nds')
PARENT = Path('out/all_routes_combined_v528_candidate.nds')
OUT = Path('work/analysis/site_descriptions_v532')
ROOT = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def paragraph(font, image, lines):
    expected = {(column * 6 + gx, 212 + row * 12 + gy)
                for row, line in enumerate(lines) for column, ch in enumerate(line)
                for gy in range(11) for gx in range(6) if font.decode(ch).getpixel((gx, gy))}
    actual = {(x, y) for y in range(212, 356) for x in range(256)
              if image.getpixel((x, y)) == (230, 230, 230)}
    assert actual == expected, (len(actual), len(expected), list(actual ^ expected)[:5])
    return {'lines': lines, 'origin': [0, 212], 'advance': 6, 'line_height': 12,
            'complete_ink_pixels': len(expected), 'all_first_last_letters_and_blank_cells_exact': True,
            'all_lines_same_left_margin_and_all_words_complete': True}


def main():
    digest, parent_digest = sha(ROM.read_bytes()), sha(PARENT.read_bytes())
    assert digest == 'ddc5541058dee0ccbb93dfece736be97e8a06ec64b53befff935753e22539f88'
    manifest, old_manifest = [read(p.with_suffix('.manifest.json')) for p in (ROM, PARENT)]
    assert manifest['profile'] == 'all-routes-unified-v532' and manifest['candidate_sha256'] == digest
    assert all(manifest['checks'].values()) and manifest['batches'] == old_manifest['batches']
    assert len(manifest['batches']) == 470 and manifest['required_batches'] == old_manifest['required_batches']
    registry = read('translations/release_stack.json')
    assert len(registry['accepted_layers']) == 114
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    a, b = [files(NdsImage.open(p)) for p in (PARENT, ROM)]
    assert sorted(p for p in a if a[p] != b[p]) == ['/__arm9__.bin']
    manuscript = read('translations/historic_site_description_manuscript_v2.json')
    expected, stage = transform(a['/__arm9__.bin'], manuscript, formatting_profile='static-site-gallery-pair-phase-v2')
    assert b['/__arm9__.bin'] == expected and len(stage['pointer_bindings']) == 82
    assert stage['owned_bytes'] == 3668 and stage['complete_compiled_bytes'] == 3631
    font = GameAsciiFont.from_arm9(expected)
    names = read('translations/historic_site_names_v2.json')['records']
    control_folder = ROOT / 'supported_site_images_v529_control'
    folder = ROOT / 'site_descriptions_v532'
    control, current = report(control_folder, parent_digest), report(folder, digest)
    assert control['scripted_input_schedule'] == current['scripted_input_schedule']
    assert 'Undefined instruction' not in Path('work/analysis/site_descriptions_v529/control_run.log').read_text(encoding='utf-8')
    assert 'Undefined instruction' not in (OUT / 'sites_run.log').read_text(encoding='utf-8')
    fixture = read(OUT / 'sites_fixture_manifest.json')
    assert fixture['only_supported_source_Gallery_images_selected']
    assert fixture['excluded_original_null_image_placeholder_ids'] == [1, 4]
    plan = read('work/analysis/site_descriptions_v529/run_plan.json')
    assert current['frames'] == control['frames'] == plan['final_frame'] == 7400
    cases = []
    for number, (row, frame) in enumerate(zip(manuscript['records'], plan['image_frames'], strict=True)):
        index = row['site_id']
        assert index == plan['supported_site_ids'][number]
        path = folder / f'frame_{frame:06d}_cold_boot.png'
        image = Image.open(path).convert('RGB')
        old_image = Image.open(control_folder / path.name).convert('RGB')
        assert image.crop((0, 0, 256, 212)).tobytes() == old_image.crop((0, 0, 256, 212)).tobytes()
        assert image.crop((0, 356, 256, 384)).tobytes() == old_image.crop((0, 356, 256, 384)).tobytes()
        resource = f'/Iseki/Iseki{number:02d}.pxl'
        assert a[resource] == b[resource]
        source = PxlImage.from_bytes(b[resource])
        assert source.width == 256 and source.height == 192
        palette = [tuple(c // 8 for c in value[:3]) for value in source.palette]
        assert all(tuple(c // 8 for c in image.getpixel((n % 256, n // 256))) == palette[value]
                   for n, value in enumerate(source.indices)), resource
        title = names[index]['english']
        title_ink, bounds = complete_mask(font, title, image, 128 - len(title) * 3, 194, (230, 230, 230))
        _, lines = formatted(row['english'], 'static-site-gallery-pair-phase-v2')
        masks = paragraph(font, image, lines)
        cases.append({'site_id': index, 'image': str(path), 'source_resource': resource,
                      'all49152_native_source_photo_pixels_exact_at5bit': True,
                      'title': title, 'complete_title_pixels': title_ink, 'title_bounds': bounds,
                      'complete_paragraph': masks, 'all_pixels_outside_description_region_exact_to_V528': True})
    # The source-supported combined collection opens, wraps and returns without
    # including original null image slots. Existing diagnostic fixtures are retained.
    for frame in (2800, plan['return_frame'], plan['final_frame']):
        name = f'frame_{frame:06d}_cold_boot.png'
        assert Image.open(folder / name).convert('RGB').tobytes() == Image.open(control_folder / name).convert('RGB').tobytes()
    wrap = Image.open(folder / f"frame_{plan['wrap_frame']:06d}_cold_boot.png").convert('RGB')
    first = Image.open(folder / 'frame_003200_cold_boot.png').convert('RGB')
    assert wrap.crop((0, 0, 256, 192)).tobytes() == first.crop((0, 0, 256, 192)).tobytes()
    paragraph(font, wrap, formatted(manuscript['records'][0]['english'], 'static-site-gallery-pair-phase-v2')[1])
    ram = (folder / 'final_arm9_ram.bin').read_bytes()
    u = machine(expected)
    u.mem_write(BASE, ram)
    call(u, 0xCB16C, ())
    store = u.reg_read(UC_ARM_REG_R0)
    for index, row in enumerate(names):
        call(u, 0x87444, (store + 4 + index * 8,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        assert pointer == struct.unpack_from('<I', ram, SITE_TABLE + index * 4)[0]
        assert bytes(u.mem_read(pointer, len(row['english']) + 1)) == row['english'].encode('ascii') + b'\0'
    for row in manuscript['records']:
        pointer = struct.unpack_from('<I', ram, DESCRIPTION_TABLE + row['site_id'] * 4)[0]
        raw = formatted(row['english'], 'static-site-gallery-pair-phase-v2')[0]
        assert ram[pointer - BASE:pointer - BASE + len(raw)] == raw
    char_folder = ROOT / 'site_descriptions_v532_characters'
    character_report = report(char_folder, digest)
    old_char_folder = ROOT / 'characters_gallery_v525'
    old_character_report = report(old_char_folder, sha(Path('out/all_routes_combined_v525_candidate.nds').read_bytes()))
    assert character_report['scripted_input_schedule'] == old_character_report['scripted_input_schedule']
    char_plan = read('work/analysis/characters_gallery_v525/run_plan.json')
    for index, frame in enumerate(char_plan['frames']):
        file = f'frame_{frame:06d}_cold_boot.png'
        assert Image.open(char_folder / file).tobytes() == Image.open(old_char_folder / file).tobytes()
        char_ram = (char_folder / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        pointer = struct.unpack_from('<I', char_ram, CHARACTERS_TABLE + index * 4)[0]
        text = f'{index:02d} {NAMES[index]}'
        assert char_ram[pointer - BASE:pointer - BASE + len(text) + 1] == text.encode('ascii') + b'\0'
        complete_mask(font, text, Image.open(char_folder / file).convert('RGB'), 128 - len(text) * 3, 262, (230, 230, 230))
    for frame in (char_plan['wrap'], char_plan['back']):
        file = f'frame_{frame:06d}_cold_boot.png'
        assert Image.open(char_folder / file).tobytes() == Image.open(old_char_folder / file).tobytes()
    fresh = report(ROOT / 'site_descriptions_v532_fresh', digest)
    old_fresh = report(ROOT / 'historic_sites_v528_fresh', parent_digest)
    assert fresh['scripted_input_schedule'] == old_fresh['scripted_input_schedule'] and fresh['core_options'] == old_fresh['core_options']
    old_frames, new_frames = [{r['frame']: r for r in data['frames_captured']} for data in (old_fresh, fresh)]
    assert old_frames.keys() == new_frames.keys() and len(new_frames) == 56
    assert all(old_frames[n]['PNG_sha256'] == new_frames[n]['PNG_sha256'] for n in old_frames)
    make_xdelta(Path('work/clean.nds'), ROM, ROM.with_suffix('.xdelta'))
    apply_xdelta(Path('work/clean.nds'), ROM.with_suffix('.xdelta'), OUT / 'reconstructed.nds')
    assert (OUT / 'reconstructed.nds').read_bytes() == ROM.read_bytes()
    pp = Path('work/analysis/historic_sites_v528/preservation_proof.json')
    preservation = read(pp)
    assert len(preservation['entries']) == 921 and all(a[r['path']] == b[r['path']] for r in preservation['entries'])
    preservation.update(candidate=str(ROM), candidate_sha256=digest,
                        exact_container_parent=str(PARENT), exact_container_parent_sha256=parent_digest,
                        parent_preservation_proof=str(pp), parent_preservation_proof_sha256=sha(pp.read_bytes()))
    (OUT / 'preservation_proof.json').write_text(json.dumps(preservation, indent=2) + '\n', encoding='utf-8')
    plaques = read('translations/graphics_completion_campaign_v1.json')['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not r['fully_completed'] for r in plaques)
    assert len(read('translations/graphics_completion_requirements_v313.json')['historical_pending_items_retained']) == 22
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()), 'exact_clean_patch_reconstruction': True,
             'all19_complete_actual_source_photos_captions_and_natural_English_paragraphs': cases,
             'all933888_source_photo_pixels_exact': True, 'all_paragraphs_complete_words_and_equal_left_margins': True,
             'all42_Characters_frames_names_wrap_and_Back_exact': True,
             'all21_original_site_name_getters_full_bytes_and_ABI_verified': True,
             'all164_Event_Scenes_caption_text_pointers_and_bounds_unchanged': True,
             'all19_supported_image_collection_wrap_and_return_verified_without_CPU_fault': True,
             'original_null_image_placeholder_slots1_4_excluded_from_fixture_not_game_patched': True,
             'all56_fresh_frames470_batches114_layers675_graphics921_preservation_entries_retained': True,
             'all_section_extents_startup_heap_cache_and_unowned_data_exact': True,
             'all22_requirements_and18_incomplete_plaques_retained': True,
             'broader_normal_discovery_gameplay_and_legacy_contexts_remain': True,
             'status': 'experimental', 'canonical_promotion': False, 'full_goal_complete': False,
             'hardware_device_verification': False}
    (OUT / 'release_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('V532:19 complete paragraphs/photos,933888 source pixels,42 exact Character frames,21 getters,56 fresh frames,inherited content and exact patch pass.')


if __name__ == '__main__':
    main()
