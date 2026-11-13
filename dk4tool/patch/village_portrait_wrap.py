"""Recompile every village clue/message for the observed portrait text box."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan, wrapper
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

SOURCE = "236c41a67fe8ddc82181b9809c82980a08154b3dc886c44d2cb0f585f202606e"
MANUSCRIPT = Path("translations/village_promised_words_manuscript_v1.json")
PREFIX = "They say it means "


def paragraph(text):
    if not text or not text.isascii() or " ".join(text.split()) != text:
        raise ValueError("Village prose must remain one unchanged ASCII paragraph")
    rows, current = [], ""
    for word in text.split(" "):
        budget = 36 if not rows else 35
        if len(word) > 35:
            raise ValueError("A complete village word exceeds the portrait box")
        if current and len(current) + 1 + len(word) > budget:
            rows.append(current)
            current = ""
        current += (" " if current else "") + word
    rows.append(current)
    if len(rows) > 4:
        raise ValueError("Village paragraph exceeds the captured four-row portrait canvas")
    compiled = "\n  ".join(rows)
    assert " ".join(compiled.split()) == text
    return compiled


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError("Village portrait wrapping requires the exact complete V604 ARM9")
    manuscript = json.loads(MANUSCRIPT.read_text(encoding="utf-8"))
    validate_natural_dialogue_batch(manuscript)
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    canonical = NdsImage.open("out/raphael_natural_v2_accepted_base.nds").read_file("/__arm9__.bin")
    code = MainCodeFile(source, BASE)
    old = [bytes(s.data) for s in code.sections]
    plan = cache_plan(source)
    assert len(old) == 5 and plan and len(old[3]) == plan["payload_bytes"] + 48
    packed = bytearray(old[3][:-112])  # Existing payload without cache wrapper/copy stub.
    assert len(packed) == plan["payload_bytes"] - 64
    records, changed, replacements, compiled_rows = manuscript["records"], [], [], []
    moved = records[37]
    assert moved["id"] == "VILLAGE_CLUE_18"
    units = [(s.ramAddress, bytes(s.data)) for s in code.sections]
    clean_rom = NdsImage.open("work/clean.nds")
    units += [(o.ramAddress, bytes(o.data)) for o in loadOverlayTable(
        clean_rom.rom.arm9OverlayTable, lambda _, f: clean_rom.rom.files[f]).values()]
    references = [(base + at, value) for base, data in units for at in range(len(data) - 3)
                  if moved["target_pointer"] <= (value := struct.unpack_from("<I", data, at)[0])
                  < moved["target_pointer"] + 20]
    assert references == [(BASE + moved["field"], moved["target_pointer"])]
    for n, row in enumerate(records):
        original = bytes.fromhex(row["source_hex"]) + b"\0"
        src = row["source_pointer"] - BASE
        assert clean[src:src + len(original)] == canonical[src:src + len(original)] == original
        pointer = row["target_pointer"]
        assert struct.unpack_from("<I", source, row["field"])[0] == pointer
        compiled_before = bytes.fromhex(row["compiled_hex"])
        at = pointer - POOL
        assert packed[at:at + len(compiled_before) + 1] == compiled_before + b"\0"
        if row["kind"] == "ANSWER" or row["kind"] == "MESSAGE" and row["index"] in (1, 5):
            continue
        expanded = PREFIX + row["english"] + "." if row["kind"] == "CLUE" else row["english"]
        compiled_expanded = paragraph(expanded)
        compiled = compiled_expanded[len(PREFIX):-1] if row["kind"] == "CLUE" else compiled_expanded
        updated = compiled.encode("ascii")
        target = pointer
        if updated != compiled_before:
            span = records[n + 1]["target_pointer"] - pointer
            assert 0 < span < 256
            if len(updated) + 1 <= span:
                assert not any(packed[at + len(compiled_before) + 1:at + span])
                packed[at:at + span] = (updated + b"\0").ljust(span, b"\0")
                replacements.append([at, at + span])
            else:
                # Kamui's clue grows by two bytes. Preserve its old slot and
                # every neighboring string; append a four-byte-aligned copy.
                assert row["id"] == "VILLAGE_CLUE_18"
                assert len(packed) % 4 == 0
                target = POOL + len(packed)
                packed.extend(updated + b"\0")
                struct.pack_into("<I", code.sections[0].data, row["field"], target)
            changed.append(row["id"])
        row_proof = {"id": row["id"], "field": row["field"], "old_pointer": pointer,
                     "target_pointer": target, "English_unchanged": row["english"],
                     "full_expanded_paragraph": expanded, "compiled_expanded": compiled_expanded,
                     "compiled_hex": updated.hex(), "old_compiled_hex": compiled_before.hex()}
        # A bounded list of every compiled context, not just changed rows.
        compiled_rows.append(row_proof)
    packed.extend(bytes((-len(packed)) % 32))
    new_size = len(packed) + 64
    assert new_size == plan["payload_bytes"] + 32
    assert POOL + new_size < STAGE and STAGE + new_size + 48 < 0x023F4000
    entry, copy = STAGE + len(packed), STAGE + new_size
    packed.extend(wrapper(entry, copy, new_size, source))
    code.sections[3].data = packed + old[3][-48:-4] + struct.pack("<I", new_size)
    struct.pack_into("<I", code.sections[0].data, 0x8E4, branch_link(BASE + 0x8E4, entry))
    struct.pack_into("<I", code.sections[0].data, 0xE45DC, POOL + new_size)
    saved = bytes(code.save())
    after = MainCodeFile(saved, BASE)
    assert cache_plan(saved)["payload_bytes"] == new_size
    assert all(bytes(after.sections[i].data) == old[i] for i in (1, 2, 4))
    main_restored = bytearray(after.sections[0].data)
    fields = (0x8E4, 0xE45DC, records[37]["field"])  # CLUE18 follows ANSWER18.
    assert records[37]["id"] == "VILLAGE_CLUE_18"
    for field in fields:
        main_restored[field:field + 4] = old[0][field:field + 4]
    settings = code.codeSettingsOffs
    main_restored[settings:settings + 12] = old[0][settings:settings + 12]
    assert bytes(main_restored) == old[0]
    pool_restored = bytearray(after.sections[3].data[:plan["payload_bytes"] - 64])
    for lo, hi in replacements:
        pool_restored[lo:hi] = old[3][lo:hi]
    assert bytes(pool_restored) == old[3][:-112]
    return saved, {"source_arm9_sha256": SOURCE, "target_arm9_sha256": sha(saved),
        "manuscript_sha256": sha(MANUSCRIPT.read_bytes()), "changed_records": changed,
        "compiled_contexts": compiled_rows, "portrait_first_row_cells": 36,
        "portrait_continuation_content_cells": 35, "generated_continuation_guard_spaces": 2,
        "actual_captured_canvas": [228, 48], "portrait_max_rows": 4,
        "all_English_answers_names_prose_and_template_semantics_unchanged": True,
        "all_native_fonts_renderers_keyboard_and_literal_hooks_unchanged": True,
        "pool_growth": 32, "sole_relocated_text": "VILLAGE_CLUE_18",
        "old_slots_preserved_for_relocated_text": True,
        "relocated_clue_all_byte_position_references": references,
        "only_main_changes_besides_autoload_metadata": list(fields),
        "cache_wrapper_and_native_copy_size_rebuilt": True,
        "status": "experimental", "full_goal_complete": False}


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    assert config["format"] == "dk4-village-portrait-wrap-v1"
    assert config["source_arm9_sha256"] == sha(source)
    assert config["manuscript_sha256"] == sha(MANUSCRIPT.read_bytes())
    result, report = transform(source)
    assert config["target_arm9_sha256"] == sha(result)
    return result, report
