"""Normal voyage progress, actual Tavern clue and battery-save persistence."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROM = Path('out/all_routes_combined_v408_candidate.nds')
ROOT = Path('work/analysis/manual_clue_progress_v409')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def report(name, digest):
    path = Path('work/emulation_v193') / name / 'capture_report.json'
    data = read(path)
    assert data['ROM_sha256'] == digest and data['cold_boot']
    assert not data['savestate_loaded'] and not data['callback_errors']
    for row in data['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    return path, data


def state(arm, row):
    raw = Path(row['path']).read_bytes()
    assert sha(raw) == row['sha256'] and row['read_only_export']
    u = machine(arm)
    u.mem_write(0x02000000, raw)
    call(u, 0xCB190, ())
    item = u.reg_read(UC_ARM_REG_R0) + 4 + 49 * 20
    item_raw = bytes(u.mem_read(item, 20))
    call(u, 0x4A394, (item,))
    known = u.reg_read(UC_ARM_REG_R0)
    score = sum(struct.unpack_from('<2I', raw, 0x2D5D24 + 0x10))
    assert bytes(u.mem_read(0x02000000, len(raw))) == raw
    return {'score': score, 'clue_flag': known, 'item_address': item,
            'item_record_hex': item_raw.hex(), 'snapshot_sha256': sha(raw)}


def main():
    digest = sha(ROM.read_bytes())
    assert digest == read(ROM.with_suffix('.manifest.json'))['candidate_sha256']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    trip_path, trip = report('manual_clue_progress_v409', digest)
    clue_path, clue = report('eligible_tavern_v410', digest)
    reload_path, reload = report('clue_saved_reload_v411', digest)
    samples = {r['frame']: r for r in trip['read_only_pause_RAM_snapshots']}
    before = state(arm, samples[5600])
    qualified = state(arm, samples[10200])
    earned = state(arm, clue['read_only_RAM_snapshot'])
    persisted = state(arm, reload['read_only_RAM_snapshot'])
    assert before['score'] == 5252 and before['clue_flag'] == 0
    assert qualified['score'] == 6176 and qualified['clue_flag'] == 0
    assert earned['score'] >= 6000 and earned['clue_flag'] == persisted['clue_flag'] == 1
    assert earned['score'] == persisted['score']
    saved = Path(clue['battery_save_preloaded']['destination'])
    assert sha(saved.read_bytes()) == reload['battery_save_preloaded']['source_sha256']
    original = Path(trip['battery_save_preloaded']['source'])
    assert sha(original.read_bytes()) == trip['battery_save_preloaded']['source_sha256']
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'reports': [str(p) for p in [trip_path, clue_path, reload_path]],
             'report_sha256': [sha(p.read_bytes()) for p in [trip_path, clue_path, reload_path]],
             'before_voyage': before, 'qualified_by_normal_voyage': qualified,
             'earned_after_normal_Treat_Everyone': earned, 'normal_save_reload': persisted,
             'actual_clue_capture': 'work/emulation_v193/eligible_tavern_v410/frame_012800_navigation.png',
             'new_saved_slot': 5, 'saved_battery': str(saved), 'saved_battery_sha256': sha(saved.read_bytes()),
             'original_Riga_donor_unchanged': True,
             'no_stats_item_unlock_or_live_RAM_injection': True,
             'clue_870_Japanese_address_and_word_split_confirmed_pending_fix': True,
             'not_finalized_guide_screen': True, 'armor_owned_or_equipped': False,
             'all18_plaques_incomplete': True, 'ROM_changed': False, 'full_goal_complete': False}
    (ROOT / 'earned_clue_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('Normal score5252->6176; Blue Oak clue0->1 via Treat Everyone; slot5 reload retains clue/score. Armor not acquired.')


if __name__ == '__main__':
    main()
