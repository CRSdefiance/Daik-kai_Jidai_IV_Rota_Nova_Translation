"""Stage the Hodram farewell, Batavia feud and the recovery of Kuhn's assets."""

from scripts import review_hodram_B65_B70_20261122 as author
from scripts import stage_hodram_B61_B64_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, paired = author.base, author.native, author.parent, author.paired
SOURCE, ROOT = paired.PACKET, author.ROOT / "B65_B70_staged"
ROM, PROOF = ROOT / "Hodram_B65_B70_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = author.ROOT / "B65_B70_scoped_manuscript.json"
BLOCKS = ((), author.SCOPE, (), ())
TOKEN, logical_end = previous.TOKEN, previous.logical_end

collect = checked_text(previous.collect, {
    'len(reused) == 1': 'len(reused) == 3',
    'len(rows) == 96': 'len(rows) == 128',
    'contextual_records_revisited=95, contextual_decisions_reused=1':
        'contextual_records_revisited=125, contextual_decisions_reused=3',
    'draft["findings"]["retention"] + 1': 'draft["findings"]["retention"] + 3',
})
scope = previous.scope | globals()
exec(compile(collect, __file__ + "::verified-archive-stage", "exec"), scope)
exec(compile(previous.previous.previous.compile_rom, __file__ + "::verified-archive-stage", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
