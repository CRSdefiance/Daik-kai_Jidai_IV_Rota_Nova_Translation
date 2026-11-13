"""Execute all three ordinary name accessors for the confirmed five field changes."""

import json
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.confirmed_character_names import BASE, FIELDS, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.execute_map_entity_tooltip_copy import STACK, STOP
from scripts.verify_ordinary_name_fidelity_research import initialized


def accessor(raw, machine, index, address):
    # The established harness invokes the real ordinary constructor and given
    # getter first; the other methods use the same native row-selection chain.
    ordinary_getter(raw, index, machine)
    root = struct.unpack_from("<I", raw, 0xCB18C)[0]
    machine.reg_write(UC_ARM_REG_LR, STOP)
    machine.reg_write(UC_ARM_REG_SP, STACK)
    machine.reg_write(UC_ARM_REG_R0, root + 4 + index * 32)
    machine.emu_start(BASE + address, STOP, count=1000)
    if machine.reg_read(UC_ARM_REG_PC) != STOP or machine.reg_read(UC_ARM_REG_SP) != STACK:
        raise ValueError("Actual name accessor did not return with its stack intact")
    pointer = machine.reg_read(UC_ARM_REG_R0)
    value = bytes(machine.mem_read(pointer, 128)).split(b"\0", 1)[0] if pointer else b""
    return pointer, value


def main():
    image = NdsImage.open("out/all_routes_combined_v190_candidate.nds")
    source = image.read_file("/__arm9__.bin")
    clean = NdsImage.open("work/clean.nds").read_file("/__arm9__.bin")
    saved, plan = transform(source, clean)
    before, after = initialized(source), initialized(saved)
    expected = {(row[1], row[2]): row[-1].encode("ascii") for row in FIELDS}
    cases = []
    for index in range(207):
        for column, address in ((0, 0x7EB0C), (4, 0x7EAF4), (8, 0x7EADC)):
            old_pointer, original = accessor(source, before, index, address)
            pointer, value = accessor(saved, after, index, address)
            if pointer != old_pointer or value != expected.get((index, column), original):
                raise ValueError(f"Unexpected native name field: {index}/{column}")
            cases.append({"index": index, "column": column, "accessor": BASE + address,
                          "pointer": pointer, "before_hex": original.hex(), "after_hex": value.hex(),
                          "before": original.decode("cp932", errors="backslashreplace"),
                          "after": value.decode("cp932", errors="backslashreplace")})
    root = Path("work/analysis/confirmed_names_v198")
    root.mkdir(parents=True, exist_ok=True)
    (root / "name_fields_research_only_arm9.bin").write_bytes(saved)
    report = {"format": "dk4-confirmed-name-fields-native-proof-v1", **plan,
              "candidate_source_sha256": sha(Path("out/all_routes_combined_v190_candidate.nds").read_bytes()),
              "native_accessor_selections": len(cases), "changed_field_outputs": len(expected),
              "unchanged_other_field_outputs": len(cases) - len(expected), "cases": cases,
              "boot_and_complete_staged_pool_copy_executed": True,
              "scope": "Native ordinary fixtures and real getter chains, not all captain/mutable-name consumers or GPU/live gameplay.",
              "playable_ROM_modified": False, "integratable_name_only_release": False}
    (root / "native_fields_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"selections": len(cases), "changed_outputs": len(expected),
                      "preserved_outputs": len(cases) - len(expected), "playable_ROM_modified": False}))


if __name__ == "__main__":
    main()
