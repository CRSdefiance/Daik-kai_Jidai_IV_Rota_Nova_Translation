"""Unequip the isolated captain's shield via native item transfer before contact."""
from pathlib import Path
import struct
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_duel_injured_contact_v1176 import apply_fixture as prior
from scripts.verify_personal_gameplay_v841 import get_machine

BASE = 0x02000000


def apply_fixture(arm, raw, request):
    if request == {'sighting_context': 'compassAttack8'}:
        return prior(arm, raw, request)
    assert request == {'duel_context': 'unarmoredContact'}
    after, parent = prior(arm, raw, {'duel_context': 'injuredContact'})
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in ((0x49DE8, 0x49F30), (0x49F30, 0x4A0F8), (0x4A5F4, 0x4A628), (0x7DCC8, 0x7DE20)):
        assert arm[lo:hi] == clean[lo:hi]
    cpu, get = get_machine(arm, after)
    assert get(0x7F244) == 1
    actor = get(0xCB184)+0x19E4
    slots = list(cpu.mem_read(actor+0x1B, 5))
    assert slots in ([219, 49, 219, 219, 219], [219]*5)
    owned = set(parent['owned_bytes'])
    transfer = None
    if slots[1] != 219:
        store = get(0xCB190)
        item = store+4+slots[1]*20
        assert get(0x4A448, item) == 3
        pointer = get(0x4A53C, item)
        name = bytes(cpu.mem_read(pointer, 80)).split(b'\0')[0].decode('cp932')
        scratch = 0x02470020
        get(0x49DE8, scratch, item)
        assert struct.unpack('<2I', cpu.mem_read(scratch+4, 8)) == (2, 1)
        fencing = get(0x7DCC8, actor, 5)
        # Descriptor kind0 is inventory. Original transfer clears its prior
        # equipment slot and records inventory ownership. No item is deleted.
        get(0x4A610, scratch, 0)
        assert get(0x49F30, item, scratch, 6, 0) == 1
        get(0x49DE8, scratch, item)
        assert struct.unpack('<I', cpu.mem_read(scratch+4, 4))[0] == 0
        assert list(cpu.mem_read(actor+0x1B, 5)) == [219]*5
        history = struct.unpack_from('<I', arm, 0x4A0EC)[0]
        allowed = set(range(actor+0x1B, actor+0x20)) | set(range(item, item+20)) | set(range(history, history+28))
        native = bytes(cpu.mem_read(BASE, 0x400000))
        differences = [BASE+i for i, (a, b) in enumerate(zip(after, native, strict=True)) if a != b]
        assert all(address in allowed for address in differences)
        owned.update(allowed)
        after = native
        transfer = {'item_ID': slots[1], 'name': name, 'category': 3,
            'prior_owner_kind_and_actor': [2, 1], 'result_owner_kind_inventory': 0,
            'original_descriptor_setter': BASE+0x4A610, 'original_transfer': BASE+0x49F30,
            'captain_slots_before': slots, 'captain_slots_after': [219]*5,
            'fencing_before_after': [fencing, get(0x7DCC8, actor, 5)],
            'native_transfer_delta_addresses': differences}
    changes = [{'address': BASE+i, 'before': a, 'after': b}
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert all(row['address'] in owned for row in changes)
    for offset in (0xD9858, 0x51A20):
        address = struct.unpack_from('<I', arm, offset)[0]
        assert not set(range(address, address+4)) & owned
        assert after[address-BASE:address-BASE+4] == raw[address-BASE:address-BASE+4]
    return after, {'context': 'unarmoredContact', 'owned_bytes': sorted(owned), 'changes': changes,
        'parent_positive_HP_and_contact_receipt': parent, 'native_armor_transfer': transfer,
        'equipped_shield_moved_to_inventory_not_deleted': transfer is not None,
        'actor_captain_IDs_fleet_ownership_original_RNG_and_duel_outcome_code_unchanged': True,
        'low_positive_starting_HP_and_native_equipment_test_state_before_duel_only': True,
        'no_earned_acquisition_or_normal_progression_claim': True,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
        'fixture_sha256': sha(Path(__file__).read_bytes())}
