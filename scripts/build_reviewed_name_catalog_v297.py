"""Build the full reviewed route catalog in owned memory; research ARM9 only."""

import json
import struct
from collections import defaultdict

from ndspy.code import MainCodeFile

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.confirmed_name_message_catalog import CALLS, MACRO
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.patch.reviewed_name_catalog import helper, pack_complete_strings, table_bytes
from dk4tool.rom.nds import NdsImage
from scripts.prepare_reviewed_names_v297 import DIGEST, ROM, ROOT
from scripts.probe_common_display_name_hook import branch_link
from scripts.revalidate_name_migration_v276 import name_fields
from scripts.verify_ordinary_name_fidelity_research import initialized


def main():
    prep = json.loads((ROOT / 'preparation.json').read_text(encoding='utf-8'))
    assert len(prep['records']) == 444 and not prep['errors']
    assert sha(ROM.read_bytes()) == DIGEST
    image = NdsImage.open(ROM)
    arm = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    named, names = name_fields(arm, clean)
    requests = defaultdict(list)
    selected = {}
    for row in prep['records']:
        if row['storage'] != 'catalog':
            continue
        owner = row['file_path'], row['id']
        key, target = bytes.fromhex(row['current_key_hex']), bytes.fromhex(row['target_hex'])
        selected[owner] = row
        requests[key].append((owner, 'whole', target))
        if row['native_actor'] is not None:
            assert key[0] == target[0] == row['native_actor']
            requests[key[1:]].append((owner, 'body', target[1:]))
    rows = []
    for key in sorted(requests):
        items = requests[key]
        assert len({item[2] for item in items}) == 1
        mask = 0
        for owner, _, _ in items:
            mask |= 1 << int(owner[0][8])
        rows.append({'key': key, 'target': items[0][2], 'route_mask': mask,
                     'requests': [{'owner': list(o), 'form': f} for o, f, _ in items]})
    lookup = {row['key']: row for row in rows}
    covered, unintended, rejected, scanned = set(), [], [], 0
    for route in range(4):
        path = f'/data/SC{route}.DK4'
        for block, data in enumerate(IlnkContainer.parse(image.read_file(path)).blocks):
            for index, raw in enumerate(data.split(b'\0')):
                scanned += 1
                owner = path, f'DK4_MES_B{block:02d}_R{index:04d}'
                for form, key in [('whole', raw), ('body', raw[1:])] if raw else []:
                    row = lookup.get(key)
                    if row is None:
                        continue
                    if not row['route_mask'] & (1 << route):
                        rejected.append({'owner': list(owner), 'form': form, 'reason': 'foreign native route'})
                        continue
                    if owner not in selected:
                        unintended.append({'owner': list(owner), 'form': form})
                        continue
                    expected = bytes.fromhex(selected[owner]['target_hex'])
                    if form == 'body':
                        expected = expected[1:]
                    assert row['target'] == expected
                    covered.add(owner)
    assert not unintended and covered == set(selected)
    code = MainCodeFile(named, BASE)
    before = [bytes(section.data) for section in code.sections]
    assert code.sections[3].ramAddress == STAGE and cache_plan(named)
    packed, pointers = pack_complete_strings(
        [raw for row in rows for raw in (row['key'], row['target'])], POOL, before[3][:-48])
    packed.extend(bytes(-len(packed) % 4))
    table = POOL + len(packed)
    packed.extend(table_bytes(rows, pointers))
    entry = POOL + len(packed)
    implementation = helper(entry, table, len(rows))
    packed.extend(implementation)
    for field in CALLS:
        assert struct.unpack_from('<I', arm, field)[0] == branch_link(BASE + field, MACRO)
        struct.pack_into('<I', code.sections[0].data, field, branch_link(BASE + field, entry))
    packed.extend(bytes(-len(packed) % 32))
    size = len(packed) + 64
    assert POOL + size <= STAGE and STAGE + size + 48 <= 0x023F4000
    packed.extend(wrapper(STAGE + len(packed), STAGE + size, size, named))
    code.sections[3].data = packed + before[3][-48:-4] + struct.pack('<I', size)
    struct.pack_into('<I', code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, STAGE + size - 64))
    struct.pack_into('<I', code.sections[0].data, 0xE45DC, POOL + size)
    saved = bytes(code.save())
    parsed = MainCodeFile(saved, BASE)
    restored = bytearray(parsed.sections[0].data)
    for at in (*CALLS, 0x8E4, 0xE45DC):
        restored[at:at + 4] = before[0][at:at + 4]
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    assert restored == before[0] and all(bytes(parsed.sections[n].data) == before[n] for n in (1, 2))
    assert bytes(parsed.sections[3].data[:len(before[3]) - 48]) == before[3][:-48]
    initialized(saved)
    (ROOT / 'catalog_arm9_research_only.bin').write_bytes(saved)
    plan = {'format': 'dk4-full-reviewed-name-catalog-v297', 'parent_ROM_sha256': DIGEST,
            'source_arm9_sha256': sha(arm), 'target_arm9_sha256': sha(saved), 'name_fields': names,
            'records': [{'key_hex': row['key'].hex(), 'target_hex': row['target'].hex(),
                         'key_pointer': pointers[row['key']], 'target_pointer': pointers[row['target']],
                         'route_mask': row['route_mask'], 'requests': row['requests']} for row in rows],
            'catalog_source_records': len(selected), 'unique_route_scoped_keys': len(rows),
            'route_segments_scanned': scanned, 'unintended_matches': unintended,
            'foreign_route_matches_rejected': rejected, 'entry': entry, 'table': table,
            'helper_bytes': len(implementation), 'pool_payload_bytes': size,
            'remaining_before_stage': STAGE - POOL - size,
            'inherited_pool_bytes_preserved': len(before[3]) - 48, 'cache': cache_plan(saved),
            'all_full_suffix_strings_first_final_letters_and_NUL_exact': True,
            'native_startup_pool_copy_cache_preservation_pass': True,
            'native_route_lookup_copy_and_complete_glyph_tests_pending': True,
            'full_registered_COMMON_HELP_art_integration_pending': True,
            'playable_ROM_modified': False, 'full_goal_complete': False}
    (ROOT / 'catalog_plan.json').write_text(json.dumps(plan, indent=2) + '\n', encoding='utf-8')
    print(f'{len(selected)} full records; {len(rows)} keys; {size} owned bytes; {STAGE - POOL - size} spare; foreign matches rejected.')


if __name__ == '__main__':
    main()
