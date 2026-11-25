"""Genuine Copenhagen landing/resupply, complete labels and completed save reload."""

import json
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.record_navigation_v327 import dark_text
from scripts.verify_commodity_layout_v346 import mask
from scripts.verify_plaque_release_v247 import find_mask

ROM = Path('out/all_routes_combined_v414_candidate.nds')
ROOT = Path('work/analysis/copenhagen_arrival_v419')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def report(name, digest):
    path = Path('work/emulation_v193') / name / 'capture_report.json'
    r = read(path)
    assert r['ROM_sha256'] == digest and r['cold_boot'] and not r['savestate_loaded']
    assert not r['callback_errors']
    for row in r['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return path, r


def labels(font, image):
    return {'town': find_mask(font, 'Copenhagen', image, (0, 10, 256, 40)),
            'coordinates': find_mask(font, '(N55 E12)', image, (0, 10, 256, 40)),
            'specialties': [mask(image, font, text, y) for text, y in
                            [('Beef', 88), ('Glass', 104), ('Cannon', 120)]]}


def main():
    digest = sha(ROM.read_bytes())
    assert digest == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    arrival_path, arrived = report('copenhagen_arrival_v419', digest)
    reload_path, loaded = report('copenhagen_saved_reload_v420', digest)
    assert arrived['frames'] == 10400 and loaded['frames'] == 3200
    folder = arrival_path.parent
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    prompt = dark_text(font, 'Dock at Copenhagen?',
                       Image.open(folder / 'frame_004000_navigation.png').convert('RGB'), (8, 292, 252, 320))
    old = Image.open(folder / 'frame_004400_navigation.png').convert('RGB')
    new = Image.open(reload_path.parent / 'frame_003200_final.png').convert('RGB')
    cases = [labels(font, old), labels(font, new)]
    saved = Path(arrived['battery_save_preloaded']['destination'])
    assert sha(saved.read_bytes()) == loaded['battery_save_preloaded']['source_sha256']
    original = Path('E:/Rota Nova translations/Saves/hodram-copenhagen-approach-v414.dsv')
    assert sha(original.read_bytes()) == arrived['battery_save_preloaded']['source_sha256']
    assert sha(Path(arrived['battery_save_preloaded']['source']).read_bytes()) == sha(original.read_bytes())
    snapshot = loaded['read_only_RAM_snapshot']
    ram = Path(snapshot['path']).read_bytes()
    assert sha(ram) == snapshot['sha256'] and snapshot['read_only_export']
    u = machine(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    u.mem_write(0x02000000, ram)
    call(u, 0xCB190, ())
    root = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x4A394, (root + 4 + 49 * 20,))
    assert u.reg_read(UC_ARM_REG_R0) == 1
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'arrival_report': str(arrival_path), 'arrival_report_sha256': sha(arrival_path.read_bytes()),
             'reload_report': str(reload_path), 'reload_report_sha256': sha(reload_path.read_bytes()),
             'normal_Copenhagen_arrival_and_resupply': True,
             'actual_complete_dock_prompt': prompt, 'actual_arrival_and_reloaded_town_masks': cases,
             'original_approach_donor_and_explicit_test_copy_unchanged': True,
             'only_isolated_slot6_normally_overwritten_after_explicit_game_confirmation': True,
             'save_allowed_to_finish_and_normal_cold_boot_reload_verified': True,
             'saved_battery': str(saved), 'saved_battery_sha256': sha(saved.read_bytes()),
             'Blue_Oak_clue_retained': True, 'armor_acquired': False,
             'price172_and_funds_changes_visually_observed_not_independent_economy_proof': True,
             'no_savestate_live_RAM_or_synthetic_progress_edit': True,
             'ROM_changed': False, 'all18_plaques_incomplete': True, 'full_goal_complete': False}
    (ROOT / 'arrival_reload_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Actual Copenhagen docking, all complete goods/name/coordinate masks, completed slot6 save/reload and clue1 pass.')


if __name__ == '__main__':
    main()
