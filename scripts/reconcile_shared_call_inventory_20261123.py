"""Carry the bounded shared-text call inventory forward to the registered ROM."""

from collections import Counter
from hashlib import sha256
from pathlib import Path
from struct import iter_unpack, unpack_from

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from scripts import checkpoint_shared_upstream_ranges_20261115 as ranges
from scripts import checkpoint_shared_wrapper_inputs_20261115 as wrappers
from scripts import register_title_reports_label_20261123 as current


BASE, base = wrappers.BASE, current.base
ROOT = Path("translations/editorial_checkpoints/shared_display_20261123")
OUT = ROOT / "bounded_calls_current_20261123.json"
REGIONAL = ROOT / "regional_attack_syracuse_20261123.json"
BOOK = ROOT.parent / "SharedText_20261110_v1"
OLDER = Path("releases/all_routes_editorial_20261115_market_trade_dialogue_candidate/verification/registered_release_verification.json")


def locks(value):
    if isinstance(value, list):
        for child in value:
            yield from locks(child)
    if not isinstance(value, dict):
        return
    if {"start", "end", "clean_and_current_sha256"} <= value.keys():
        yield value["start"], value["end"], value["clean_and_current_sha256"]
    if value.get("registered_child") == 0x02156058:
        start = value["registered_child"]
        yield start, start + 0x1C, value["bytes_sha256"]
    for child in value.values():
        if isinstance(child, (list, dict)):
            yield from locks(child)


def raw_hash(arm, start, end):
    assert BASE <= start < end <= BASE + len(arm)
    return sha256(arm[start-BASE:end-BASE]).hexdigest()


def check_locks(old, current_arm, evidence):
    reviewed = sorted(set(locks(evidence)))
    assert reviewed
    differences = []
    for start, end, expected in reviewed:
        assert raw_hash(old, start, end) == expected, (hex(start), hex(end))
        fresh = raw_hash(current_arm, start, end)
        if fresh != expected:
            differences.append(dict(start=start, end=end, historical_sha256=expected, current_sha256=fresh))
    return dict(verified_historical_spans=len(reviewed), changed_dependencies=differences)


def literal_offsets(arm, start, end):
    start -= BASE
    for i, (word,) in enumerate(iter_unpack("<I", arm[start:end-BASE])):
        if word >> 28 == 15 or word & 0x0F7F0000 != 0x051F0000:
            continue
        off = start + i * 4 + 8
        addr = off + (word & 0xFFF if word & 0x800000 else -(word & 0xFFF))
        assert 0 <= addr <= len(arm) - 4
        yield addr


def argument_window(row):
    proof = row["proof"]
    if row["basis"] == "bounded control flow":
        return proof["candidate"]["window_start"], proof["candidate"]["window_end"]
    if row["basis"] == "bounded instruction tail":
        return proof["start"], proof["end"]
    raise ValueError(f"Unknown bounded argument proof {row['basis']}")


def finite_outcomes(source, historical_arm, arm, prior, pending):
    decoder = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    decoder.detail = True
    decoder.skipdata = True
    counts, unchanged, fresh, unresolved, all_hits = Counter(), [], [], [], []
    for row in prior:
        address, entry = row["address"], row["entry"]
        context = row["proof"]
        if row["basis"] == "previously checked native selector":
            counts["native_receipt_rows"] += 1
            continue
        start, end = argument_window(row)
        historic = raw_hash(historical_arm, start, end)
        if row["basis"] == "bounded instruction tail":
            assert historic == context["matched_code_sha256"]
        literal_changes = [BASE + p for p in sorted(set(literal_offsets(historical_arm, start, end)))
                           if historical_arm[p:p+4] != arm[p:p+4]]
        tables = context.get("typed_tables", [])
        for table in tables:
            at = table["address"] - BASE
            slots = tuple(table["slots"])
            assert unpack_from(f"<{len(slots)}i", historical_arm, at) == slots
        data_changed = any(tuple(table["slots"]) != tuple(ranges.voice.load_table(arm, table["address"], len(table["slots"])) or ())
                           for table in tables)
        previous_ids = row["ids"]
        live = raw_hash(arm, start, end)
        if live == historic and not literal_changes and not data_changed:
            counts["exact_window_literal_and_table_reuse"] += 1
            unchanged.append(dict(address=address, entry=entry, historical_and_current_code_sha256=live,
                start=start, end=end, PC_relative_literals_exact=True, typed_tables_exact=True))
            continue
        register, width = ranges.voice.NATIVE.get(entry, (ranges.ALL_TARGETS.get(entry), None))
        assert register in ("r0", "r1")
        now, basis, proof = ranges.finite_arguments(source, arm, address, register, decoder)
        change = dict(address=address, entry=entry, code_from=start, code_to=end,
            historical_code_sha256=historic, current_code_sha256=live, changed_literal_addresses=literal_changes,
            prior_ids=previous_ids, prior_table_changed=data_changed, fresh_proof=proof)
        if now is None:
            counts["current_inputs_unbound"] += 1
            unresolved.append(change)
            continue
        if width:
            slots = [ranges.voice.load_table(arm, ptr, width) for ptr in now]
            if any(not value for value in slots):
                counts["current_inputs_unbound"] += 1
                unresolved.append(change | dict(reason="Current table input could not be verified", pointers=now))
                continue
            # The surviving table choices, including original default slots,
            # select only IDs drawn from the typed signed words.
            now = sorted({n for values in slots for n in values if n >= 0})
        if not now or min(now) < 0 or max(now) >= 3668:
            counts["current_inputs_unbound"] += 1
            unresolved.append(change | dict(reason="Output outside known catalogue", values=now))
            continue
        hits = sorted(pending.intersection(now))
        all_hits.extend((address, key) for key in hits)
        counts["refreshed_bounded_arguments"] += 1
        fresh.append(change | dict(current_basis=basis, current_ids=now, pending_hits=hits))

    assert sum(counts.values()) == len(prior)
    return dict(counts=dict(counts), matched_dependencies=unchanged, refreshed_arguments=fresh,
        unresolved_current_windows=unresolved, pending_message_results=all_hits)


def main():
    assert not OUT.exists()
    release, older = map(base.load, (current.RELEASE, OLDER))
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(current.stage.CLEAN) == release["clean_input_sha256"] == older["clean_input_sha256"]
    older_rom = Path(older["candidate"])
    assert base.digest(older_rom) == older["candidate_sha256"]
    source, parent, active = [base.NdsImage.open(p) for p in (current.stage.CLEAN, older_rom, current.ROM)]
    ja, old, en = (img.read_file(current.ARM) for img in (source, parent, active))
    for arm, details in ((old, older), (en, release)):
        assert sha256(arm).hexdigest() == details["target_ARM9_sha256"]
    pending = {row["message_ID"] for row in base.load(current.REVIEW)["shared_consumer_binding"]["records"]}
    assert len(pending) == 276
    cases = {
        "references": wrappers.OUTPUT,
        "bounded": ranges.OUTPUT,
        "fixed": ranges.fixed.OUTPUT,
        "selectors": ranges.stock.OUTPUT,
        "tables": ranges.tables.OUTPUT,
        "crew_forwarders": BOOK / "shared_crew_and_wrapper_routes_20261115_v1.json",
        "upstream_tails": BOOK / "shared_upstream_tails_20261115_v1.json",
        "relocations": BOOK / "shared_relocated_references_20261115_v1.json",
    }
    proof = {name: base.load(path) for name, path in cases.items()}
    assert all(d["candidate_sha256"] == older["candidate_sha256"] for name, d in proof.items() if name != "tables")
    historical_record = proof["references"]
    common = {tuple(row) for row in historical_record["all_shared_reference_candidates"]}
    old_set = common | {tuple(row) for row in historical_record["current_only_reference_candidates"]}
    ja_set = common | {tuple(row) for row in historical_record["clean_only_reference_candidates"]}
    assert wrappers.census(current.stage.CLEAN) == ja_set
    actual = wrappers.census(current.ROM)
    assert actual == old_set and len(actual) == 827
    assert not proof["upstream_tails"]["remaining_common_reference_candidates"]
    assert set(map(int, proof["relocations"]["supported_ids_by_changed_reference"])) == {r[0] for r in (ja_set ^ old_set)}
    assert all(pending.isdisjoint(values) for values in proof["relocations"]["supported_ids_by_changed_reference"].values())

    inherited = base.load(REGIONAL)["prior_bounded_selector_worklist"]["sites"]
    first = {row["address"] for row in inherited}
    coverage = {
        "crew": {row["site"] for row in proof["crew_forwarders"]["crew_selectors"]},
        "fixed": set(proof["fixed"]["resolved_sites"]),
        "forward": {row["site"] for row in proof["crew_forwarders"]["forwarding_sites"]},
    }
    assert (len(first), *(len(group) for group in coverage.values())) == (43, 5, 25, 13)
    assert first == set().union(*coverage.values())
    covered = [dict(address=site, original_proof=kind) for kind, sites in coverage.items() for site in sorted(sites)]
    references = proof["bounded"]["reference_outcomes"]
    assert len(references) == 773 and all(pending.isdisjoint(row["ids"]) for row in references)
    scope = finite_outcomes(ja, old, en, references, pending)
    dependency_checks = {}
    for name in ("fixed", "selectors", "tables", "crew_forwarders", "upstream_tails", "references"):
        data = proof[name]
        if name == "tables":
            data = data["cases"]
        dependency_checks[name] = check_locks(old, en, data)
    base.save(OUT, dict(candidate_sha256=release["candidate_sha256"], clean_sha256=release["clean_input_sha256"],
        historical_candidate_sha256=older["candidate_sha256"], earlier_43_address_worklist_reconciled=covered,
        bounded_reference_scope=dict(current_reference_count=len(actual), clean_reference_count=len(ja_set),
            current_added_or_retired_vs_historical=0, relocated_historical_references=len(ja_set ^ old_set)),
        bounded_arguments=scope, native_dependency_comparisons=dependency_checks, pending_stored_keys=len(pending),
        independent_stored_display_ownership_open=True, new_gameplay_runs=0, new_editorial_credit=0,
        evidence={str(p): base.digest(p) for p in [OLDER, REGIONAL, current.RELEASE, *cases.values(), Path(__file__)]}))
    print(f"Reconciled the 43-address worklist. Bounded argument checks: {scope['counts']}.")


if __name__ == "__main__":
    main()
