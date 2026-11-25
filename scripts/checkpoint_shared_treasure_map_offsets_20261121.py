"""Classify the four remaining numeric leads for COMMON 284 and 304."""

from collections import Counter
from pathlib import Path
from struct import unpack_from

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R3, UC_ARM_REG_SP

from scripts import checkpoint_shared_numeric_and_lil_artwork_20261121 as earlier
from scripts import reconcile_shared_display_20261121 as worklist
from scripts import register_moonlit_violin_20261121 as current
from scripts.probe_button_prompt_native import BASE, STACK, machine


base, native = current.base, current.native
OUTPUT = worklist.OUTPUT.with_name("shared_treasure_map_offsets_20261121_v1.json")
OBJECT = 0x02460000
TEXT_READERS = {0x0205528C, 0x020534F4}
BASE_SETUP, RECTANGLE_SETUP, RECTANGLE_BOUNDARY = 0x020AE314, 0x020AE0F0, 0x020AE120
VIEWS = (
    dict(key=304, type_name="CMysteryHuntMapView", constructor=0x02100B70, first_call=0x02100BA4,
        end=0x02100BC4, table=0x0216C930, construction_table=0x0216C3B0, target_delta=0xC,
        table_argument=0x0216C024, original_word_consumer=0x020AE104, virtual_part_register=UC_ARM_REG_R3,
        inner_word_consumer=0x020AE328, primary_store=0x02100B88, inner_store=0x020AE32C,
        primary_value=0x0216C968, inner_value=0x0216C3E8, bridge=(0x020D44D4, 0x020D3BD4, 0x020D4318)),
    dict(key=284, type_name="CMysteryHuntDataView", constructor=0x0210119C, first_call=0x021011D8,
        end=0x021011FC, table=0x0216CD84, construction_table=0x0216C7D0, target_delta=0x14,
        table_argument=0x0216C0FC, original_word_consumer=0x020AE108, virtual_part_register=UC_ARM_REG_R1,
        inner_word_consumer=0x020AE348, primary_store=0x021011C4, inner_store=0x020AE34C,
        primary_value=0x0216CE5C, inner_value=0x0216C868, bridge=(0x020D3BD4, 0x020D4318, 0x020C7368)),
)


def word(data, address):
    return unpack_from("<I", data, address - BASE)[0]


def table_record(arm, table, name, delta, expected):
    info = word(arm, table - 4)
    name_pointer = word(arm, info + 4)
    type_label = f"{len(name)}{name}".encode("ascii") + b"\0"
    assert arm[name_pointer-BASE:name_pointer-BASE+len(type_label)] == type_label
    assert word(arm, table - 8) == 0
    offsets = [word(arm, table - offset) for offset in (0x14, 0x10, 0xC)]
    assert word(arm, table - delta) == expected
    assert offsets == ([372, 324, 304] if expected == 304 else [284, 236, 216])
    return dict(type_name=name, table=table, type_info=info, type_label_address=name_pointer,
        displacement_words=offsets, matching_word_address=table-delta,
        allocation_delta=delta, value=expected)


def execute_view(arm, view):
    key, table, inner, delta = (view[k] for k in ("key", "table", "construction_table", "target_delta"))
    principal = table_record(arm, table, view["type_name"], delta, key)
    inherited = table_record(arm, inner, "CBaseFlatSpriteView", delta, key)
    assert word(arm, view["table_argument"]) == inner
    assert word(arm, table + 6 * 4) == RECTANGLE_SETUP
    cpu = machine(arm)
    reads, writes, bridged, setup_calls = [], [], [], []

    def register(reg):
        return cpu.reg_read(reg)

    def code(uc, pc, _size, _data):
        assert pc not in TEXT_READERS
        if pc == BASE_SETUP:
            setup_calls.append((register(UC_ARM_REG_R0), register(UC_ARM_REG_R1)))
        if pc in view["bridge"]:
            bridged.append(pc)
            uc.reg_write(UC_ARM_REG_PC, register(UC_ARM_REG_LR))

    def read(uc, _access, address, size, _value, _data):
        if address in (table - delta, inner - delta):
            assert size == 4
            reads.append((register(UC_ARM_REG_PC), address, word(arm, address)))

    def write(uc, _access, address, size, value, _data):
        if address in (OBJECT, OBJECT + key):
            assert size == 4
            writes.append((register(UC_ARM_REG_PC), address - OBJECT, value))

    hooks = [cpu.hook_add(event, callback) for event, callback in (
        (UC_HOOK_CODE, code), (UC_HOOK_MEM_READ, read), (UC_HOOK_MEM_WRITE, write))]
    try:
        # Keep the real object header and subobject pointers from the original constructor.
        cpu.mem_write(OBJECT, bytes(0x200))
        cpu.reg_write(UC_ARM_REG_R0, OBJECT)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.emu_start(view["constructor"], view["first_call"], count=40)
        assert register(UC_ARM_REG_PC) == view["first_call"]
        assert unpack_from("<I", cpu.mem_read(OBJECT, 4)) == (table,)
        primary, = [w for w in writes if w[1] == key]
        assert primary == (view["primary_store"], key, view["primary_value"])
        cpu.reg_write(UC_ARM_REG_R0, OBJECT)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.emu_start(RECTANGLE_SETUP, RECTANGLE_BOUNDARY, count=64)
        assert register(UC_ARM_REG_PC) == RECTANGLE_BOUNDARY
        assert register(view["virtual_part_register"]) == OBJECT + key
        assert reads == [(view["original_word_consumer"], table-delta, key)]
        outer_read = reads.pop()

        cpu.mem_write(OBJECT, bytes(0x200))
        cpu.reg_write(UC_ARM_REG_R0, OBJECT)
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.emu_start(view["constructor"], view["end"], count=256)
        assert register(UC_ARM_REG_PC) == view["end"]
        assert tuple(bridged) == view["bridge"] and setup_calls == [(OBJECT, view["table_argument"])]
        inner_write, = [w for w in writes if w[0] == view["inner_store"]]
        assert inner_write == (view["inner_store"], key, view["inner_value"])
        assert unpack_from("<I", cpu.mem_read(OBJECT + key, 4)) == (view["inner_value"],)
        matched = [r for r in reads if r[0] == view["inner_word_consumer"]]
        assert matched == [(view["inner_word_consumer"], inner-delta, key)]
        assert all(r[1:] == (inner-delta, key) for r in reads)
    finally:
        for hook in hooks:
            cpu.hook_del(hook)
    return dict(value=key, complete_object=principal, base_under_construction=inherited,
        constructor_address=view["constructor"], supplied_object=OBJECT, bridged_nested_calls=bridged,
        source_rectangle_read=outer_read, source_rectangle_subobject=OBJECT+key,
        original_full_view_assignment=primary, original_base_initializer_read=matched[0],
        original_base_initializer_assignment=inner_write, common_getter_or_copier_entered=False)


def main():
    assert not OUTPUT.exists()
    release, draft, previous, earlier_numeric = map(base.load, (
        current.RELEASE, current.REVIEW, worklist.OUTPUT, earlier.OUTPUT))
    assert base.digest(current.ROM) == release["candidate_sha256"] == draft["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(worklist.CLEAN) == release["clean_input_sha256"] == previous["clean_sha256"]
    with current.mapped(base.LEDGER) as ledger:
        parent = current.value(ledger, "current_integrated_candidate", 1)
        assert parent["sha256"] == release["candidate_sha256"]
        assert current.value(ledger, "records_editorially_completed", 1) == 27700
        assert current.value(ledger, "pending_shared_consumer_checkpoint_20261114", 1)["remaining_total"] == 276
    clean, active = map(base.NdsImage.open, (worklist.CLEAN, current.ROM))
    ja, arm = (rom.read_file(worklist.ARM) for rom in (clean, active))
    assert native.digest(arm) == release["target_ARM9_sha256"]
    assert native.digest(active.read_file(worklist.COMMON)) == release["target_COMMON_sha256"]
    source = worklist.workflow.common_message_entries(clean.read_file(worklist.COMMON), ja)
    installed = worklist.entries(active)
    count = Counter()
    bindings = []
    for row in previous["records"]:
        num = row["message_ID"]
        assert source[num].text.hex() == row["source_hex"] and installed[num].text.hex() == row["current_hex"]
        assert worklist.workflow.reference(source[num]) == row["source_reference"]
        assert worklist.workflow.reference(installed[num]) == row["current_reference"]
        count[row["kind"]] += 1
        if num in (284, 304):
            bindings.append({k: row[k] for k in ("message_ID", "source_reference", "current_reference",
                "source_hex", "current_hex", "draft", "other_COMMON_display_paths")})
    assert count == {"scene": 214, "online": 31, "legacy": 31}
    proofs = [execute_view(ja, view) for view in VIEWS]
    assert proofs == [execute_view(arm, view) for view in VIEWS]
    for p in proofs:
        prior = earlier_numeric["remaining_graphics_or_data_word_matches_unclassified"][str(p["value"])]
        assert sorted(prior) == sorted(p[k]["matching_word_address"] for k in ("complete_object", "base_under_construction"))
    assert len(bindings) == 2
    base.save(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        registered_release=str(current.RELEASE), full_row_binding_parent=str(worklist.OUTPUT), rows=dict(count),
        all_previous_source_and_current_byte_references_exact=True,
        classified_legacy_numeric_locations=proofs, related_stored_references=bindings,
        prior_investigation=str(earlier.OUTPUT), other_display_paths_remain_open=True,
        new_editorial_credit=0, new_emulator_replays=0, open_stored_rows=276,
        evidence={str(p): base.digest(p) for p in (Path(__file__), current.RELEASE, worklist.OUTPUT, earlier.OUTPUT)}))
    print("Verified four treasure-map subobject offsets and rebound all 276 stored text entries.")


if __name__ == "__main__":
    main()
