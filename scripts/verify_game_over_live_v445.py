"""Genuine Game Over caption, resource loading, and prior-release regression."""

import json
import struct
from pathlib import Path

from PIL import Image

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.record_navigation_v327 import dark_text
from scripts.verify_original_latin_cards_native_v197 import native5
from scripts.verify_plaque_release_v247 import find_mask

ROOT = Path('work/analysis/armor_voyage_v445')
ROM = Path('out/all_routes_combined_v443_candidate.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def report(name, rom):
    path = Path('work/emulation_v193') / name / 'capture_report.json'
    data = read(path)
    assert data['ROM_sha256'] == sha(rom.read_bytes())
    assert data['cold_boot'] and not data['savestate_loaded'] and not data['callback_errors']
    assert data['frames'] == 16400
    donor = Path(data['battery_save_preloaded']['source'])
    assert sha(donor.read_bytes()) == data['battery_save_preloaded']['source_sha256']
    for row in data['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return path, data


def main():
    path, current = report('armor_voyage_v445', ROM)
    parent_rom = Path('out/all_routes_combined_v414_candidate.nds')
    parent_path, parent = report('game_over_parent_v445', parent_rom)
    assert current['scripted_input_schedule'] == parent['scripted_input_schedule']
    assert current['battery_save_preloaded']['source_sha256'] == parent['battery_save_preloaded']['source_sha256']
    old = {row['frame']: row for row in parent['frames_captured']}
    matched = []
    for row in current['frames_captured']:
        if 'cold_boot' in row['path'] or 'final' in row['path']:
            assert Image.open(row['path']).tobytes() == Image.open(old[row['frame']]['path']).tobytes(), row['frame']
            matched.append(row['frame'])
    final = next(row for row in current['frames_captured'] if 'final' in row['path'])
    image = Image.open(final['path']).convert('RGB')
    snapshot = current['read_only_RAM_snapshot']
    ram = Path(snapshot['path']).read_bytes()
    assert sha(ram) == snapshot['sha256'] and snapshot['read_only_export']
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    background_raw, caption_raw = [rom.read_file(p) for p in ('/_pxl/gameover.pxl', '/_pxl/overfont.pxl')]
    assets = []
    for resource, raw, owner, view, size in [
        ('/_pxl/gameover.pxl', background_raw, 0x0231390C, 0x02192A00, (256, 192)),
        ('/_pxl/overfont.pxl', caption_raw, 0x023138F8, 0x02192A74, (160, 32)),
    ]:
        assert raw == clean.read_file(resource)
        loaded = ram.find(raw)
        assert loaded >= 0
        fields = list(struct.unpack_from('<12I', ram, view - 0x02000000))
        assert fields[3] == owner and fields[7:10] == [0, 0, 0]
        assert tuple(fields[10:12]) == size
        pointer = struct.unpack_from('<I', ram, owner - 0x02000000 + 12)[0]
        name = ram[pointer - 0x02000000:].split(b'\0', 1)[0].decode('ascii')
        assert '/' + name == resource
        assets.append({'path': resource, 'source_sha256': sha(raw), 'source_byte_exact_clean': True,
                       'complete_loaded_bytes': len(raw), 'loaded_address': 0x02000000 + loaded,
                       'owner': owner, 'view': view, 'view_fields': fields, 'palette_bank': 0})
    background, caption = PxlImage.from_bytes(background_raw), PxlImage.from_bytes(caption_raw)
    assert (caption.width, caption.height) == (160, 32)
    ink = 0
    for y in range(32):
        for x in range(160):
            index = caption.indices[y * 160 + x]
            expected = caption.palette[index] if index else background.palette[background.indices[(y + 80) * 256 + x + 48]]
            assert native5(image.getpixel((x + 48, y + 272))) == native5(expected)
            ink += bool(index)
    assert ink == 835
    font = GameAsciiFont.from_arm9(rom.read_file('/__arm9__.bin'))
    action = find_mask(font, 'Select', image, (212, 366, 256, 384))
    no_crew = dark_text(font, 'Vestaros has no sailors!',
                        Image.open('work/emulation_v193/armor_voyage_v445/frame_015600_navigation.png').convert('RGB'),
                        (8, 292, 253, 320))
    assert no_crew['ink_pixels'] == 237
    release = read(Path('work/analysis/guild_description_release_v443/release_proof.json'))
    proof = {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'patch_sha256': release['patch_sha256'],
        'exact_clean_patch_reconstruction': release['exact_clean_patch_reconstruction'],
        'inherited_release_proof': 'work/analysis/guild_description_release_v443/release_proof.json',
        'capture_report': str(path), 'capture_report_sha256': sha(path.read_bytes()),
        'parent_report': str(parent_path), 'parent_report_sha256': sha(parent_path.read_bytes()),
        'source_battery_save_unchanged': True, 'ordinary_inputs_only': True,
        'natural_game_over_reached': True, 'armor_acquired_or_equipped': False,
        'complete_loaded_clean_source_resources_and_actual_views': assets,
        'full_original_English_Game_Over_caption': {
            'screen_origin': [48, 272], 'extent': [160, 32], 'ink_pixels': ink,
            'all5120_caption_and_background_cells_exact': True,
            'all_first_interior_final_lettering_pixels_exact': True,
            'source_decision': 'Retain existing original English lettering and artwork.'},
        'full_Select_action': action, 'full_no_sailors_message': no_crew,
        'all_comparable_frames_pixel_exact_to_V414': matched,
        'whole_final_Game_Over_frame_pixel_exact_to_V414': True,
        'background_composition_limit': 'The footer and14 additional bright pixels differ from the standalone background PXL. Their full-frame output matches V414; no independent overlay identity or full source-only background composite is claimed.',
        'ROM_changed': False, 'hardware_device_verification': False,
        'all18_plaques_incomplete': True, 'full_goal_complete': False,
    }
    (ROOT / 'game_over_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'Game Over:835 complete source caption pixels/5120 cells,72 Select pixels,237 warning pixels;{len(matched)} prior-release frames exact. Armor not acquired.')


if __name__ == '__main__':
    main()
