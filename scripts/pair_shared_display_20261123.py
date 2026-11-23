"""Rebind the pending shared display records to the active cumulative ROM."""

from collections import Counter
from pathlib import Path

from scripts import reconcile_shared_display_20261121 as prior
from scripts import register_hodram_midroute_followups_20261123 as release

base, native = release.base, release.native
SOURCE = prior.OUTPUT
OUTPUT = Path("translations/editorial_checkpoints/shared_display_20261123/paired_worklist.json")


def main():
    worklist, manifest = map(base.load, (SOURCE, release.RELEASE))
    candidate = base.digest(release.ROM)
    assert candidate == manifest["candidate_sha256"]
    assert base.digest(base.REGISTRY) == manifest["registry_sha256"]
    assert base.digest(prior.CLEAN) == worklist["clean_sha256"] == manifest["clean_input_sha256"]
    with release.scope["mapped"](base.LEDGER) as ledger:
        active = release.scope["value"](ledger, "current_integrated_candidate", 1)
        pending = release.scope["value"](ledger, "pending_shared_consumer_checkpoint_20261114", 1)
    assert pending["candidate_sha256"] == active["sha256"] == candidate and pending["remaining_total"] == 276

    clean, current = [base.NdsImage.open(p) for p in (prior.CLEAN, release.ROM)]
    arm, common = [current.read_file(p) for p in (prior.ARM, prior.COMMON)]
    assert native.digest(arm) == manifest["target_ARM9_sha256"] and native.digest(common) == manifest["target_COMMON_sha256"]
    source = prior.workflow.common_message_entries(clean.read_file(prior.COMMON), clean.read_file(prior.ARM))
    installed = prior.entries(current)
    results, counts = [], Counter()
    for record in worklist["records"]:
        key = record["message_ID"]
        left, right = source[key], installed[key]
        assert left.text.hex() == record["source_hex"] and prior.workflow.reference(left) == record["source_reference"]
        reference = prior.workflow.reference(right)
        counts[record["kind"]] += 1
        results.append(dict(message_ID=key, kind=record["kind"], file_path=record["file_path"],
            source_reference=record["source_reference"], current_reference=reference,
            source_hex=left.text.hex(), current_hex=right.text.hex(),
            source_Japanese=left.text.decode("cp932"), current_English=right.text.decode("cp932"),
            body_unchanged_since_prior=right.text.hex() == record["current_hex"],
            reference_unchanged_since_prior=reference == record["current_reference"],
            prior_display_scope=record["established_display_scope"],
            prior_review_reference=record["draft"],
            separate_gallery_draw_evidence_count=len(record["independent_gallery_draw_sources"]),
            story_artwork_association=record.get("story_image_request"),
            ownership_and_editorial_gate_open=True))
    assert counts["legacy"] == len(pending["remaining_legacy_keys"]) == 31 and sum(counts.values()) == 276
    assert {r["message_ID"] for r in results if r["kind"] == "legacy"} == set(pending["remaining_legacy_keys"])
    assert not OUTPUT.exists()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=worklist["clean_sha256"],
        ARM9_sha256=native.digest(arm), COMMON_sha256=native.digest(common),
        source_worklist=dict(path=str(SOURCE), sha256=base.digest(SOURCE), candidate_sha256=worklist["candidate_sha256"]),
        records=results, prior_scopes=dict(Counter(r["prior_display_scope"] for r in results)),
        current_owner_gate_complete=False, new_gameplay_runs=0, new_editorial_credit=0))
    unchanged = sum(r["body_unchanged_since_prior"] for r in results)
    same_location = sum(r["reference_unchanged_since_prior"] for r in results)
    print(f"Rebound {len(results)} clean and installed shared records. {unchanged} bodies and {same_location} references match the prior worklist.")


if __name__ == "__main__":
    main()
