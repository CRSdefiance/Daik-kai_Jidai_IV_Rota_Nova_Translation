"""Trace actual synthetic-header palette/canvas provenance without raw-display claims."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R10

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine

ROM = Path("out/all_routes_combined_v546_candidate.nds")
ROOT = Path("work/analysis/legacy_descriptor_v547")
CAPTURE = Path("E:/Rota Nova translations/Generated/work/emulation_v193/legacy_descriptor_v547")
BASE = 0x02000000


def words(raw, address):
    return struct.unpack_from("<5I", raw, address - BASE)


def descriptor(raw, address):
    value = words(raw, address)
    return {"address": address, "words": list(value), "format": value[0],
            "palette_pointer": (address + value[3]) & 0xFFFFFFFF,
            "pixels_pointer": (address + value[4]) & 0xFFFFFFFF}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open(ROM), NdsImage.open("work/clean.nds")
    digest = sha(ROM.read_bytes())
    assert digest == "499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3"
    run = json.loads((CAPTURE / "capture_report.json").read_text(encoding="utf-8"))
    assert run["ROM_sha256"] == digest and run["cold_boot"] and not run["savestate_loaded"]
    assert not run["callback_errors"] and not run.get("battery_save_preloaded")
    raw_path = CAPTURE / "frame_002400_arm9_ram.bin"
    raw = raw_path.read_bytes()
    assert len(raw) == 0x400000
    arm, original = rom.read_file("/__arm9__.bin"), clean.read_file("/__arm9__.bin")
    ranges = [(0x10D5A8,0x10D5E8),(0x10DC24,0x10DCA0),(0x9ED40,0x9ED94)]
    assert all(arm[a:b] == original[a:b] for a,b in ranges)
    pattern = struct.pack("<3I",8,52,136)
    matches = [at for at in range(0,len(raw)-20,4) if raw[at:at+12] == pattern]
    assert len(matches) == 1
    address = BASE + matches[0]
    owner = address - 0x934
    captured = descriptor(raw,address)
    assert captured["palette_pointer"] == 0x02279938 and captured["pixels_pointer"] == 0x022A5774
    # Re-execute the actual constructor header fragment on the current captured
    # parent and globals. This proves the fragment, not the full UI constructor.
    u = machine(arm)
    u.mem_write(BASE,raw)
    u.mem_write(address,b"\xA5"*20)
    u.mem_write(address,raw[matches[0]:matches[0]+4])
    before = bytes(u.mem_read(BASE,len(raw)))
    u.reg_write(UC_ARM_REG_R10,owner)
    u.emu_start(BASE+0x9ED40,BASE+0x9ED94,count=64)
    assert u.reg_read(UC_ARM_REG_PC) == BASE+0x9ED94
    after = bytes(u.mem_read(BASE,len(raw)))
    assert after[matches[0]:matches[0]+20] == raw[matches[0]:matches[0]+20]
    assert all(a == b for i,(a,b) in enumerate(zip(before,after))
               if not matches[0] <= i < matches[0]+20)
    # Complete original shared-canvas initializer: indexed8 and direct16 headers
    # share the exact same pixel storage; full native call/ABI executes.
    canvas8, canvas16 = 0x022A554C,0x022A5560
    u.mem_write(canvas8-16,b"\xA5"*72)
    u.mem_write(canvas8,raw[canvas8-BASE:canvas8-BASE+4])
    u.mem_write(canvas16,raw[canvas16-BASE:canvas16-BASE+4])
    call(u,0x10DC24,())
    assert bytes(u.mem_read(canvas8-16,16)) == b"\xA5"*16
    assert bytes(u.mem_read(canvas16+20,16)) == b"\xA5"*16
    headers = bytes(u.mem_read(canvas8,40))
    assert struct.unpack_from("<5I",headers) == words(raw,canvas8)
    d16 = struct.unpack_from("<5I",headers,20)
    assert d16[:3] == (16,256,192)
    assert (canvas16+d16[4])&0xFFFFFFFF == captured["pixels_pointer"]
    # Original palette-bearing face strip header setup ends before resource/UI
    # initialization. Do not infer a full initializer ABI from this fragment.
    u.mem_write(BASE,raw)
    u.mem_write(0x02279894,b"\xA5"*20)
    u.mem_write(0x02279894,raw[0x279894:0x279898])
    before = bytes(u.mem_read(BASE,len(raw)))
    u.emu_start(BASE+0x10D5A8,BASE+0x10D5E8,count=32)
    assert u.reg_read(UC_ARM_REG_PC) == BASE+0x10D5E8
    after = bytes(u.mem_read(BASE,len(raw)))
    offset = 0x02279894-BASE
    assert after[offset:offset+20] == raw[offset:offset+20]
    assert all(a == b for i,(a,b) in enumerate(zip(before,after)) if not offset <= i < offset+20)
    palette_at = captured["palette_pointer"]-BASE
    palette = struct.unpack_from("<256H",raw,palette_at)
    native_data = rom.read_file("/GRP/CMMNIMG.000")
    native = struct.unpack_from("<256H",native_data)
    assert [v&0x7FFF for v in palette] == [v&0x7FFF for v in native]
    differences = sum(a != b for a,b in zip(palette,native))
    legacy = IlnkContainer.parse(rom.read_file("/GRP/CMMNIMG.DK4")).blocks[0]
    legacy_palette = struct.unpack_from("<256H",legacy)
    assert [v&0x7FFF for v in palette] != [v&0x7FFF for v in legacy_palette]
    slack = IlnkContainer.parse(rom.read_file("/GRP/SLACKIMG.DK4")).blocks
    raw_buffer = struct.unpack_from("<I",arm,0x9F0B4)[0]
    assert raw_buffer == 0x02233040 and raw_buffer != captured["pixels_pointer"]
    assert raw[raw_buffer-BASE:raw_buffer-BASE+14144] == slack[17]
    assert raw[captured["pixels_pointer"]-BASE:captured["pixels_pointer"]-BASE+14144] != slack[17]
    proof = {"candidate":str(ROM),"candidate_sha256":digest,"ROM_changed":False,
             "current_cold_boot_report":str(CAPTURE/"capture_report.json"),
             "snapshot":str(raw_path),"snapshot_sha256":sha(raw),
             "original_code_ranges_exact":ranges,"actual_controller":owner,
             "captured_synthetic_header":captured,"constructor_header_fragment_reproduced_exact":True,
             "all_other_parent_RAM_bytes_unchanged_by_fragment":True,
             "original_shared_canvas_initializer_full_return_stack_and_saved_register_ABI":True,
             "shared_canvas8_header":descriptor(raw,canvas8),"shared_canvas16_header_words":list(d16),
             "indexed8_and_direct16_views_share_pixel_storage":True,
             "face_strip_header_fragment_reproduced_exact":True,
             "face_strip_header":descriptor(raw,0x02279894),
             "all256_palette_lower15_colours_match_native_CMMNIMG_000":True,
             "palette_words_with_high_bit_changes":differences,
             "palette_alpha_semantics_not_proven_by_normalization":True,
             "legacy_CMMNIMG_DK4_palette_not_equivalent":True,
             "raw_SLACK17_buffer_byte_exact":True,"raw_buffer_address":raw_buffer,
             "raw_buffer_does_not_supply_this_synthetic_header_pixels":True,
             "full_controller_other_users_raw_palette_or_comic19_GPU_usage_not_proven":True,
             "all22_requirements_and18_incomplete_entries_retained":True,"full_goal_complete":False}
    (ROOT/"descriptor_proof.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
    print("V547: actual descriptor, shared8/16 canvas, native256-colour provenance and separate raw buffer verified; ROM unchanged.")


if __name__ == "__main__":
    main()
