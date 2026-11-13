"""Bounded current V636 condition display fixture; no ROM or save writes."""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import call, machine

BASE = 0x02000000
ARM_SHA = '1f6ed33c8ee91bdeb1667e3f7524f3731ac7b0ba89a07f4be4ee1422cd7851bb'


def set_condition(arm, raw, values):
    if sha(arm) != ARM_SHA or len(raw) != 0x400000:
        raise ValueError('Condition fixture requires exact V636 ARM9 and 4 MiB RAM')
    if not isinstance(values, dict) or set(values) != {'actor', 'health', 'mood'}:
        raise ValueError('Supply actor, health and mood')
    actor_id, health, mood = (values[k] for k in ('actor', 'health', 'mood'))
    if any(type(v) is not int for v in (actor_id, health, mood)):
        raise ValueError('Condition fields must be integers')
    if actor_id not in (3, 10, 11) or not 0 <= health < 7 or not 0 <= mood < 6:
        raise ValueError('Choose Maria/Xien/Jam and original valid condition states')
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0xCB184, ())
    store = u.reg_read(UC_ARM_REG_R0)
    call(u, 0x7F244, ())
    captain = u.reg_read(UC_ARM_REG_R0)
    if captain != 3:
        raise ValueError('This fixture requires the isolated Maria save')
    captain_offset = struct.unpack_from('<I', arm, 0x80ABC)[0]
    if captain_offset != 0x19E4:
        raise ValueError('Original captain record offset differs')
    actor = store + (captain_offset if actor_id == captain else 4 + actor_id * 32)
    if not BASE <= actor < BASE + len(raw) - 32:
        raise ValueError('Invalid original actor pointer')
    vtable = struct.unpack('<I', u.mem_read(actor, 4))[0]
    getter = struct.unpack('<I', u.mem_read(vtable + 0x20, 4))[0]
    call(u, getter - BASE, (actor,))
    name = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 64)).split(b'\0')[0].decode('cp932')
    if name != {3: 'Maria', 10: 'Xien', 11: 'Jam'}[actor_id]:
        raise ValueError('Original actor identity differs')
    offset = actor + 6 - BASE
    after = bytearray(raw)
    after[offset:offset + 2] = bytes((health, mood))
    changes = [{'address': BASE + i, 'before': raw[i], 'after': after[i]}
               for i in range(offset, offset + 2) if raw[i] != after[i]]
    return bytes(after), {
        'synthetic_condition_fixture': True, 'fixture_version': 'v637-current-v636',
        'natural_condition_event_verified': False, 'actor_id': actor_id,
        'actor_address': actor, 'actor_given_name': name, 'active_captain_id': captain,
        'original_Sailor_Info_captain_vs_ordinary_resolution': True,
        'prior_health': raw[offset], 'prior_mood': raw[offset + 1],
        'health': health, 'mood': mood, 'changes': changes,
        'only_two_actor_condition_bytes_permitted': True,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
    }
