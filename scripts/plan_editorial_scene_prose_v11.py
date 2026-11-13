"""Preserve whole coda/clause boundaries and prevent two observed FE blank rows."""
import inspect
import linecache
from scripts import plan_editorial_scene_prose_v10 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    '    def page_cut_penalty(row,words,stop,line,final):':
    '''    page_phrases.update({
        'DK4_MES_B117_R0031': "We'll entrust it to you.",
        'DK4_MES_B120_R0036': 'Japan barely escaped disaster.',
        'DK4_MES_B121_R0118': "It's no use just sitting here with me.",
        'DK4_MES_B123_R0089': 'and the brutal soldiers who plunder it.',
        'DK4_MES_B123_R0118': 'to stop them.',
        'DK4_MES_B123_R0124': 'we can meet them on equal terms or better.',
        'DK4_MES_B129_R0077': 'No one will be allowed to trade without its permission.',
    })
    adapter=checked_text(adapter,{
        "cells=38 if row['kind']=='system-FE' else 36;limit=4;":
        "cells=(36 if row['id'] in ('DK4_MES_B118_R0022','DK4_MES_B127_R0053') else 38) if row['kind']=='system-FE' else 36;limit=4;",
    })
    def page_cut_penalty(row,words,stop,line,final):''',
    '    pairs=previous.PAIRS|':
        "    pairs=previous.PAIRS|{('let','me'),('me','ask'),('ask','you'),('you','another'),('fills','up'),('turn','them'),('equal','terms'),('stop','them')}|",
    '        FE_geometry_source=':
        "        FE_source_scoped_guard_budget_findings=['DK4_MES_B118_R0022','DK4_MES_B127_R0053'],FE_native_physical_width_228_unchanged=True,FE_row_budget_36_only_for_two_observed_extra_wraps=True,\n        FE_geometry_source=",
})
env={**previous.main.__globals__,'__file__':__file__}
filename=__file__+'::source-scoped-page-cadence-and-observed-FE-guard-wraps'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']
if __name__=='__main__':main()
