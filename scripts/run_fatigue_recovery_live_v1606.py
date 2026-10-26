"""Coherent original region2 Search context, normal inputs, no event forcing."""
import inspect
from scripts import run_fatigue_recovery_live_v1603 as prior
if __name__=='__main__':
    source=inspect.getsource(prior)
    for old,new in [('scripts.native_fatigue_shore_fixture_v1602','scripts.native_fatigue_region2_fixture_v1605'),
        ('work/analysis/fatigue_recovery_live_v1603','work/analysis/fatigue_recovery_live_v1606'),
        ('emulation_v193/fatigue_recovery_live_v1603_1594','emulation_v193/fatigue_recovery_live_v1606_1594')]:
        assert source.count(old)==1;source=source.replace(old,new)
    env={**prior.__dict__,'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
