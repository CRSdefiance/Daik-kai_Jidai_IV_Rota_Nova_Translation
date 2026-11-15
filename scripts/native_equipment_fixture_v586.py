"""Explicit Maria equipment display fixtures using original transfer/setter code.

Slots are category-correct, but explicit slot assignment is not proof of normal
eligibility, acquisition or player progression. Only isolated live RAM changes.
"""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import call, machine

ARM_SHA = "60948e7a8f50abc838cfdf49114782aeeb977b75352dc741e90e8dafd161150e"
BASE, SCRATCH = 0x02000000, 0x02470020


def equip(arm, raw, items):
    if sha(arm) != ARM_SHA or len(raw) != 0x400000:
        raise ValueError("Equipment display fixture requires exact V581 and4 MiB live RAM")
    if not isinstance(items, list) or len(items) != 5:
        raise ValueError("Supply exactly five category-correct item IDs or null")
    selected = [i for i in items if i is not None]
    if any(type(i) is not int or not 0 <= i < 218 for i in selected) or len(set(selected)) != len(selected):
        raise ValueError("Equipment fixture IDs must be unique integers0..217")
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0x7F244, ())
    captain = u.reg_read(UC_ARM_REG_R0)
    if captain != 3:
        raise ValueError("This fixture requires Maria's isolated save")
    call(u, 0xCB184, ())
    crew_store = u.reg_read(UC_ARM_REG_R0)
    # Source literal used by49F30/4A0F8 for the active captain's separate record.
    captain_offset = int.from_bytes(u.mem_read(0x0204A0F4, 4), "little")
    assert captain_offset == 0x19E4
    owner = crew_store + captain_offset
    old = list(u.mem_read(owner + 0x1B, 5))
    assert all(i < 218 or i == 0xDB for i in old)
    call(u, 0xCB190, ())
    item_store = u.reg_read(UC_ARM_REG_R0)
    history = struct.unpack_from("<I", arm, 0x4A0EC)[0]
    permitted = set(range(history, history + 28)) | set(range(owner + 0x1B, owner + 0x20))
    affected = sorted(set(selected + [i for i in old if i != 0xDB]))
    metadata = {}
    for item_id in affected:
        item = item_store + 4 + item_id * 20
        permitted.update(range(item, item + 20))
        call(u, 0x49DE8, (SCRATCH, item))
        kind, prior_owner = struct.unpack("<2I", u.mem_read(SCRATCH + 4, 8))
        if kind == 3:
            raise ValueError("Fixture will not change ship equipment")
        if kind == 2:
            if not 0 <= prior_owner < 114:
                raise ValueError("Unexpected prior crew owner index")
            prior = owner if prior_owner == captain else crew_store + 4 + prior_owner * 32
            permitted.update(range(prior + 0x1B, prior + 0x20))
        call(u, 0x4A448, (item,))
        category = u.reg_read(UC_ARM_REG_R0)
        call(u, 0x4A53C, (item,))
        name = bytes(u.mem_read(u.reg_read(UC_ARM_REG_R0), 128)).split(b"\0")[0].decode("cp932")
        metadata[item_id] = {"item_id": item_id, "name": name, "category": category,
                             "prior_owner_kind": kind, "prior_owner_if_crew": prior_owner if kind == 2 else None}
    for slot, item_id in enumerate(items):
        if item_id is not None and metadata[item_id]["category"] != (2 if slot == 0 else 3 if slot == 1 else 4):
            raise ValueError("Fixture item does not match the weapon/armor/accessory slot category")
    # Clear existing gear and make all selected items inventory-owned first,
    # preserving the original game's ownership cleanup and acquisition history.
    for item_id in affected:
        item = item_store + 4 + item_id * 20
        call(u, 0x4A610, (SCRATCH, 0))
        call(u, 0x49F30, (item, SCRATCH, 6, 0))
        assert u.reg_read(UC_ARM_REG_R0) == 1
    assert bytes(u.mem_read(owner + 0x1B, 5)) == b"\xDB" * 5
    for slot, item_id in enumerate(items):
        if item_id is None:
            continue
        call(u, 0x4A5F4, (SCRATCH, captain))
        call(u, 0x49F30, (item_store + 4 + item_id * 20, SCRATCH, slot, 0))
        assert u.reg_read(UC_ARM_REG_R0) == 1
    expected = bytes(0xDB if i is None else i for i in items)
    assert bytes(u.mem_read(owner + 0x1B, 5)) == expected
    for item_id in selected:
        call(u, 0x49DE8, (SCRATCH, item_store + 4 + item_id * 20))
        assert struct.unpack("<2I", u.mem_read(SCRATCH + 4, 8)) == (2, captain)
    after = bytes(u.mem_read(BASE, len(raw)))
    changes = [{"address": BASE + i, "before": a, "after": b}
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    if any(change["address"] not in permitted for change in changes):
        raise ValueError("Original transfer changed bytes outside selected item/history/crew equipment extents")
    return after, {"synthetic_equipment_display_fixture": True, "captain": captain,
                   "before_items": old, "items": items,
                   "selected_native_names": [metadata[i] for i in selected],
                   "category_correct_explicit_slot_assignment_not_eligibility_proof": True,
                   "original_transfer_entry": 0x02049F30, "original_owner_setter": 0x0204A5F4,
                   "changes": changes, "before_RAM_sha256": sha(raw), "after_RAM_sha256": sha(after),
                   "normal_acquisition_or_eligibility_verified": False}
