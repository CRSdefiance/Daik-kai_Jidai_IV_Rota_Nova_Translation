"""Stage the complete miracle, treasure, and Proof of Conquest exchanges."""

from types import SimpleNamespace

from scripts import register_hodram_B81_B89_20261122 as parent
from scripts import review_hodram_B95_B110_20261122 as decisions
from scripts import refine_hodram_B91_B110_visual_20261122 as visual
from scripts.compact_hodram_wraps_20261122 import qualified_plan
from scripts import stage_hodram_B81_B89_20261122 as previous
from scripts.stage_hodram_B0_B23_20261122 import compile_rom
from scripts.source_locked_derivation_v5118 import checked_text


base, native, paired = previous.base, previous.native, decisions.paired
author = SimpleNamespace(OUTPUT=visual.OUTPUT, GLYPHS=set(),
                         CONTEXTS=decisions.previous.CONTEXTS | decisions.CONTEXTS)
SOURCE, ROOT = paired.PACKET, decisions.ROOT / "B91_B110_staged_v2"
ROM, PROOF = ROOT / "Hodram_B91_B110_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = decisions.ROOT / "B91_B110_scoped_manuscript_v2.json"
BLOCKS = ((), tuple(sorted(author.CONTEXTS)), (), ())
TOKEN, logical_end = previous.TOKEN, previous.logical_end

collect = checked_text(previous.collect, {
    'len(reused) == 9': 'len(reused) == 2',
    'len(rows) == 306': 'len(rows) == 211',
    'contextual_records_revisited=297, contextual_decisions_reused=9':
        'contextual_records_revisited=209, contextual_decisions_reused=2',
    'draft["findings"]["retention"] + 9': 'draft["findings"]["retention"] + 2',
})
def plan_progressive(row, selector, old, original):
    ident = row["id"].partition("_B")[2]
    planner = qualified_plan if ident in visual.PHRASES else previous.scope["plan_progressive"]
    return planner(row, selector, old, original)


scope = previous.scope | globals()
for source in (collect, compile_rom):
    exec(compile(source, __file__ + "::verified-archive-stage", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
