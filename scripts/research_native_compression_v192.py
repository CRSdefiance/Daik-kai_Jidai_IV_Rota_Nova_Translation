"""Decode unresolved streams through the actual IWRAM code; no ROM mutations."""

import hashlib
import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image
from unicorn import (
    UC_ARCH_ARM,
    UC_HOOK_MEM_READ,
    UC_HOOK_MEM_WRITE,
    UC_MEM_WRITE,
    UC_MODE_ARM,
    Uc,
    UcError,
)
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_SP,
)

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import bgr555
from dk4tool.rom.nds import NdsImage
from scripts.inventory_embedded_graphics_v151 import decode
from scripts.probe_button_prompt_native import SAVED

BASE = Path("out/raphael_natural_v2_accepted_base.nds")
CANDIDATE = Path("out/all_routes_combined_v189_candidate.nds")
ROOT = Path("work/qa/native_compression_v192")
REPORT = Path("work/analysis/native_compression_v192.json")
SOURCE, OUTPUT, CONTEXT = 0x03900010, 0x03080000, 0x03F00010
CAPACITY, STACK, STOP = 0x800000, 0x027F0000, 0x027E0000


def sha(data):
    return hashlib.sha256(data).hexdigest()


def native_decode(arm, data):
    machine = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    machine.mem_map(0x02000000, 0x800000)
    machine.mem_map(0x01FF0000, 0x10000)
    machine.mem_map(0x03000000, 0x1000000)
    for section in MainCodeFile(arm, 0x02000000).sections:
        machine.mem_write(section.ramAddress, bytes(section.data))
    machine.mem_write(SOURCE - 16, b"\xa5" * (len(data) + 32))
    machine.mem_write(SOURCE, data)
    machine.mem_write(OUTPUT - 16, b"\xa5" * (CAPACITY + 32))
    machine.mem_write(CONTEXT - 16, b"\xa5" * 48)
    source_high, output_high = SOURCE, OUTPUT

    def access(uc, kind, address, size, value, user):
        nonlocal source_high, output_high
        if SOURCE - 16 <= address < SOURCE + len(data) + 16:
            if kind == UC_MEM_WRITE or not SOURCE <= address < address + size <= SOURCE + len(data):
                raise ValueError("Native decoder crosses or writes its bounded input")
            source_high = max(source_high, address + size)
        if 0x03000000 <= address < SOURCE - 16:
            if not OUTPUT <= address < address + size <= OUTPUT + CAPACITY:
                raise ValueError("Native output/backreference crosses the controlled output buffer")
            if kind == UC_MEM_WRITE:
                output_high = max(output_high, address + size)

    read_hook = machine.hook_add(UC_HOOK_MEM_READ, access)
    write_hook = machine.hook_add(UC_HOOK_MEM_WRITE, access)
    saved = {register: 0xA5A51000 + index for index, register in enumerate(SAVED)}
    for register, value in saved.items():
        machine.reg_write(register, value)
    for register, value in ((UC_ARM_REG_R0, CONTEXT), (UC_ARM_REG_R1, OUTPUT), (UC_ARM_REG_R2, SOURCE), (UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP)):
        machine.reg_write(register, value)
    try:
        machine.emu_start(0x01FF8000, STOP, count=30_000_000)
    finally:
        machine.hook_del(read_hook)
        machine.hook_del(write_hook)
    assert machine.reg_read(UC_ARM_REG_PC) == STOP and machine.reg_read(UC_ARM_REG_SP) == STACK
    assert all(machine.reg_read(register) == value for register, value in saved.items())
    length = machine.reg_read(UC_ARM_REG_R0)
    assert 0 < length <= CAPACITY and output_high == OUTPUT + length
    assert bytes(machine.mem_read(OUTPUT - 16, 16)) == b"\xa5" * 16
    assert bytes(machine.mem_read(OUTPUT + length, 16)) == b"\xa5" * 16
    assert bytes(machine.mem_read(SOURCE - 16, 16)) == b"\xa5" * 16
    assert bytes(machine.mem_read(SOURCE + len(data), 16)) == b"\xa5" * 16
    assert bytes(machine.mem_read(CONTEXT - 16, 16)) == b"\xa5" * 16
    assert bytes(machine.mem_read(CONTEXT + 16, 16)) == b"\xa5" * 16
    return bytes(machine.mem_read(OUTPUT, length)), {"input_read_extent": source_high - SOURCE, "output_bytes": length, "complete_return_ABI_and_canaries": True}


def main():
    assert sha(BASE.read_bytes()) == "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
    assert sha(CANDIDATE.read_bytes()) == "0361d5ab8d08b2493c1dfd1bb495b1ffbe42126da51b4296771582c0ceae1e74"
    base, candidate = NdsImage.open(BASE), NdsImage.open(CANDIDATE)
    arm = candidate.read_file("/__arm9__.bin")
    sections = MainCodeFile(arm, 0x02000000).sections
    original_sections = MainCodeFile(base.read_file("/__arm9__.bin"), 0x02000000).sections
    code = next(section for section in sections if section.ramAddress == 0x01FF8000)
    original_code = bytes(next(section.data for section in original_sections if section.ramAddress == 0x01FF8000))
    # V189 appends earlier accepted renderer repair code to this section.
    # The entire original prefix, including the decoder, remains exact.
    assert len(original_code) >= 0x400 and bytes(code.data)[:len(original_code)] == original_code
    ROOT.mkdir(parents=True, exist_ok=True)
    rows = []
    for path, indices in (("/GRP/CHARA.DK4", (4, 5)), ("/GRP/CMMNIMG.DK4", (0, 2, 3, 7))):
        blocks = IlnkContainer.parse(base.read_file(path)).blocks
        saved_blocks = IlnkContainer.parse(candidate.read_file(path)).blocks
        for index in indices:
            raw = blocks[index]
            assert raw == saved_blocks[index]
            row = {"path": path, "block_index": index, "source_bytes": len(raw), "source_sha256": sha(raw), "candidate_block_unchanged": True}
            try:
                result, proof = native_decode(arm, raw)
                output = ROOT / f"{Path(path).stem}_{index}_decoded.bin"
                output.write_bytes(result)
                row.update(proof, decoded=str(output), decoded_sha256=sha(result), decoded_head_words=list(struct.unpack_from("<5I", result)), native_decompression_pass=True)
                decoded = decode(result)
                if decoded is not None:
                    colors = [bgr555(value) for value, in struct.iter_unpack("<H", decoded["palette"][:32 if decoded["depth"] == 4 else 512])]
                    image = Image.new("RGBA", (decoded["width"], decoded["height"]))
                    image.putdata([colors[value] for value in decoded["indices"]])
                    preview = ROOT / f"{Path(path).stem}_{index}.png"
                    image.save(preview)
                    row.update(decoded_storage_type="bounded-type16-image", dimensions=list(image.size), depth=decoded["depth"], palette_banks=decoded["palette_banks"], trailing_bytes=decoded["unclassified_trailing_bytes"], preview=str(preview), preview_sha256=sha(preview.read_bytes()), visual_review="pending")
                else:
                    row.update(decoded_storage_type="not-type16-image; further-structure-review-required")
                print(path, index, len(raw), "->", len(result), row["decoded_storage_type"], flush=True)
            except (ValueError, AssertionError, UcError, struct.error) as error:
                row.update(native_decompression_pass=False, error=str(error) or type(error).__name__)
                print(path, index, "REJECTED", row["error"], flush=True)
            rows.append(row)
    report = {"candidate_sha256": sha(CANDIDATE.read_bytes()), "native_decoder_address": 0x01FF8000, "native_IWRAM_sha256": sha(bytes(code.data)), "canonical_IWRAM_prefix_bytes": len(original_code), "canonical_IWRAM_prefix_sha256": sha(original_code), "native_decoder_code_identical_to_canonical": True, "results": rows, "hardware_GPU_input_gameplay_verified": False, "rom_changed": False, "limits": ["Decoder executes actual loaded IWRAM ARM code in controlled buffers; allocation/hardware/parent rendering are not proved.", "Only accepted bounded decoder results can support subsequent source inspection; rejected interpretations are not adopted."]}
    REPORT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
