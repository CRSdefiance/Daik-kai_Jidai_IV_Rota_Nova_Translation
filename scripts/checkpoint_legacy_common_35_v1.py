"""Bind the last 35 shared legacy keys and reject a misleading Market ID lead."""

from collections import Counter
from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.script.common_message_table import common_message_entries
from scripts import register_ancient_map_hint_label_v1 as parent
from scripts import review_sound_bgm_titles_v1 as common
from scripts.probe_button_prompt_native import BASE, call, machine


base, ARM, COMMON = parent.base, parent.ARM, parent.COMMON
OUTPUT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/legacy_common_35_checkpoint_v1.json')
GROUPS = {
    'setup_and_storage': [*range(98, 112), *range(113, 118), 119, 124],
    'fleet_and_discovery': [284, 287, 296, 300, 304],
    'exhibition_and_options': [318, 330, 331, 332, 333, 336],
    'market_restart_and_rebuff': [750, 751, 752],
}
ROOT = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
EARLIER = ('setup_save_equipment_context_v1.json', 'setup_save_live_consumer_verification_v1.json',
           'shipyard_fleet_setup_context_v1.json', 'discovery_rewards_context_v1.json')


def actor_data(arm):
    table = unpack_from('<I', arm, 0xCDAC0)[0]
    assert table == 0x02120B80
    cpu = machine(arm)
    call(cpu, 0xCDAB4, (25,))
    row = cpu.reg_read(UC_ARM_REG_R0)
    assert row == table + 25 * 32 and row + 12 == 0x02120EAC
    data = bytes(cpu.mem_read(row, 32))
    assert data == arm[row-BASE:row-BASE+32] and unpack_from('<I', data, 12)[0] == 750
    return row, data


def main():
    assert not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(parent.CLEAN) == release['clean_input_sha256']
    clean, target = (base.NdsImage.open(path) for path in (parent.CLEAN, parent.ROM))
    source_arm, arm = (image.read_file(ARM) for image in (clean, target))
    source = common_message_entries(clean.read_file(COMMON), source_arm)
    current = common.owned_entries(target.read_file(COMMON), arm,
        sha256(arm[common.DIRECTORY_OFFSET:common.TABLE_OFFSET]).hexdigest())
    assert source_arm[0xCDAB4:0xCDAC4] == arm[0xCDAB4:0xCDAC4]
    address, original = actor_data(source_arm)
    _, data = actor_data(arm)
    assert data[12:] == original[12:]
    call_inventory = Path('work/analysis/native_common_extended_calls_clean.json')
    calls = base.load(call_inventory)
    assert calls['source_rom_sha256'] == release['clean_input_sha256']
    ledger = base.load(base.LEDGER)
    keys = {row['id'] for row in ledger[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    rows = []
    for group, ids in GROUPS.items():
        for n in ids:
            s, c = source[n], current[n]
            rid = f'COMMON_MESSAGE_{n}'
            assert rid not in keys and s.message_id == c.message_id == n
            direct = [row['runtime_address'] for row in calls['candidates'] if row['native_id_constant'] == n]
            assert not direct
            rows.append(dict(id=rid, message_ID=n, family=group, clean_reference=common.reference(s),
                current_reference=common.reference(c), Japanese=s.text.decode('cp932'),
                current_text=c.text.decode('cp932'), clean_hex=s.text.hex(), current_hex=c.text.hex(),
                original_native_call_binding='pending', direct_constant_hits=direct))
    assert Counter(row['family'] for row in rows) == {group: len(ids) for group, ids in GROUPS.items()}
    assert len(rows) == 35
    sources = [*(ROOT / name for name in EARLIER), call_inventory, Path(__file__)]
    base.save(OUTPUT, dict(current_ROM_sha256=release['candidate_sha256'], clean_ROM_sha256=release['clean_input_sha256'],
        records=rows, actor_table_rejection=dict(value=750, field=address + 12, record_address=address, record_index=25,
            original_native_resolver=0x020CDAB4, clean_record_hex=original.hex(), current_record_hex=data.hex(),
            classification='numeric field in an actor record; this address does not establish a COMMON call'),
        scope='These 35 records are outside the 245 Online and scene-label keys. The named call inventory is bounded.',
        new_editorial_credit=0, evidence={str(path): base.digest(path) for path in sources}))
    print('Bound 35 pending clean/current legacy keys; the aligned 750 hit resolves to actor-table data.')


if __name__ == '__main__':
    main()
