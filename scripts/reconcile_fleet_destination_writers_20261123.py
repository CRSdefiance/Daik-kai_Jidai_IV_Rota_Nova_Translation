"""Reconcile the scheduled Fleet Info destination with shipped story operands."""

from pathlib import Path
from re import DOTALL, compile as regex
from struct import iter_unpack, pack

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R4
from unicorn.arm_const import UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_SP

from dk4tool.formats.ilnk import IlnkContainer
from scripts.inventory_arm9_text import loaded_components
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.native_call_abi_v764 import STACK
from scripts.reconcile_class_names_20261123 import type_name, word
from scripts.reconcile_fleet_destination_name_caller_20261123 import OUT as LEGACY
from scripts.reconcile_fleet_destination_name_caller_20261123 import code_at
from scripts.stage_azores_wording_20261123 import ARM, BASE, digest_bytes
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, write
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_stock_encounter_names_20261121 import read_ram


RELEASE = Path("releases/all_routes_editorial_20261123_assigned_fleet_info_candidate/verification/registered_release_verification.json")
OUT = LEGACY.with_name("fleet_destination_writers_20261123.json")
MONSTER = LEGACY.with_name("monster_fish_transition_current_20261123.json")
CATALOGUE = LEGACY.with_name("retail_event_coverage_current_20261123.json")
TOWN_NAMES = LEGACY.with_name("town_trend_catalogue_current_20261123.json")
FLEET_REPLAY = LEGACY.with_name("assigned_fleet_detail_20261123.json")
WRITER = 0x02035A24
CONSTRUCTOR = 0x02093BAC
STORY_TYPE6 = 0x0202AF30
MENU_TYPE6 = 0x02056D6C
POINTER_TO_TOWN = 0x020B5600
SCHEDULED_WRITE = 0x02092790
MISSIONARY_SLOT = 114
TOWN_STRIDE, FLEET_STRIDE = 108, 132
# Match every byte offset, including potential matches inside command payloads.
STORY_EVENT = regex(rb"(?=\x00\xa0.{5}[\xb0-\xb9])", flags=DOTALL)
SPANS = (
    (0x0202AD00, 0x0202AD9C), (0x0202AF0C, 0x0202AF34),
    (0x0202BE8C, 0x0202BF74), (0x0202BFEC, 0x0202BFF8),
    (0x0203B160, 0x0203B330), (0x0203BA44, 0x0203BB60),
    (WRITER, WRITER + 12), (0x02056C38, 0x02056C4C), (0x02056D48, 0x02056D70),
    (0x02056FA0, 0x02057010), (0x02057068, 0x02057184),
    (0x020917B0, 0x02091838), (0x020925E4, 0x02092604),
    (0x02092764, 0x02092794), (CONSTRUCTOR, 0x02093C04),
    (POINTER_TO_TOWN, 0x020B5630),
)


def references(image):
    targets = (WRITER, CONSTRUCTOR, 0x02056C38)
    found = {target: {"aligned_ARM_BL": [], "aligned_exact_pointer": []} for target in targets}
    for area, base, data in loaded_components(image):
        for index, (value,) in enumerate(iter_unpack("<I", data[:len(data) // 4 * 4])):
            pc = base + index * 4
            target = direct_bl_target(value, pc)
            if target in found:
                found[target]["aligned_ARM_BL"].append([area, pc])
            if value in found:
                found[value]["aligned_exact_pointer"].append([area, pc])
    return found


def story_operands(image):
    result = []
    paths = [f"/{directory}/SC{route}.DK4" for directory in ("data", "testdata") for route in range(4)]
    for path in paths:
        archive = image.read_file(path)
        sections = IlnkContainer.parse(archive).blocks
        matches = []
        for block, raw in enumerate(sections):
            for match in STORY_EVENT.finditer(raw):
                offset = match.start()
                command = raw[offset:offset + 8]
                matches.append(dict(block=block, block_offset=offset, exact_hex=command.hex(),
                                    subtype=command[-1] & 15,
                                    destination_operand=command[4] & 127,
                                    standard_marker=command[2:4] == b"\xff\xff"))
        assert all(row["subtype"] != 6 for row in matches), (path, matches)
        result.append(dict(path=path, sha256=digest_bytes(archive), sections=len(sections),
                           raw_effect_family_candidates=matches, type6_raw_candidates=0))
    assert sum(row["sections"] for row in result[:4]) == 1307
    assert sum(row["sections"] for row in result[4:]) == 1310
    assert any(row["standard_marker"] for arc in result for row in arc["raw_effect_family_candidates"])
    return result


def snapshot_slots(raw, fleet_root):
    records = raw[fleet_root - BASE + 4:fleet_root - BASE + 4 + 64 * FLEET_STRIDE]
    assert len(records) == 64 * FLEET_STRIDE
    return {label: sorted(set(records[offset::FLEET_STRIDE])) for label, offset in
            (("docking_0x3c", 0x3c), ("destination_0x3f", 0x3f))}


def capture_slots(capture, frames, fleet_root):
    snapshots = {row["frame"]: row for row in capture["read_only_pause_RAM_snapshots"]}
    observed = []
    for frame in frames:
        snapshot = snapshots[frame]
        slots = snapshot_slots(read_ram(snapshot), fleet_root)
        assert all(MISSIONARY_SLOT not in values for values in slots.values())
        observed.append(dict(frame=frame, snapshot=snapshot, values=slots))
    return observed


def run_fragment(cpu, begin, stop, registers):
    for register, value in registers:
        cpu.reg_write(register, value)
    cpu.emu_start(begin, stop, count=64)
    assert cpu.reg_read(UC_ARM_REG_PC) == stop


def probe_scheduled_path(arm, capture, fleet_capture, assigned_town):
    assert capture["cold_boot"] and not capture["savestate_loaded"]
    frames = {row["frame"]: row for row in capture["read_only_pause_RAM_snapshots"]}
    raw = read_ram(frames[4800])
    assert all(code_at(raw, start, stop) == code_at(arm, start, stop) for start, stop in SPANS)
    cpu, call = get_machine(arm, raw)
    town_root, fleet_root = call(0xCB178), call(0xCB1A8)
    missionary = town_root + 4 + MISSIONARY_SLOT * TOWN_STRIDE
    vtable = word(raw, missionary)
    assert type_name(raw, vtable) == "6CAdman"
    assert word(raw, vtable + 8) == 0x0202BFEC
    active_predicate = word(raw, vtable + 0x10)
    assert active_predicate == 0x0202C000 and call(active_predicate - BASE, missionary) == 1
    assert call(POINTER_TO_TOWN - BASE, missionary) == MISSIONARY_SLOT

    for low_byte in range(256):
        cpu.mem_write(STACK, bytes(16))
        run_fragment(cpu, 0x0202AF0C, STORY_TYPE6, (
            (UC_ARM_REG_SP, STACK), (UC_ARM_REG_R0, 0), (UC_ARM_REG_R1, 0xB6000000 | low_byte),
            (UC_ARM_REG_R2, 0), (UC_ARM_REG_R3, 0), (UC_ARM_REG_R4, 0), (UC_ARM_REG_R6, 0),
        ))
        assert cpu.reg_read(UC_ARM_REG_R1) == 6
        assert bytes(cpu.mem_read(STACK + 8, 4)) == pack("<I", low_byte & 127)

    for slot in range(115):
        town = town_root + 4 + slot * TOWN_STRIDE
        # Enter at the town-to-index conversion and stop before the actual RAM write.
        run_fragment(cpu, 0x02092774, SCHEDULED_WRITE, (
            (UC_ARM_REG_SP, STACK), (UC_ARM_REG_R4, town),
            (UC_ARM_REG_R5, fleet_root), (UC_ARM_REG_R6, 1),
        ))
        assert cpu.reg_read(UC_ARM_REG_R0) == fleet_root + 4 + FLEET_STRIDE
        assert cpu.reg_read(UC_ARM_REG_R1) == 3 and cpu.reg_read(UC_ARM_REG_R2) == slot
    assert bytes(cpu.mem_read(BASE, len(raw))) == raw

    observed = capture_slots(capture, (4800, 7250, 10100), fleet_root)
    assigned = capture_slots(fleet_capture, (10600, 12000, 12400, 12800), fleet_root)
    assert any(assigned_town in sample["values"]["destination_0x3f"] for sample in assigned)
    return dict(packed_operand_cases=256, supplied_scheduled_write_slots=115,
                supplied_missionary_class=dict(slot=MISSIONARY_SLOT, address=missionary, vtable=vtable,
                    name_getter=0x0202BFEC, active_predicate=active_predicate, active_result=1),
                monster_fish_snapshot_field_values=observed, assigned_fleet_snapshot_field_values=assigned)


def main():
    release = read(RELEASE)
    assert digest(CLEAN) == release["clean_input_sha256"]
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest(REGISTRY) == release["registry_sha256"]
    clean_image, current_image = [NdsImage.open(path) for path in (CLEAN, release["candidate"])]
    clean, current = [image.read_file(ARM) for image in (clean_image, current_image)]
    assert digest_bytes(current) == release["target_ARM9_sha256"]
    exact_code = []
    for start, stop in SPANS:
        raw = code_at(clean, start, stop)
        assert raw == code_at(current, start, stop)
        exact_code.append(dict(address=start, end=stop, exact_hex=raw.hex(), sha256=digest_bytes(raw)))
    for caller, target in (
        (0x0202BF68, 0x0202ACC0), (STORY_TYPE6, CONSTRUCTOR), (MENU_TYPE6, CONSTRUCTOR),
        (0x02056FA8, 0x02057068), (0x02056FD4, 0x02057104), (0x0205700C, 0x02056C38),
        (0x02092778, POINTER_TO_TOWN), (SCHEDULED_WRITE, WRITER),
    ):
        assert direct_bl_target(word(current, caller), caller) == target
    for address, hex_code in {
        0x0203B160: "0200a0e3",
        0x0203B164: "44008de5",
        0x0203B178: "0400a0e3",
        0x0203B188: "3c008de5",
        0x0203B2BC: "3c109de5",
        0x0203B320: "44109de5",
        0x0203BA44: "0800a0e3",
        0x0203BA48: "50008de5",
        0x0203BB50: "50109de5",
        0x02056C48: "0360a0e1",
        0x02056D50: "08608de5",
        0x02056D68: "0610a0e3",
        0x02057084: "0650a0e1",
        0x020570E8: "065188c7",
        0x020570F0: "015085e2",
        0x020570F4: "5a0055e3",
        0x020570F8: "e5ffffba",
        0x02057174: "00019517",
        0x02057178: "7300a003",
        0x020925E4: "0860d8e5",
        0x02093BD0: "0810c4e5",
    }.items():
        assert code_at(current, address, address + 4).hex() == hex_code

    original_calls, installed_calls = map(references, (clean_image, current_image))
    assert original_calls == installed_calls
    assert all(not rows["aligned_exact_pointer"] for rows in installed_calls.values())
    assert len(installed_calls[WRITER]["aligned_ARM_BL"]) == 27
    assert installed_calls[0x02056C38]["aligned_ARM_BL"] == [["arm9_section_0", 0x0205700C]]
    constructor_sites = installed_calls[CONSTRUCTOR]["aligned_ARM_BL"]
    assert len(constructor_sites) == 31 and all(area == "arm9_section_0" for area, _ in constructor_sites)
    immediate_type6 = []
    for _, pc in constructor_sites:
        # ARM mov r1, #6, without condition. The three stack-fed sites are recorded separately.
        if pack("<I", 0xE3A01006) in code_at(current, pc - 24, pc):
            immediate_type6.append(pc)
    assert immediate_type6 == [STORY_TYPE6, MENU_TYPE6]

    original_story, installed_story = map(story_operands, (clean_image, current_image))
    monster = read(MONSTER)
    capture_report = next(row for row in monster.values() if isinstance(row, dict) and
                          row.get("path", "").endswith("/current/capture/capture_report.json"))
    assigned_replay = read(FLEET_REPLAY)
    assert assigned_replay["cold_boot_and_ordinary_controller_input_after_prepared_save"]
    fleet_report = next(item for item in assigned_replay["trials"]["packed_report"]["evidence"]
                        if item["path"].endswith("/capture/capture_report.json"))
    for receipt in (capture_report, fleet_report):
        assert reference(receipt["path"]) == receipt
        assert read(receipt["path"])["ROM_sha256"] == release["candidate_sha256"]
    assigned_town = next(row for row in read(TOWN_NAMES)["town_table"]["installed"] if row["name"] == "Stockholm")
    assert assigned_town["town"] == 7 and assigned_town["exact_hex"] == "53746f636b686f6c6d00"
    probe = probe_scheduled_path(current, read(capture_report["path"]), read(fleet_report["path"]), assigned_town["town"])
    clean_label = code_at(clean, 0x021370F8, 0x02137104)
    current_label = code_at(current, 0x021370F8, 0x02137104)
    assert clean_label.split(b"\0")[0].decode("cp932") == "\u76ee\u6a19\u8857\uff1a%s"
    assert current_label == b"To: %s\0\0\0\0\0\0"
    write(OUT, dict(registered_release=reference(RELEASE), exact_candidate_sha256=release["candidate_sha256"],
                    previous_slot_proof=reference(LEGACY), retail_event_catalogue=reference(CATALOGUE),
                    earlier_fixture_trace=reference(MONSTER), capture_report=capture_report,
                    earlier_assigned_fleet_gameplay=reference(FLEET_REPLAY), fleet_capture_report=fleet_report,
                    town_name_catalogue=reference(TOWN_NAMES), earlier_assigned_town=assigned_town,
                    identical_source_and_current_native_ranges=exact_code, native_reference_census=installed_calls,
                    immediate_type6_constructor_sites=immediate_type6,
                    stack_fed_constructor_sites=[dict(call=0x0203B2C8, slot=0x3C, literal_type=4),
                                                 dict(call=0x0203B32C, slot=0x44, literal_type=2),
                                                 dict(call=0x0203BB5C, slot=0x50, literal_type=8)],
                    menu_path=dict(list_builder=0x02057068, selector=0x02057104,
                                   eligible_slots=[0, 89], cancel_value=115, cancel_skips_constructor=True),
                    source_story_scan=original_story, installed_story_scan=installed_story,
                    offline_native=probe, destination_caption=dict(address=0x021370F8,
                        clean_hex=clean_label.hex(), installed_hex=current_label.hex(),
                        installed="To: %s", original_runtime_substitutions=1),
                    scope=dict(new_gameplay=False, other_destination_writers_open=True,
                               alternate_archives_scanned_as_fallback_data=True,
                               indirect_and_unaligned_reference_paths_outside_census=True,
                               changed_records=0, new_editorial_credit=0, ROM_changed=False)))
    print("27 aligned fleet-writer calls and 31 event constructors. No B6 effect in 2,617 shipped story sections per ROM.")
    print("Ordinary selector domain 0-89. Supplied Missionary slot survives the native scheduled write argument.")


if __name__ == "__main__":
    main()
