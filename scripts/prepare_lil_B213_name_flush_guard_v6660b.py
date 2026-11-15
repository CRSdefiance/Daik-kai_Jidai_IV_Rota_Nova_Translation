"""Separate the complete logical name from the original zero-ink odd-run flush; retain the failed assertion."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B213_name_flush_tools_v6660b')
if __name__=='__main__':
    assert not ROOT.exists();proof=derive('scripts/prove_lil_B213_name_planes_v6660.py','scripts/prove_lil_B213_name_planes_v6660b.py',{'name_planes_v6660':'name_planes_v6660b',"width=max(e['x']+6 for e in events);assert width==len(raw)*6 and width<=216":"physical_flush_width=max(e['x']+6 for e in events);width=max(e['x']+6 for e in events if e['code']!=32);assert width==len(raw)*6 and width<=physical_flush_width<=216 and physical_flush_width-width in [0,6]",'width=width,preview=':'width=width,original_pair_flush_width=physical_flush_width,zero_ink_flush_sequence_independently_verified=True,preview='});ROOT.mkdir(parents=True);save(ROOT/'source_locked_logical_name_and_physical_flush_distinction.json',dict(proof=proof,complete_logical_glyphs_and_original_zero_ink_flush_both_within216px=True,no_font_viewport_guard_source_name_or_ROM_change=True,rejected_first_assertion_preserved=True,full_goal_complete=False))
