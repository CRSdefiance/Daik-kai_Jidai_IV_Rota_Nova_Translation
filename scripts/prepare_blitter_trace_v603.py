"""Research-only bounded source-rectangle trace; never a production candidate."""

import json
import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

ROOT = Path("work/analysis/blitter_trace_v603")
SOURCE = Path("out/all_routes_combined_v599_candidate.nds")
ENTRY, TILE_ENTRY, CONTROL, RECORDS, END = (0x01FFD000, 0x01FFD020, 0x01FFD500, 0x01FFD540, 0x01FFF000)
CAPACITY, STRIDE = 84, 80
CORNER, TILE = 0x01FF92D8, 0x01FFAE70
FIELDS = ("kind", "return_LR", "header", "screen", "bank", "source_x", "source_y", "source_w", "source_h",
          "destination_x", "destination_y", "destination_w", "destination_h", "flags", "width_words", "height",
          "adapter_owner", "original_r5", "first_pixel_word", "hits")


def build_body():
    # Saved registers start at scratch+88, original SP at scratch+144. No
    # source/getter/resource is substituted; both original prologues execute.
    assembly = f"""
push {{r0-r12, lr}}
mrs r4, cpsr
push {{r4, r5}}
mov r4, #0
b common
nop
nop
nop
push {{r0-r12, lr}}
mrs r4, cpsr
push {{r4, r5}}
mov r4, #1
b common
common:
sub sp, sp, #80
str r4, [sp]
ldr r6, control_address
ldr r7, [r6]
add r7, r7, #1
str r7, [r6]
ldr r0, [sp, #92]
ldr r1, main_start
cmp r0, r1
blo finish
ldr r1, main_limit
sub r1, r1, #20
cmp r0, r1
bhi finish
tst r0, #3
bne finish
ldr r1, [r0]
and r2, r1, #255
cmp r2, #4
bne finish
str r1, [sp, #52]
ldr r1, [r0, #4]
ldr r2, [r0, #8]
str r1, [sp, #56]
str r2, [sp, #60]
cmp r1, #12
cmpeq r2, #20
beq selected
cmp r2, #8
bne atlas
cmp r1, #4
cmpne r1, #6
cmpne r1, #8
cmpne r1, #12
beq selected
atlas:
cmp r2, #256
bne finish
cmp r1, #64
cmpne r1, #128
bne finish
ldr r2, [sp, #100]
ldr r3, [r2]
ldr r5, [r2, #4]
cmp r4, #0
ldreq r7, [sp, #144]
ldreq r7, [r7, #4]
ldrne r7, [r2, #12]
cmp r7, #0
moveq r7, #1
add r7, r5, r7
cmp r5, #56
bge positive_control
cmp r7, #32
ble positive_control
cmp r1, #128
moveq r8, #440
movne r8, #184
cmp r4, #0
ldreq r7, [sp, #144]
ldreq r7, [r7]
ldrne r7, [r2, #8]
cmp r7, #0
moveq r7, #1
add r7, r3, r7
cmp r7, r8
ble positive_control
add r8, r8, #72
cmp r3, r8
blt selected
positive_control:
ldr r7, [r6, #16]
mov r8, #1
mov r8, r8, lsl r4
tst r7, r8
bne finish
orr r7, r7, r8
str r7, [r6, #16]
selected:
ldr r7, [r6, #4]
add r7, r7, #1
str r7, [r6, #4]
ldr r7, [sp, #140]
str r7, [sp, #4]
str r0, [sp, #8]
ldr r1, [sp, #88]
str r1, [sp, #12]
ldr r1, [sp, #96]
str r1, [sp, #16]
ldr r1, [sp, #100]
ldr r2, [r1]
ldr r3, [r1, #4]
str r2, [sp, #20]
str r3, [sp, #24]
cmp r4, #0
ldreq r1, [sp, #144]
addeq r2, sp, #28
addne r1, r1, #8
ldr r2, [r1]
ldr r3, [r1, #4]
str r2, [sp, #28]
str r3, [sp, #32]
cmp r4, #0
ldreq r1, [sp, #148]
ldrne r1, [sp, #144]
ldr r5, [r1]
ldr r8, [r1, #4]
str r5, [sp, #36]
str r8, [sp, #40]
cmp r4, #0
ldrne r2, [r1, #8]
ldrne r3, [r1, #12]
subne r2, r2, r5
subne r3, r3, r8
str r2, [sp, #44]
str r3, [sp, #48]
mov r1, #0
str r1, [sp, #64]
ldr r2, [sp, #108]
str r2, [sp, #68]
ldr r3, adapter_return0
cmp r7, r3
ldr r3, adapter_return1
cmpne r7, r3
bne sample
ldr r3, main_start
cmp r2, r3
blo sample
ldr r3, main_limit
sub r3, r3, #16
cmp r2, r3
bhi sample
ldr r1, [r2, #12]
str r1, [sp, #64]
sample:
mov r1, #0
ldr r2, [r0, #16]
cmp r2, #20
blo sample_done
cmp r2, #0x100000
bhi sample_done
adds r2, r0, r2
bcs sample_done
ldr r3, main_limit
sub r3, r3, #4
cmp r2, r3
ldrls r1, [r2]
sample_done:
str r1, [sp, #72]
mov r1, #1
str r1, [sp, #76]
ldr r7, [r6, #8]
ldr r8, record_address
mov r9, #0
record_loop:
cmp r9, r7
bhs new_record
mov r10, #0
word_loop:
ldr r11, [sp, r10]
ldr r12, [r8, r10]
cmp r11, r12
bne next_record
add r10, r10, #4
cmp r10, #76
blo word_loop
ldr r11, [r8, #76]
add r11, r11, #1
str r11, [r8, #76]
b finish
next_record:
add r8, r8, #80
add r9, r9, #1
b record_loop
new_record:
cmp r7, #{CAPACITY}
bhs overflow
mov r10, #0
copy_loop:
ldr r11, [sp, r10]
str r11, [r8, r10]
add r10, r10, #4
cmp r10, #80
blo copy_loop
add r7, r7, #1
str r7, [r6, #8]
b finish
overflow:
ldr r7, [r6, #12]
add r7, r7, #1
str r7, [r6, #12]
finish:
ldr r4, [sp]
add sp, sp, #80
cmp r4, #0
bne tile_restore
pop {{r4, r5}}
msr cpsr_f, r4
pop {{r0-r12, lr}}
push {{r4-r9, lr}}
b {CORNER + 4:#x}
tile_restore:
pop {{r4, r5}}
msr cpsr_f, r4
pop {{r0-r12, lr}}
push {{r4-r11, lr}}
b {TILE + 4:#x}
control_address: .word {CONTROL}
record_address: .word {RECORDS}
main_start: .word 0x02000000
main_limit: .word 0x02400000
adapter_return0: .word 0x020CFDE0
adapter_return1: .word 0x020CFE5C
"""
    body = bytes(Ks(KS_ARCH_ARM, KS_MODE_ARM).asm(assembly, ENTRY)[0])
    assert len(body) < CONTROL - ENTRY
    assert RECORDS + STRIDE * CAPACITY <= END
    return body


def main():
    assert sha(SOURCE.read_bytes()) == "1c72049ca2eba551825d67de2429b4ac9751179183afc2ddb5749666d398eba5"
    root = NdsImage.open(SOURCE)
    arm = root.read_file("/__arm9__.bin")
    code = MainCodeFile(arm, 0x02000000)
    before = MainCodeFile(arm, 0x02000000)
    assert len(code.sections) == 5
    assert all(not (s.ramAddress < END and ENTRY < s.ramAddress + len(s.data) + s.bssSize) for s in code.sections)
    overlay = loadOverlayTable(root.rom.arm9OverlayTable, lambda _id, fid: root.rom.files[fid])[0]
    assert overlay.ramAddress == 0x01FFA000 and len(overlay.data) == 6208 and overlay.flags == 0
    tile = bytearray(overlay.data)
    clean = NdsImage.open("work/clean.nds")
    clean_overlay = loadOverlayTable(clean.rom.arm9OverlayTable, lambda _id, fid: clean.rom.files[fid])[0]
    assert tile == clean_overlay.data
    section = next(s for s in code.sections if s.ramAddress <= CORNER < s.ramAddress + len(s.data))
    at = CORNER - section.ramAddress
    assert section.data[at:at + 4] == bytes.fromhex("f0432de9")
    assert tile[TILE - overlay.ramAddress:TILE - overlay.ramAddress + 4] == bytes.fromhex("f04f2de9")
    body = build_body()
    payload = bytearray(END - ENTRY)
    payload[:len(body)] = body
    struct.pack_into("<I", payload, CONTROL - ENTRY + 20, 0x603B117)
    code.sections.append(MainCodeFile.Section(payload, ENTRY, 0))
    struct.pack_into("<I", section.data, at, branch_link(CORNER, ENTRY) & ~0x01000000)
    struct.pack_into("<I", tile, TILE - overlay.ramAddress, branch_link(TILE, TILE_ENTRY) & ~0x01000000)
    revised = bytes(code.save())
    restored = MainCodeFile(revised, 0x02000000)
    for index, old in enumerate(before.sections):
        new = bytearray(restored.sections[index].data)
        if old.ramAddress == section.ramAddress:
            new[at:at + 4] = old.data[at:at + 4]
        if index == 0:
            settings = code.codeSettingsOffs
            new[settings:settings + 12] = old.data[settings:settings + 12]
        assert bytes(new) == bytes(old.data)
    root.replace_file("/__arm9__.bin", revised)
    root.rom.files[overlay.fileID] = bytes(tile)
    ROOT.mkdir(parents=True, exist_ok=True)
    target = ROOT / "current_blitter_trace_RESEARCH_ONLY.nds"
    root.save(target)
    saved = NdsImage.open(target)
    original = NdsImage.open(SOURCE)
    files = {p: b for _, p, b in saved.iter_files()} | dict(saved.iter_components())
    old_files = {p: b for _, p, b in original.iter_files()} | dict(original.iter_components())
    changed = sorted(p for p in files if files[p] != old_files[p])
    assert changed == ["/__arm9__.bin", "/__unnamed__/file_00000.bin"]
    assert saved.rom.arm9OverlayTable == original.rom.arm9OverlayTable
    manifest = {"research_only": True, "production_ROM": str(SOURCE), "production_ROM_sha256": sha(SOURCE.read_bytes()),
        "research_ROM": str(target), "research_ROM_sha256": sha(target.read_bytes()),
        "changed_components": changed, "new_autoload_section": [ENTRY, END], "helper_body_bytes": len(body),
        "corner_hook": CORNER, "tile_hook": TILE, "tile_entry": TILE_ENTRY,
        "control": CONTROL, "records": RECORDS, "capacity": CAPACITY, "record_stride": STRIDE, "fields": FIELDS,
        "selection": "4bit48x20 Confirm or16/24/32/48x8;256/512x256 atlas source intersects miniature band;one atlas positive per routine",
        "negative_evidence_scope": "Only sampled calls through these two routines; overflow is explicit. Not global nonuse.",
        "resources_getters_crops_palettes_and_original_drawing_not_substituted": True,
        "instrumentation_can_change_timing": True, "ordinary_guide_credit": False,
        "script_sha256": sha(Path(__file__).read_bytes()), "production_changed": False, "goal_complete": False}
    (ROOT / "fixture_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"V603 research trace prepared: {len(body)} byte helper, {CAPACITY} records; production unchanged.")


if __name__ == "__main__":
    main()
