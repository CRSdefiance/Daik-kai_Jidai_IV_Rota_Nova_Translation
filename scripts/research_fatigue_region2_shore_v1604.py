"""Original terrain-only region2 shore research; no event or RNG manipulation."""
import inspect
from pathlib import Path
from scripts import research_fatigue_shore_v1587c as prior
if __name__=='__main__':
    source=inspect.getsource(prior)
    for old,new in [("work/analysis/fatigue_shore_context_v1587c","work/analysis/fatigue_region2_shore_v1604"),
        ('out/all_routes_combined_v1578_candidate.nds','out/all_routes_combined_v1594_candidate.nds'),
        ('region in [2,3]','region == 2'),("q['original_event_region'] in [2,3]","q['original_event_region'] == 2")]:
        assert source.count(old)==1,old;source=source.replace(old,new)
    env={**prior.__dict__,'__name__':'__main__','__file__':__file__}
    exec(compile(source,__file__,'exec'),env)
