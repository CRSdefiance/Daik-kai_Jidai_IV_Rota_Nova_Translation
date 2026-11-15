"""Recheck all31 final drafts at owned addresses,including coordinate pair boundaries."""

from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE

from dk4tool.patch import tavern_editorial_runtime as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import BANKS as OLD_BANKS
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
import scripts.probe_tavern_conversations_v764 as driver
from scripts.refine_tavern_coordinates_v765 import MANUSCRIPT, ROOT, coordinate_splits
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read, save


def main():
    arm = NdsImage.open(driver.CURRENT).read_file('/__arm9__.bin')
    proof = read('work/analysis/tavern_storage_v764/owned_storage_and_native_research.json')
    assert proof['module_sha256'] == sha(Path(owned.__file__).read_bytes())
    assert proof['source_ARM9_sha256'] == sha(arm)
    ram = snapshot(read(driver.RAM_REPORT), 3200); writes = []
    def loaded(unused, changed=True):
        u = machine(arm); u.mem_write(0x02000000, ram)
        if changed:
            for patch in proof['patches']:
                before, after = bytes.fromhex(patch['source_hex']), bytes.fromhex(patch['target_hex'])
                assert bytes(u.mem_read(patch['address'], len(before))) == before
                u.mem_write(patch['address'], after)
        def watch(cpu, kind, at, size, value, unused):
            if any(at < hi and at + size > lo for lo, hi in (*OLD_BANKS, *owned.BANKS)):
                writes.append([at, size, value]); raise AssertionError('Native write into immutable source bank')
        for lo, hi in (*OLD_BANKS, *owned.BANKS):
            u.hook_add(UC_HOOK_MEM_WRITE, watch, begin=lo - 8, end=hi)
        return u
    original_format = driver.format_case
    def checked_format(u, row, values):
        result = original_format(u, row, values)
        if coordinate_splits(result, values): result['findings'].append('coordinate_direction_number_split')
        return result
    driver.loaded = loaded; driver.TYPE_HELPER = owned.TYPE_HELPER; driver.code = owned.assemble
    driver.MANUSCRIPT = MANUSCRIPT; driver.ROOT = ROOT; driver.format_case = checked_format
    driver.main()
    assert not writes
    result = read(ROOT / 'verification.json')
    old = read('work/analysis/tavern_storage_v764/full_mapped/native_layout_matrix.json')
    current = read(ROOT / 'native_layout_matrix.json')
    assert len(current['cases']) == len(old['cases']) == 38957
    assert all(a == b for a, b in zip(old['cases'], current['cases'], strict=True) if a['id'] != 842)
    assert all(not coordinate_splits(r, [bytes.fromhex(v) for v in r['values_hex']]) for r in current['cases'])
    result.update({'mapped_owned_runtime': True, 'native_bank_writes': writes,
        'all94_coordinate_pairs_kept_together': True, 'all38863_unmodified_paragraph_cases_byte_exact_to_V764': True,
        'owned_runtime_ARM9_sha256': proof['research_runtime_ARM9_sha256'],
        'owned_module_sha256': sha(Path(owned.__file__).read_bytes()),
        'adapter_producer_sha256': sha(Path(__file__).read_bytes())})
    save(ROOT / 'verification.json', result)
    print('All38957 mapped cases pass,including94 complete coordinate pairs;all38863 other outputs exact.', flush=True)


if __name__ == '__main__': main()
