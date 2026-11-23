"""Verify the ongoing-wrap release and pair every remaining lead in the stored scan."""

from inspect import getsource

from scripts import finish_all_routes_next_review_wraps_20261118 as previous
from scripts import register_all_routes_remaining_phrase_wraps_20261118 as registered
from scripts.source_locked_derivation_v5118 import checked_text

base, native = registered.base, registered.native
QUEUE = registered.stage.ROOT / "followup_wrap_queue.json"
NEXT = registered.stage.review.ROOT.with_name("all_routes_final_flagged_wraps_20261118")


def observed_followup(review, banks):
    ident = "DK4_MES_B208_R0046"
    row, = [r for r in review["records"] if r["route"] == 3 and r["id"] == ident]
    ref = row["registered_reference"]
    path, n, offset = (ref[k] for k in ("file_path", "block", "offset"))
    block = banks[path][1][n]
    payload = bytes.fromhex(ref["exact_stored_hex"])
    assert block[offset:offset + len(payload)] == payload
    proof = registered.replay.LIVE
    observed, = [r for r in base.load(proof)["holds"] if r["id"] == ident and r.get("route") == 3]
    body = payload[1:]
    assert body == bytes.fromhex(observed["body_hex"])
    lines = [line.strip().decode("ascii") for line in body.split(b"\n")]
    assert lines[:2] == ["What made the sound is", "still a mystery. We don't even know"]
    assert base.digest(observed["capture"]["path"]) == observed["capture"]["PNG_sha256"]
    return dict(file_path=path, block=n, offset=offset, source_selector=payload[0],
        block_sha256=native.digest(block), native_preamble_hex=block[offset-5:offset+1].hex(),
        stored_body_hex=body.hex(), rows=lines, disposition="open editorial lead",
        findings=[dict(kind="split_predicate_after_copula", after_row=1)],
        source="initialized Maria excerpt",
        observation=dict(id=ident, receipt=str(proof), receipt_sha256=base.digest(proof), capture=observed["capture"]))


verify = checked_text(getsource(previous.verify_registration), {
    'len(manifest["batches"]) == 884 and len(manifest["checks"]) == 219': 'len(manifest["batches"]) == 885 and len(manifest["checks"]) == 220',
    'len(review["records"]) == 132': 'len(review["records"]) == 163',
})
carry = checked_text(getsource(previous.carry_queue), {
    'queue["counts"]["open editorial lead"] == 114': 'queue["counts"]["open editorial lead"] == 93',
    'len(closed) == 21': 'len(closed) == 30',
    'queue["counts"]["open editorial lead"] == 93\n    queue["scope"]':
        'queue["counts"]["open editorial lead"] == 64\n    queue["scope"]',
    '    queue["candidate_sha256"] = release["candidate_sha256"]':
        '    queue["records"].append(observed_followup(review, banks))\n'
        '    queue["candidate_sha256"] = release["candidate_sha256"]',
    "resolved in next contextual wrap review": "resolved in ongoing story wrap review",
    "The carried-forward scan has 93 open leads.":
        "The scan has 63 open leads in Lil's and Maria's routes. The Maria replay also showed an early break "
        "in Charles's next line, B208 R46. The queue includes the exact capture and stored text.",
    "Exact carry-forward of the ASCII progressive wrap scan. Every revised page received fresh native and visual checks.":
        "Exact carry-forward of the ASCII progressive wrap scan and one new finding from the initialized Maria excerpt.",
    "all_routes_next_review_wraps_20261118/research_v1/followup_wrap_queue.json":
        "all_routes_remaining_phrase_wraps_20261118/research_v1/followup_wrap_queue.json",
})
pair = checked_text(getsource(previous.pair_next), {
    "limits = (8, 1, 8, 7)": "limits = (0, 0, 28, 29)",
    "len(selected) >= sum(limits)": "len(selected) == len(leads) == 64",
})
env = vars(previous) | globals() | {"pair": previous.pair}
for code, label in ((verify, "registration"), (carry, "queue-carry-forward"), (pair, "source-pairing"),
                    (getsource(previous.main), "finish")):
    exec(compile(code, __file__ + "::" + label, "exec"), env)

if __name__ == "__main__":
    env["main"]()
