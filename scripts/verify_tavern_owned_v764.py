"""Exact retired-slot ownership and bounded native tests; no ROM emitted."""

import struct
from itertools import islice
from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch import tavern_editorial_runtime as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.shipyard_editorial import BANKS as PRIOR_BANKS
from dk4tool.rom.nds import NdsImage
from ndspy.code import MainCodeFile
import scripts.probe_tavern_conversations_v764 as probe
from scripts.native_call_abi_v764 import call
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_storage_v764')


def main():
    rom = NdsImage.open(probe.CURRENT); arm = rom.read_file('/__arm9__.bin')
    assert sha(arm) == owned.SOURCE
    inventory_path = ROOT / 'retired_source_inventory.json'
    inventory = read(inventory_path)
    assert inventory['source_ARM9_sha256'] == sha(arm)
    assert inventory['source_ROM_sha256'] == sha(probe.CURRENT.read_bytes())
    eligible = [r for r in inventory['source_allocations'] if not any(r[k] for k in ('aliases', 'branches', 'adr', 'crossing_strings'))]
    for lo, hi in owned.BANKS:
        assert all(any(r['lo'] <= at < r['hi'] for r in eligible) for at in range(lo, hi))
        assert all(not (lo < b and a < hi) for a, b in PRIOR_BANKS)
    for row in eligible:
        assert arm[row['lo'] - owned.BASE:row['hi'] - owned.BASE].hex() == row['source_hex']
    blobs = owned.assemble(); patched = bytearray(arm); patches = []
    for at, blob in blobs.items():
        assert (any(a <= at < at + len(blob) <= b for a, b in owned.BANKS)
                or at in (0x02147E54, 0x02059CC8, 0x02058F08, 0x02058F0C, 0x02058F10))
        before = arm[at - owned.BASE:at - owned.BASE + len(blob)]
        patched[at - owned.BASE:at - owned.BASE + len(blob)] = blob
        patches.append({'address': at, 'source_hex': before.hex(), 'target_hex': blob.hex()})
    patched = bytes(patched)
    assert len(patched) == len(arm) and cache_plan(patched) == cache_plan(arm)
    original_sections, sections = [MainCodeFile(a, owned.BASE).sections for a in (arm, patched)]
    assert [len(s.data) for s in sections] == [len(s.data) for s in original_sections]
    assert all(bytes(a.data) == bytes(b.data) for a, b in zip(original_sections[1:], sections[1:], strict=True))
    # Preserve the actual shared UI cardinal arrays and the native coordinate formatter.
    for lo, hi in ((0x118B40, 0x118B64), (0x51580, 0x51670)):
        assert patched[lo:hi] == arm[lo:hi]
    initial_load = probe.loaded
    writes, machine_count = [], 0
    def loaded(unused, changed=True):
        nonlocal machine_count
        u = initial_load(arm, False)
        if changed:
            for p in patches:
                before, after = bytes.fromhex(p['source_hex']), bytes.fromhex(p['target_hex'])
                assert bytes(u.mem_read(p['address'], len(before))) == before
                u.mem_write(p['address'], after)
        def watch(cpu, kind, at, length, value, unused):
            if any(at < hi and at + length > lo for lo, hi in (*PRIOR_BANKS, *owned.BANKS)):
                writes.append([at, length, value]); raise AssertionError('Write into immutable reviewed bank')
        u.hook_add(UC_HOOK_MEM_WRITE, watch); machine_count += 1
        return u
    probe.loaded = loaded
    scopes = probe.dispatch(arm)
    print('Owned-location caller/table memberships pass.', flush=True)
    doc = read(probe.MANUSCRIPT)
    context = read('work/analysis/tavern_conversations_v763/native_context.json')
    samples = []
    for row in doc['records']:
        values = list(probe.variants(row['message_id'], context))
        # Exact full cross-products are tested separately; exercise each paragraph
        # with its first and final provider values at the mapped storage locations.
        for args in (values[:1] + values[-1:] if len(values) > 1 else values):
            result = probe.format_case(loaded(arm), row, args)
            assert not result['findings'], result
            samples.append(result)
    old, new = loaded(arm, False), loaded(arm)
    professions = []
    for value in range(256):
        actual = []
        for u, fn in ((old, 0x3CF70), (new, owned.TYPE_HELPER - owned.BASE)):
            u.mem_write(0x02478000, bytes(9) + bytes((value,)) + bytes(6))
            call(u, fn, (0x02478000,))
            actual.append(bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 64)).split(b'\0')[0])
        assert actual[1] == (owned.PROFESSIONS[value] if value < 4 else actual[0])
        professions.append({'enum': value, 'source_hex': actual[0].hex(), 'new_hex': actual[1].hex()})
    assert not writes
    save(ROOT / 'owned_storage_and_native_research.json', {
        'source_ROM_sha256': sha(probe.CURRENT.read_bytes()), 'source_ARM9_sha256': sha(arm),
        'research_runtime_ARM9_sha256': sha(patched), 'patches': patches,
        'immutable_banks': owned.BANKS, 'complete_retired_source_inventory_sha256': sha(inventory_path.read_bytes()),
        'all57_active_replacements_exact': inventory['all57_active_replacements_exact'],
        'dispatcher': scopes, 'complete_layout_samples': samples, 'all256_profession_enum_outputs': professions,
        'native_writes_into_all_prior_and_new_banks': writes, 'initialized_machines': machine_count,
        'no_section_or_staged_payload_growth_and_cache_plan_unchanged': True,
        'shared_cardinal_tables_and_original_coordinate_provider_unchanged': True,
        'module_sha256': sha(Path(owned.__file__).read_bytes()), 'producer_sha256': sha(Path(__file__).read_bytes()),
        'research_only_all_layouts_fonts_prior_outputs_actual_gameplay_and_registered_release_still_required': True})
    print(f'{len(samples)} whole paragraphs and256 enum values pass; no native bank writes. No playable ROM emitted.', flush=True)


if __name__ == '__main__': main()
