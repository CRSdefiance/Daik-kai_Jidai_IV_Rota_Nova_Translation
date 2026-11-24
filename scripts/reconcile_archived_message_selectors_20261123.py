"""Bind remaining conditional COMMON selectors to current executable and table bytes."""

from struct import unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_INS_CMP, ARM_INS_LDR, ARM_INS_MOV, ARM_OP_MEM, ARM_REG_PC
from unicorn import UC_ARCH_ARM, UC_MODE_ARM, Uc
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R4, UC_ARM_REG_SP

from dk4tool.script.common_message_table import common_message_entries
from scripts import rebind_shared_forwarding_20261123 as prior
from scripts import register_missionary_destination_20261123 as current
from scripts import checkpoint_shared_upstream_tails_20261115 as historical
from scripts.inventory_native_common_calls import direct_bl_target
from scripts.reconcile_elegy_acceptance_20261123 import common_rows
from scripts.reconcile_fleet_destination_writers_20261123 import run_fragment
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


OUT = prior.OUTPUT.with_name("archived_message_selectors_20261123.json")
BASE, KEYS = prior.BASE, prior.KEYS
SITES = {
    0x0201351C: (UC_ARM_REG_R4, 15, (1357, 1358)),
    0x02013668: (UC_ARM_REG_R0, 0, (1359, 1360)),
    0x02059D78: (UC_ARM_REG_R0, 0, (818, 819)),
    0x02059D94: (UC_ARM_REG_R0, 0, (52, 53)),
    0x02059F04: (UC_ARM_REG_R0, 0, (60, 61)),
    0x0205E11C: (UC_ARM_REG_R0, 0, (1159, 1163)),
    0x0205FBB8: (UC_ARM_REG_R4, 135, (732, 734)),
    0x02071DD4: (UC_ARM_REG_R4, 0, (0x021176E0, 0x02117760)),
    0x020BA37C: (UC_ARM_REG_R0, 4, (8, 773)),
    0x020BBEE8: (UC_ARM_REG_R0, 0, (775, 778)),
    0x020BC0A8: (UC_ARM_REG_R0, 0, (782, 783)),
    0x020BC0D8: (UC_ARM_REG_R0, 0, (9, 10)),
}


def seal(clean, installed, lo, hi):
    contents = installed[lo - BASE:hi - BASE]
    assert len(contents) == hi - lo and contents == clean[lo - BASE:hi - BASE]
    return dict(start=lo, stop=hi, sha256=sha256(contents).hexdigest())


def inspect_selectors(clean, arm, unbound):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    cpu = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    cpu.mem_map(BASE, 0x400000)
    cpu.mem_write(BASE, arm)
    results = []
    for address, (reg, threshold, expected) in SITES.items():
        start = address - 16
        code = seal(clean, arm, start, address + 4)
        tail = list(decoder.disasm(arm[start - BASE:address - BASE], start))
        assert len(tail) == 4 and tail[0].id == ARM_INS_CMP
        assert all(ins.id in (ARM_INS_LDR, ARM_INS_MOV) for ins in tail[1:])
        entry = unbound[address]["entry"]
        assert direct_bl_target(unpack_from("<I", arm, address - BASE)[0], address) == entry
        literals = []
        for ins in tail[1:]:
            operand = ins.operands[-1]
            if operand.type == ARM_OP_MEM and operand.mem.base == ARM_REG_PC:
                literal = ins.address + 8 + operand.mem.disp
                literals.append(seal(clean, arm, literal, literal + 4))
        cases = []
        for value in sorted({0, 1, 0xFFFFFFFF, 0x80000000, 0x7FFFFFFF,
                             (threshold - 1) & 0xFFFFFFFF, threshold, threshold + 1}):
            run_fragment(cpu, start, address, ((UC_ARM_REG_SP, 0x023EE000),
                                                (reg, value), (UC_ARM_REG_R1, 0xAAAAAAAA)))
            cases.append(dict(supplied_compare_value=value, original_r1=cpu.reg_read(UC_ARM_REG_R1)))
        actual = sorted({row["original_r1"] for row in cases})
        assert actual == list(expected), (address, actual, expected)
        tables, ids = [], set(actual)
        if entry == 0x02053D44:
            ids = set()
            for pointer in actual:
                binding = seal(clean, arm, pointer, pointer + 32)
                slots = prior.earlier.voice.load_table(arm, pointer, 8)
                assert slots and slots[0] >= 0
                tables.append(binding | dict(source_slots=list(slots)))
                ids.update(n for n in slots if n >= 0)
        assert not ids.intersection(KEYS) and min(ids) >= 0 and max(ids) < 3668
        results.append(dict(call_site=address, entry=entry, code=code, literals=literals,
                            cases=cases, voice_tables=tables, possible_COMMON_ids=sorted(ids)))
    return results


def exact_locks(tree, arm):
    if isinstance(tree, dict):
        if {"start", "end", "clean_and_current_sha256"} <= tree.keys():
            start, end = tree["start"] - BASE, tree["end"] - BASE
            return [tree | dict(exact=sha256(arm[start:end]).hexdigest() == tree["clean_and_current_sha256"])]
        return [item for value in tree.values() for item in exact_locks(value, arm)]
    if isinstance(tree, list):
        return [item for value in tree for item in exact_locks(value, arm)]
    return []


def rebind_older_scope(clean, arm, unbound, fresh):
    tails, crew, producer = map(read, (historical.OUTPUT, historical.crew.OUTPUT, historical.producer.OUTPUT))
    assert not tails["remaining_common_reference_candidates"]
    cases = {row["site"]: row for row in tails["in_scope_conditional_tails"]}
    checked = {int(site): path for site, path in tails["reconciled_previously_checked"].items()}
    forwarded = {row["site"]: row for row in crew["forwarding_sites"] if row["site"] in unbound}
    crew_cases = {row["site"]: row for row in crew["crew_selectors"]}
    assert cases.keys() == SITES.keys()
    assert cases.keys() | checked.keys() | forwarded.keys() == unbound.keys()
    assert sorted(forwarded) == sorted(map(int, tails["internal_forwarding"]))
    for row in fresh:
        assert set(row["possible_COMMON_ids"]) <= set(cases[row["call_site"]]["ids"])

    earlier_market = producer["native_market"]
    market_sites = {*earlier_market["stock_sites"], earlier_market["contract_site"]}
    market = historical.producer.market_branches(clean, arm)
    assert market["supported_ids"] == earlier_market["supported_ids"]
    narration_sites = set(producer["narration"]["primary_loaded_sites"])
    narration_locks = exact_locks(producer["narration"], arm)
    inherited_locks = exact_locks(producer["retained_native_proofs"], arm)
    groups = []
    for site, previous in cases.items():
        locked = exact_locks(previous, arm)
        assert locked and all(row["exact"] for row in locked)
        assert not set(previous["ids"]).intersection(KEYS)
        groups.append(dict(site=site, kind="conditional producer", possible_COMMON_ids=previous["ids"], locks=locked))
    for site, previous in forwarded.items():
        locked = exact_locks(previous, arm)
        assert locked and all(row["exact"] for row in locked)
        groups.append(dict(site=site, kind="forwards its caller's argument", locks=locked))
    for site, proof in checked.items():
        row = dict(site=site, earlier_proof=reference(proof))
        if site in crew_cases:
            groups.append(row | dict(kind="crew selector", locks=exact_locks(crew_cases[site], arm),
                                     possible_COMMON_ids=crew_cases[site]["supported_ids"]))
        elif site in market_sites:
            groups.append(row | dict(kind="rechecked native Market supplier",
                                     possible_COMMON_ids=market["supported_ids"]))
        elif site in narration_sites:
            groups.append(row | dict(kind="native narration input bounds", locks=narration_locks,
                                     possible_COMMON_ids=producer["narration"]["supported_ids"]))
        else:
            assert site in {*producer["retained_native_proofs"]["sites"], 0x02059134, 0x020BF334}
            groups.append(row | dict(kind="indirect producer or consumed text", locks=inherited_locks))
    assert len(groups) == 42
    changed = [row["site"] for row in groups if "locks" in row and
               (not row["locks"] or not all(lock["exact"] for lock in row["locks"]))]
    assert all(not set(KEYS).intersection(row.get("possible_COMMON_ids", ())) for row in groups)
    return dict(references=groups, changed_dependencies=changed, rechecked_market=market,
                proof=reference(historical.OUTPUT), other_computed_and_display_paths_open=True)


def main():
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(current.ROM) == release["candidate_sha256"]
    assert digest(CLEAN) == release["clean_input_sha256"]
    archive = read(prior.ARCHIVED)
    clean, image = map(NdsImage.open, (CLEAN, current.ROM))
    ja, arm = [rom.read_file(current.ARM) for rom in (clean, image)]
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    original = common_message_entries(clean.read_file(current.COMMON), ja)
    installed = common_rows(image.read_file(current.COMMON), arm)
    records = archive["source_and_installed_COMMON"]
    assert {row["message_ID"] for row in records} == set(KEYS)
    for row in records:
        key = row["message_ID"]
        assert original[key].text.hex() == row["source_hex"] and prior.text_reference(original[key]) == row["source_reference"]
        assert installed[key].text.hex() == row["installed_hex"] and prior.text_reference(installed[key]) == row["installed_reference"]
    report = read(prior.earlier.OUTPUT)
    unbound = {row["address"]: row for row in report["still_unbound_reference_candidates"]}
    assert len(unbound) == 42 and SITES.keys() <= unbound.keys()
    results = inspect_selectors(ja, arm, unbound)
    older = rebind_older_scope(ja, arm, unbound, results)
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], original_archive_evidence=reference(prior.ARCHIVED),
        earlier_bounded_census=reference(prior.earlier.OUTPUT), registered_release=reference(current.RELEASE),
        source_and_installed_records=records, selectors=results, earlier_matching_reference_scope=older,
        new_gameplay=False, new_editorial_credit=0))
    print(f"Reconciled {len(older['references'])} earlier references. Changed dependency groups: {len(older['changed_dependencies'])}.")


if __name__ == "__main__":
    main()
