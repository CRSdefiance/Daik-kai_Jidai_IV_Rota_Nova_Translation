"""Record exact native class-name ownership and the observed regional replay scope."""

import json
from pathlib import Path
from struct import iter_unpack, unpack_from

from dk4tool.rom.nds import NdsImage
from scripts.inventory_arm9_text import loaded_components
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.observe_class_names_20261123 import GETTERS, ORDER, PAINTER, RELEASE, ROOT
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, OUT, digest, read, reference


REPORT = OUT.with_name("native_class_names_20261123.json")
PRIOR = ROOT.parent / "regional_orders/regional/capture/capture_report.json"
LABELS = ("イベント", "伝道師", "世界")
TYPES = ("6CEvent", "6CAdman", "6CWorld", "10CWorldData")
TOWN_ROOT_GETTER = 0x020CB178


def word(memory, address):
    at = address - BASE
    assert 0 <= at <= len(memory) - 4
    return unpack_from("<I", memory, at)[0]


def c_string(memory, address, limit=32):
    at = address - BASE
    assert 0 <= at < len(memory) - limit
    raw, terminator, _ = memory[at:at + limit].partition(b"\0")
    assert terminator and raw
    return raw + terminator


def type_name(memory, vtable):
    return c_string(memory, word(memory, word(memory, vtable - 4) + 4))[:-1].decode("ascii")


def profiles(image, clean):
    arm = image.read_file(ARM)
    original = clean.read_file(ARM)
    targets = {address for getter, (label, _) in GETTERS.items() for address in (getter, label)}
    references = {address: [] for address in targets}
    branches = {getter: [] for getter in GETTERS}
    for area, base, data in loaded_components(image):
        for i, (value,) in enumerate(iter_unpack("<I", data[:len(data) // 4 * 4])):
            pc = base + 4 * i
            if value in references:
                references[value].append((area, pc))
            if (destination := direct_bl_target(value, pc)) in branches:
                branches[destination].append((area, pc))

    records = []
    for (getter, (label, tables)), text in zip(GETTERS.items(), LABELS, strict=True):
        loc = getter - BASE
        assert arm[loc:loc + 12] == original[loc:loc + 12]
        assert tuple(word(arm, getter + 4 * i) for i in range(3)) == (0xE59F0000, 0xE12FFF1E, label)
        source = c_string(original, label)
        assert c_string(arm, label) == source == text.encode("cp932") + b"\0"
        assert references[getter] == [("arm9_section_0", addr + 8) for addr in tables]
        assert references[label] == [("arm9_section_0", getter + 8)] and not branches[getter]
        table_types = []
        for table in tables:
            assert word(arm, table + 8) == word(original, table + 8) == getter
            assert type_name(arm, table) == type_name(original, table)
            table_types.append(type_name(arm, table))
        records.append(dict(source_Japanese=text, getter=getter, exact_ARM9_offset=label - BASE,
            source_reference=dict(address=label, hex=source.hex()),
            installed_reference=dict(address=label, hex=source.hex()),
            class_tables=[dict(address=a, rtti=b) for a, b in zip(tables, table_types, strict=True)],
            table_slot_offset=8, aligned_label_references=references[label],
            aligned_getter_references=references[getter], direct_ARM_BL_calls=branches[getter]))
    assert tuple(row["rtti"] for record in records for row in record["class_tables"]) == TYPES
    return records


def replay(release):
    case = ROOT / "regional"
    evidence = [case / p for p in ("capture/capture_report.json", "requests.json", "source_contract.json", "terminal.json")]
    capture, trace, contract, terminal = map(read, evidence)
    before = read(PRIOR)
    assert capture["ROM_sha256"] == terminal["ROM_sha256"] == release["candidate_sha256"]
    assert capture["frames"] == terminal["completed_frames"] == before["frames"] == 36600
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert not any(value for k, value in capture.items() if k.startswith("synthetic_"))
    assert capture["scripted_input_schedule"] == before["scripted_input_schedule"]
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_contract_sha256"] == digest(evidence[2])
    assert contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert {row["PC"] for row in contract["targets"]} == {*GETTERS, PAINTER, ORDER}
    assert trace["rows"] == terminal["caption_calls"]
    orders = [row for row in trace["rows"] if row["PC"] == ORDER]
    assert len(orders) == 6
    actual, earlier = ({row["frame"]: row for row in report["frames_captured"] if not row["path"].endswith("_final.png")}
                       for report in (capture, before))
    assert actual.keys() == earlier.keys() and len(actual) == 20
    for frame, row in actual.items():
        assert digest(row["path"]) == row["PNG_sha256"] and row["framebuffer_sha256"] == earlier[frame]["framebuffer_sha256"]
    return dict(evidence=[reference(path) for path in (*evidence, PRIOR)], ordinary_controller_replay=True,
        copied_save_source_sha256=donor["source_sha256"], matched_full_frame_captures=sorted(actual),
        order_calls=orders, all_trace_rows=trace["rows"], total_callback_count=trace["callbacks"])


def main():
    assert not REPORT.exists()
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert digest("work/clean.nds") == release["clean_input_sha256"]
    assert digest("translations/release_stack.json") == release["registry_sha256"]
    clean, installed = map(NdsImage.open, ("work/clean.nds", release["candidate"]))
    arm = installed.read_file(ARM)
    records = profiles(installed, clean)

    startup_path = Path(release["own_registered_startup"])
    startup = read(startup_path)
    assert digest(startup_path) == release["own_registered_startup_sha256"]
    assert startup["candidate_sha256"] == release["candidate_sha256"]
    payload = startup["read_only_snapshot"]
    assert digest(payload["path"]) == payload["sha256"]
    ram = Path(payload["path"]).read_bytes()
    town_root = word(arm, TOWN_ROOT_GETTER + 8)
    assert word(ram, TOWN_ROOT_GETTER + 8) == town_root
    town_slots = [type_name(ram, word(ram, town_root + 4 + i * 108)) for i in range(115)]
    assert town_slots[:] == ["5CTown"] * 114 + ["6CAdman"]
    checked = replay(release)
    for row in records:
        address = row["installed_reference"]["address"]
        hits = [item for item in checked["all_trace_rows"] if item["PC"] == row["getter"]]
        rendered = [item for item in checked["all_trace_rows"] if item["PC"] == PAINTER and item["text_pointer"] == address]
        row.update(scoped_getter_calls=hits, scoped_direct_painter_calls=rendered,
                   other_indirect_or_copied_text_consumers_unverified=True)
    output = dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        registered_release=reference(RELEASE), records=records, regional_playback=checked,
        initialized_town_table=dict(root=town_root, stride=108, CTown_slots=114, next_object_RTTI=town_slots[-1],
            startup=reference(startup_path), read_only_snapshot=payload),
        live_ROM_changed=False, new_editorial_credit=0)
    REPORT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print("Bound three class getters and the current regional replay to the installed bytes.")


if __name__ == "__main__":
    main()
