"""Inventory actual surname getters and the real company-leader rumor resolution."""

import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.probe_tavern_conversations_v764 import CURRENT, loaded
from scripts.verify_village_wrap_v608 import save


def main():
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    u = loaded(arm, False)
    call(u, 0xCB184, ()); root = u.reg_read(UC_ARM_REG_R0)
    rows = []
    for index in range(207):
        obj = root + 4 + index * 32
        vtable = struct.unpack('<I', u.mem_read(obj, 4))[0]
        getter = struct.unpack('<I', u.mem_read(vtable + 0x24, 4))[0]
        call(u, getter - 0x02000000, (obj,))
        result = u.reg_read(UC_ARM_REG_R0)
        if not any(lo <= result and result + 255 <= hi for lo, hi, _ in u.mem_regions()):
            rows.append({'index': index, 'object': obj, 'vtable': vtable, 'full_name_getter': getter,
                         'name_pointer': result, 'name_hex': '', 'name': '', 'bytes': 0,
                         'status': 'getter-result-not-resident-string', 'plain_ASCII': False})
            continue
        name = bytes(u.mem_read(result, 256)).split(b'\0')[0]
        try:
            text = name.decode('cp932')
            status = 'printable' if text and text.isprintable() else 'empty-or-control'
        except UnicodeError:
            text, status = '', 'invalid-cp932'
        rows.append({'index': index, 'object': obj, 'vtable': vtable, 'full_name_getter': getter, 'name_pointer': result,
                     'name_hex': name.hex(), 'name': text, 'bytes': len(name),
                     'status': status, 'plain_ASCII': bool(name) and all(32 <= value < 127 for value in name)})
    call(u, 0xCB160, ()); companies = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x7F244, ()); admiral = u.reg_read(UC_ARM_REG_R0)
    captain_offset = struct.unpack_from('<I', arm, 0x59CFC)[0]
    assert captain_offset == 0x19E4
    leaders = []
    for company in range(20):
        force = companies + 4 + company * 0x4C
        call(u, 0x3CD78, (force,)); index = u.reg_read(UC_ARM_REG_R0)
        if index >= 207:
            leaders.append({'company': company, 'leader_index': index, 'status': 'no-ordinary-leader-index'})
            continue
        obj = root + (captain_offset if index == admiral else 4 + index * 32)
        vtable = struct.unpack('<I', u.mem_read(obj, 4))[0]
        getter = struct.unpack('<I', u.mem_read(vtable + 0x24, 4))[0]
        call(u, getter - 0x02000000, (obj,))
        name = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 256)).split(b'\0')[0]
        assert name and all(32 <= value < 127 for value in name), (company, index, name)
        leaders.append({'company': company, 'leader_index': index, 'actual_admiral_special_object': index == admiral,
                        'object': obj, 'native_name_getter': getter, 'name': name.decode('ascii'), 'name_hex': name.hex(),
                        'status': 'actual-native-leader-name'})
    path = Path('work/analysis/tavern_storage_v764/actual_native_person_arguments.json')
    save(path, {'source_ROM_sha256': sha(CURRENT.read_bytes()), 'ARM9_sha256': sha(arm),
        'rows': rows, 'count': len(rows), 'maximum_bytes': max(r['bytes'] for r in rows),
        'non_ASCII_or_invalid_indices': [r['index'] for r in rows if not r['plain_ASCII']],
        'actual20_company_leader_resolutions': leaders,
        'range_reference': 'Original207-object loop0207F254..0207F28C; ordinary virtual+24 is table surname at+4, not a full name. Source59C10..59C38 resolves company leader and the current admiral special object.',
        'scope': 'All207 initialized ordinary objects plus current20 company leader resolutions. Ordinary generic placeholders/null slots are not claimed eligible rumor speakers. Future story leader replacements and edited names require separate coverage.',
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print('Actual ordinary names', len(rows), 'maximum bytes', max(r['bytes'] for r in rows), flush=True)
    print(sorted(((r['name'], r['bytes']) for r in rows), key=lambda x: -x[1])[:8], flush=True)
    print('Not plain ASCII', [(r['index'], r['name'], r['name_hex'], r['status']) for r in rows if not r['plain_ASCII']], flush=True)
    print('Actual leader arguments', [(r['company'], r.get('name'), r['status']) for r in leaders], flush=True)


if __name__ == '__main__': main()
