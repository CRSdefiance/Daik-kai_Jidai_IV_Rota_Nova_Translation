"""Stage Sera's memories, the Nagarpur procession and the sea-king legend."""

from scripts import review_hodram_B61_B64_20261122 as author
from scripts import stage_hodram_B54_B60_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, paired = author.base, author.native, author.parent, author.paired
SOURCE, ROOT = paired.PACKET, author.ROOT / "B61_B64_staged_v3"
ROM, PROOF = ROOT / "Hodram_B61_B64_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = author.ROOT / "B61_B64_scoped_manuscript_v3.json"
BLOCKS = ((), author.SCOPE, (), ())
TOKEN, logical_end = previous.TOKEN, previous.logical_end

collect = checked_text(previous.collect, {
    'len(reused) == 3': 'len(reused) == 1',
    'len(rows) == 82': 'len(rows) == 96',
    'contextual_records_revisited=79, contextual_decisions_reused=3':
        'contextual_records_revisited=95, contextual_decisions_reused=1',
    'draft["findings"]["retention"] + 3': 'draft["findings"]["retention"] + 1',
})
scope = previous.scope | globals()
exec(compile(collect, __file__ + "::verified-archive-stage", "exec"), scope)
exec(compile(previous.previous.compile_rom, __file__ + "::verified-archive-stage", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
