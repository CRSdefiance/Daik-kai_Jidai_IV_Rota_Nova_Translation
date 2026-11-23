"""Bind the existing shared-display worklist to the final Hodram wrap candidate."""

from collections import defaultdict

from scripts import pair_shared_display_20261123 as paired
from scripts import register_hodram_b261_b310_wrap_fixes_20261123 as current


base, native = current.base, current.native
SOURCE = paired.OUTPUT
OUTPUT = SOURCE.with_name("binding_after_hodram_20261123.json")
LEGACY = "Legacy dialogue with remaining display questions"
UNASSOCIATED = "Scene label without a specific display association"


def main():
    worklist, release = map(base.load, (SOURCE, current.RELEASE))
    candidate = base.digest(current.ROM)
    assert candidate == release["candidate_sha256"] and base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(paired.prior.CLEAN) == release["clean_input_sha256"] == worklist["clean_sha256"]
    with current.scope["mapped"](base.LEDGER) as ledger:
        pending = current.scope["value"](ledger, "pending_shared_consumer_checkpoint_20261114", 1)
        active = current.scope["value"](ledger, "current_integrated_candidate", 1)
    assert pending["candidate_sha256"] == active["sha256"] == candidate
    archive = base.NdsImage.open(current.ROM)
    arm, common = [archive.read_file(path) for path in (paired.prior.ARM, paired.prior.COMMON)]
    assert native.digest(arm) == release["target_ARM9_sha256"] == worklist["ARM9_sha256"]
    assert native.digest(common) == release["target_COMMON_sha256"] == worklist["COMMON_sha256"]
    installed = paired.prior.entries(archive)
    by_scope = defaultdict(list)
    for row in worklist["records"]:
        key = row["message_ID"]
        entry = installed[key]
        assert entry.text.hex() == row["current_hex"]
        assert paired.prior.workflow.reference(entry) == row["current_reference"]
        by_scope[row["prior_display_scope"]].append(key)
    counts = {scope: len(ids) for scope, ids in by_scope.items()}
    assert counts == worklist["prior_scopes"] and sum(counts.values()) == pending["remaining_total"] == 276
    priority = by_scope[LEGACY] + by_scope[UNASSOCIATED]
    assert len(priority) == 35 and len(set(priority)) == 35
    result = dict(candidate_sha256=candidate, previous_binding_sha256=worklist["candidate_sha256"],
        source_worklist=str(SOURCE), source_worklist_sha256=base.digest(SOURCE),
        clean_sha256=worklist["clean_sha256"], ARM9_sha256=native.digest(arm), COMMON_sha256=native.digest(common),
        exact_stored_bytes_and_locations=True, ARM9_and_COMMON_unchanged=True, by_prior_scope=dict(by_scope),
        legacy_and_unassociated_first_pass=priority, shared_owner_gate_complete=False, gameplay_credit_added=0)
    if OUTPUT.exists():
        assert base.load(OUTPUT) == result
    else:
        base.save(OUTPUT, result)
    print("Bound 276 shared entries to the current candidate. The 27 legacy and eight unassociated entries are ready for focused follow-up.")


if __name__ == "__main__":
    main()
