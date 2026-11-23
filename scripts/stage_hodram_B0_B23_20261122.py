"""Compile the reviewed Hodram opening scenes with the registered native writer."""

from inspect import getsource
from types import SimpleNamespace

from scripts import register_hodram_opening_20261122 as parent
from scripts import review_hodram_B0_B23_20261122 as author
from scripts import stage_hodram_opening_20261122 as previous
from scripts.review_rafael_east_asia_followup_20261121 import company_scope, company_source
from scripts.source_locked_derivation_v5118 import checked_text


base, native, paired, compiler = previous.base, previous.native, author.paired, previous.compiler
SOURCE, ROOT = paired.PACKET, author.ROOT / "staged"
ROM, PROOF = ROOT / "Hodram_B0_B23_STAGED.nds", ROOT / "stored_proof.json"
OUTPUT = author.ROOT / "scoped_manuscript_v2.json"
BLOCKS = ((), tuple(author.DECISIONS), (), ())
TOKEN = previous.TOKEN
logical_end = previous.logical_end
FLEET_CELLS = 22

fleet_scope = company_scope | {"PLANNER": previous.PLANNER, "MAX_COMPANY_CELLS": FLEET_CELLS}
exec(compile(company_source, __file__ + "::fleet-widths", "exec"), fleet_scope)


def plan_progressive(row, selector, old, original):
    plan = fleet_scope["plan_progressive"] if "FO" in TOKEN.findall(row["english"]) else previous.plan_progressive
    return plan(row, selector, old, original)


collect = checked_text(getsource(previous.manuscript), {
    'len(reused) == 2': 'len(reused) == 6',
    'len(rows) == 120': 'len(rows) == 201',
    'contextual_records_revisited=118, contextual_decisions_reused=2':
        'contextual_records_revisited=195, contextual_decisions_reused=6',
    'draft["findings"]["retention"] + 2': 'draft["findings"]["retention"] + 6',
})
compile_rom = checked_text(getsource(previous.main), {
    '    scope["main"]()': '''    if not PROOF.exists():
        scope["main"]()
    else:
        proof = base.load(PROOF)
        assert proof["candidate_sha256"] == base.digest(ROM)
        assert proof["predecessor_sha256"] == base.digest(parent.ROM)
        assert proof["manuscript_sha256"] == base.digest(OUTPUT)
        assert proof["whole_parent_inverse"]''',
    '{paired.ARCHIVE: expected}': '{ARCHIVE: expected}',
})
ARCHIVE = previous.paired.ARCHIVE
scope = vars(previous) | globals()
for source in (collect, compile_rom):
    exec(compile(source, __file__ + "::source-qualified-opening", "exec"), scope)


if __name__ == "__main__":
    scope["main"]()
