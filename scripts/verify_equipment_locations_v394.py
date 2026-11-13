"""Original location/name/category getters on genuine saved item data; no acquisition claim."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROM = Path('out/all_routes_combined_v388_candidate.nds')
REPORT = Path('work/emulation_v193/town_transition_v393_v388/capture_report.json')
ROOT = Path('work/analysis/equipment_locations_v394')
OUT = 0x02470020


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    report = json.loads(REPORT.read_text(encoding='utf-8'))
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    digest = sha(ROM.read_bytes())
    assert digest == report['ROM_sha256']
    assert digest == json.loads(ROM.with_suffix('.manifest.json').read_text(encoding='utf-8'))['candidate_sha256']
    snapshot = report['read_only_RAM_snapshot']
    ram = Path(snapshot['path']).read_bytes()
    assert sha(ram) == snapshot['sha256'] and snapshot['read_only_export']
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    original = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in [(0x49DE8, 0x49F30), (0x4A368, 0x4A42C), (0x4A448, 0x4A468),
                   (0x4A53C, 0x4A588), (0x4A5BC, 0x4A624), (0xCD6B8, 0xCD6CC)]:
        assert arm[lo:hi] == original[lo:hi]
    u = machine(arm)
    u.mem_write(0x02000000, ram)

    def getter(offset, args=()):
        call(u, offset, args)
        return u.reg_read(UC_ARM_REG_R0)

    def string(pointer):
        return bytes(u.mem_read(pointer, 128)).split(b'\0', 1)[0].decode('cp932')

    store = getter(0xCB190)
    rows = []
    for index in range(218):
        actor = store + 4 + index * 20
        category = getter(0x4A448, (actor,))
        if category not in (2, 3):
            continue
        name = string(getter(0x4A53C, (actor,)))
        before = bytes(u.mem_read(actor, 20))
        u.mem_write(OUT - 16, b'\xA5' * 48)
        getter(0x49DE8, (OUT, actor))
        descriptor = bytes(u.mem_read(OUT, 16))
        kind = struct.unpack_from('<I', descriptor, 4)[0]
        row = {'item_id': index, 'name': name, 'category': category,
               'location_descriptor_type': kind, 'descriptor_hex': descriptor.hex(),
               'descriptor_type6_extra_fields_not_assumed_valid': True,
               'price': getter(0x4A410, (actor,)),
               'item_address': actor, 'item_record_hex': before.hex()}
        if kind == 4:
            city = struct.unpack_from('<I', descriptor, 8)[0]
            city_meta = getter(0xCD6B8, (city,))
            city_name = string(struct.unpack('<I', u.mem_read(city_meta, 4))[0])
            row.update(city_index=city, city_name=city_name,
                       original_city_metadata_address=city_meta)
        assert bytes(u.mem_read(actor, 20)) == before
        assert bytes(u.mem_read(OUT - 16, 16)) == b'\xA5' * 16
        assert bytes(u.mem_read(OUT + 16, 16)) == b'\xA5' * 16
        rows.append(row)
    cutlass = next(r for r in rows if r['item_id'] == 29)
    assert cutlass['category'] == 2 and cutlass['name'] == 'Golden Cutlass'
    assert cutlass['location_descriptor_type'] == 4 and cutlass['city_index'] == 22
    assert cutlass['city_name'] == 'Istanbul' and cutlass['price'] == 30000
    assert bytes(u.mem_read(0x02000000, len(ram))) == ram
    proof = {'candidate': str(ROM), 'candidate_sha256': digest,
             'capture_report': str(REPORT), 'capture_report_sha256': sha(REPORT.read_bytes()),
             'snapshot_sha256': sha(ram), 'item_store': store, 'weapons_and_armor': rows,
             'all218_original_category_queries_executed': True,
             'original_location_and_name_price_city_getters_and_ABI_pass': True,
             'all_captured_RAM_and_item_records_unchanged': True,
             'Golden_Cutlass_native_location_Istanbul_price30000': True,
             'city22_from_original_CD6B8_not_unrelated_crew_name_table': True,
             'descriptor_type4_original_item_detail_displays_Price': True,
             'Guild_arrival_stock_purchase_equipping_and_GPU_not_proven': True,
             'buried_type6_stale_extra_fields_not_used_as_city_ids': True,
             'isolated_native_snapshot_not_live_state_injection': True,
             'all18_plaques_incomplete': True, 'ROM_changed': False, 'full_goal_complete': False}
    (ROOT / 'proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'{len(rows)} genuine weapon/armor records: original getter/descriptor/ABI and RAM preservation pass. '
          'Golden Cutlass: weapon, Istanbul22, price30000; gameplay acquisition remains open.')


if __name__ == '__main__':
    main()
