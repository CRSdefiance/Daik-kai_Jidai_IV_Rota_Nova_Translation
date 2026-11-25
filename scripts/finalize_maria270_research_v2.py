"""Qualify zero style objects explicitly rather than requesting absent style-case metadata."""
from scripts.finalize_maria270_research_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "assert sum(len(x['rejected']) for x in styles['compiler_negatives']) == 0":
        "assert not stored['style_records'] and not styles['objects'] and styles['physical_alternatives']==styles['native_target_slot_cases']==0",
})
exec(compile(source,__file__+'::same-five-gates-explicit-empty-style-scope','exec'),globals())
