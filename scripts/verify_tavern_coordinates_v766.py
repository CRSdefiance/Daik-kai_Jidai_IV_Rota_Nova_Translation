"""Owned842-only coordinate compaction,complete dispatch and31-paragraph matrix."""

import inspect
import re
import struct
from itertools import product
from pathlib import Path

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.patch import tavern_coordinate_runtime as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.shipyard_editorial import BANKS as OLD_BANKS, DIRECT, LITERAL, YESNO
from dk4tool.rom.nds import NdsImage
from scripts.native_machine_scoped_v764 import machine
import scripts.probe_tavern_conversations_v764 as driver
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_coordinates_v766')
MANUSCRIPT = Path('translations/tavern_conversations_editorial_manuscript_v3.json')


def dispatch(arm):
    u = driver.loaded(arm); count = 0
    h = u.hook_add(UC_HOOK_CODE, lambda cpu, pc, size, unused: cpu.emu_stop() if pc in (LITERAL, owned.COORD, 0x01FFCF40) else None)
    try:
        for parent, table, n in product((0x02054014, 0x02053FCC, 0x02054044, 0x02053D24, 0x02053DB8), (0x02118460, 0x021184C0), range(3668)):
            u.mem_write(driver.STACK + 0x264, struct.pack('<I', parent)); u.mem_write(driver.STACK + 0x274, struct.pack('<I', n))
            u.mem_write(driver.STACK + 0x270, bytes(4)); u.mem_write(driver.STACK + 0x27C, struct.pack('<I', table))
            u.reg_write(UC_ARM_REG_SP, driver.STACK)
            u.emu_start(0x01FFCF3C, 0x027E0000, count=200)
            selected = (parent == 0x02054014 and n in (*DIRECT, 808, 1245, *range(820, 851))
                or parent == 0x02053FCC and n in (*YESNO, 1246, 839)
                or parent in (0x02053D24, 0x02053DB8) and table == 0x02118460)
            expected = owned.COORD if parent == 0x02054014 and n == 842 else LITERAL if selected else 0x01FFCF40
            assert u.reg_read(UC_ARM_REG_PC) == expected and u.reg_read(UC_ARM_REG_SP) == driver.STACK, (parent, table, n)
            count += 1
        for parent, table, unrelated in product((0x02053C14, 0x02053C5C), (0x021166E0, 0x02116610, 825, 0x02118460, 0), (0, 825, 850, 3667, 0x02412345)):
            u.mem_write(driver.STACK + 0x264, struct.pack('<I', parent)); u.mem_write(driver.STACK + 0x270, struct.pack('<I', table))
            u.mem_write(driver.STACK + 0x274, struct.pack('<I', unrelated)); u.reg_write(UC_ARM_REG_SP, driver.STACK)
            u.emu_start(0x01FFCF3C, 0x027E0000, count=200)
            selected = parent == 0x02053C14 and table in (0x021166E0, 0x02116610) or parent == 0x02053C5C and table == 825
            assert u.reg_read(UC_ARM_REG_PC) == (LITERAL if selected else 0x01FFCF40)
            assert u.reg_read(UC_ARM_REG_SP) == driver.STACK
    finally: u.hook_del(h)
    return {'all36680_original_scopes': count, 'all50_gift_player_contracts': True,
            'coordinate_compaction_only_direct842': True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    arm = NdsImage.open(driver.CURRENT).read_file('/__arm9__.bin')
    assert sha(arm) == owned.SOURCE
    inventory = read('work/analysis/tavern_storage_v764/retired_source_inventory.json')
    assert inventory['source_ARM9_sha256'] == sha(arm)
    eligible = [r for r in inventory['source_allocations'] if not any(r[k] for k in ('aliases', 'branches', 'adr', 'crossing_strings'))]
    for lo, hi in owned.BANKS:
        assert all(any(r['lo'] <= at < r['hi'] for r in eligible) for at in range(lo, hi))
        assert all(not (lo < b and a < hi) for a, b in OLD_BANKS)
    for row in eligible: assert arm[row['lo'] - owned.BASE:row['hi'] - owned.BASE].hex() == row['source_hex']
    blobs = owned.assemble(); patches = []; target = bytearray(arm)
    for at, blob in blobs.items():
        before = arm[at - owned.BASE:at - owned.BASE + len(blob)]
        target[at - owned.BASE:at - owned.BASE + len(blob)] = blob
        patches.append({'address': at, 'source_hex': before.hex(), 'target_hex': blob.hex()})
    assert len(target) == len(arm) and cache_plan(bytes(target)) == cache_plan(arm)
    ram = snapshot(read(driver.RAM_REPORT), 3200); writes = []
    def loaded(unused, changed=True):
        u = machine(arm); u.mem_write(owned.BASE, ram)
        if changed:
            for patch in patches:
                before, after = bytes.fromhex(patch['source_hex']), bytes.fromhex(patch['target_hex'])
                assert bytes(u.mem_read(patch['address'], len(before))) == before
                u.mem_write(patch['address'], after)
        def watch(cpu, kind, at, size, value, unused):
            if any(at < hi and at + size > lo for lo, hi in (*OLD_BANKS, *owned.BANKS)):
                writes.append([at, size, value]); raise AssertionError('Native bank write')
        for lo, hi in (*OLD_BANKS, *owned.BANKS): u.hook_add(UC_HOOK_MEM_WRITE, watch, begin=lo - 8, end=hi)
        return u
    # Retain the exact original printf byte check. Only the post-format expected
    # representation of842 changes,removing spaces inside compass/number pairs.
    source = inspect.getsource(driver.format_case)
    marker = "    assert b' '.join(result.split()) == b' '.join(expected.split()), (n, values, result, expected)"
    assert source.count(marker) == 1
    replacement = "    if n == 842: expected = re.sub(rb'([NSEW]) +([0-9])', rb'\\1\\2', expected)\n" + marker
    context = dict(driver.__dict__); context['re'] = re
    exec(compile(source.replace(marker, replacement), str(Path(__file__)), 'exec'), context)
    formatter = context['format_case']
    def checked(u, row, values):
        result = formatter(u, row, values)
        if row['message_id'] == 842:
            normalized = ' '.join(values[0].decode('ascii').split())
            pairs = [letter + number for letter, number in re.findall(r'\b([NSEW]) (\d+)\b', normalized)]
            if not all(any(pair in line for line in result['lines']) for pair in pairs): result['findings'].append('coordinate_pair_split')
        return result
    driver.loaded = loaded; driver.TYPE_HELPER = owned.TYPE_HELPER; driver.code = owned.assemble
    driver.MANUSCRIPT = MANUSCRIPT; driver.ROOT = ROOT; driver.dispatch = dispatch; driver.format_case = checked
    save(ROOT / 'owned_runtime_plan.json', {'source_ARM9_sha256': sha(arm), 'target_ARM9_sha256': sha(bytes(target)),
        'patches': patches, 'immutable_banks': owned.BANKS, 'module_sha256': sha(Path(owned.__file__).read_bytes()),
        'earlier_runtime_module_sha256': sha(Path('dk4tool/patch/tavern_editorial_runtime.py').read_bytes()),
        'all57_prior_replacement_texts_verified_by_inventory': inventory['all57_active_replacements_exact'],
        'complete_source_inventory_sha256': sha(Path('work/analysis/tavern_storage_v764/retired_source_inventory.json').read_bytes()),
        'only_direct842_post_printf_field_representation_changes': True,
        'global_coordinate_formatter_source_bytes_unchanged': bytes(target)[0x51580:0x51670] == arm[0x51580:0x51670],
        'producer_sha256': sha(Path(__file__).read_bytes())})
    driver.main()
    assert not writes
    cases = read(ROOT / 'native_layout_matrix.json')['cases']
    old = read('work/analysis/tavern_storage_v764/full_mapped/native_layout_matrix.json')['cases']
    assert len(cases) == len(old) == 38957
    assert all(a == b for a, b in zip(old, cases, strict=True) if a['id'] != 842)
    result = read(ROOT / 'verification.json')
    result.update({'all94_coordinate_pairs_intact': True, 'all38863_other_outputs_byte_exact_to_V764': True,
        'typed_coordinate_compaction_after_original_printf_only': True, 'native_bank_writes': writes,
        'owned_runtime_plan_sha256': sha((ROOT / 'owned_runtime_plan.json').read_bytes()),
        'adapter_producer_sha256': sha(Path(__file__).read_bytes())})
    save(ROOT / 'verification.json', result)
    print('38957 full mapped cases pass;94 typed coordinates intact;38863 other outputs unchanged.', flush=True)


if __name__ == '__main__': main()
