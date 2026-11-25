"""Correct rejected full-word values from actual source/current instructions; retain both failures."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B209_source_tools_v6450c')
if __name__=='__main__':
    assert not ROOT.exists()
    r=derive('scripts/map_lil_B209_source_v6450b.py','scripts/map_lil_B209_source_v6450c.py',{
        'source_v6450b\')':'source_v6450c\')',
        'lil_B209_source_span_binding_v6450b':'lil_B209_source_span_binding_v6450c',
        'source_span_matches_registered_pointer_literals':'source_span_matches_registered_renderer_branches',
    })
    ROOT.mkdir(parents=True);save(ROOT/'prepared_tool.json',dict(tool=r,earlier_failures_preserved=True,correction='Three changed words are registered ARM BL instructions,not pointer data. The prior fresh helper incorrectly guessed high byte02 from a byte-difference listing;all three actual complete words have EB. This successor binds measured full clean/current words and whole current ARM9 equality to V6380. No game code or guard was changed.',source_current_instruction_words=[['0x242C8','0xEB00BD91','0xEB0E02BD'],['0x24310','0xEB00BD7F','0xEB0E02AB'],['0x24330','0xEB00BD77','0xEB0E02A3']],no_ROM_registry_ledger_mutation_before_rejections=True,full_goal_complete=False))
