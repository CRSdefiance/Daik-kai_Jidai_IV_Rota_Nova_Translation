"""Bind the initialized name getters and the ordinary Forces Chart replay to the registered ROM."""

from struct import pack

from PIL import Image

from scripts.inventory_arm9_text import loaded_components
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.observe_event_and_world_names_20261123 import EVENT, FOCUS, FRAMES, HOME, OBJECT_CALLS
from scripts.observe_event_and_world_names_20261123 import REFERENCE, RELEASE, REQUESTS, ROOT, WORLD
from scripts.reconcile_class_names_20261123 import BASE, GETTERS, PAINTER, c_string, profiles, type_name, word
from scripts.reconcile_queued_sailing_hints_20261123 import ARM, CLEAN, NdsImage, OUT, REGISTRY
from scripts.reconcile_queued_sailing_hints_20261123 import digest, read, reference, write
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_stock_encounter_names_20261121 import read_ram


REPORT = OUT.with_name("event_and_world_names_current_20261123.json")
SHEET = REPORT.with_suffix(".png")
SCAN_START = 0x02170000
OWNERS = {0x02134168: EVENT, 0x0215B4AC: WORLD, 0x0215B710: None}


def aligned_positions(raw, base, value):
    marker = pack("<I", value)
    offset = raw.find(marker)
    while offset != -1:
        if (base + offset) % 4 == 0:
            yield base + offset
        offset = raw.find(marker, offset + 1)


def stored_objects(release, candidate, clean):
    startup_path = release["own_registered_startup"]
    assert digest(startup_path) == release["own_registered_startup_sha256"]
    startup = read(startup_path)
    assert startup["candidate_sha256"] == release["candidate_sha256"]
    ram = read_ram(startup["read_only_snapshot"])
    arm, original_arm = (image.read_file(ARM) for image in (candidate, clean))
    assert digest(REGISTRY) == release["registry_sha256"]
    current, source = map(loaded_components, (candidate, clean))
    labels = profiles(candidate, clean)
    cpu, call = get_machine(arm, ram)
    objects = []
    for table, expected_owner in OWNERS.items():
        addresses = list(aligned_positions(ram[SCAN_START - BASE:], SCAN_START, table))
        assert addresses == ([] if expected_owner is None else [expected_owner])
        getter = word(ram, table + 8)
        text, tables = GETTERS[getter]
        assert table in tables and getter == word(arm, table + 8) == word(original_arm, table + 8)
        assert type_name(ram, table) == type_name(arm, table) == type_name(original_arm, table)
        targets = (table,) if expected_owner is None else (table, expected_owner)
        refs = {}
        for value in targets:
            matches = [(area, addr) for area, base, data in current for addr in aligned_positions(data, base, value)]
            assert matches and matches == [(area, addr) for area, base, data in source
                                          for addr in aligned_positions(data, base, value)]
            refs[f"0x{value:08X}"] = matches
        returned = None
        if expected_owner is not None:
            returned = call(getter - BASE, expected_owner)
            assert returned == text and c_string(ram, returned) == c_string(original_arm, text)
            assert bytes(cpu.mem_read(BASE, len(ram))) == ram
        objects.append(dict(type=type_name(ram, table), table=table, getter_table_offset=8,
                            getter_address=getter, owner_address=expected_owner,
                            offline_getter_return=returned, source_and_installed_aligned_references=refs))
    return dict(startup=reference(startup_path), startup_RAM=startup["read_only_snapshot"],
                initialized_RAM_scan_range=[SCAN_START, BASE + len(ram)], class_labels=labels,
                objects=objects)


def chart_replay(release, arm, source):
    folder = ROOT / "forces_chart"
    capture_path = folder / "capture/capture_report.json"
    trace_path, contract_path = folder / "requests.json", folder / "source_contract.json"
    capture, trace, contract = map(read, (capture_path, trace_path, contract_path))
    donor = capture["battery_save_preloaded"]
    assert capture["ROM_sha256"] == release["candidate_sha256"]
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert not any(value for key, value in capture.items() if key.startswith("synthetic_"))
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_contract_sha256"] == digest(contract_path)
    assert contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert {row["PC"] for row in contract["targets"]} == {PAINTER, HOME, *GETTERS, *OBJECT_CALLS, *REQUESTS}
    assert capture["scripted_input_schedule"] == read(REFERENCE)["scripted_input_schedule"]

    calls = trace["rows"]
    assert trace["callbacks"]
    chart_calls = [row for row in calls if row["PC"] == HOME and 13001 <= row["frame"] <= 14001]
    assert [(row["frame"], row["LR"]) for row in chart_calls] == [(13004, 0x0208D248), (13306, 0x0208D248)]
    owner_calls = [row for row in calls if row["PC"] in OBJECT_CALLS]
    assert [(row["PC"], row["LR"], row["object_address"]) for row in owner_calls] == [
        (0x020CB3CC, 0x0203EDDC, WORLD), (0x02022EF8, 0x0203EDE8, EVENT)]
    for row in calls:
        if row["PC"] in OBJECT_CALLS:
            assert row["object_address"] == OBJECT_CALLS[row["PC"]]
            assert type_name(arm, row["vtable"]) in {"6CEvent", "6CWorld"}
        site = row["LR"] - 4
        instruction = word(arm, site)
        assert instruction == word(source, site) and direct_bl_target(instruction, site) == row["PC"]
        row["exact_original_and_installed_call_instruction"] = dict(address=site, word=instruction)
    label_calls = [row for row in calls if row["PC"] in GETTERS or row["PC"] == PAINTER]
    uses = [row for row in trace["source_requests"] if row["message_ID"] in FOCUS]
    assert not label_calls and not uses

    shots = {row["frame"]: row for row in capture["frames_captured"] if row["frame"] in FRAMES}
    assert tuple(shots) == FRAMES
    sheet = Image.new("RGB", (256 * len(shots), 384))
    for i, shot in enumerate(shots.values()):
        assert digest(shot["path"]) == shot["PNG_sha256"]
        with Image.open(shot["path"]) as image:
            assert image.size == (256, 384)
            sheet.paste(image, (256 * i, 0))
    sheet.save(SHEET)

    return dict(actual_gameplay=True, unmodified_battery_save=True, completed_frames=capture["frames"],
                frame_order=list(shots), frames=list(shots.values()), contact_sheet=reference(SHEET),
                observed_owner_and_chart_calls=calls, class_label_getter_and_direct_painter_calls=label_calls,
                archived_COMMON_IDs_watched=sorted(FOCUS), archived_COMMON_calls=uses,
                observed_COMMON_requests=trace["source_requests"],
                synthetic_setup_used=False, hardware=False,
                evidence=[reference(path) for path in (capture_path, trace_path, contract_path, REFERENCE)])


def main():
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    candidate, clean = map(NdsImage.open, (release["candidate"], CLEAN))
    initialization = stored_objects(release, candidate, clean)
    gameplay = chart_replay(release, candidate.read_file(ARM), clean.read_file(ARM))
    write(REPORT, dict(registered_release=reference(RELEASE), candidate_sha256=release["candidate_sha256"],
                       clean_sha256=release["clean_input_sha256"], file_path=ARM,
                       offline_native=initialization, ordinary_forces_chart_gameplay=gameplay,
                       unvisited=["Other indirect name calls", "Other consumers of copied class names",
                                  "Other callers of the five archived COMMON entries"],
                       ROM_changed=False, new_editorial_credit=0))
    print("Verified the initialized Event and World getters and five ordinary Forces Chart navigation holds.")


if __name__ == "__main__":
    main()
