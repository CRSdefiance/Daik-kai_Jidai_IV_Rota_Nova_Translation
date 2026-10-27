"""Replay frozen earlier/native-leader checks with the coordinate-safe runtime."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_tavern_conversations_v764 import CURRENT, RAM_REPORT
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_coordinates_v766')
SOURCE = Path('scripts/verify_tavern_inherited_v764.py')


def main():
    old = read('work/analysis/tavern_storage_v764/inherited_outputs.json')
    assert sha(SOURCE.read_bytes()) == old['producer_sha256']
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    text = SOURCE.read_text(encoding='utf-8')
    replacements = {
        'from dk4tool.patch import tavern_editorial_runtime as owned': 'from dk4tool.patch import tavern_coordinate_runtime as owned',
        "ROOT = Path('work/analysis/tavern_storage_v764')": "ROOT = Path('work/analysis/tavern_coordinates_v766')",
        "ROOT / 'owned_storage_and_native_research.json'": "ROOT / 'owned_runtime_plan.json'",
        'u = tavern.loaded(arm, False)': 'u = scoped_machine(arm); u.mem_write(BASE, initialized_ram)',
        'u.hook_add(UC_HOOK_MEM_WRITE, watch)': 'for lo, hi in (*OLD_BANKS, *owned.BANKS):\n            u.hook_add(UC_HOOK_MEM_WRITE, watch, begin=lo - 8, end=hi)',
        "ROOT / 'actual_native_person_arguments.json'": "Path('work/analysis/tavern_storage_v764/actual_native_person_arguments.json')"}
    for before, after in replacements.items():
        assert text.count(before) in (1, 2), (before, text.count(before))
        text = text.replace(before, after)
    exec(compile(text, str(SOURCE), 'exec'), {'__name__': '__main__', '__file__': str(SOURCE.resolve()),
        'scoped_machine': machine, 'initialized_ram': snapshot(read(RAM_REPORT), 3200)})
    previous = read('work/analysis/tavern_storage_v764/actual_leader_layout_matrix.json')
    now = read(ROOT / 'actual_leader_layout_matrix.json')
    assert now['count'] == previous['count'] == 14400 and not now['findings'] and not now['native_bank_writes']
    assert now['cases'] == previous['cases']
    for name in ('inherited_outputs.json', 'actual_leader_layout_matrix.json'):
        result = read(ROOT / name)
        result['coordinate_runtime_adapter'] = {'original_source_sha256': sha(SOURCE.read_bytes()),
            'effective_program_sha256': sha(text.encode('utf-8')), 'adapter_sha256': sha(Path(__file__).read_bytes()),
            'runtime_plan_sha256': sha((ROOT / 'owned_runtime_plan.json').read_bytes()),
            'original_frozen_file_unchanged': True}
        save(ROOT / name, result)
    print('Coordinate runtime preserves1124 Yard/40 Port/180 controls and all14400 leader-name layouts.', flush=True)


if __name__ == '__main__': main()
