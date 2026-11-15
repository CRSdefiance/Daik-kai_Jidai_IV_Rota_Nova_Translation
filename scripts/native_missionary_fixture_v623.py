"""Three-byte isolated Chapel/Manuel assignment for the Square display test."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine

ARMS = ('a49549b7300e6e101d52cdeabeab857ba32a20a49bbe7bad75f69d17a6f5be3b',
        '9a05ef9a25367d53dc7affa1c24e70b84fa9123388701adefcf94e0d21add280')


def assign(arm, raw, request):
    if sha(arm) not in ARMS or len(raw) != 0x400000 or request is not True:
        raise ValueError('Missionary fixture requires exact V621/V623,4MiB RAM and true')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0x7B60, 0x7C34), (0x132C0, 0x132CC), (0x825E4, 0x8261C),
                   (0x829C8, 0x82A44), (0x82BC4, 0x82BD0), (0x82E04, 0x82E2C),
                   (0xCB184, 0xCB190), (0xCB1A8, 0xCB1B4)):
        assert arm[lo:hi] == clean[lo:hi]
    u = machine(arm)
    u.mem_write(BASE, raw)

    def get(fn, args=()):
        call(u, fn, args)
        return u.reg_read(UC_ARM_REG_R0)

    root = get(0xCB1A8)
    assert get(0x2E58C) == 1
    controller = root + 0x2090
    assert get(0x825E4, (controller, 10)) == 208
    model = get(0x82E04, (controller,))
    assert bytes(u.mem_read(model + 8, 24)).split(b'\0')[0] == b'Vestaros'
    assert struct.unpack('<I', u.mem_read(model, 4))[0] == 0x0215EE94
    assert get(0x7B60, (10,)) == 18
    assert get(0x132C0, (model, 18)) == 24  # Original unused room.
    assert get(0x82BC4, (controller, 18)) == 208
    assert get(0x82BC4, (controller, 3)) == 23
    actor = get(0xCB184) + 4 + 23 * 32
    vt = struct.unpack('<I', u.mem_read(actor, 4))[0]
    name = get(struct.unpack('<I', u.mem_read(vt + 0x20, 4))[0] - BASE, (actor,))
    assert bytes(u.mem_read(name, 24)).split(b'\0')[0] == b'Manuel'
    get(0x36180, (root + 4 + 0x84, 0x02440000))
    cargo_count = u.reg_read(UC_ARM_REG_R0)
    assert cargo_count == 2
    # These fields are independently read by the original room/occupant getters.
    # No qualification, refit purchase, earned placement or new goods are claimed.
    changes = [
        {'address': model + 0x1E + 18, 'before': 24, 'after': 18},
        {'address': controller + 6 + 3, 'before': 23, 'after': 208},
        {'address': controller + 6 + 18, 'before': 208, 'after': 23}]
    after = bytearray(raw)
    for row in changes:
        assert after[row['address'] - BASE] == row['before']
        after[row['address'] - BASE] = row['after']
    u.mem_write(BASE, bytes(after))
    assert get(0x132C0, (model, 18)) == 18
    assert get(0x82BC4, (controller, 3)) == 208
    assert get(0x825E4, (controller, 10)) == 23
    assert sum(a != b for a, b in zip(raw, after, strict=True)) == 3
    return bytes(after), {
        'synthetic_missionary_Chapel_assignment_fixture': True, 'controller': controller,
        'source_named_model': model, 'source_named_model_name': 'Vestaros',
        'crew_member': 'Manuel', 'actor': actor, 'old_room': 3, 'new_room': 18,
        'new_room_type': 18, 'original_Missionary_getter': 0x020825E4,
        'original_getter_after_assignment': 23, 'original_cargo_count_unchanged': cargo_count,
        'only_three_declared_room_type_and_assignment_bytes_changed': True,
        'original_code_inventory_stats_money_location_and_all_other_bytes_unchanged': True,
        'earned_qualifications_refit_assignment_or_goods_acquisition_verified': False,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
        'ARM9_sha256': sha(arm), 'changes': changes}
