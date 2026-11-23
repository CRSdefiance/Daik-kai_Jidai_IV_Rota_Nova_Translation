"""Bind the observed Lisbon heading to a real town object and its clean name."""

import json

from dk4tool.rom.nds import NdsImage
from scripts.reconcile_class_names_20261123 import PAINTER, RELEASE, REPORT, ROOT, c_string, type_name, word
from scripts.reconcile_editorial_acceptance_20261123 import ARM, BASE, digest, read, reference


OUT = REPORT.with_name("native_class_names_lisbon_20261123.json")
GET_TOWN_LABEL = 0x020B6058
DRAW_RETURN = 0x020B6068
CAPTURE = 3720


def main():
    assert not OUT.exists()
    release, earlier = read(RELEASE), read(REPORT)
    case = ROOT / "lisbon"
    capture_path, trace_path, contract_path = (case / name for name in (
        "capture/capture_report.json", "requests.json", "source_contract.json"))
    capture, trace, contract = map(read, (capture_path, trace_path, contract_path))
    assert capture["ROM_sha256"] == release["candidate_sha256"] == digest(release["candidate"])
    assert earlier["candidate_sha256"] == release["candidate_sha256"] and capture["frames"] == 5200
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture["callback_errors"]
    assert not any(value for key, value in capture.items() if key.startswith("synthetic_"))
    donor = capture["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and digest(donor["source"]) == donor["source_sha256"]
    assert trace["all_host_slots_restored_and_core_file_exact"] and not trace["errors"] and not trace["mismatches"]
    assert trace["source_contract_sha256"] == digest(contract_path)
    assert contract["ARM9_sha256"] == release["target_ARM9_sha256"]
    assert {row["PC"] for row in contract["targets"]} == {PAINTER, GET_TOWN_LABEL, 0x020C134C, 0x020A1458,
                                                          *(r["getter"] for r in earlier["records"])}
    rows = trace["rows"]
    assert len(rows) == 8
    for getter, paint in zip(rows[::2], rows[1::2], strict=True):
        assert getter["PC"] == GET_TOWN_LABEL and paint["PC"] == PAINTER and paint["LR"] == DRAW_RETURN
        assert getter["frame"] == paint["frame"] and paint["text_hex"] == b"Lisbon".hex()
        assert [getter[k] for k in ("object_address", "vtable")] == [rows[0][k] for k in ("object_address", "vtable")]
        assert paint["text_pointer"] == rows[1]["text_pointer"]
    arm, clean = (NdsImage.open(path).read_file(ARM) for path in (release["candidate"], "work/clean.nds"))
    vtable = rows[0]["vtable"]
    assert type_name(arm, vtable) == type_name(clean, vtable) == "5CTown"
    assert word(arm, vtable + 8) == word(clean, vtable + 8)
    start = GET_TOWN_LABEL - BASE - 8
    end = DRAW_RETURN - BASE
    assert arm[start:end] == clean[start:end]
    displacement = rows[0]["object_address"] - earlier["initialized_town_table"]["root"] - 4
    index, remainder = divmod(displacement, 108)
    assert not remainder and 0 <= index < 114
    label = rows[1]["text_pointer"]
    before, after = c_string(clean, label), c_string(arm, label)
    assert before == "リスボン".encode("cp932") + b"\0" and after == b"Lisbon\0"
    shot, = [row for row in capture["frames_captured"] if row["frame"] == CAPTURE]
    assert digest(shot["path"]) == shot["PNG_sha256"]
    evidence = [RELEASE, REPORT, capture_path, trace_path, contract_path, shot["path"]]
    output = dict(candidate_sha256=release["candidate_sha256"], file_path=ARM,
        text="Lisbon", source_Japanese="リスボン", decision="retention",
        reason="Lisbon is the established English city name and the complete label fits the original town heading.",
        source_reference=dict(offset=label - BASE, exact_C_string_hex=before.hex()),
        installed_reference=dict(offset=label - BASE, exact_C_string_hex=after.hex()),
        real_town_slot_index=index, name_getter=word(arm, vtable + 8),
        panel_code=dict(address=BASE + start, exclusive_end=DRAW_RETURN, bytes=arm[start:end].hex()),
        ordinary_controller_replay=True, town_label_calls=rows[::2], exact_painter_inputs=rows[1::2],
        visible_heading_frame=CAPTURE, hardware=False, class_name_getter_calls=0, evidence=[reference(p) for p in evidence],
        other_town_views_and_conditions_unvisited=True, new_editorial_credit=0)
    OUT.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    print(f"Verified four original Lisbon header calls from CTown slot {index} and its six complete ASCII letters.")


if __name__ == "__main__":
    main()
