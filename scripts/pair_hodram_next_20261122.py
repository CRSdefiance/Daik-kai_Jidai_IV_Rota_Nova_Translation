"""Bind Hodram's opening and next post-lesson exchanges to the verified release."""

from collections import Counter

from scripts import pair_hodram_opening_20261122 as pairing
from scripts import register_hodram_opening_20261122 as build


base = pairing.base
SPANS = (range(0, 24), range(54, 71))
PACKAGES = (*pairing.PACKAGES, "20261119_battle_dialogue_followup", "20261121_refit_sailing_parallel_routes")


def main():
    for blocks in SPANS:
        root = pairing.ROOT.with_name(f"hodram_B{blocks.start}_B{blocks.stop - 1}_followup_20261122")
        packet_path, review_path = [root / name for name in ("paired_source_registered_candidate.json", "prior_contextual_decisions.json")]
        assert not packet_path.exists() and not review_path.exists()
        packet = pairing.source_and_current(build, blocks)
        root.mkdir(exist_ok=True)
        base.save(packet_path, packet)
        review = pairing.prior_decisions(packet, packet_path, PACKAGES)
        base.save(review_path, review)
        carried = len(review["reused_records"])
        pending = Counter(row["block"] for row in review["pending_records"])
        print(f"B{blocks.start}–{blocks.stop - 1}: {carried} exact prior decisions and {pending.total()} pending.")
        print(dict(sorted(pending.items())))


if __name__ == "__main__":
    main()
