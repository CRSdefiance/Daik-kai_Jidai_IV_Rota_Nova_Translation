"""V1676 binding of source-proven48/20/10-byte location,supply,crew test fixtures."""
import inspect
from pathlib import Path
from types import SimpleNamespace
from scripts import native_fatigue_region2_fixture_v1605 as source_location
from scripts import native_hot_spring_provisions_v1642 as source_supply
from scripts import native_hot_spring_crew_v1650 as source_crew
from scripts.native_hot_spring_resilient_v1644 import preserve_natural_health

ROM=Path('out/all_routes_combined_v1676_candidate.nds')
ROOT=Path('work/analysis/search_reports_fixture_v1679')
REQUEST=source_crew.REQUEST
previous=SimpleNamespace(REQUEST=source_supply.REQUEST)


def location(arm,raw,request):
    source=preserve_natural_health(inspect.getsource(source_location.apply_fixture))
    old="read('work/analysis/fatigue_status_release_v1593/registered_release_verification.json')['ARM9_sha256']"
    assert source.count(old)==1
    source=source.replace(old,"read('translations/search_reports_editorial_release_v1.json')['target_arm9_sha256']")
    env={**source_location.__dict__,'__file__':__file__,'ROM':ROM,'ROOT':ROOT}
    exec(compile(source,__file__,'exec'),env);after,proof=env['apply_fixture'](arm,raw,request)
    proof['naturally_changed_Hull_Crew_preserved_no_recruitment_or_healing']=True
    return after,proof


def apply_fixture(arm,raw,request):
    if request==REQUEST:
        source=inspect.getsource(source_crew.apply_fixture)
        env={**source_crew.__dict__,'__file__':__file__,'ROM':ROM,'ROOT':ROOT}
    elif request==source_supply.REQUEST:
        source=preserve_natural_health(inspect.getsource(source_supply.apply_fixture))
        env={**source_supply.__dict__,'__file__':__file__,'ROM':ROM,'ROOT':ROOT,'location':SimpleNamespace(apply_fixture=location)}
    else:
        assert request==source_location.REQUEST
        return location(arm,raw,request)
    old='translations/hot_spring_notice_editorial_release_v1.json'
    assert source.count(old)==1;source=source.replace(old,'translations/search_reports_editorial_release_v1.json')
    exec(compile(source,__file__,'exec'),env)
    return env['apply_fixture'](arm,raw,request)
