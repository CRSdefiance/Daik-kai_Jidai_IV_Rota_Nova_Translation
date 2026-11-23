"""Stage the linked Hodram exchanges using the verified saga layout."""

from inspect import getsource

from scripts import review_hodram_B54_B60_20261122 as author
from scripts import stage_hodram_B0_B23_20261122 as previous
from scripts.source_locked_derivation_v5118 import checked_text


base, native, parent, paired = author.base, author.native, author.parent, author.paired
SOURCE, ROOT = paired.PACKET, author.ROOT / "B54_B60_staged"
ROM, PROOF = ROOT / "Hodram_B54_B60_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = author.ROOT / "B54_B60_scoped_manuscript.json"
BLOCKS = ((), author.SCOPE, (), ())
ARCHIVE, TOKEN, logical_end = author.ARCHIVE, previous.TOKEN, previous.logical_end
compiler, plan_progressive = previous.compiler, previous.plan_progressive
collect = checked_text(previous.collect, {
    'len(reused) == 6': 'len(reused) == 3',
    'len(rows) == 201': 'len(rows) == 82',
    'contextual_records_revisited=195, contextual_decisions_reused=6':
        'contextual_records_revisited=79, contextual_decisions_reused=3',
    'draft["findings"]["retention"] + 6': 'draft["findings"]["retention"] + 3',
})
scope = previous.scope | globals()
for source in (collect, previous.compile_rom):
    exec(compile(source, __file__ + "::verified-archive-stage", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
