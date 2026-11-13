"""Select Maria explicitly from source-derived navigator button coordinates."""

import argparse
import copy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts import observe_room_gender_v694 as observer
from scripts import run_room_gender_v694 as runner
from scripts.verify_village_wrap_v608 import read, save

ROOT = runner.ROOT / 'selection'


def prepare():
    ROOT.mkdir()
    original = read(runner.ROOT / 'preflight.json')
    inputs = [r for r in read(runner.ROOT / 'inputs.json') if r['start'] <= 8401]
    # Actual sorted room list: actor IDs12,10,3,11,21. Original button rectangles
    # are x88..104,108..124,128..144,... and y12..44 relative to roster origin.
    # Their screen centers are (96,68),(116,68),(136,68),... on the touchscreen.
    inputs += [{'start': frame, 'duration': 8, 'touch': [x, 68]} for frame, x in (
        (8801, 136), (9201, 96), (9601, 136), (10001, 116), (10401, 136))]
    inputs.append({'start': 10801, 'duration': 8, 'buttons': ['B']})
    save(ROOT / 'inputs.json', inputs)
    pre = copy.deepcopy(original)
    pre['inputs_sha256'] = sha((ROOT / 'inputs.json').read_bytes())
    pre['selection_source'] = {'sorted_actor_ids': [12, 10, 3, 11, 21],
        'source_snapshot': str(runner.CAP / 'room_gender_v694_maria/frame_008800_arm9_ram.bin'),
        'source_snapshot_sha256': sha((runner.CAP / 'room_gender_v694_maria/frame_008800_arm9_ram.bin').read_bytes()),
        'original_button_rectangles_start': 0x0218AA8C, 'stride': 0x58,
        'Maria_sorted_index': 2, 'screen_touch_center': [136, 68],
        'launcher_sha256': sha(Path(__file__).read_bytes())}
    save(ROOT / 'preflight.json', pre)
    (ROOT / 'source_contract.json').write_bytes((runner.ROOT / 'source_contract.json').read_bytes())
    print('V694 explicit Maria/male return-cycle schedule pinned to actual original buttons.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('prepare', 'selected', 'selected_baseline'))
    args = parser.parse_args()
    if args.action == 'prepare':
        prepare()
    else:
        assert read(ROOT / 'preflight.json')['selection_source']['launcher_sha256'] == sha(Path(__file__).read_bytes())
        observer.ROOT = ROOT
        runner.ROOT = ROOT
        runner.run('maria_' + args.action, 'maria', args.action.endswith('baseline'))
