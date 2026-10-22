"""Check six earlier source-row definitions and their original control flow."""

import json
from collections import deque
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.trace_frame_crop_arguments_v584 import branch

ROOT = Path("work/analysis/frame_callers_v584")
# entry, source MOV, source STR, source-row stack offset, constructor call, row
CASES = [
    (0x0208C968, 0x0208E360, 0x0208E374, 0x68, 0x0208E410, 224),
    (0x020A21AC, 0x020A2860, 0x020A2864, 0x3C, 0x020A28BC, 224),
    (0x020A6ED8, 0x020A7654, 0x020A7658, 0x44, 0x020A76B0, 224),
    (0x020C0FE4, 0x020C162C, 0x020C164C, 0x64, 0x020C175C, 216),
    (0x020C3274, 0x020C340C, 0x020C3410, 0x54, 0x020C356C, 216),
    (0x020C37B0, 0x020C38DC, 0x020C38E0, 0x4C, 0x020C3A7C, 216),
]


def main():
    current = NdsImage.open("out/all_routes_combined_v581_candidate.nds")
    clean = NdsImage.open("work/clean.nds")
    u, original = (machine(r.read_file("/__arm9__.bin")) for r in (current, clean))
    u.mem_write(POOL, bytes(MainCodeFile(current.read_file("/__arm9__.bin"), BASE).sections[3].data[:-48]))
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    records = []
    for entry, mov, store, slot, target, row in CASES:
        end = target + 4
        for address in range(target + 4, target + 0x2000, 4):
            word = int.from_bytes(u.mem_read(address, 4), "little")
            if word & 0xFFFF4000 == 0xE92D4000:
                end = address
                break
        source = bytes(u.mem_read(entry, end - entry))
        original_source = bytes(original.mem_read(entry, end - entry))
        differences = [entry + at for at in range(0, len(source), 4)
                       if source[at:at + 4] != original_source[at:at + 4]]
        literal_changes = []
        if entry == 0x0208C968:
            assert differences == [0x0208D7A8, 0x0208D848, 0x0208E56C]
            for address, source_text, english in ((0x0208D7A8, "艦隊・村", "Fleet/Village"),
                                                 (0x0208D848, "品不足", "Shortage"),
                                                 (0x0208E56C, "%s提督", "%s Admiral")):
                texts = []
                for uc in (original, u):
                    pointer = int.from_bytes(uc.mem_read(address, 4), "little")
                    texts.append(bytes(uc.mem_read(pointer, 128)).split(b"\0")[0].decode("cp932"))
                assert texts == [source_text, english]
                literal_changes.append({"address": address, "Japanese": source_text, "inherited_English": english})
        else:
            assert not differences
        instructions = {i.address: i for address in range(entry, end, 4)
                        for i in decoder.disasm(bytes(u.mem_read(address, 4)), address)}
        mov_ins, store_ins = instructions[mov], instructions[store]
        assert mov_ins.mnemonic == "mov" and mov_ins.op_str == f"r0, #{hex(row)}"
        assert store_ins.mnemonic == "str" and store_ins.op_str == f"r0, [sp, #{hex(slot)}]"
        assert all(not any(i.reg_name(reg) == "r0" for reg in i.regs_access()[1])
                   for address, i in instructions.items() if mov < address < store)
        # Direct stack slot writes elsewhere in the source function are retained
        # explicitly; no arbitrary state-memory read is promoted to a constant.
        writes = [address for address, i in instructions.items() if i.mnemonic.startswith("str")
                  and f"[sp, #{hex(slot)}]" in i.op_str]
        assert writes == [store], (hex(target), writes)
        unresolved = set()
        jump_tables = {}

        def edges(address, instructions=instructions, jump_tables=jump_tables,
                  unresolved=unresolved, entry=entry, end=end):
            ins = instructions.get(address)
            if ins is None:
                if entry <= address < end:
                    unresolved.add(address)
                return []
            word = int.from_bytes(ins.bytes, "little")
            condition = word >> 28
            destination = branch(word, address)
            if destination is not None:
                if word & 0x01000000:  # call: normal preserved-stack ABI return
                    return [address + 4]
                return [destination] + ([address + 4] if condition != 14 else [])
            if ins.mnemonic.startswith("blx"):
                return [address + 4]
            if ins.mnemonic.startswith("bx") or (ins.mnemonic.startswith(("pop", "ldm")) and "pc" in ins.op_str):
                return [address + 4] if condition != 14 else []
            if any(ins.reg_name(reg) == "pc" for reg in ins.regs_access()[1]):
                if ins.mnemonic.startswith("add") and ins.op_str.startswith("pc, pc,") and "lsl #2" in ins.op_str:
                    targets = []
                    for index in range(64):
                        at = address + 8 + index * 4
                        candidate = int.from_bytes(u.mem_read(at, 4), "little")
                        dest = branch(candidate, at)
                        if dest is None or candidate >> 28 != 14 or candidate & 0x01000000:
                            break
                        targets.append(at)
                    assert targets
                    jump_tables[address] = targets
                    return targets + ([address + 4] if condition != 14 else [])
                unresolved.add(address)
                return []
            return [address + 4]

        def reachable(blocked, entry=entry, end=end, target=target, edges=edges):
            seen, pending = set(), deque([entry])
            while pending:
                address = pending.popleft()
                if address == blocked or address in seen or not entry <= address < end:
                    continue
                seen.add(address)
                if address != target:
                    pending.extend(edges(address))
            return target in seen, seen

        full, visited = reachable(None)
        assert full and not unresolved, (hex(target), unresolved)
        assert not set(differences) & visited
        without_store, _ = reachable(store)
        assert not without_store and not unresolved, hex(target)
        records.append({"function_entry": entry, "function_end": end,
                        "complete_region_sha256": sha(source), "clean_region_sha256": sha(original_source),
                        "all_reachable_instructions_exact_clean": True,
                        "nonexecuted_inherited_localized_text_pointer_differences": literal_changes,
                        "source_mov": mov, "source_store": store, "source_row": row,
                        "stack_slot": slot, "constructor_call": target,
                        "source_store_dominates_constructor_in_checked_original_CFG": True,
                        "only_direct_store_to_source_row_slot": writes,
                        "computed_branch_tables": jump_tables,
                        "normal_call_stack_ABI_and_no_aliased_slot_write_are_assumptions": True,
                        "ordinary_live_consumer_or_global_nonuse_not_claimed": True})
    result = {"candidate_sha256": sha(Path("out/all_routes_combined_v581_candidate.nds").read_bytes()),
              "six_original_row_definitions": records, "all_six_source_rows_outside_caption_band": True,
              "source_row_band": [32, 56], "no_ROM_changes": True,
              "direct_blit_style_arguments_and_other_aliases_remain_open": True}
    (ROOT / "original_source_row_proof.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print("Six original stack row definitions dominate their constructors; source rows224/216, outside miniature band32..55.")


if __name__ == "__main__":
    main()
