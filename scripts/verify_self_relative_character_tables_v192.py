"""Execute native table selection for every recovered character descriptor record."""

import hashlib
import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.research_embedded_structures_v190 import paired_sections

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
CANDIDATE = Path("out/all_routes_combined_v189_candidate.nds")
INPUT = 0x02410000
REPORT = Path("work/analysis/self_relative_character_tables_v192.json")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    assert sha(BASE.read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    # Keep the exact identity explicit; no inferred candidate ancestry.
    candidate_sha = sha(CANDIDATE.read_bytes())
    assert candidate_sha == "0361d5ab8d08b2493c1dfd1bb495b1ffbe42126da51b4296771582c0ceae1e74"
    base, candidate = NdsImage.open(BASE), NdsImage.open(CANDIDATE)
    arm, original = candidate.read_file("/__arm9__.bin"), base.read_file("/__arm9__.bin")
    assert arm[0x8A10:0x8A2C] == original[0x8A10:0x8A2C]
    descriptor_ranges = [(0x8298, 0x844C), (0x87B0, 0x880C)]
    assert all(arm[start:end] == original[start:end] for start, end in descriptor_ranges)
    blocks = IlnkContainer.parse(base.read_file("/GRP/CHARA.DK4")).blocks
    saved_blocks = IlnkContainer.parse(candidate.read_file("/GRP/CHARA.DK4")).blocks
    decode_report = json.loads(Path("work/analysis/native_compression_v192.json").read_text())
    inputs = [(index, blocks[index], "original-uncompressed-container") for index in range(6, 14)]
    for row in decode_report["results"]:
        if row["path"] != "/GRP/CHARA.DK4" or not row["native_decompression_pass"]:
            continue
        index = row["block_index"]
        data = Path(row["decoded"]).read_bytes()
        assert sha(blocks[index]) == row["source_sha256"] and sha(data) == row["decoded_sha256"]
        inputs.append((index, data, "actual-IWRAM-decompressed-container"))
    uc = machine(arm)
    rows, selections, control_words = [], 0, 0
    for index, data, mode in inputs:
        assert blocks[index] == saved_blocks[index]
        parsed = paired_sections(data)
        spans = []
        for record_index, (parts, controls) in enumerate(zip(parsed["groups"][0]["payloads"], parsed["groups"][1]["payloads"])):
            assert parts["bytes"] % 4 == 0 and controls["bytes"] % 2 == 0
            start = parsed["groups"][1]["table_start"] + parsed["groups"][1]["relative_offsets"][record_index]
            words = [value for value, in struct.iter_unpack("<H", data[start : start + controls["bytes"]])]
            part_count = parts["bytes"] // 4
            assert all((value & 0xFFF) + ((value >> 12) & 7) + 1 <= part_count for value in words)
            control_words += len(words)
            spans.append({"record": record_index, "four_byte_descriptors": part_count, "control_words": len(words), "all_native_start_count_ranges_bounded": True})
        uc.mem_write(INPUT - 16, b"\xa5" * (len(data) + 32))
        uc.mem_write(INPUT, data)
        selected = []
        for group_index, group in enumerate(parsed["groups"]):
            header = INPUT if group_index == 0 else INPUT + 4
            for record_index, relative in enumerate(group["relative_offsets"]):
                expected = group["table_start"] + relative
                trace = call(uc, 0x8A10, (header, record_index))
                actual = header + uc.reg_read(UC_ARM_REG_R0) - INPUT
                assert actual == expected and 0x02008A10 in trace
                payload = group["payloads"][record_index]
                assert sha(bytes(uc.mem_read(INPUT + actual, payload["bytes"]))) == payload["sha256"]
                selected.append({"group": group_index, "record": record_index, "offset": actual, "bytes": payload["bytes"]})
                selections += 1
        assert bytes(uc.mem_read(INPUT, len(data))) == data
        assert bytes(uc.mem_read(INPUT - 16, 16)) == b"\xa5" * 16
        assert bytes(uc.mem_read(INPUT + len(data), 16)) == b"\xa5" * 16
        rows.append({"path": "/GRP/CHARA.DK4", "block_index": index, "mode": mode, "source_block_sha256": sha(blocks[index]), "container_sha256": sha(data), "paired_records": parsed["paired_records"], "corrected_self_relative_structure": parsed, "native_selections": selected, "bounded_descriptor_spans": spans, "all_native_returns_ABI_source_bytes_and_canaries_exact": True})
    result = {"status": "pass-all-native-self-relative-record-selections", "candidate_sha256": candidate_sha, "native_selector_address": 0x02008A10, "native_selector_code_sha256": sha(arm[0x8A10:0x8A2C]), "native_selector_identical_to_canonical": True, "containers": rows, "paired_records": sum(row["paired_records"] for row in rows), "native_selections": selections, "bounded_native_control_words": control_words, "control_semantics": {"first_descriptor_index": "word & 0xFFF", "descriptor_count": "((word >> 12) & 7) + 1", "flip_flag": "word & 0x8000", "part_descriptor_stride": 4}, "previous_section-relative-origin_hypothesis_superseded": True, "header_first_word_is_table_offset_not_type_tag": True, "rom_changed": False, "limits": ["Numeric descriptor/frame selection is verified; full actor construction, pixel atlas binding, GPU and gameplay remain open."]}
    result["native_descriptor_parser_ranges_identical_to_canonical"] = [{"start_offset": start, "end_exclusive": end, "sha256": sha(arm[start:end])} for start, end in descriptor_ranges]
    REPORT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Pass: {selections} native selections across {result['paired_records']} pairs in {len(rows)} containers.")


if __name__ == "__main__":
    main()
