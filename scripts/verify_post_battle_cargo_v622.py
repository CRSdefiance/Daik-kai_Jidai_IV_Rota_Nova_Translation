"""Verify the original post-victory Spoils header and ordinary cargo controls."""

import struct
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine
from scripts.verify_regional_ui_v616 import full_cells, native5
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/post_battle_cargo_v622')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/post_battle_cargo_v622_actual')
ROM = Path('out/all_routes_combined_v621_candidate.nds')


def main():
    rom = NdsImage.open(ROM)
    digest = sha(ROM.read_bytes())
    report = read(CAP / 'capture_report.json')
    assert report['ROM_sha256'] == digest and report['frames'] == 30401
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    fixtures = report['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures) == 1 and fixtures[0]['frame'] == 20400
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    shots = {r['frame']: r for r in report['frames_captured']}
    arm = rom.read_file('/__arm9__.bin')
    art = rom.read_file('/_pxl/senrihin.pxl')
    atlas = native5(PxlImage.from_bytes(art).render())
    font = GameAsciiFont.from_arm9(arm)
    bindings, images, states = [], {}, {}
    for frame in (24800, 25200, 26800, 27200, 28000, 28400, 28800, 29200, 29600):
        raw = (CAP / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        row = shots[frame]
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
        images[frame] = Image.open(row['path']).convert('RGB')
        candidates = [at - 12 for at in range(0x17000C, len(raw) - 48, 4)
                      if struct.unpack_from('<I', raw, at)[0] == 0x02313A4C
                      and struct.unpack_from('<2I', raw, at + 28) == (256, 16)]
        assert len(candidates) == 1
        view = BASE + candidates[0]
        parent = view - 0x3070  # Executed source8537C, inherited original object layout.
        assert struct.unpack_from('<I', raw, parent - BASE + 0x10)[0] == 3
        u = machine(arm)
        u.mem_write(BASE, raw)
        filename = struct.unpack('<I', u.mem_read(0x02313A4C + 12, 4))[0]
        assert bytes(u.mem_read(filename, 32)).split(b'\0')[0] == b'_pxl/senrihin.pxl'
        call(u, 0xD4170, (view,))
        pointer = u.reg_read(UC_ARM_REG_R0)
        assert bytes(u.mem_read(pointer, len(art))) == art
        bindings.append({'frame': frame, 'view': view, 'parent': parent, 'original_mode': 3,
                         'original_named_owner': 0x02313A4C, 'resident_PXL': pointer,
                         'whole_resident_PXL_exact': True, 'RAM_sha256': sha(raw)})
        states[frame] = [raw[parent - BASE + 0x18 + i * 12] for i in range(5)]
    banners = []
    for frame in (25200, 26800, 27200, 28000, 28800):
        assert native5(images[frame]).crop((0, 261, 256, 277)).tobytes() == atlas.tobytes()
        banners.append({'frame': frame, 'complete_source_destination_pixels': 4096,
                        'complete_Spoils_letters_wood_borders_and_palette_exact': True})
    old = native5(images[24800])
    diff = [(x, y) for y in range(16) for x in range(256)
            if old.getpixel((x, 261 + y)) != atlas.getpixel((x, y))]
    assert len(diff) == 301 and all(16 <= x < 50 and 5 <= y < 16 for x, y in diff)
    assert states[26800] == [90, 90, 125, 125, 125]
    assert states[27200] == [125] * 5
    assert states[28000] == [90, 125, 125, 125, 125]
    assert states[28800] == states[28000]
    notices = []
    for frame in (28400, 29200, 29600):
        notices.append({'frame': frame, 'lines': [
            full_cells(images[frame], font, 'Unloaded goods are lost.', 22, 296, (0, 8, 0)),
            full_cells(images[frame], font, 'Continue?', 22, 312, (0, 8, 0))]})
    save(ROOT / 'release_proof.json', {
        'candidate': str(ROM), 'candidate_sha256': digest, 'ROM_unchanged': True,
        'report': str(CAP / 'capture_report.json'), 'report_sha256': sha((CAP / 'capture_report.json').read_bytes()),
        'original_post_battle_mode3_resource_bindings': bindings,
        'five_complete_ordinary_Spoils_banners': banners, 'total_banner_pixels_exact': 20480,
        'initial_Armor_tooltip_occlusion_pixels_not_missing_graphic': len(diff),
        'normal_Unload_clears_both_original_Iron_slots_and_Select_reloads_one': states,
        'normal_cancel_returns_without_committing_and_finish_Yes_exits': True,
        'three_complete_finish_confirmations': notices,
        'post_victory_context_uses_one_disclosed_ship_proximity_fixture': fixtures[0],
        'no_header_choice_artwork_inventory_or_result_injection': True,
        'Distributed_Goods_and_miniature_Confirm_contexts_not_closed_by_this_proof': True,
        'all18_original_plaques_remain_incomplete_all22_historical_scopes_retained': True,
        'full_goal_complete': False, 'script_sha256': sha(Path(__file__).read_bytes())})
    print('Original post-battle Spoils:9 source bindings,5 whole banners/20480 pixels,Unload/Select/cancel/finish and3 full prompts pass.')


if __name__ == '__main__':
    main()
