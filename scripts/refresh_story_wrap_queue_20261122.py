"""Carry verified editorial decisions forward into the current heuristic wrap queue."""

from collections import Counter

from scripts import register_rafael_diplomacy_and_friends_20261122 as current
from scripts import review_current_story_wraps_20261122 as baseline


base, native = current.base, current.native
OUTPUT = current.stage.draft.ROOT / "current_wrap_queue.json"


def main():
    assert not OUTPUT.exists()
    meta = base.load(current.RELEASE)
    assert base.digest(current.ROM) == meta["candidate_sha256"]
    assert base.digest(current.MANIFEST) == meta["manifest_sha256"]
    assert base.digest(base.REGISTRY) == meta["registry_sha256"]
    image = base.NdsImage.open(current.ROM)
    reviewed = {}
    for ledger in (current.parent.REVIEW, current.REVIEW):
        for row in base.load(ledger)["records"]:
            ref = row.get("registered_reference")
            if not ref:
                continue
            key = (row["file_path"], row["block"], ref["offset"])
            assert key not in reviewed
            reviewed[key] = row, ref, ledger

    stats, notices = {}, []
    for route in range(4):
        path = f"/data/SC{route}.DK4"
        archive = image.read_file(path)
        assert native.digest(archive) == meta[f"target_SC{route}_sha256"]
        totals, leads = baseline.scanner.scan(path, archive)
        for lead in leads:
            key = (path, lead["block"], lead["offset"])
            match = reviewed.get(key)
            if match:
                row, ref, ledger = match
                if lead["block_sha256"] == ref["block_sha256"] and lead["stored_body_hex"] == ref["exact_body_hex"]:
                    lead["reviewed"] = dict(id=row["id"], ledger=ledger.as_posix(), decision=row["decision"],
                                             finding=row["localization_note"])
        open_leads = [lead for lead in leads if "reviewed" not in lead]
        stats[path] = dict(totals) | dict(heuristic_leads=len(leads), needs_context=len(open_leads),
            early_clusters=Counter(lead["block"] for lead in open_leads if lead["block"] < 90).most_common(12))
        notices.extend(leads)

    base.save(OUTPUT, dict(candidate_sha256=meta["candidate_sha256"],
        exact_release_sha256=base.digest(current.RELEASE), stats=stats, records=notices,
        ledger_hashes={ledger.as_posix(): base.digest(ledger) for ledger in (current.parent.REVIEW, current.REVIEW)},
        screen_for_possible_wrap_issues_only=True, contextual_followup_needed=True, new_editorial_credit=0))
    print(f"{len(notices)} heuristic leads on the current candidate. "
          f"{sum('reviewed' in lead for lead in notices)} have current source-based decisions.")


if __name__ == "__main__":
    main()
