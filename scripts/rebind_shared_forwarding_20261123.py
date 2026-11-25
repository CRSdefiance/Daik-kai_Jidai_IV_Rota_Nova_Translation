"""Rebind the bounded COMMON forwarding evidence to the Price Info candidate."""

from collections import Counter
from functools import lru_cache
from pathlib import Path
from struct import unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_INS_LDR, ARM_OP_MEM, ARM_REG_PC

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts import checkpoint_shared_upstream_ranges_20261115 as earlier
from scripts import register_price_info_descriptions_20261123 as active
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.seal_shared_text_source_v1 import reference as text_reference
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, digest, read, reference, write


BASE = earlier.BASE
ROOT = Path("translations/editorial_checkpoints/shared_display_20261123")
ARCHIVED = ROOT / "archived_message_operands_20261123.json"
OUTPUT = ROOT / "shared_forwarding_delta_20261123.json"
KEYS = (284, 318, 750, 751, 752)


def bounds(proof):
    if "candidate" in proof:
        window = proof["candidate"]
        return window["window_start"], window["window_end"]
    return proof["start"], proof["end"]


def static_results(old, now, rows):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = decoder.skipdata = True

    @lru_cache(maxsize=None)
    def dependencies(lo, hi):
        first, last = lo - BASE, hi - BASE
        literals = set()
        for ins in decoder.disasm(old[first:last], lo):
            if ins.id != ARM_INS_LDR:
                continue
            operand = ins.operands[-1]
            if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC and not operand.mem.index:
                offset = ins.address + 8 + operand.mem.disp - BASE
                if 0 <= offset <= len(old) - 4:
                    literals.add(offset)
        return old[first:last] == now[first:last], sorted(literals)

    results = []
    for row in rows:
        proof = row["proof"]
        if "receipt" in proof:
            continue
        lo, hi = bounds(proof)
        code_exact, literals = dependencies(lo, hi)
        changed_literals = [BASE + at for at in literals if old[at:at + 4] != now[at:at + 4]]
        tables = proof.get("typed_tables", [])
        old_addresses = [table["address"] for table in tables]
        changed_tables = [table["address"] for table in tables
                          if unpack_from(f"<{len(table['slots'])}i", now, table["address"] - BASE)
                          != tuple(table["slots"])]
        result = dict(address=row["address"], entry=row["entry"], window=[lo, hi],
                      prior_ids=row["ids"], prior_pc_relative_literals_checked=len(literals),
                      changed_literals=changed_literals, changed_tables=changed_tables, code_exact=code_exact)
        if code_exact and not changed_literals and not changed_tables:
            results.append(result | dict(status="reused exact dependencies", ids=row["ids"]))
            continue

        address, entry = row["address"], row["entry"]
        register, width = earlier.voice.NATIVE.get(entry, (earlier.ALL_TARGETS.get(entry), None))
        assert register in ("r0", "r1")
        if "candidate" in proof:
            flow = earlier.flow.window(now, address, register)
            values = flow["values"] if flow else None
        else:
            instructions = list(decoder.disasm(now[lo - BASE:address - BASE], lo))
            complete = len(instructions) == (address - lo) // 4 and all(ins.id for ins in instructions)
            value = earlier.joined_context_argument(instructions, now, BASE, register) if complete else None
            values = None if value is None else [value]
        if values is None:
            results.append(result | dict(status="changed dependencies need new proof", ids=None))
            continue
        if width:
            current_tables = [earlier.voice.load_table(now, pointer, width) for pointer in values]
            if not all(current_tables):
                results.append(result | dict(status="changed dependencies need new proof", ids=None))
                continue
            result.update(prior_table_addresses=old_addresses, current_table_addresses=values)
            values = sorted({key for slots in current_tables for key in slots if key >= 0})
        status = "rechecked same IDs" if values == row["ids"] else "rechecked different IDs"
        results.append(result | dict(status=status, ids=values))
    return results


def main():
    release, previous, bounds_ledger = map(read, (active.RELEASE, earlier.current.RELEASE, earlier.OUTPUT))
    assert digest(REGISTRY) == release["registry_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"] == previous["clean_input_sha256"]
    assert digest(earlier.current.ROM) == previous["candidate_sha256"] == bounds_ledger["candidate_sha256"]
    assert digest(active.ROM) == release["candidate_sha256"]
    clean, old, now = map(NdsImage.open, (CLEAN, earlier.current.ROM, active.ROM))
    clean_arm, old_arm, arm = [image.read_file(active.ARM) for image in (clean, old, now)]
    assert earlier.tables.sha(arm) == release["target_ARM9_sha256"]
    prior_refs = earlier.prior.census(earlier.current.ROM)
    current_refs = earlier.prior.census(active.ROM)
    receipt = read(earlier.prior.OUTPUT)
    assert prior_refs == {tuple(row) for field in ("all_shared_reference_candidates",
                                                 "current_only_reference_candidates") for row in receipt[field]}
    assert current_refs == prior_refs
    results = static_results(old_arm, arm, bounds_ledger["reference_outcomes"])
    assert len(results) == 706
    assert all(not set(KEYS).intersection(row["ids"]) for row in results if row["ids"] is not None)
    source = common_message_entries(clean.read_file(active.COMMON), clean_arm)
    installed = common_rows(now.read_file(active.COMMON), arm)
    archived_rows = {row["message_ID"]: row for row in read(ROOT / "shared_editorial_coverage_20261123.json")["records"]}
    exact = []
    for key in KEYS:
        row = archived_rows[key]
        assert text_reference(source[key]) == row["source_reference"] and source[key].text.hex() == row["source_hex"]
        assert text_reference(installed[key]) == row["installed_reference"] and installed[key].text.hex() == row["installed_hex"]
        exact.append(dict(message_ID=key, source_reference=row["source_reference"], source_hex=row["source_hex"],
                          installed_reference=row["installed_reference"], installed_hex=row["installed_hex"]))
    counts = dict(Counter(row["status"] for row in results))
    write(OUTPUT, dict(candidate_sha256=release["candidate_sha256"], earlier_candidate_sha256=previous["candidate_sha256"],
                      aligned_reference_candidates=len(current_refs), added_reference_candidates=0,
                      removed_reference_candidates=0, counts=counts, archived_records=exact, static_results=results,
                      earlier_native_selector_proofs_outside_this_check=67, new_gameplay_runs=0, new_editorial_credit=0,
                      scope="Historical aligned reference scan and bounded ARM arguments. Computed paths and actual display remain open.",
                      evidence=[reference(path) for path in (active.RELEASE, earlier.OUTPUT, earlier.prior.OUTPUT,
                                                           ARCHIVED, Path(earlier.flow.__file__), Path(__file__))]))
    print(f"{len(current_refs)} reference candidates match the historical census. Static argument proofs: {counts}.")


if __name__ == "__main__":
    main()
