"""Preserve the preflight stop on an existing research filename;use a fresh ROM path."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B225_English_fixture_repair_v7219b')
if __name__=='__main__':
    assert not ROOT.exists() and Path('out/lil_B225_English_v7203_reviewed_English_RESEARCH_ONLY.nds').exists() and not Path('out/lil_B225_English_v7219_reviewed_English_RESEARCH_ONLY.nds').exists() and not Path('work/analysis/lil_B225_English_fixture_v7219').exists()
    target='scripts/research_lil_B225_English_fixture_v7219b.py';assert not Path(target).exists();r=derive('scripts/research_lil_B225_English_fixture_v7219.py',target,{'English_v7203_reviewed_English':'English_v7219_reviewed_English'});ROOT.mkdir(parents=True);save(ROOT/'source_locked_fresh_ROM_filename.json',dict(tool=r,old_ROM_preserved_preflight_stopped_before_any_write=True,no_source_prose_control_schedule_orreference_change=True,new_credit=0))
