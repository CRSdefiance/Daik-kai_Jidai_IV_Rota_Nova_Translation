"""Bind the cathedral, riddle, and village sequences to the cumulative candidate."""

from collections import Counter

from scripts import pair_hodram_next_20261122 as prior
from scripts import pair_hodram_opening_20261122 as pairing
from scripts import register_hodram_B91_B110_20261122 as build


base = pairing.base
BLOCKS = range(111, 131)
ROOT = pairing.ROOT.with_name("hodram_B111_B130_followup_20261122")
PACKET, CARRY = [ROOT / name for name in ("paired_source_registered_candidate.json", "prior_contextual_decisions.json")]
PACKAGES = (*prior.PACKAGES, "20261122_hodram_B91_B110", "20261122_hodram_B81_B89")


def main():
    assert not PACKET.exists() and not CARRY.exists()
    packet = pairing.source_and_current(build, BLOCKS)
    assert sum(len(group["records"]) for group in packet["groups"]) == 323
    ROOT.mkdir(exist_ok=True)
    base.save(PACKET, packet)
    carry = pairing.prior_decisions(packet, PACKET, PACKAGES)
    base.save(CARRY, carry)
    pending = Counter(row["block"] for row in carry["pending_records"])
    print(f"{len(carry['reused_records'])} exact prior decisions and {pending.total()} fresh comparisons.")
    print(dict(sorted(pending.items())))


if __name__ == "__main__":
    main()

