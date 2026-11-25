"""Full31-entry matrix and fonts at owned locations,with the exact scoped CPU model."""

from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE

from dk4tool.patch import tavern_editorial_runtime as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import BANKS as OLD_BANKS
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
import scripts.probe_tavern_conversations_v764 as driver
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_storage_v764/full_mapped')


def main():
    rom = NdsImage.open(driver.CURRENT); arm = rom.read_file('/__arm9__.bin')
    proof = read('work/analysis/tavern_storage_v764/owned_storage_and_native_research.json')
    equivalent = read('work/analysis/tavern_storage_v764/scoped_machine_equivalence.json')
    assert equivalent['total'] == 1408
    assert equivalent['adapter_sha256'] == sha(Path('scripts/native_machine_scoped_v764.py').read_bytes())
    assert proof['module_sha256'] == sha(Path(owned.__file__).read_bytes())
    assert proof['source_ARM9_sha256'] == sha(arm)
    ram = snapshot(read(driver.RAM_REPORT), 3200)
    writes = []
    def loaded(unused, changed=True):
        u = machine(arm); u.mem_write(0x02000000, ram)
        if changed:
            for patch in proof['patches']:
                before, after = bytes.fromhex(patch['source_hex']), bytes.fromhex(patch['target_hex'])
                assert bytes(u.mem_read(patch['address'], len(before))) == before
                u.mem_write(patch['address'], after)
        def watch(cpu, kind, at, length, value, unused):
            if any(at < hi and at + length > lo for lo, hi in (*OLD_BANKS, *owned.BANKS)):
                writes.append([at, length, value]); raise AssertionError('Native write into immutable source bank')
        for lo, hi in (*OLD_BANKS, *owned.BANKS):
            u.hook_add(UC_HOOK_MEM_WRITE, watch, begin=lo - 8, end=hi)
        return u
    driver.loaded = loaded
    driver.TYPE_HELPER = owned.TYPE_HELPER
    driver.code = owned.assemble
    driver.MANUSCRIPT = Path('translations/tavern_conversations_editorial_manuscript_v2.json')
    driver.ROOT = ROOT
    driver.main()
    assert not writes
    result = read(ROOT / 'verification.json')
    result.update({'mapped_owned_storage_runtime': True, 'native_bank_writes': writes,
        'owned_runtime_ARM9_sha256': proof['research_runtime_ARM9_sha256'],
        'owned_module_sha256': sha(Path(owned.__file__).read_bytes()),
        'scoped_machine_equivalence_report_sha256': sha(Path('work/analysis/tavern_storage_v764/scoped_machine_equivalence.json').read_bytes()),
        'adapter_producer_sha256': sha(Path(__file__).read_bytes())})
    save(ROOT / 'verification.json', result)
    print('Full mapped matrix complete;all immutable source-bank write watches clean. No ROM emitted.', flush=True)


if __name__ == '__main__': main()
