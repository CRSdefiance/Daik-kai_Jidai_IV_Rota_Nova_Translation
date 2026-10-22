"""Bounded isolated display fixture for the source regional financial columns."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine

ARM = 'd1bf89d13b0094eaa27464849279e1fdb3254cc6f9f82699522adf0ae8e188df'
VALUES = {'income': 1234567890, 'expenses': 4294967295, 'invested': 987654321}
FIELDS = {'income': 0x10, 'expenses': 0x0C, 'invested': 0x14}


def populate(arm, raw, values):
    if sha(arm) != ARM or len(raw) != 0x400000 or values != VALUES:
        raise ValueError('Regional financial display fixture requires pinned V617,4 MiB RAM and reviewed unsigned values')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    if arm[0x8DFD8:0x8DFE4] != clean[0x8DFD8:0x8DFE4]:
        raise ValueError('Original Income/Expenses/Invested field loads changed')
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0xCB1A8, ())
    root = u.reg_read(UC_ARM_REG_R0)
    fleet = root + 4 + 57 * 0x84
    predicates = []
    for offset in (0x36914, 0x36948, 0x367FC):
        call(u, offset, (fleet,))
        predicates.append(u.reg_read(UC_ARM_REG_R0))
    finance = predicates[2]
    if predicates[:2] != [1, 0] or finance % 4 or not BASE <= finance < BASE + len(raw) - 24:
        raise ValueError('Expected original own non-main fleet57 with a bounded finance record')
    vt = struct.unpack('<I', u.mem_read(fleet, 4))[0]
    name_getter = struct.unpack('<I', u.mem_read(vt + 8, 4))[0]
    call(u, name_getter - BASE, (fleet,))
    name = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 64)).split(b'\0')[0]
    if name != b'Manuel Fleet':
        raise ValueError('Financial fixture requires the declared isolated Manuel Fleet')
    before = {key: struct.unpack_from('<I', raw, finance - BASE + off)[0] for key, off in FIELDS.items()}
    if any(before.values()):
        raise ValueError('Financial display fixture requires all three original zero values; no overwrite or repeat')
    after = bytearray(raw)
    for key, offset in FIELDS.items():
        struct.pack_into('<I', after, finance - BASE + offset, values[key])
    after = bytes(after)
    changes = [{'address': BASE + i, 'before': a, 'after': b}
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert changes and all(finance + 12 <= c['address'] < finance + 24 for c in changes)
    return after, {'synthetic_regional_financial_display_fixture': True, 'fleet_index': 57, 'actual_fleet': fleet,
                   'original_own_main_finance_getters': predicates, 'actual_finance_record': finance,
                   'original_source_field_offsets': FIELDS, 'before_values': before, 'display_values': values,
                   'source_native_format': '%8lu', 'unsigned_32_bit_maximum_expense_case': True,
                   'changes': changes, 'only_three_declared_finance_words_changed': True,
                   'company_money_fleet_operating_funds_ships_orders_code_other_fields_and_source_saves_preserved': True,
                   'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm),
                   'actual_monthly_income_expense_investment_or_earned_progression_verified': False}
