"""Source-bound Cappadocia map fixture through the original inventory transfer."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000
ITEM_ID = 164
NAME_DESCRIPTOR = 0x11F170


def set_condition(arm, raw, request):
    cfg = read('translations/ceremony_editorial_release_v1.json')
    assert sha(arm) in (cfg['source_arm9_sha256'], cfg['target_arm9_sha256'])
    assert len(raw) == 0x400000 and request == {'mode': 'ceremony-Cappadocia-map'}
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = ((0x49DE8, 0x4A624), (0xCB190, 0xCB19C), (0xCDAFC, 0xCDB90))
    assert all(clean[a:b] == arm[a:b] for a, b in spans)
    ptr = struct.unpack_from('<I', clean, NAME_DESCRIPTOR)[0]
    jp = clean[ptr-BASE:].split(b'\0')[0].decode('cp932')
    assert jp == '岩窟集落への地図'
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args, instruction_limit=500000)
        return u.reg_read(UC_ARM_REG_R0)

    assert get(0xB65E4) == 22
    item = get(0xCB190) + 4 + ITEM_ID * 20
    assert get(0x4A448, (item,)) == 10
    name_ptr = get(0x4A53C, (item,))
    name = bytes(u.mem_read(name_ptr, 128)).split(b'\0')[0].decode('ascii')
    assert name == 'Cave Village Map'
    descriptor = 0x02470020
    get(0x49DE8, (descriptor, item))
    before_owner = bytes(u.mem_read(descriptor, 12))
    prior_kind = struct.unpack_from('<I', before_owner, 4)[0]
    assert prior_kind not in (2, 3), 'Do not remove an equipped owner'
    get(0x4A610, (descriptor, 0))
    assert get(0x49F30, (item, descriptor, 6, 0)) == 1
    get(0x49DE8, (descriptor, item))
    after_owner = bytes(u.mem_read(descriptor, 12))
    assert struct.unpack_from('<I', after_owner, 4)[0] == 0
    result = bytes(u.mem_read(BASE, len(raw)))
    history = struct.unpack_from('<I', arm, 0x4A0EC)[0]
    permitted = set(range(item, item+20)) | set(range(history, history+28))
    changes = [dict(address=BASE+i, before=a, after=b)
               for i, (a, b) in enumerate(zip(raw, result, strict=True)) if a != b]
    assert all(row['address'] in permitted for row in changes)
    return result, dict(synthetic_ceremony_map_fixture=True, item_ID=ITEM_ID,
        clean_Japanese=jp, current_English=name, category=10, native_transfer=BASE+0x49F30,
        prior_owner_descriptor_hex=before_owner.hex(), result_owner_descriptor_hex=after_owner.hex(),
        owned_item_span=[item, item+20], acquisition_history_span=[history, history+28],
        original_code_spans_exact=spans, changes=changes,
        before_RAM_sha256=sha(raw), after_RAM_sha256=sha(result), ARM9_sha256=sha(arm),
        normal_map_acquisition_not_claimed=True,
        quests_calendar_facility_flags_location_dialogue_and_every_other_RAM_byte_exact=True)
