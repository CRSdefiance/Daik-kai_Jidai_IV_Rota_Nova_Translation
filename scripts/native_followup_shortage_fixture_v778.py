"""Two-byte Amsterdam shortage display fixture on exact V776/V778 images."""

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read

BASE = 0x02000000


def set_condition(arm, raw, request):
    target = read('work/analysis/scheme_followup_integration_v778/prospective_common_repack.json')['target_ARM9_sha256']
    if sha(arm) not in ('f54d9d10c96edbebffbbab4d184550b2df1157827fe41ac9ffb1a60565c7f523', target) or len(raw) != 0x400000:
        raise ValueError('Exact V776/V778 RAM required')
    if request != {'town': 2, 'status': 5, 'days': 30}:
        raise ValueError('Only the declared Amsterdam status5 duration30 fixture is allowed')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for a, b in ((0xB2E04, 0xB2E14), (0x579C4, 0x57A3C)):
        assert arm[a:b] == clean[a:b]
    u = machine(arm)
    u.mem_write(BASE, raw)
    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)
    town, here = get(0xCB178)+4+2*108, get(0xB6618)
    assert get(0xB2B48, (here,)) == get(0xB2B48, (town,)) == 0
    assert get(0xB2E04, (town,)) == 12
    at = town+0x6A-BASE
    after = bytearray(raw)
    after[at:at+2] = bytes((5, 30))
    u.mem_write(BASE, bytes(after))
    assert get(0xB2E04, (town,)) == 5
    label = bytes(u.mem_read(get(0xB2D58, (town,)), 64)).split(b'\0')[0]
    changes = [{'address': BASE+i, 'before': raw[i], 'after': after[i]} for i in range(at, at+2) if raw[i] != after[i]]
    assert len(changes) == 2
    return bytes(after), {'synthetic_town_condition_display_fixture': True, 'town_ID': 2, 'town_object': town,
                          'status': 5, 'duration': 30, 'native_UI_label_hex': label.hex(), 'changes': changes,
                          'only_status_and_duration_bytes_changed': True, 'all_other4MiB_bytes_exact': True,
                          'ROM_or_donor_save_changed': False, 'natural_condition_event_verified': False,
                          'original_native_getters_verified': True, 'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after)}
