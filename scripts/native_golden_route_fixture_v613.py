"""Opt-in Golden Route display records through the original trade-record setter.

The reported-state byte is explicit synthetic test data. No trade, discovery,
guild reporting, payment or user-save progress is claimed.
"""

import struct

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import BASE, STACK, call, machine

ARMS = {"0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731",
        "35a29ad707a3d035c1db3aed3e98646180bdc5bde8bd6b38cf57f3a6252e9ada"}
TABLE, COUNT, SIZE = 0x0237455C, 77, 28


def populate(arm, raw, rows):
    if sha(arm) not in ARMS or len(raw) != 0x400000:
        raise ValueError("Golden Route fixture requires exact clean/V612 code and 4 MiB RAM")
    if not isinstance(rows, list) or not 1 <= len(rows) <= 5:
        raise ValueError("Supply one to five explicit Golden Route display records")
    keys = {"good_id", "sea_area", "origin_town", "destination_town", "purchase", "sale"}
    for row in rows:
        if not isinstance(row, dict) or row.keys() != keys or any(type(v) is not int for v in row.values()):
            raise ValueError("Golden Route fixture requires exactly six integer fields per row")
        if (not 0 <= row["good_id"] < 77 or not 0 <= row["sea_area"] < 18
                or not 0 <= row["origin_town"] < 90 or not 0 <= row["destination_town"] < 90
                or row["origin_town"] == row["destination_town"]
                or not 0 < row["purchase"] < row["sale"] <= 1000000
                or row["sale"] // row["purchase"] < 6):
            raise ValueError("Golden Route fixture fields exceed reviewed source ranges")
    if len({r["good_id"] for r in rows}) != len(rows):
        raise ValueError("Golden Route fixture goods must be distinct")
    if any(raw[TABLE - BASE + i * SIZE] for i in range(COUNT)):
        raise ValueError("Golden Route fixture will not overwrite existing route history")
    u = machine(arm)
    u.mem_write(BASE, raw)
    assert struct.unpack("<I", u.mem_read(0x020DB528, 4))[0] == TABLE
    metadata = []
    for i, row in enumerate(rows):
        # Original caller020BB734/738 supplies sale then purchase on the stack;
        # r0 good, r1 area, r2 destination, r3 origin. Inspect actual output words.
        u.mem_write(STACK, struct.pack("<2I", row["sale"], row["purchase"]))
        executed = call(u, 0xDB148, (row["good_id"], row["sea_area"], row["destination_town"], row["origin_town"]))
        assert 0x020DB148 in executed and u.reg_read(UC_ARM_REG_R0) == 1
        address = TABLE + i * SIZE
        words = struct.unpack("<7I", u.mem_read(address, SIZE))
        assert words == (0x1801, row["purchase"], row["sale"], row["origin_town"], row["destination_town"], row["good_id"], row["sea_area"])
        # The original record viewers admit state>=3. This promotion is the
        # explicit fixture, not a simulated guild transaction.
        u.mem_write(address, b"\x03")
        metadata.append({**row, "record": address, "original_setter_words": list(words),
                         "explicit_synthetic_record_state": 3})
    call(u, 0xDB4F4, (3,))
    assert u.reg_read(UC_ARM_REG_R0) == 1
    scratch = 0x02460000
    u.mem_write(scratch, bytes(20))
    call(u, 0xDB2E8, (scratch, 5))
    selected = list(struct.unpack("<5I", u.mem_read(scratch, 20)))
    assert {p for p in selected if p} == {r["record"] for r in metadata}
    after = bytes(u.mem_read(BASE, len(raw)))
    changes = [{"address": BASE + i, "before": a, "after": b}
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert changes and all(TABLE <= r["address"] < TABLE + len(rows) * SIZE for r in changes)
    return after, {"synthetic_golden_route_display_fixture": True, "rows": metadata,
                   "table": TABLE, "source_table_capacity": COUNT, "record_size": SIZE,
                   "original_setter_and_original_nonempty_sorted_selector_executed": True,
                   "original_sorted_selection": selected, "changes": changes,
                   "only_declared_record_bytes_changed": True,
                   "before_RAM_sha256": sha(raw), "after_RAM_sha256": sha(after), "ARM9_sha256": sha(arm),
                   "normal_trade_discovery_reporting_payment_or_user_save_progress_verified": False}


def discount_salt_purchase(arm, raw, cost):
    """One working-model cost word; original sale/discovery handling must run."""
    if sha(arm) not in ARMS or len(raw) != 0x400000 or type(cost) is not int or not 1 <= cost <= 10:
        raise ValueError("Purchase-cost fixture requires exact code,4 MiB RAM,and reviewed cost1..10")
    if any(raw[TABLE - BASE + i * SIZE] for i in range(COUNT)):
        raise ValueError("Purchase-cost discovery fixture requires no existing Golden Route history")
    u = machine(arm)
    u.mem_write(BASE, raw)
    vt = 0x02158698
    ti = struct.unpack("<I", u.mem_read(vt - 4, 4))[0]
    name = struct.unpack("<I", u.mem_read(ti + 4, 4))[0]
    assert bytes(u.mem_read(name, 32)).split(b"\0")[0] == b"12CTradingView"
    candidates = []
    for offset in range(0x170000, len(raw) - 0x600, 4):
        if struct.unpack_from("<I", raw, offset)[0] != vt:
            continue
        model = struct.unpack_from("<I", raw, offset + 0x5F8)[0]
        if not BASE + 0x170000 <= model <= BASE + len(raw) - 0x610:
            continue
        words = struct.unpack_from("<6I", raw, model - BASE + 0xE4)
        if words == (13, 4, 0, 0, 11, 572):
            candidates.append((BASE + offset, model, words))
    if len(candidates) != 1:
        raise ValueError("Expected one actual Trade view with the legitimate572-cost Salt hold")
    view, model, words = candidates[0]
    for routine, expected in ((0xBCD5C, 13), (0xBCD14, 11), (0xBCCFC, 572)):
        call(u, routine, (model, 0, 0))
        assert u.reg_read(UC_ARM_REG_R0) == expected
    address = model + 0xF8
    after = bytearray(raw)
    struct.pack_into("<I", after, address - BASE, cost)
    u.mem_write(BASE, bytes(after))
    call(u, 0xBCCFC, (model, 0, 0))
    assert u.reg_read(UC_ARM_REG_R0) == cost
    changes = [{"address": BASE + i, "before": a, "after": b}
               for i, (a, b) in enumerate(zip(raw, after, strict=True)) if a != b]
    assert changes and all(address <= c["address"] < address + 4 for c in changes)
    return bytes(after), {"synthetic_golden_route_purchase_cost_fixture": True, "actual_trade_view": view,
        "actual_trade_model": model, "actual_view_RTTI": "12CTradingView", "ship": 0, "hold": 0,
        "legitimate_preexisting_Cargo_Salt_fields": list(words), "purchase_cost_address": address,
        "before_purchase_cost": 572, "fixture_purchase_cost": cost,
        "original_Cargo_good_origin_cost_getters_executed": True, "changes": changes,
        "only_temporary_trade_model_purchase_cost_word_changed": True,
        "record_table_inventory_quantity_location_money_code_and_source_saves_unchanged_by_fixture": True,
        "before_RAM_sha256": sha(raw), "after_RAM_sha256": sha(bytes(after)), "ARM9_sha256": sha(arm),
        "natural_profit_or_earned_discovery_reporting_payment_verified": False}
