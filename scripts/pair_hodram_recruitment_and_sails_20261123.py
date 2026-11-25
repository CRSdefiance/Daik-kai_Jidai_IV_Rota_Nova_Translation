"""Bind six complete Hodram exchanges to the current registered ROM."""

from collections import Counter

from scripts import cleanup_hodram_midroute_followups_20261123 as checkpoint
from scripts import pair_hodram_angelo_recruitment_20261123 as angelo
from scripts import pair_hodram_midroute_followups_20261123 as established
from scripts import register_hodram_midroute_followups_20261123 as release

base, native, ARCHIVE = angelo.base, angelo.native, angelo.ARCHIVE
OUTPUT = angelo.OUTPUT.parent / "hodram_recruitment_and_sails_paired.json"
INTERVALS = {"B151_B160": (157, 159), "B161_B170": (161,), "B171_B180": (171,)}


def main():
    assert not OUTPUT.exists()
    active, queue, recruitment = map(base.load, (release.RELEASE, checkpoint.QUEUE, angelo.OUTPUT))
    candidate = base.digest(release.ROM)
    assert candidate == active["candidate_sha256"] == queue["candidate_sha256"] == recruitment["candidate_sha256"]
    clean_digest = base.digest(native.CLEAN)
    assert clean_digest == active["clean_input_sha256"] == recruitment["clean_sha256"]
    assert base.digest(base.REGISTRY) == active["registry_sha256"]
    images = [base.NdsImage.open(path) for path in (native.CLEAN, release.ROM)]
    files = [image.read_file(ARCHIVE) for image in images]
    hashes = [native.digest(data) for data in files]
    assert hashes[1] == active["target_SC1_sha256"]
    arms = [image.read_file(native.ARM) for image in images]
    blocks = [native.IlnkContainer.parse(data).blocks for data in files]

    def bind(block, records):
        leads = {row["offset"]: row for row in queue["records"]
                 if row["file_path"] == ARCHIVE and row["block"] == block and "reviewed" not in row}
        return established.binding["bind_block"](block, records, [bank[block] for bank in blocks], hashes, arms, leads)

    references = {str(angelo.OUTPUT): base.digest(angelo.OUTPUT), str(release.REVIEW): base.digest(release.REVIEW)}
    priest = []
    for row in base.load(release.REVIEW)["records"]:
        if row["block"] != 110:
            continue
        ref = row["registered_reference"]
        selector = row["source_selector"]
        registered = ref | dict(exact_stored_hex=bytes([selector]).hex() + ref["exact_body_hex"])
        priest.append(row | dict(native_command_word=0x4000, selector=selector, slots=[],
                                  registered_reference=registered))
    groups = [bind(110, priest), recruitment["group"]]
    warning, = [row for row in groups[0]["records"] if row["id"] == "DK4_MES_B110_R0047"]
    assert "I tell" in warning["current_English"]
    for interval, numbers in INTERVALS.items():
        path = release.REVIEW.parents[2] / f"all_routes_editorial_20261122_hodram_{interval}_candidate/verification/registered_review.json"
        references[str(path)] = base.digest(path)
        source = base.load(path)["records"]
        groups.extend(bind(block, [row for row in source if row["block"] == block]) for block in numbers)
    groups.sort(key=lambda group: group["block"])
    count = Counter(row["native_command_word"] for group in groups for row in group["records"])
    assert count == {0x4000: 194, 0x2100: 2}
    assert sum(len(group["open_wrap_leads"]) for group in groups) == 8
    base.save(OUTPUT, dict(candidate_sha256=candidate, clean_sha256=clean_digest,
        groups=groups, earlier_reviews=references, contextual_review_pending=True, new_review_credit=0,
        ordinary_display_leads=recruitment["ordinary_Istanbul_display_leads"],
        focused_display_leads=[dict(id=warning["id"], offset=warning["current_offset"],
            observed_break_after="I tell", evidence_reference=str(release.VERIFY / "verified_gameplay.json"))]))
    print("Bound 196 texts in six exchanges, including eight queued wrap leads and two original choices.")


if __name__ == "__main__":
    main()
