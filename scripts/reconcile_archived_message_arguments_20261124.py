"""Resolve the 17 remaining argument sets in the verified COMMON reference census."""

from collections import Counter
from struct import iter_unpack, pack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs
from capstone.arm import ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG, ARM_REG_PC, ARM_REG_R1
from scripts import checkpoint_pending_shared_native_20261115 as registry
from scripts import checkpoint_shared_crew_and_wrapper_routes_20261115 as crew
from scripts import checkpoint_shared_display_owners_20261119 as displays
from scripts import rebind_archived_message_scope_20261124 as continuity
from scripts import reconcile_shared_reference_coverage_20261124 as prior
from scripts import register_tavern_buy_a_round_20261124 as active
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


OUT = continuity.OUT.with_name("archived_message_argument_ranges_20261124.json")
BASE = prior.forwarding.BASE
GETTER = 0x0205528C
SWITCH_POINTER = (0x02059134, 0x02053FE4)
SHELF_POINTER = (0x020BF334, 0x020546B8)
DIAGNOSTIC = {0x020EDF80: 112, 0x020EDF98: 111, 0x020EDFCC: 112}


def exact_bytes(clean, current, lo, hi):
    value = current[lo - BASE:hi - BASE]
    assert len(value) == hi - lo and value == clean[lo - BASE:hi - BASE]
    return dict(start=lo, end=hi, sha256=sha256(value).hexdigest())


def indirect(clean_rom, current_rom, clean, current):
    historical = read(registry.OUTPUT)["native_indirect_cases"]
    switch, shelf = historical
    assert switch["entry"] == 0x02058F4C and switch["indirect_target"] == SWITCH_POINTER[1]
    assert shelf["entry"] == 0x020BF328 and shelf["indirect_target"] == SHELF_POINTER[1]
    assert shelf["sole_direct_caller"] == 0x020BE534
    exact = [exact_bytes(clean, current, lo, hi) for lo, hi in
             ((0x02058F4C, 0x02059138), (0x020BE51C, 0x020BE53C), (0x020BF328, 0x020BF338))]
    for pc, target in (SWITCH_POINTER, SHELF_POINTER):
        assert unpack_from("<I", current, pc - BASE) == (target,)
    # The signed switch has one default and 17 explicit IDs.
    # Check every register assignment in its common output arm. The historical
    # native exercise covers every non-default case and both signed extremes.
    md = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    md.detail = True
    values = []
    for ins in md.disasm(current[0x59064:0x590F0], 0x02059064):
        if ins.mnemonic == "b":
            assert ins.op_str == "#0x20590f0"
            continue
        dest, source = ins.operands
        assert dest.type == ARM_OP_REG and dest.reg == ARM_REG_R1
        if ins.mnemonic == "ldr":
            assert source.type == ARM_OP_MEM and source.mem.base == ARM_REG_PC and not source.mem.index
            at = ins.address + 8 + source.mem.disp
            assert 0x020590FC <= at < SWITCH_POINTER[0]
            value, = unpack_from("<I", current, at - BASE)
        else:
            assert ins.mnemonic == "mov" and source.type == ARM_OP_IMM
            value = source.imm
        values.append(value)
    assert sorted(values) == switch["observed_ids"] == [998, *range(1003, 1020)]
    assert shelf["observed_ids"] == list(range(137, 261))
    references = [(name, pc, mode) for name, base, data in registry.components(current_rom.rom)
                  for pc, _, mode in registry.branch_hits(data, base, {shelf["entry"]})]
    assert references == [("ARM9 section 0", shelf["sole_direct_caller"], "arm_bl")]
    sink = displays.legacy_sink(clean_rom, current_rom)
    assert sink == read(displays.OUTPUT)["legacy_save_diagnostic_sink"]
    results = {SWITCH_POINTER: dict(kind="Original bounded switch", ids=sorted(values), references=exact[:1]),
               SHELF_POINTER: dict(kind="Original Market commodity range", ids=shelf["observed_ids"], references=exact[1:])}
    for site, key in DIAGNOSTIC.items():
        assert sink["common_getter_calls"][hex(site)] == key
        results[site, GETTER] = dict(kind="Legacy save diagnostic followed by the original immediate return", ids=[key],
            consumer=sink["entry"], source=reference(displays.CONTINUE))
    return results


def addressing_candidates(image, entries):
    """Check simple address sources outside the aligned transfer and literal census."""
    matches = set()
    for owner, base, raw in registry.components(image.rom):
        for pos, (word,) in enumerate(iter_unpack("<I", raw[:len(raw) & ~3])):
            pc = base + 4 * pos
            op = (word >> 21) & 15
            if word >> 28 == 15 or word & 0x0E0F0000 != 0x020F0000 or op not in (2, 4):
                continue
            imm, rot = word & 255, (word >> 8 & 15) * 2
            value = (imm >> rot | imm << (32 - rot)) & 0xFFFFFFFF
            target = (pc + 8 + (value if op == 4 else -value)) & 0xFFFFFFFF
            if target & ~1 in entries:
                matches.add((owner, pc, target, "ARM PC-relative immediate address"))
        for pos, (half,) in enumerate(iter_unpack("<H", raw[:len(raw) & ~1])):
            if half & 0xF800 == 0xA000:
                pc = base + 2 * pos
                target = ((pc + 4) & ~3) + 4 * (half & 255)
                if target in entries:
                    matches.add((owner, pc, target, "Thumb ADR"))
        for entry in entries:
            for target in (entry, entry | 1):
                needle = pack("<I", target)
                offset = raw.find(needle)
                while offset >= 0:
                    if (base + offset) & 3:
                        matches.add((owner, base + offset, target, "unaligned exact address word"))
                    offset = raw.find(needle, offset + 1)
    return sorted(matches)


def main():
    release, current_scope, census = map(read, (active.RELEASE, continuity.OUT, prior.OUT))
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(active.ROM) == release["candidate_sha256"] == current_scope["candidate_sha256"]
    assert current_scope["inherited_dispositions"] == reference(prior.OUT)
    original, installed = map(NdsImage.open, (CLEAN, active.ROM))
    ja, en = [image.read_file(active.ARM) for image in (original, installed)]
    assert sha256(en).hexdigest() == release["target_ARM9_sha256"]
    rows = {(r["call_site"], r["entry"]): r for r in census["references"]}
    assert len(rows) == current_scope["exact_census_count"] == 827
    pending = {k for k, r in rows.items() if r["possible_COMMON_ids"] is None}
    assert len(pending) == 17
    resolved = indirect(original, installed, ja, en)
    assert len(resolved) == 5 and resolved.keys() <= pending
    for row in read(crew.OUTPUT)["forwarding_sites"]:
        site, entry = row["site"], row["entry"]
        key = (site, GETTER)
        if key not in pending:
            continue
        assert key not in resolved and rows[key]["kind"] == "forwards its caller's argument"
        locks = [exact_bytes(ja, en, lock["start"], lock["end"]) for lock in row["code_locks"]]
        assert locks and all(lock["sha256"] == old["clean_and_current_sha256"]
                             for lock, old in zip(locks, row["code_locks"], strict=True))
        incoming = {p: r for p, r in rows.items() if p[1] == entry}
        assert incoming and all(r["possible_COMMON_ids"] is not None or p in resolved for p, r in incoming.items())
        supported = sorted({n for p, r in incoming.items() for n in (
            r["possible_COMMON_ids"] if r["possible_COMMON_ids"] is not None else resolved[p]["ids"])})
        assert supported
        resolved[key] = dict(kind="Original wrapper forwards the already bounded incoming argument", ids=supported,
            wrapper_entry=entry, exact_locks=locks, incoming_scoped_sites=len(incoming))
    assert resolved.keys() == pending
    keys = set(census["separate_open_keys"])
    assert keys == {284, 318, 750, 751, 752}
    assert all(not keys.intersection(row["possible_COMMON_ids"] if k not in pending else resolved[k]["ids"])
               for k, row in rows.items())

    targets = {target for _, target in rows}
    original_hits, installed_hits = (addressing_candidates(image, targets) for image in (original, installed))
    assert original_hits == installed_hits
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], inherited_dispositions=reference(prior.OUT),
        latest_continuity=reference(continuity.OUT), fully_bounded_census_sites=len(rows),
        completed_bindings=[dict(call_site=site, target=target, **proof) for (site, target), proof in sorted(resolved.items())],
        new_binding_kinds=dict(Counter(r["kind"] for r in resolved.values())),
        original_and_current_additional_address_candidates=installed_hits, archived_ids=sorted(keys),
        scope="Finite argument sets for the inventoried calls and pointer words; other computed pathways remain open.",
        evidence=list(map(reference, (active.RELEASE, registry.OUTPUT, crew.OUTPUT, displays.OUTPUT))),
        new_gameplay_runs=0, ROM_changed=False, new_editorial_credit=0))
    print(f"Bound the final {len(resolved)} argument sets. All {len(rows)} inventoried references exclude the five keys. "
          f"Additional address candidates: {len(installed_hits)}.")


if __name__ == "__main__":
    main()
