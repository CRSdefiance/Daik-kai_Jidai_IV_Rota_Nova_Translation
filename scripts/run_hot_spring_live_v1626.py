"""Normal Search controls at the original legal shore in registered V1622."""
import inspect
from scripts import run_fatigue_recovery_live_v1603 as previous
if __name__=='__main__':
    source=inspect.getsource(previous)
    for old,new in [('scripts.native_fatigue_shore_fixture_v1602','scripts.native_hot_spring_location_v1625'),
        ('work/analysis/fatigue_status_release_v1593/registered_release_verification.json','work/analysis/hot_spring_release_v1621/registered_release_verification.json'),
        ('work/analysis/fatigue_recovery_live_v1603','work/analysis/hot_spring_live_v1626'),
        ('emulation_v193/fatigue_recovery_live_v1603_1594','emulation_v193/hot_spring_live_v1626_1622')]:
        assert source.count(old)==1;source=source.replace(old,new)
    env={**previous.__dict__,'__name__':'__main__','__file__':__file__};exec(compile(source,__file__,'exec'),env)
