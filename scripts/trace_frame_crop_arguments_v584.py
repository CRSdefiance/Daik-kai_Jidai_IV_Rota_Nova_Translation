"""Conservative basic-block crop argument census; no ordinary caller credit."""

import json
import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG
from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path("work/analysis/frame_callers_v584")
ROM = Path("out/all_routes_combined_v581_candidate.nds")
OWNER = 0x02313F60
TARGETS = {0x020D3B34: "view_setter", 0x020D3D30: "view_constructor", 0x020D6558: "resource_getter"}


def branch(word, address):
    if word & 0x0E000000 != 0x0A000000:
        return None
    offset = word & 0xFFFFFF
    if offset & 0x800000:
        offset -= 0x1000000
    return address + 8 + offset * 4


def transfer(word):
    return (word & 0x0E000000 == 0x0A000000 or word & 0x0FFFFFF0 in (0x012FFF10, 0x012FFF30)
            or word & 0x0FFF8000 == 0x08BD8000)


def abstract_block(decoder, data, base, start, end):
    registers, stack = {}, {}
    registers["sp"] = 0x70000000
    instructions = list(decoder.disasm(data[start:end], base + start))

    def value(ins, operand, registers=registers):
        if operand.type == ARM_OP_IMM:
            return operand.imm & 0xFFFFFFFF
        if operand.type != ARM_OP_REG:
            return None
        name = ins.reg_name(operand.reg)
        result = registers.get(name)
        if operand.shift.type:
            if result is None or operand.shift.type != 2:
                return None
            result <<= operand.shift.value
        return result & 0xFFFFFFFF if result is not None else None

    for ins in instructions:
        if ins.id == 0:
            continue
        operands = ins.operands
        condition = int.from_bytes(ins.bytes, "little") >> 28
        if condition != 14:
            for register in ins.regs_access()[1]:
                registers[ins.reg_name(register)] = None
            if ins.mnemonic.startswith("str"):
                stack.clear()
            continue
        if ins.mnemonic == "push":
            if registers["sp"] is not None:
                registers["sp"] -= 4 * len(operands)
            continue
        if ins.mnemonic == "str" and operands[1].type == ARM_OP_MEM:
            mem = operands[1].mem
            if ins.reg_name(mem.base) == "sp" and not mem.index:
                if registers["sp"] is None:
                    stack.clear()
                else:
                    stack[registers["sp"] + mem.disp] = value(ins, operands[0])
            continue
        if ins.mnemonic == "ldr" and operands[1].type == ARM_OP_MEM:
            mem = operands[1].mem
            name = ins.reg_name(mem.base)
            result = None
            if not mem.index and name == "pc":
                source = ins.address + 8 + mem.disp - base
                if 0 <= source <= len(data) - 4:
                    result = struct.unpack_from("<I", data, source)[0]
            elif not mem.index and name == "sp" and registers["sp"] is not None:
                result = stack.get(registers["sp"] + mem.disp)
            registers[ins.reg_name(operands[0].reg)] = result
            continue
        if ins.mnemonic in ("mov", "mvn", "add", "sub"):
            args = [value(ins, op) for op in operands[1:]]
            result = None
            if all(v is not None for v in args):
                result = (args[0] if ins.mnemonic == "mov" else ~args[0] if ins.mnemonic == "mvn"
                          else args[0] + args[1] if ins.mnemonic == "add" else args[0] - args[1]) & 0xFFFFFFFF
            registers[ins.reg_name(operands[0].reg)] = result
            continue
        for register in ins.regs_access()[1]:
            name = ins.reg_name(register)
            if name not in ("pc", "cpsr"):
                registers[name] = None
    return registers, stack


def main():
    rom = NdsImage.open(ROM)
    arm = rom.read_file("/__arm9__.bin")
    sections = [(f"main{i}", s.ramAddress, bytes(s.data)) for i, s in enumerate(MainCodeFile(arm, 0x02000000).sections)]
    sections += [(f"overlay{i}", o.ramAddress, bytes(o.data)) for i, o in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _id, file_id: rom.rom.files[file_id]).items()]
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    decoder.skipdata = True
    captions = [("Pick Cargo", (208, 32, 256, 40)), ("Pick Ship", (208, 40, 240, 48)),
                ("Done", (240, 40, 256, 48)), ("Rank", (184, 48, 208, 56)), ("Cancel", (208, 48, 256, 56))]
    cases = []
    for label, base, data in sections:
        for at in range(0, len(data) - 3, 4):
            word = struct.unpack_from("<I", data, at)[0]
            if word & 0x0F7F0000 != 0x051F0000:
                continue
            literal = at + 8 + (word & 4095) * (1 if word & 0x800000 else -1)
            if not (0 <= literal <= len(data) - 4 and struct.unpack_from("<I", data, literal)[0] == OWNER):
                continue
            end = None
            for offset in range(at + 4, min(len(data) - 3, at + 260), 4):
                target = branch(struct.unpack_from("<I", data, offset)[0], base + offset)
                if target in TARGETS:
                    end = offset
                    break
                if transfer(struct.unpack_from("<I", data, offset)[0]):
                    break
            if end is None:
                cases.append({"owner_load": base + at, "unit": label, "kind": "initialization_or_unresolved_control_transfer"})
                continue
            start = max(0, at - 160)
            for offset in range(start, at, 4):
                if transfer(struct.unpack_from("<I", data, offset)[0]):
                    start = offset + 4
            registers, stack = abstract_block(decoder, data, base, start, end)
            target = branch(struct.unpack_from("<I", data, end)[0], base + end)
            case = {"owner_load": base + at, "unit": label, "call": base + end, "target": target,
                    "kind": TARGETS[target], "block_start": base + start,
                    "block_sha256": sha(data[start:end + 4]),
                    "abstract_registers": {k: registers.get(k) for k in ("r0", "r1", "r2", "r3")}}
            if target != 0x020D6558:
                sp = registers["sp"]
                args = [registers.get("r2"), registers.get("r3"), stack.get(sp), stack.get(sp + 4) if sp is not None else None]
                case["source_XYWH"] = args
                case["palette"] = stack.get(sp + 8) if sp is not None else None
                case["flags"] = stack.get(sp + 12) if sp is not None else None
                case["owner_argument_proven"] = registers.get("r1") == OWNER
                if all(v is not None for v in args) and case["owner_argument_proven"]:
                    x, y, width, height = args
                    case["intersecting_caption_cells"] = [name for name, (l, t, r, b) in captions
                                                         if x < r and y < b and x + width > l and y + height > t]
                    case["geometry_statically_resolved"] = True
                else:
                    case["geometry_statically_resolved"] = False
            cases.append(case)
    result = {"candidate": str(ROM), "candidate_sha256": sha(ROM.read_bytes()), "ARM9_sha256": sha(arm),
              "method": "AL basic-block constant propagation; unknown state reads/conditions remain unknown",
              "all_loaded_main_sections_and_declared_overlay_scanned": True,
              "owner_load_cases": cases, "no_ROM_changes": True,
              "dynamic_arguments_and_indirect_owners_not_excluded": True,
              "ordinary_native_caption_context_not_proven_by_this_analysis": True}
    (ROOT / "crop_argument_census.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print({"owner_loads": len(cases), "resolved_views": sum(c.get("geometry_statically_resolved", False) for c in cases),
           "unresolved_views": [hex(c["call"]) for c in cases if c.get("geometry_statically_resolved") is False],
           "caption_intersections": [c for c in cases if c.get("intersecting_caption_cells")]})


if __name__ == "__main__":
    main()
