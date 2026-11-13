"""Correct the frozen preparer's exact pre-replacement B179 message key."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B180_research_tools_v4800b')
if __name__=='__main__':
    assert not ROOT.exists()
    successor='scripts/prepare_lil_B180_research_v4800c.py'
    proof=derive('scripts/prepare_lil_B180_research_v4800.py',successor,{
        "'New B180 research:336 original loads/cache hits and672 modes pass;byte-identical V4701 parent proof reused exactly. Representative/release pending.':":
        "'New B179 research:336 original loads/cache hits and672 modes pass;byte-identical V4701 parent proof reused exactly. Representative/release pending.':"})
    ROOT.mkdir(parents=True);save(ROOT/'exact_key_correction.json',dict(tool=proof,reason='derive checks original keys before simultaneous replacement; the frozen producer used the already-replaced label.',no_previous_producer_overwritten=True,full_goal_complete=False))
    import runpy
    runpy.run_path(successor,run_name='__main__')
