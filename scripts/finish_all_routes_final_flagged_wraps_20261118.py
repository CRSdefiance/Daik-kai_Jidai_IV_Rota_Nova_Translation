"""Verify the registered candidate and close the source-bound wrap queue."""

from collections import Counter
from inspect import getsource

from scripts import finish_all_routes_next_review_wraps_20261118 as verification
from scripts import prepare_pending_shared_text_20261118 as shared
from scripts import register_all_routes_final_flagged_wraps_20261118 as registered
from scripts.source_locked_derivation_v5118 import checked_text

base, native = registered.base, registered.native
QUEUE = registered.stage.ROOT / "followup_wrap_queue.json"

source = checked_text(getsource(verification.verify_registration), {
    'len(manifest["batches"]) == 884 and len(manifest["checks"]) == 219':
        'len(manifest["batches"]) == 886 and len(manifest["checks"]) == 221',
    'len(review["records"]) == 132': 'len(review["records"]) == 175',
})
env = vars(verification) | globals()
exec(compile(source, __file__ + "::registered-candidate", "exec"), env)


def close_queue(release, review, previous, current):
    prior = registered.stage.review.QUEUE
    queue = base.load(prior)
    assert queue["candidate_sha256"] == base.digest(registered.parent.ROM)
    assert queue["counts"]["open editorial lead"] == 64
    rows = {(r["file_path"], r["block"], r["current_reference"]["offset"], r["current_hex"]): r
            for r in review["records"]}
    banks = {}
    for lead in queue["records"]:
        path = lead["file_path"]
        if path not in banks:
            banks[path] = [native.IlnkContainer.parse(im.read_file(path)).blocks for im in (previous, current)]
    resolved, carried = [], []
    for lead in queue["records"]:
        path, n = (lead[k] for k in ("file_path", "block"))
        before, after = [bank[n] for bank in banks[path]]
        if lead["disposition"] == "open editorial lead":
            assert native.digest(before) == lead["block_sha256"]
            at = lead["offset"]
            payload = bytes([lead["source_selector"]]) + bytes.fromhex(lead["stored_body_hex"])
            assert before[at:at + len(payload)] == payload
            row = rows[path, n, at, payload.hex()]
            assert row["wrap_lead"] and row["decision"] == "revision"
            ref = row["registered_reference"]
            installed = bytes.fromhex(ref["exact_stored_hex"])
            new_at = ref["offset"]
            assert after[new_at:new_at + len(installed)] == installed
            lead.update(disposition="resolved in Lil and Maria story wrap review",
                        review=ref | {"id": row["id"], "reason": row["localization_note"]})
            resolved.append(row["id"])
        elif before != after:
            # The convoy's prior one-page repair in B208 is upstream of the new sound-description edit.
            earlier = lead.get("carried_forward_reference", lead["review"])
            ident = earlier["id"]
            assert ident == "DK4_MES_B208_R0043" and path == "/data/SC3.DK4"
            row = rows[path, n, earlier["offset"], earlier["exact_stored_hex"]]
            assert row["decision"] == "retention"
            latest = row["registered_reference"]
            span = bytes.fromhex(latest["exact_stored_hex"])
            for block, ref in ((before, earlier), (after, latest)):
                at = ref["offset"]
                assert block[at:at + len(span)] == span
            lead["carried_forward_reference"] = earlier | latest
            carried.append(ident)
    assert len(resolved) == 64 and Counter(resolved) == Counter(review["resolved_wrap_leads"])
    assert carried == ["DK4_MES_B208_R0043"]
    queue["candidate_sha256"] = release["candidate_sha256"]
    queue["counts"] = dict(Counter(r["disposition"] for r in queue["records"]))
    assert queue["counts"].get("open editorial lead", 0) == 0
    queue["counts"]["open editorial lead"] = 0
    queue["scope"] = "All leads in the carried-forward progressive wrap scan and the added emulator finding have individual dispositions."
    queue["predecessor_queue"] = dict(path=str(prior), sha256=base.digest(prior))
    if QUEUE.exists():
        assert base.load(QUEUE) == queue
    else:
        base.save(QUEUE, queue)


def main():
    release, review, previous, current = env["verify_registration"]()
    close_queue(release, review, previous, current)
    shared.main()
    note = ("\nThe 64 leads in the current queue are closed. The wider editorial goal remains active with 276 exact shared-text bindings "
            "and open display ownership. [Wrap queue](../work/all_routes_final_flagged_wraps_20261118/research_v1/followup_wrap_queue.json) · "
            "[Shared text bindings](../work/all_routes_final_flagged_wraps_20261118/research_v1/shared_text_current_binding.json)\n")
    doc = registered.DOC.read_text(encoding="utf-8")
    if note not in doc:
        registered.DOC.write_text(doc + note, encoding="utf-8", newline="\n")
    print("Verified the registered candidate and exact clean patch. Closed all 64 queued wrap leads.")


if __name__ == "__main__":
    main()
