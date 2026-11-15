"""Reproduce the source-locked Charlotte actor-byte/body-pointer proof."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R5

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine


def main():
    path = Path("out/all_routes_combined_v275_candidate.nds")
    assert sha(path.read_bytes()) == "94fa82c8edd99de4f21829bc94b1b98013929f98cc1378c73fe0768e1d1caddf"
    arm = NdsImage.open(path).read_file("/__arm9__.bin")
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    assert arm[0x29B18:0x29B30] == clean[0x29B18:0x29B30]
    assert arm[0x2434C:0x24360] == clean[0x2434C:0x24360]
    cpu = machine(arm)
    obj = 0x02460000
    cpu.mem_write(obj, bytes(4) + struct.pack("<H", 0x5000) + b"Rafael... Mine is Charlotte.\0")
    cpu.reg_write(UC_ARM_REG_R5, obj)
    cpu.emu_start(0x02029B18, 0x0202425C, count=20)
    assert cpu.reg_read(UC_ARM_REG_PC) == 0x0202425C
    assert cpu.reg_read(UC_ARM_REG_R0) == 0x50 and cpu.reg_read(UC_ARM_REG_R1) == obj + 6
    call(cpu, 0x2434C, (0x50,))
    assert cpu.reg_read(UC_ARM_REG_R0) == 0x50
    pointer = struct.unpack_from("<I", arm, 0x120B80 + 80 * 32)[0]
    original = struct.unpack_from("<I", clean, 0x120B80 + 80 * 32)[0]
    assert arm[pointer - 0x02000000:].split(b"\0", 1)[0] == b"Charlotte"
    assert clean[original - 0x02000000:].split(b"\0", 1)[0].decode("cp932") == "シャルロット"
    proof = {"format": "dk4-charlotte-printable-presentation-state-v279",
             "native_caller_window": "02029B18..02029B2C", "native_character_selector": "0202434C",
             "presentation_byte": 80, "source_name": "シャルロット", "native_English_name": "Charlotte",
             "actor_argument": 80, "body_pointer_skips_the_metadata_high_byte": True,
             "original_clean_and_current_parser_code_identical": True,
             "scope": "Original native caller argument setup and selector/table proof; original deep scene traversal still pending."}
    out = Path("work/analysis/fixed_names_v279/charlotte_50_native_parser_proof.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    # Preserve the exact Windows serialization pinned by the scoped mapping.
    data = (json.dumps(proof, ensure_ascii=False, indent=2) + "\n").replace("\n", "\r\n").encode("utf-8")
    if out.exists():
        assert out.read_bytes() == data
    out.write_bytes(data)
    print("Native Charlotte actor80/body separation proof reproduced exactly.")


if __name__ == "__main__":
    main()
