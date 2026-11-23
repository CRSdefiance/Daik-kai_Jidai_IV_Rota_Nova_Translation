"""Verify the registered snapshot, carry the wrap queue forward and pair the next exchanges."""

from collections import Counter
from types import FunctionType

from scripts import prepare_london_guild_assignments_20261118 as pair
from scripts import register_all_routes_next_review_wraps_20261118 as registered

base, native = registered.base, registered.native
QUEUE = registered.stage.ROOT / "followup_wrap_queue.json"
NEXT = registered.stage.review.ROOT.with_name("all_routes_remaining_phrase_wraps_20261118")


def verify_registration():
    release = base.load(registered.RELEASE)
    registry, ledger, manifest = map(base.load, (base.REGISTRY, base.LEDGER, registered.MANIFEST))
    review = base.load(registered.REVIEW)
    assert release["candidate_sha256"] == base.digest(registered.ROM) == ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"] == manifest["release_stack_sha256"]
    assert base.digest(registered.MANIFEST) == release["manifest_sha256"]
    assert base.digest(registered.PATCH) == release["patch_sha256"] == base.digest(registered.stage.ROOT / "clean_input.xdelta")
    assert registered.ROM.read_bytes() == (registered.stage.ROOT / "clean_rebuilt.nds").read_bytes()
    assert len(manifest["batches"]) == 884 and len(manifest["checks"]) == 219 and all(manifest["checks"].values())
    earlier = base.load(release["predecessor"]["registry"])
    assert len(registry["accepted_layers"]) == 114 and registry["accepted_layers"] == earlier["accepted_layers"]
    assert "ascii_glyph_right_bounds" in registry["profiles"][registered.PROFILE]
    assert ledger["records_editorially_completed"] == 27700
    pending = ledger["pending_shared_consumer_checkpoint_20261114"]
    assert pending["remaining_total"] == 276 and pending["candidate_sha256"] == release["candidate_sha256"]
    assert len(review["records"]) == 132
    assert all(len(row["review"]) == 5 and all(row["review"].values()) for row in review["records"])
    assert base.digest(base.PROMOTED) == base.load(registered.VERIFY / "registration_mutation_plan.json")["main_sha256"]
    previous, current = map(base.NdsImage.open, (registered.parent.ROM, registered.ROM))
    for path in (native.ARM, "/COMMON/MESFILE.DK4", "/GRP/KANJI.FNT", "/_pxl/personinfo.pxl"):
        assert previous.read_file(path) == current.read_file(path)
    return release, review, previous, current


def carry_queue(release, review, previous, current):
    previous_queue = registered.stage.review.QUEUE
    queue = base.load(previous_queue)
    assert queue["candidate_sha256"] == base.digest(registered.parent.ROM) and queue["counts"]["open editorial lead"] == 114
    selected = {(r["file_path"], r["block"], r["current_reference"]["offset"], r["current_hex"]): r
                for r in review["records"] if r.get("wrap_lead")}
    banks = {f"/data/SC{i}.DK4": [native.IlnkContainer.parse(im.read_file(f"/data/SC{i}.DK4")).blocks
                                 for im in (previous, current)] for i in range(4)}
    closed = []
    for lead in queue["records"]:
        path, n, offset = (lead[k] for k in ("file_path", "block", "offset"))
        before, after = [bank[n] for bank in banks[path]]
        if before == after:
            if lead["disposition"] == "open editorial lead":
                assert native.digest(after) == lead["block_sha256"]
            continue
        payload = bytes([lead["source_selector"]]).hex() + lead["stored_body_hex"]
        row = selected[path, n, offset, payload]
        assert lead["disposition"] == "open editorial lead" and native.digest(before) == lead["block_sha256"]
        ref = row["registered_reference"]
        new = bytes.fromhex(ref["exact_stored_hex"])
        at = ref["offset"]
        assert after[at:at + len(new)] == new
        lead.update(disposition="resolved in next contextual wrap review",
                    review=ref | {"id": row["id"], "reason": row["localization_note"]})
        closed.append(row["id"])
    assert len(closed) == 21 and set(closed) == set(review["resolved_wrap_leads"])
    queue["candidate_sha256"] = release["candidate_sha256"]
    queue["counts"] = dict(Counter(r["disposition"] for r in queue["records"]))
    assert queue["counts"]["open editorial lead"] == 93
    queue["scope"] = "Exact carry-forward of the ASCII progressive wrap scan. Every revised page received fresh native and visual checks."
    queue["predecessor_queue"] = dict(path=str(previous_queue), sha256=base.digest(previous_queue))
    if QUEUE.exists():
        assert base.load(QUEUE) == queue
    else:
        base.save(QUEUE, queue)
    note = ("\nThe carried-forward scan has 93 open leads. "
            "[Current wrap queue](../work/all_routes_next_review_wraps_20261118/research_v1/followup_wrap_queue.json)\n")
    content = registered.DOC.read_text(encoding="utf-8")
    if note not in content:
        registered.DOC.write_text(content + note, encoding="utf-8", newline="\n")
    return [r for r in queue["records"] if r["disposition"] == "open editorial lead"]


def pair_next(leads, candidate):
    limits = (8, 1, 8, 7)
    blocks = tuple(tuple(dict.fromkeys(r["block"] for r in leads if r["file_path"] == f"/data/SC{i}.DK4"))[:limit]
                   for i, limit in enumerate(limits))
    assert tuple(map(len, blocks)) == limits
    contexts = tuple(f"Review {name}'s selected wraps in the complete exchange."
                     for name in ("Rafael", "Hodram", "Lil", "Maria"))
    packet = NEXT / "paired_source.json"
    if not packet.exists():
        scope = vars(pair) | dict(ROOT=NEXT, parent=registered, BLOCKS=blocks, CONTEXT=contexts)
        FunctionType(pair.main.__code__, scope)()
    paired = base.load(packet)
    assert paired["candidate_sha256"] == candidate
    refs = {(g["file_path"], g["block"], r["current_offset"], r["current_body_hex"]): r["source_record_index"]
            for g in paired["groups"] for r in g["records"]}
    scheduled = {(f"/data/SC{i}.DK4", n) for i, route_blocks in enumerate(blocks) for n in route_blocks}
    selected = []
    for lead in leads:
        key = (lead["file_path"], lead["block"], lead["offset"], lead["stored_body_hex"])
        if key[:2] in scheduled:
            selected.append(lead | {"source_record_index": refs[key]})
    assert len(selected) >= sum(limits)
    target = NEXT / "selected_wrap_leads.json"
    value = dict(candidate_sha256=candidate, queue_sha256=base.digest(QUEUE),
                 paired_source_sha256=base.digest(packet), records=selected)
    if not target.exists():
        base.save(target, value)
    else:
        assert base.load(target) == value
    print(f"Verified registered ROM and patch. Carried {len(leads)} open wrap leads forward and paired the next {len(selected)}.")


def main():
    release, review, previous, current = verify_registration()
    leads = carry_queue(release, review, previous, current)
    pair_next(leads, release["candidate_sha256"])


if __name__ == "__main__":
    main()
