"""Research-only native result animation; no resource/crop/getter substitution."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

ROOT = Path("work/analysis/material_review_v600")
SOURCE = Path("out/all_routes_combined_v599_candidate.nds")
ENTRY, GUARD, COUNTERS, END = 0x01FFD000, 0x01FFD100, 0x01FFD200, 0x01FFDB00
HOOK = 0xCF7A4


def main():
    assert sha(SOURCE.read_bytes()) == "1c72049ca2eba551825d67de2429b4ac9751179183afc2ddb5749666d398eba5"
    current, clean = NdsImage.open(SOURCE), NdsImage.open("work/clean.nds")
    arm = current.read_file("/__arm9__.bin")
    assert arm[HOOK:HOOK + 4] == clean.read_file("/__arm9__.bin")[HOOK:HOOK + 4] == bytes.fromhex("30402de9")
    for start, end in ((0xA6BC, 0xA964), (0xA964, 0xA994), (0xC054, 0xC2C0), (0xC354, 0xC3A4)):
        assert arm[start:end] == clean.read_file("/__arm9__.bin")[start:end]
    code = MainCodeFile(arm, 0x02000000)
    assert len(code.sections) == 5
    assert all(not (s.ramAddress < END and ENTRY < s.ramAddress + len(s.data) + s.bssSize) for s in code.sections)
    assembly = f"""
push {{r0-r12, lr}}
mrs r4, cpsr
push {{r4, r5}}
ldr r4, guard_address
ldr r5, [r4]
cmp r5, #1
bne restore
ldr r6, view_address
ldr r7, [r6]
ldr r8, view_vtable
cmp r7, r8
bne restore
ldr r7, [r6, #0x40]
ldr r8, ship_address
cmp r7, r8
bne restore
ldr r7, [r6, #0x48]
cmp r7, #0
beq restore
mov r5, #0
str r5, [r4]
ldr r0, counter_address
bl 0x0200A964
restore:
pop {{r4, r5}}
msr cpsr_f, r4
pop {{r0-r12, lr}}
push {{r4, r5, lr}}
b 0x020CF7A8
guard_address: .word {GUARD}
view_address: .word 0x02185A9C
view_vtable: .word 0x02133814
ship_address: .word 0x022D9E94
counter_address: .word {COUNTERS}
"""
    body = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(assembly, ENTRY)[0])
    assert len(body) <= GUARD - ENTRY
    payload = bytearray(END - ENTRY)
    payload[:len(body)] = body
    struct.pack_into("<I", payload, GUARD - ENTRY, 1)
    struct.pack_into("<3I", payload, COUNTERS - ENTRY + 0x8E4, 10, 2, 12)
    code.sections.append(MainCodeFile.Section(payload, ENTRY, 0))
    struct.pack_into("<I", code.sections[0].data, HOOK, branch_link(0x02000000 + HOOK, ENTRY) & ~0x01000000)
    revised = bytes(code.save())
    restored = MainCodeFile(revised, 0x02000000)
    assert len(restored.sections) == 6
    main_before = MainCodeFile(arm, 0x02000000).sections[0].data
    main_after = bytearray(restored.sections[0].data)
    main_after[HOOK:HOOK + 4] = main_before[HOOK:HOOK + 4]
    settings = code.codeSettingsOffs
    assert {i for i, (a, b) in enumerate(zip(main_before, main_after, strict=True)) if a != b} <= set(range(settings, settings + 12))
    # Autoload-list metadata changes are produced by ndspy; all preexisting
    # autoload section payloads must remain identical.
    assert all(bytes(restored.sections[i].data) == bytes(code.sections[i].data) for i in range(1, 5))
    assert bytes(restored.sections[-1].data) == bytes(payload)
    paths = {}
    for label in ("current", "original_score_control", "blank_label_control"):
        rom = NdsImage.open(SOURCE)
        rom.replace_file("/__arm9__.bin", revised)
        if label == "original_score_control":
            rom.replace_file("/_pxl/deck04.pxl", clean.read_file("/_pxl/deck04.pxl"))
        if label == "blank_label_control":
            image = PxlImage.from_bytes(current.read_file("/_pxl/deck04.pxl"))
            for y in range(24):
                for x in range(160, 208):
                    image.indices[y * image.width + x] = 0
            rom.replace_file("/_pxl/deck04.pxl", image.to_bytes())
        path = ROOT / (label + "_native_score_RESEARCH_ONLY.nds")
        if path.exists():
            assert path.read_bytes() == bytes(rom.rom.save())
        else:
            rom.save(path)
        saved = NdsImage.open(path)
        assert saved.read_file("/__arm9__.bin") == revised
        files = {p: b for _, p, b in saved.iter_files()} | dict(saved.iter_components())
        original = {p: b for _, p, b in current.iter_files()} | dict(current.iter_components())
        changed = sorted(p for p in files if files[p] != original[p])
        assert changed == (["/__arm9__.bin"] if label == "current" else ["/__arm9__.bin", "/_pxl/deck04.pxl"])
        paths[label] = {"path": str(path), "sha256": sha(path.read_bytes()), "changed_components": changed}
    plan = {"production_ROM": str(SOURCE), "production_ROM_sha256": sha(SOURCE.read_bytes()),
        "research_only_not_playable_release": True, "research_ROMs": paths,
        "original_frame_pump_entry": 0x02000000 + HOOK, "displaced_instruction": "push {r4,r5,lr}",
        "new_autoload_section": [ENTRY, END], "helper_body_bytes": len(body),
        "one_shot_guard": GUARD, "synthetic_counters": {"address": COUNTERS, "Won": 10, "Lost": 2, "total": 12},
        "original_result_selector": 0x0200A964, "original_tally_animation": 0x0200A6BC,
        "actual_tally_view_ctor_and_setup": [0x0200C354, 0x0200C14C],
        "score_owner_corrected": 0x02313A38, "previous_wrong_owner_is_Ironclad_deckchip15": 0x023139FC,
        "owner_header_source_crop_palette_and_all_original_renderers_not_overridden": True,
        "won_lost_gameplay_outcome_not_earned": True, "all_other_ship_model_fields_unchanged": True,
        "helper_preserves_registers_and_CPSR_flags_and_executes_displaced_push": True,
        "full_goal_complete": False, "script_sha256": sha(Path(__file__).read_bytes())}
    (ROOT / "native_score_fixture_manifest.json").write_text(json.dumps(plan, indent=2) + "\n", encoding="utf-8")
    print("Prepared three RESEARCH_ONLY original-result animations:10 Won/2 Lost; correct owner/crops and full native rendering unchanged.")


if __name__ == "__main__":
    main()
