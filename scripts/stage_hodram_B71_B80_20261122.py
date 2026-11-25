"""Stage the Hangzhou and war exchanges through the registered archive writer."""

from types import SimpleNamespace

from scripts import register_hodram_B65_B70_20261122 as parent
from scripts import review_hodram_B71_B80_20261122 as decisions
from scripts import stage_hodram_B65_B70_20261122 as previous
from scripts.stage_hodram_B0_B23_20261122 import compile_rom
from scripts.source_locked_derivation_v5118 import checked_text


base, native, paired = previous.base, previous.native, decisions.paired
author = SimpleNamespace(OUTPUT=decisions.COMBINED, GLYPHS=decisions.GLYPHS,
                         CONTEXTS=decisions.prior.CONTEXTS | decisions.CONTEXTS)
SOURCE, ROOT = paired.PACKET, decisions.ROOT / "B71_B80_staged"
ROM, PROOF = ROOT / "Hodram_B71_B80_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = decisions.ROOT / "B71_B80_scoped_manuscript.json"
BLOCKS = ((), tuple(range(71, 81)), (), ())
TOKEN, logical_end = previous.TOKEN, previous.logical_end

collect = checked_text(previous.collect, {
    'len(reused) == 3': 'len(reused) == 4',
    'len(rows) == 128': 'len(rows) == 144',
    'contextual_records_revisited=125, contextual_decisions_reused=3':
        'contextual_records_revisited=140, contextual_decisions_reused=4',
    'draft["findings"]["retention"] + 3': 'draft["findings"]["retention"] + 4',
})
scope = previous.scope | globals()
for source in (collect, compile_rom):
    exec(compile(source, __file__ + "::verified-archive-stage", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
