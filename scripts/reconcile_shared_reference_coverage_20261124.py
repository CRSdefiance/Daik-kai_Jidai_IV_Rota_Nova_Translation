"""Account for every aligned reference in the retained COMMON wrapper census."""

from struct import unpack

from ndspy.code import MainCodeFile

from scripts import checkpoint_shared_relocated_references_20261115 as relocated
from scripts import rebind_shared_forwarding_20261123 as forwarding
from scripts import reconcile_archived_message_selectors_20261123 as selectors
from scripts import reconcile_kurushima_acceptance_20261123 as earlier
from scripts import reconcile_shared_call_inventory_20261123 as locks
from scripts import register_athens_item_rumor_20261124 as current
from scripts import verify_shared_number_call_followups_20261123 as numbers
from scripts.stage_cartridge_title_20261123 import CLEAN, REGISTRY, NdsImage, digest, read, reference, sha256, write


OUT = earlier.ROOT / "shared_reference_coverage_20261124.json"
ARCHIVED = set(earlier.ARCHIVED)


def durable_spans(arm, rows, except_spans=()):
    evidence = set(locks.locks(rows))
    assert evidence
    changed = {(lo, hi) for lo, hi, expected in evidence if locks.raw_hash(arm, lo, hi) != expected}
    assert changed == set(except_spans), changed
    return [dict(start=lo, end=hi, sha256=expected) for lo, hi, expected in sorted(evidence)
            if (lo, hi) not in changed]


def tape(arm, lo, hi):
    return arm[lo - forwarding.BASE:hi - forwarding.BASE]


def alias_inputs(clean, installed, fleet_arm, market_arm):
    fleet, pirate, battle = relocated.fleet_code, relocated.pirate, relocated.battle
    native_ranges = ((fleet.PIRATE_ENTRY, relocated.BATTLE_ALIAS_ENTRY, fleet_arm),
                     (relocated.BATTLE_ALIAS_ENTRY, relocated.BATTLE_ALIAS_TAIL + 4, market_arm))
    exact = []
    for lo, hi, historical in native_ranges:
        chunks = []
        for arm in (historical, installed):
            section, = [item for item in MainCodeFile(arm, forwarding.BASE).sections
                        if item.ramAddress <= lo < hi <= item.ramAddress + len(item.data)]
            chunks.append(bytes(section.data[lo - section.ramAddress:hi - section.ramAddress]))
        assert chunks[0] == chunks[1]
        exact.append(dict(start=lo, end=hi, sha256=sha256(chunks[0]).hexdigest()))
    tables = {**fleet.CALLSITES, pirate.CALL: pirate.TABLES, battle.CALL: (battle.TABLE,)}
    targets = {**dict.fromkeys(fleet.CALLSITES, fleet.MAPPER_ENTRY),
               pirate.CALL: fleet.PIRATE_ENTRY, battle.CALL: relocated.BATTLE_ALIAS_ENTRY}
    result = {}
    for site, pointers in tables.items():
        assert relocated.branch_target(clean, site, {pirate.WRAPPER}) == pirate.WRAPPER
        assert relocated.branch_target(installed, site, {targets[site]}) == targets[site]
        assert tape(installed, site, site + 4) == tape(market_arm, site, site + 4)
        values = set()
        for pointer in pointers:
            raw = tape(installed, pointer, pointer + 32)
            assert raw == tape(clean, pointer, pointer + 32) == tape(market_arm, pointer, pointer + 32)
            values.update(value for value in unpack("<8i", raw) if value >= 0)
        result[site] = sorted(values)
    for lo, hi in fleet.CALL_SCOPES:
        assert tape(installed, lo, hi) == tape(market_arm, lo, hi)
    for literal in (*fleet.TABLE_LITERALS, 0x02071F04):
        value = tape(installed, literal, literal + 4)
        assert value == tape(clean, literal, literal + 4) == tape(market_arm, literal, literal + 4)
    result[fleet.WRAPPER_TAIL] = sorted({n for site, ids in result.items() if site != battle.CALL for n in ids})
    result[relocated.BATTLE_ALIAS_TAIL] = result[battle.CALL]
    return result, exact


def main():
    release, accepted, prior, enum, archived_selector, moved = map(read, (current.RELEASE,
        earlier.OUT, forwarding.earlier.OUTPUT, forwarding.earlier.prior.OUTPUT, selectors.OUT, relocated.OUTPUT))
    assert digest(REGISTRY) == release["registry_sha256"] and digest(CLEAN) == release["clean_input_sha256"]
    assert digest(current.ROM) == release["candidate_sha256"]
    clean, live = map(NdsImage.open, (CLEAN, current.ROM))
    ja, arm = (image.read_file(current.ARM) for image in (clean, live))
    assert sha256(arm).hexdigest() == release["target_ARM9_sha256"]
    prior_release = read(earlier.current.RELEASE)
    assert accepted["candidate_sha256"] == prior_release["candidate_sha256"]
    assert NdsImage.open(prior_release["candidate"]).read_file(current.ARM) == arm
    assert NdsImage.open(selectors.current.ROM).read_file(current.ARM) == arm
    assert accepted["archived_message_scope"]["exact_bounded_forwarding_arguments"] == 706
    assert accepted["archived_message_scope"]["retained_native_selector_references"] == 42

    matched, installed_only = ({tuple(row) for row in enum[field]} for field in
                              ("all_shared_reference_candidates", "current_only_reference_candidates"))
    assert forwarding.earlier.prior.census(current.ROM) == matched | installed_only
    assert len(matched | installed_only) == 827 and len(installed_only) == 5
    slots = {(pc, target): (pc, target, kind, component) for pc, target, kind, component in matched | installed_only}
    assert len(slots) == 827
    keys = ARCHIVED
    outcomes = {}
    for row in prior["reference_outcomes"]:
        assert not keys.intersection(row["ids"])
        proof = row["proof"]
        outcomes[row["address"], row["entry"]] = dict(kind="earlier native selector" if "receipt" in proof else "bounded argument",
            possible_COMMON_ids=row["ids"], historical_receipt=proof.get("receipt"))
    assert len(outcomes) == 773
    resolved_native = [row for row in outcomes.values() if row["kind"] == "earlier native selector"]
    assert len(resolved_native) == 67
    native_receipts = {path: durable_spans(arm, read(path)) for path in {row["historical_receipt"] for row in resolved_native}}

    fresh = {row["site"]: row for row in archived_selector["earlier_matching_reference_scope"]["references"]}
    remaining = prior["still_unbound_reference_candidates"]
    assert len(fresh) == len(remaining) == 42
    assert fresh.keys() == {row["address"] for row in remaining}
    for row in remaining:
        value = fresh[row["address"]]
        ids = value.get("possible_COMMON_ids")
        assert ids is None or not keys.intersection(ids)
        outcomes[row["address"], row["entry"]] = dict(kind=value["kind"], possible_COMMON_ids=ids)

    fixed = enum["exact_argument_sources"]
    assert len(fixed) == 7
    fixed_locks = durable_spans(arm, fixed, ((0x02057524, 0x020575F4),))
    number_proof = read(numbers.OUT)
    number_arm = NdsImage.open(numbers.current.ROM).read_file(current.ARM)
    assert tape(number_arm, 0x02057524, 0x020575F4) == tape(arm, 0x02057524, 0x020575F4)
    assert number_proof["current_local_requests"]["volunteers"]["message_ID"] == 904
    for row in fixed:
        assert not keys.intersection(row["supported_ids"])
        outcomes[row["site"], row["entry"]] = dict(kind="dedicated original wrapper argument", possible_COMMON_ids=row["supported_ids"])

    earlier_relocation = read(relocated.current.RELEASE)
    assert digest(earlier_relocation["candidate"]) == earlier_relocation["candidate_sha256"] == moved["candidate_sha256"]
    earlier_arm = NdsImage.open(earlier_relocation["candidate"]).read_file(current.ARM)
    art = read(relocated.inventory.OUTPUT)["current_thumb_and_owned_table_routes"]
    lookups = relocated.lookup_calls(ja, arm, earlier_arm, art)
    original_fleet_arm = NdsImage.open(relocated.fleet.ROM).read_file(current.ARM)
    aliases, alias_spans = alias_inputs(ja, arm, original_fleet_arm, earlier_arm)
    relocated_ids = lookups | aliases
    assert relocated_ids == {int(pc): ids for pc, ids in moved["supported_ids_by_changed_reference"].items()}
    for pc, entry, _, _ in installed_only:
        ids = relocated_ids[pc]
        assert not keys.intersection(ids)
        outcomes[pc, entry] = dict(kind="registered renderer or alias relocation", possible_COMMON_ids=ids)
    assert slots.keys() == outcomes.keys()
    # The internal forwarding sites carry a parameter from a caller. Their local
    # proof does not independently impose an ID range on a new computed caller.
    rows = [dict(call_site=pc, entry=entry, instruction=slots[pc, entry][2], component=slots[pc, entry][3], **result)
            for (pc, entry), result in sorted(outcomes.items())]
    write(OUT, dict(candidate_sha256=release["candidate_sha256"], aligned_reference_count=len(rows),
        references=rows, supplementary_literal_and_table_locks=fixed_locks, earlier_native_locks=native_receipts,
        exact_alias_code_spans=alias_spans,
        separate_open_keys=sorted(keys), computed_or_indirect_targets_outside_census_open=True,
        evidence=list(map(reference, (earlier.OUT, forwarding.earlier.OUTPUT, forwarding.earlier.prior.OUTPUT,
            selectors.OUT, relocated.OUTPUT, numbers.OUT, current.RELEASE))), new_gameplay_runs=0, new_editorial_credit=0))
    print(f"Reconciled all {len(rows)} aligned references with their proof on the current candidate.")


if __name__ == "__main__":
    main()
