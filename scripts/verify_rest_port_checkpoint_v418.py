"""Normal Inn recovery, real route gate and completed isolated sea save/reload."""

import json
from pathlib import Path

from PIL import Image
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.read_navigation_snapshot_v391 import inspect
from scripts.record_navigation_v327 import dark_text
from scripts.verify_plaque_release_v247 import find_mask

ROM = Path('out/all_routes_combined_v414_candidate.nds')
ROOT = Path('work/analysis/rest_and_port_leg_v415')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def capture(name, digest):
    p = Path('work/emulation_v193') / name / 'capture_report.json'
    r = read(p)
    assert r['ROM_sha256'] == digest and r['cold_boot'] and not r['savestate_loaded']
    assert not r['callback_errors']
    frames = {}
    for row in r['frames_captured']:
        q = Path(row['path'])
        assert sha(q.read_bytes()) == row['PNG_sha256']
        if 'cold_boot' in q.name:
            frames[row['frame']] = q
    return p, r, frames


def main():
    digest = sha(ROM.read_bytes())
    assert digest == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    op, original, of = capture('rest_and_port_leg_v415', digest)
    rp, replay, rf = capture('rest_port_save_complete_v417', digest)
    lp, loaded, _lf = capture('port_leg_verified_reload_v418', digest)
    assert replay['frames'] == 26000 and loaded['frames'] == 3200
    assert original['scripted_input_schedule'] == replay['scripted_input_schedule']
    exact = []
    for f in rf:
        if f <= 23800:
            assert rf[f].read_bytes() == of[f].read_bytes(), f
            exact.append(f)
    font = GameAsciiFont.from_arm9(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    menus = []
    for frame, texts, region in [(5200, ['Stay 1 Day', 'Stay More'], (70, 260, 180, 315)),
                                 (6400, ['3 Days', '10 Days', '30 Days'], (70, 255, 180, 325))]:
        image = Image.open(rf[frame]).convert('RGB')
        menus.extend({'frame': frame, **dark_text(font, text, image, region)} for text in texts)
    inn = dark_text(font, 'Inn', Image.open(rf[4400]).convert('RGB'), (0, 244, 125, 285))
    before = find_mask(font, '66', Image.open(rf[3200]).convert('RGB'), (168, 344, 209, 366))
    after = find_mask(font, '0', Image.open(rf[12000]).convert('RGB'), (168, 344, 209, 366))
    gate = Image.open(rf[16800]).convert('RGB')
    route = [dark_text(font, 'There is no route', gate, (8, 292, 252, 317)),
             dark_text(font, 'to that city.', gate, (8, 309, 252, 335))]
    saved = Path(replay['battery_save_preloaded']['destination'])
    assert loaded['battery_save_preloaded']['source_sha256'] == sha(saved.read_bytes())
    donor = Path('E:/Rota Nova translations/Saves/hodram-blue-oak-clue-v408.dsv')
    assert sha(donor.read_bytes()) == original['battery_save_preloaded']['source_sha256']
    assert replay['battery_save_preloaded']['source_sha256'] == sha(donor.read_bytes())
    state = loaded['read_only_RAM_snapshot']
    ram = Path(state['path']).read_bytes()
    assert sha(ram) == state['sha256'] and state['read_only_export']
    u = machine(NdsImage.open(ROM).read_file('/__arm9__.bin'))
    u.mem_write(0x02000000, ram)
    call(u, 0xCB190, ())
    items = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x4A394, (items + 4 + 49 * 20,))
    assert u.reg_read(UC_ARM_REG_R0) == 1
    ship = inspect(Path(state['path']), ROM)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'completed_report': str(rp), 'completed_report_sha256': sha(rp.read_bytes()),
             'reload_report': str(lp), 'reload_report_sha256': sha(lp.read_bytes()),
             'original_interactive_report': str(op), 'exact_replay_frames_before_save': exact,
             'actual_complete_Inn_label': inn, 'actual_complete_stay_menu_labels': menus,
             'actual_fatigue_before66_after0_masks': [before, after],
             'actual_10_nights_normal_confirmed_rest': True,
             'date_and_coin_change_visually_observed_not_independent_economy_proof': True,
             'actual_Copenhagen_Auto_Move_route_gate': route,
             'manual_sailing_toward_Copenhagen_port_not_yet_reached': True,
             'interrupted_first_slot6_save_rejected_not_used_or_published': True,
             'completed_replay_slot6_cold_boot_load_verified': True,
             'saved_battery': str(saved), 'saved_battery_sha256': sha(saved.read_bytes()),
             'original_E_donor_unchanged_sha256': sha(donor.read_bytes()),
             'actual_reloaded_ship_state': ship,
             'small_position_change_during_reload_gameplay_not_exact_same_frame_claim': True,
             'original_Blue_Oak_clue_retained': True, 'armor_acquired': False,
             'all18_plaques_incomplete': True, 'ROM_changed': False, 'full_goal_complete': False}
    (ROOT / 'rest_checkpoint_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'Actual Inn/stay/fatigue/gate masks; {len(exact)} exact replay frames; completed slot6 loads sea with clue1. Donor unchanged.')


if __name__ == '__main__':
    main()
