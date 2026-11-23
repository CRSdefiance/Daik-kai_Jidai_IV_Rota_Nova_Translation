"""Bind the next Hodram exchanges to the cumulative candidate."""

from collections import Counter

from scripts import pair_hodram_opening_20261122 as pairing
from scripts import pair_hodram_B131_B150_20261122 as previous
from scripts import register_hodram_B131_B150_20261122 as build


base = pairing.base
BLOCKS = range(151,161)
ROOT = pairing.ROOT.with_name("hodram_B151_B160_followup_20261122")
PACKET,CARRY = [ROOT/name for name in ("paired_source_registered_candidate.json","prior_contextual_decisions.json")]
PACKAGES = (*previous.PACKAGES,"20261122_hodram_B131_B150")


def main():
    assert not PACKET.exists() and not CARRY.exists()
    packet = pairing.source_and_current(build,BLOCKS)
    assert sum(len(g["records"]) for g in packet["groups"]) == 331
    ROOT.mkdir(exist_ok=True)
    base.save(PACKET,packet)
    carry = pairing.prior_decisions(packet,PACKET,PACKAGES)
    base.save(CARRY,carry)
    pending = Counter(row["block"] for row in carry["pending_records"])
    print(f"{len(carry['reused_records'])} exact prior decisions and {pending.total()} fresh comparisons.")
    print(dict(sorted(pending.items())))


if __name__ == "__main__":
    main()

