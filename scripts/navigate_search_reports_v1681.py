"""Ordinary Search navigation;stop on any revised report,hot spring,or unknown UI."""
import inspect
from pathlib import Path
from types import FunctionType
from scripts import navigate_hot_spring_search_v1648 as previous
from scripts import observe_hot_spring_navigation_v1641b as observer
from scripts.navigate_hot_spring_crew_v1652 import visible_paper
from dk4tool.patch.search_reports_editorial import current_entries
from scripts.search_reports_native_plan_v1661 import IDS

if __name__=='__main__':
    root=Path('work/analysis/search_reports_live_v1680')
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/search_reports_live_v1680_1676')
    source=inspect.getsource(previous.main)
    old="'out/all_routes_combined_v1637_candidate.nds'";assert source.count(old)==1
    source=source.replace(old,"'out/all_routes_combined_v1676_candidate.nds'")
    old="        template = raw[owner + 0x2030:owner + 0x2230].split(b'\\0')[0]"
    new="""        if not visible_paper(picture):
            record({'frame':frame,'stop':'not Sea View or visible dialogue;loaded buffers may be stale;no input sent'})
            break
"""+old
    assert source.count(old)==1;source=source.replace(old,new)
    old='if any(n in {310, *range(2275, 2288)} for n in ids):';assert source.count(old)==1
    source=source.replace(old,'if any(n in TARGETS for n in ids):')
    source=source.replace('hot spring requires direct inspection and separate full verification','revised report or pending hot spring requires direct inspection and full verification')
    mode=FunctionType(observer.mode.__code__,{**observer.__dict__,'ROOT':root,'CAP':cap},argdefs=observer.mode.__defaults__)
    env={**previous.__dict__,'__file__':__file__,'ROOT':root,'CAP':cap,'JOURNAL':root/'navigation.jsonl',
         'EVENTS':root/'bounded_navigator_v1681.jsonl','visible_paper':visible_paper,'mode':mode,'current_entries':current_entries,
         'KNOWN':{308,309,2234,2239,2244,2245,339},'TARGETS':set(IDS)|{310,*range(2275,2288)}}
    exec(compile(source,__file__,'exec'),env);env['main']()
