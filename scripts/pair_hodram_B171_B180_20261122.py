"""Bind the next ten Hodram blocks to the registered ship and tavern build."""

from collections import Counter

from scripts import pair_hodram_B161_B170_20261122 as previous
from scripts import register_hodram_B161_B170_20261122 as build


base, pairing = previous.base, previous.pairing
BLOCKS = range(171,181)
ROOT = previous.ROOT.with_name("hodram_B171_B180_followup_20261122")
PACKET, CARRY = [ROOT / name for name in ("paired_source_registered_candidate.json", "prior_contextual_decisions.json")]
PACKAGES = (*previous.PACKAGES, "20261122_hodram_B161_B170")


def main():
    assert not PACKET.exists() and not CARRY.exists()
    packet = pairing.source_and_current(build, BLOCKS)
    assert sum(len(g["records"]) for g in packet["groups"]) == 315
    ROOT.mkdir(exist_ok=True)
    base.save(PACKET, packet)
    carry = pairing.prior_decisions(packet, PACKET, PACKAGES)
    base.save(CARRY, carry)
    print(f"{len(carry['reused_records'])} exact prior decisions and {len(carry['pending_records'])} fresh comparisons.")
    print(dict(sorted(Counter(row["block"] for row in carry["pending_records"]).items())))


if __name__ == "__main__":
    main()
