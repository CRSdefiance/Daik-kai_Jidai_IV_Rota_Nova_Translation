"""Authorized isolated funds fixture using the original CForce money method."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import BASE, call, machine

ARM = '35a29ad707a3d035c1db3aed3e98646180bdc5bde8bd6b38cf57f3a6252e9ada'


def fund_company(arm, raw, target):
    if sha(arm) != ARM or len(raw) != 0x400000 or type(target) is not int or not 100000 <= target <= 1000000:
        raise ValueError('Funds fixture requires pinned code,4 MiB RAM and a reviewed100000..1000000 target')
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0xCB160, ())
    table = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x397D8, (table,))
    index = u.reg_read(UC_ARM_REG_R0)
    if not 0 <= index < 40:
        raise ValueError('Original selected faction index outside bounded source table')
    force = table + 4 + index * 0x4C
    vt = struct.unpack('<I', u.mem_read(force, 4))[0]
    ti = struct.unpack('<I', u.mem_read(vt - 4, 4))[0]
    name = struct.unpack('<I', u.mem_read(ti + 4, 4))[0]
    if bytes(u.mem_read(name, 32)).split(b'\0')[0] != b'6CForce':
        raise ValueError('Selected faction does not have the source CForce RTTI')
    call(u, 0x3CCC8, (force,))
    before = u.reg_read(UC_ARM_REG_R0)
    if before != 38371 or target <= before:
        raise ValueError('Expected the unchanged38371-coin isolated Syracuse fixture')
    # Original method clamps legal funds and owns exactly force+0Ch.
    call(u, 0x3CC80, (force, target - before))
    call(u, 0x3CCC8, (force,))
    assert u.reg_read(UC_ARM_REG_R0) == target
    after = bytes(u.mem_read(BASE, len(raw)))
    changes = [{'address': BASE + i, 'before': a, 'after': b}
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert changes and all(force + 12 <= c['address'] < force + 16 for c in changes)
    return after, {'synthetic_company_funds_fixture': True, 'original_company_table': table,
                   'selected_faction_index': index, 'actual_CForce': force, 'actual_CForce_vtable': vt,
                   'original_getter': 0x0203CCC8, 'original_money_method': 0x0203CC80,
                   'before_funds': before, 'fixture_funds': target, 'changes': changes,
                   'only_one_company_funds_word_changed': True, 'code_ships_crew_location_history_and_source_saves_unchanged': True,
                   'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm),
                   'earned_wealth_or_normal_regional_fleet_prerequisites_verified': False}


def enable_admiral(arm, raw, target, *, actor_id=16):
    """One named companion attribute; original computation reaches Command150."""
    if sha(arm) != ARM or len(raw) != 0x400000 or type(target) is not int or target != 150 or actor_id not in (16, 23):
        raise ValueError('Admiral fixture requires pinned code,4 MiB RAM and target Command150')
    name_text, field, old_value, new_value, old_command, expected_level = {
        16: ('Gerhard', 4, 83, 96, 138, 37),
        23: ('Manuel', 2, 63, 97, 120, 33),
    }[actor_id]
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0xCB160, ())
    call(u, 0x397D8, (u.reg_read(UC_ARM_REG_R0),))
    company = u.reg_read(UC_ARM_REG_R0)
    call(u, 0xCB184, ())
    actor = u.reg_read(UC_ARM_REG_R0) + 4 + actor_id * 32
    vt = struct.unpack('<I', u.mem_read(actor, 4))[0]
    given = struct.unpack('<I', u.mem_read(vt + 0x20, 4))[0]
    call(u, given - BASE, (actor,))
    if bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 32)).split(b'\0')[0] != name_text.encode():
        raise ValueError('Original person getter does not identify the declared companion')
    call(u, 0x7E958, (actor,))
    if u.reg_read(UC_ARM_REG_R0) != company:
        raise ValueError('Companion is not in the actual player faction')
    call(u, 0x7DCC8, (actor, 1))
    before = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x7E728, (actor,))
    level = u.reg_read(UC_ARM_REG_R0)
    attribute = bytes(u.mem_read(actor + 8 + field, 1))[0]
    if before != old_command or attribute != old_value or level != expected_level:
        raise ValueError('Expected original Syracuse companion skill,attribute and level')
    call(u, 0x7E750, (actor, field, new_value - old_value))
    call(u, 0x7DCC8, (actor, 1))
    assert u.reg_read(UC_ARM_REG_R0) == target and bytes(u.mem_read(actor + 8 + field, 1)) == bytes([new_value])
    call(u, 0x7E728, (actor,))
    assert u.reg_read(UC_ARM_REG_R0) == level
    after = bytes(u.mem_read(BASE, len(raw)))
    changes = [{'address': BASE + i, 'before': a, 'after': b}
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert changes == [{'address': actor + 8 + field, 'before': old_value, 'after': new_value}]
    return after, {'synthetic_admiral_ability_fixture': True, 'actor_id': actor_id, 'actor': actor,
                   'original_given_name': name_text, 'actual_player_faction': company,
                   'original_attribute_method': 0x0207E750, 'original_skill_method': 0x0207DCC8,
                   'attribute': 'Spirit' if field == 4 else 'Charm', 'before_attribute': old_value, 'fixture_attribute': new_value,
                   'before_Command': before, 'fixture_Command': target, 'unchanged_level': level,
                   'changes': changes, f'only_one_{name_text}_attribute_byte_changed': True,
                   'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after), 'ARM9_sha256': sha(arm),
                   'all_code_money_ships_other_stats_health_mood_and_source_saves_unchanged': True,
                   'earned_abilities_or_ordinary_fleet_prerequisites_verified': False}
