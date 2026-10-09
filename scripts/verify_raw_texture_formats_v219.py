"""Execute fixed and parameterized native 2F000 texture-format writes."""

import json
import struct
from pathlib import Path

from unicorn import UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import STACK, machine

ROOT = Path("work/analysis/raw_resource_v219")


def main():
    rom, clean = NdsImage.open("out/all_routes_combined_v218_candidate.nds"), NdsImage.open("work/clean.nds")
    arm = rom.read_file("/__arm9__.bin")
    original = clean.read_file("/__arm9__.bin")
    cases = []
    # The fixed fragment loads its own format and TEX_FORMAT register literals.
    # The dynamic fragment obtains the width exponent from an explicit preceding
    # stack fixture; sampling those exponents does not identify a record's parent.
    specs = [("fixed", 0x6C064, 0x6C074, None)]
    specs.extend(("dynamic", 0x6B6B8, 0x6B6CC, n) for n in range(6))
    for label, start, end, exponent in specs:
        assert arm[start:end] == original[start:end]
        u = machine(arm)
        u.mem_map(0x04000000, 0x10000)
        u.reg_write(UC_ARM_REG_SP, STACK)
        if exponent is not None:
            u.mem_write(STACK + 4, struct.pack("<I", exponent))
        writes = []
        h = u.hook_add(UC_HOOK_MEM_WRITE, lambda uc, access, addr, size, value, data, writes=writes:
                       writes.append({"address": addr, "bytes": size, "value": value}))
        u.emu_start(0x02000000 + start, 0x02000000 + end, count=20)
        u.hook_del(h)
        assert u.reg_read(UC_ARM_REG_PC) == 0x02000000 + end
        assert len(writes) == 1 and writes[0]["address"] == 0x040004A8
        value = writes[0]["value"]
        width, height = 8 << (value >> 20 & 7), 8 << (value >> 23 & 7)
        assert (value >> 26 & 7) == 3 and (value & 65535) * 8 == 0x2F000
        assert height == 256 and width == (256 if exponent is None else 8 << exponent)
        cases.append({"fragment": label, "code_span": [0x02000000 + start, 0x02000000 + end],
                      "preceding_width_exponent_fixture": exponent, "writes": writes,
                      "native_texture_dimensions": [width, height], "format": "16-color indexed / four bits per pixel",
                      "color_zero_transparent_flag": bool(value & 1 << 29),
                      "complete_native_register_fragment_executed": True})
    result = {"format": "dk4-raw-native-texture-format-proof-v1", "ROM_sha256": sha(rom.source.read_bytes()),
              "cases": cases, "record_to_parent_width_selection_not_inferred": True,
              "source_shape_coherence_is_separate_from_native_parent_identity": True,
              "GPU_projection_palette_selection_and_physical_alpha_not_executed": True,
              "hardware_field_reference": "https://github.com/devkitPro/libnds/blob/master/include/nds/arm9/videoGL.h",
              "ROM_modified": False, "full_goal_complete": False}
    (ROOT / "texture_format_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"native_register_cases": len(cases), "fixed_dimensions": [256, 256],
                      "dynamic_widths": [r["native_texture_dimensions"][0] for r in cases[1:]], "source_bit_depth": 4}))


if __name__ == "__main__":
    main()
