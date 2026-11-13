"""Current V1676 binding of original live-fleet8 close/compass prerequisites."""
import inspect
from pathlib import Path
from types import FunctionType
from scripts import native_sighting_context_v1109 as original

ROM=Path('out/all_routes_combined_v1676_candidate.nds')
water=FunctionType(original.water.__code__,{**original.__dict__,'ROM':ROM},argdefs=original.water.__defaults__)

def apply_fixture(arm,raw,request):
    source=inspect.getsource(original.apply_fixture)
    old='translations/sighting_grammar_editorial_release_v1.json';assert source.count(old)==1
    source=source.replace(old,'translations/search_reports_editorial_release_v1.json')
    env={**original.__dict__,'__file__':__file__,'ROM':ROM,'water':water}
    exec(compile(source,__file__,'exec'),env)
    return env['apply_fixture'](arm,raw,request)
