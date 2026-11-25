"""Bind Rafael's ordinary custom-name replay to its source and live display buffers."""

import json
import string
from hashlib import sha256
from pathlib import Path
from struct import unpack_from

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.village_promised_words_release import keyboard_ascii_wrapper
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, call, machine

ROOT = Path("work/rafael_custom_name_20261119")
CAPTURE = ROOT / "capture"
REPORT = CAPTURE / "capture_report.json"
REVIEW = Path("releases/all_routes_editorial_20261119_rafael_departure_and_debrief_candidate"
              "/verification/registered_review.json")
ROM_HASH = "350f1ba938d339c079986a4c0f85a0e7faad4def628f4d23c7e19843033d86e2"
EDITOR = 0x0218EEC8
NAME = "RafaelＭａａ".encode("cp932")
FRAMES = (2790, 3270, 3510, 5130, 5340, 6890, 7220)


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(data):
    return sha256(data).hexdigest()


def snapshot(rows, frame, hash_key):
    row, = (row for row in rows if row["frame"] == frame)
    path = Path(row["path"])
    data = path.read_bytes()
    assert digest(data) == row[hash_key]
    return data, {"path": path.as_posix(), "sha256": row[hash_key]}


def require_string(memory, address, data):
    offset = address - BASE
    assert memory[offset:offset + len(data) + 1] == data + b"\0"
    return {"address": hex(address), "bytes_hex": data.hex(), "text": data.decode("cp932")}


def source_references(clean, current):
    review = read(REVIEW)
    archives = [image.read_file("/data/SC0.DK4") for image in (clean, current)]
    blocks = [IlnkContainer.parse(archive).blocks[44] for archive in archives]
    result = []
    for record_id in ("DK4_MES_B44_R0017", "DK4_MES_B44_R0021"):
        row, = (row for row in review["records"] if row["id"] == record_id)
        source, installed = row["source_reference"], row["registered_reference"]
        assert digest(archives[0]) == source["archive_sha256"]
        for ref, block in zip((source, installed), blocks, strict=True):
            at, data = ref["offset"], bytes.fromhex(ref["exact_stored_hex"])
            assert ref["block"] == 44 and at == ref["command_offset"] + 5
            assert block[at:at + len(data) + 1] == data + b"\0"
        current_ref = installed | {"candidate_sha256": ROM_HASH, "archive_sha256": digest(archives[1])}
        result.append({"id": record_id, "japanese": row["Japanese"], "english": row["english"],
                       "source": source, "current": current_ref, "decision": row["decision"],
                       "retention_or_revision_reason": row["localization_note"]})
    return result


def keyboard_table(clean, current, memory):
    first, last = 0xD1B00, 0xD1F00
    arms = [image.read_file("/__arm9__.bin") for image in (clean, current)]
    assert arms[0][first:last] == arms[1][first:last] == memory[first:last]
    assert clean.read_file("/GRP/KANJI.FNT") == current.read_file("/GRP/KANJI.FNT")
    cpu = machine(arms[1])
    cpu.mem_write(BASE, memory)
    label, keys = 0x02470000, 0x02470100
    cpu.mem_write(label, "英".encode("cp932") + b"\0")
    call(cpu, 0xD1E3C, (EDITOR + 4, label))
    assert cpu.reg_read(UC_ARM_REG_R0) == 50
    cpu.mem_write(0x027F0000, b"\xff" * 4)
    call(cpu, 0xD1BBC, (EDITOR + 4, 50, keys, 0))
    count = cpu.reg_read(UC_ARM_REG_R0)
    table = bytes(cpu.mem_read(keys, 2 * count))
    assert count == 52
    assert table.decode("cp932") == "".join(chr(ord(c) + 0xFEE0) for c in string.ascii_letters)
    insertion, village_marker, original_append = 0x01FF9E40, 0x01FF9E38, 0x020B08D8
    wrapper = keyboard_ascii_wrapper(insertion, village_marker)
    assert bytes(cpu.mem_read(insertion, len(wrapper))) == wrapper
    assert unpack_from("<I", memory, 0xAED2C)[0] == 0xEB000000 | (((insertion - 0x020AED34) // 4) & 0xFFFFFF)
    provider_addr = EDITOR + 4
    original_provider = bytes(cpu.mem_read(provider_addr, 4))
    assert original_provider == bytes.fromhex("1c591502")
    for pos, letter in enumerate(string.ascii_letters):
        key = table[2 * pos:2 * pos + 2] + b"\0"
        for provider, expected in ((original_provider, key), (village_marker.to_bytes(4, "little"),
                                                               letter.encode("ascii") + b"\0\0")):
            cpu.mem_write(provider_addr, provider)
            cpu.mem_write(label, key + b"\xa5")
            cpu.reg_write(UC_ARM_REG_R0, EDITOR + 0x38)
            cpu.reg_write(UC_ARM_REG_R1, label)
            cpu.emu_start(insertion, original_append, count=64)
            assert cpu.reg_read(UC_ARM_REG_PC) == original_append
            assert bytes(cpu.mem_read(label, 4)) == expected + b"\xa5"
    return {"provider_entry": "0x020D1BBC", "table_count": count, "table_hex": table.hex(),
            "clean_equal_checked_code_span": [hex(BASE + first), hex(BASE + last)],
            "original_KANJI_FNT_exact": True, "offline_on_captured_state": True,
            "existing_key_wrapper": hex(insertion), "original_append_entry": hex(original_append),
            "captain_unmarked_keys_preserved": count,
            "village_marked_keys_converted_on_isolated_copy": count}


def main():
    report = read(REPORT)
    journal_path = CAPTURE / "navigation_command_journal.json"
    journal = read(journal_path)
    rom, clean_rom = Path(report["ROM"]), Path("work/clean.nds")
    assert digest(rom.read_bytes()) == report["ROM_sha256"] == ROM_HASH
    assert report["frames"] == 7880 and report["cold_boot"] and not report["savestate_loaded"]
    assert not report.get("battery_save_preloaded") and not report["callback_errors"]
    assert not report["hardware_device_verification"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert journal["last_command_frame"] == report["frames"]
    memory, evidence = {}, {}
    for frame in FRAMES:
        memory[frame], ram = snapshot(report["read_only_pause_RAM_snapshots"], frame, "sha256")
        _, png = snapshot(report["frames_captured"], frame, "PNG_sha256")
        evidence[frame] = {"capture": png, "read_only_RAM": ram}
    editor_states = {}
    for frame, data in ((2790, b"Rafael"), (3510, "RafaelＭ".encode("cp932")), (5130, NAME)):
        raw = memory[frame]
        fields = [unpack_from("<I", raw, EDITOR - BASE + n)[0] for n in (0, 4, 0x38, 0xD8)]
        assert fields == [0x021558CC, 0x0215591C, 0x02155D44, 16]
        editor_states[frame] = require_string(raw, EDITOR + 0xB4, data)
    confirms = require_string(memory[5340], 0x02192E8C, NAME)
    dialogue = b"Say, " + NAME + b"... what \n do you think of men who go to sea? "
    uses = {
        6890: {"actor_first_name": require_string(memory[6890], 0x022D5D44, NAME),
               "expanded_dialogue": require_string(memory[6890], 0x0218EDC8, dialogue)},
        7220: {"actor_first_name": require_string(memory[7220], 0x022D5D44, NAME),
               "speaker_label": require_string(memory[7220], 0x022A4F78, NAME + b" Castor"),
               "reply": require_string(memory[7220], 0x0218EDC8, b"Hmm... That's hard to answer... ")},
    }
    clean, current = map(NdsImage.open, (clean_rom, rom))
    proof = {"candidate_sha256": ROM_HASH, "clean_sha256": digest(clean_rom.read_bytes()),
             "ordinary_input_and_no_state_injection": True, "frames": evidence,
             "report": REPORT.as_posix(), "report_sha256": digest(REPORT.read_bytes()),
             "navigation_journal": journal_path.as_posix(), "navigation_journal_sha256": digest(journal_path.read_bytes()),
             "editor_states": editor_states, "editor_capacity_field": 16, "confirmation": confirms,
             "live_uses": uses, "story_records": source_references(clean, current),
             "original_latin_provider": keyboard_table(clean, current, memory[3270]),
             "finding": "Latin input leaves full-width bytes in the live name, dialogue and speaker label.",
             "new_editorial_coverage_credit": 0, "hardware_verified": False, "fix_verified": False}
    (ROOT / "custom_name_evidence.json").write_text(json.dumps(proof, indent=2, ensure_ascii=False) + "\n",
                                                   encoding="utf-8")
    print("Verified edited name, both live display consumers, exact story records and 52 Latin keys.")


if __name__ == "__main__":
    main()
