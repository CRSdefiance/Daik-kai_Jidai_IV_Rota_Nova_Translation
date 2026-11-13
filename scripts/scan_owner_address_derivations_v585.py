"""Bounded straight-line constant/address candidates, not whole-program reachability."""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.trace_frame_crop_arguments_v584 import transfer

ROOT = Path("work/analysis/resource_owners_v585")
TARGETS = {"frame": (0x02313F60, 0x02313F74), "Confirm": (0x023139C0, 0x023139D4)}


def main():
    rom = NdsImage.open("out/all_routes_combined_v581_candidate.nds")
    arm = rom.read_file("/__arm9__.bin")
    sections = [(f"main{i}", s.ramAddress, bytes(s.data)) for i, s in enumerate(MainCodeFile(arm, 0x02000000).sections)]
    sections += [(f"overlay{i}", o.ramAddress, bytes(o.data)) for i, o in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _id, file_id: rom.rom.files[file_id]).items()]
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail, decoder.skipdata = True, True
    candidates, totals = [], {}
    for label, base, data in sections:
        registers, count = {}, 0
        for ins in decoder.disasm(data, base):
            count += 1
            if ins.id == 0:
                registers.clear()
                continue
            operands = ins.operands
            registers["pc"] = ins.address + 8

            def value(op, ins=ins, registers=registers):
                if op.type == ARM_OP_IMM:
                    return op.imm & 0xFFFFFFFF
                if op.type != ARM_OP_REG:
                    return None
                val = registers.get(ins.reg_name(op.reg))
                if op.shift.type:
                    if val is None or op.shift.type not in (2, 3):
                        return None
                    val = val << op.shift.value if op.shift.type == 2 else val >> op.shift.value
                return val & 0xFFFFFFFF if val is not None else None

            destination, result = None, None
            if int.from_bytes(ins.bytes, "little") >> 28 == 14 and operands:
                if operands[0].type == ARM_OP_REG:
                    destination = ins.reg_name(operands[0].reg)
                if ins.mnemonic in ("mov", "mvn", "add", "sub", "rsb", "orr", "and", "eor", "bic", "lsl", "lsr"):
                    args = [value(op) for op in operands[1:]]
                    if args and all(v is not None for v in args):
                        a, b = args[0], args[1] if len(args) > 1 else 0
                        operations = {"mov": a, "mvn": ~a, "add": a + b,
                                      "sub": a - b, "rsb": b - a,
                                      "orr": a | b, "and": a & b,
                                      "eor": a ^ b, "bic": a & ~b,
                                      "lsl": a << min(b, 32), "lsr": a >> min(b, 32)}
                        result = operations[ins.mnemonic] & 0xFFFFFFFF
                elif ins.mnemonic == "ldr" and len(operands) == 2 and operands[1].type == ARM_OP_MEM:
                    mem = operands[1].mem
                    if ins.reg_name(mem.base) == "pc" and not mem.index:
                        offset = ins.address + 8 + mem.disp - base
                        if 0 <= offset <= len(data) - 4:
                            result = struct.unpack_from("<I", data, offset)[0]
                # A base-plus-offset access can touch an owner without ever
                # constructing the exact owner base in a register.
                for op in operands:
                    if op.type != ARM_OP_MEM or ins.reg_name(op.mem.base) == "pc":
                        continue
                    address = registers.get(ins.reg_name(op.mem.base))
                    if address is None or op.mem.index:
                        continue
                    address = (address + op.mem.disp) & 0xFFFFFFFF
                    for target, (lo, hi) in TARGETS.items():
                        if lo <= address < hi:
                            candidates.append({"unit": label, "instruction": ins.address,
                                               "assembly": ins.mnemonic + " " + ins.op_str,
                                               "target": target, "kind": "constant_base_memory_operand",
                                               "address": address})
            for reg in ins.regs_access()[1]:
                registers[ins.reg_name(reg)] = None
            if destination:
                registers[destination] = result
                if result is not None and ins.mnemonic != "ldr":
                    for target, (lo, hi) in TARGETS.items():
                        if lo <= result < hi:
                            candidates.append({"unit": label, "instruction": ins.address,
                                               "assembly": ins.mnemonic + " " + ins.op_str,
                                               "target": target, "kind": "arithmetic_or_register_copy",
                                               "address": result})
            if transfer(int.from_bytes(ins.bytes, "little")):
                registers.clear()
        totals[label] = count
    assert [r["instruction"] for r in candidates] == [
        0x02085460, 0x0210E1D4, 0x0210E1D8, 0x0210E1DC,
        0x0210EBF0, 0x0210EBF4, 0x0210EBF8]
    previous_path = Path("work/analysis/frame_callers_v584/crop_argument_census.json")
    previous = json.loads(previous_path.read_text(encoding="utf-8"))
    known = next(r for r in previous["owner_load_cases"] if r["owner_load"] == 0x02085434)
    assert known["call"] == 0x02085470 and known["source_XYWH"] == [80, 216, 8, 8]
    result = {"candidate_sha256": sha(rom.source.read_bytes()),
              "script_sha256": sha(Path(__file__).read_bytes()), "decoded_slots_per_unit": totals,
              "targets": TARGETS, "candidates": candidates,
              "six_candidates_are_original_initializer_field_writes": True,
              "remaining_candidate_is_previously_bound_source_row216_view": known,
              "previous_crop_census_sha256": sha(previous_path.read_bytes()),
              "limits": ["ARM-aligned straight-line candidates include possible data; no reachability inference.",
                         "Every transfer clears all constants; values across calls/branches, Thumb, runtime reads, indexed loads and relative-pointer interpretation remain unknown.",
                         "Only AL arithmetic and immediate memory offsets are modeled; absence does not establish global non-use."],
              "no_ROM_changes": True, "ordinary_parent_context_not_proven": True}
    (ROOT / "address_derivation_candidates.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("V585 bounded owner-address candidates:", candidates)


if __name__ == "__main__":
    main()
