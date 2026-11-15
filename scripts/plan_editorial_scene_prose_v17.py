"""Apply recorded, byte-bound visual findings without changing prose or native geometry."""
import inspect
import linecache

from scripts import plan_editorial_scene_prose_v16 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(previous.main), {
    "    args=parser.parse_args();assert not args.out.exists()":
    """    parser.add_argument('--preferences',type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    preferences=load(args.preferences)""",
    "    bound_zero_bodies,source_bindings=qualify_source(doc)":
    """    by_id={r['id']:r for r in doc['records']}
    for record_id,preference in preferences['records'].items():
        row=by_id[record_id]
        for key in ['source_hex','current_hex','english']:
            assert sha(row[key].encode('utf-8'))==preference['bindings'][key],(record_id,key)
    bound_zero_bodies,source_bindings=qualify_source(doc)""",
    "    def page_cut_penalty(row,words,stop,line,final):":
    """    page_phrases.update({k:v['page_clause'] for k,v in preferences['records'].items() if 'page_clause' in v})
    def page_cut_penalty(row,words,stop,line,final):""",
    "    env={**previous.ENV,":
    """    adapter=checked_text(adapter,{
        "ordinary=pair in ({('quite','a')} if row['id']=='DK4_MES_B85_R0123' else set());":
        "ordinary=pair in ({('quite','a')} if row['id']=='DK4_MES_B85_R0123' else set()) or pair in ORDINARY.get(row['id'],set());",
        'or pair in PAIRS));':"or pair in PAIRS or pair in COHERENT.get(row['id'],set())));",
        "if row['kind']!='system-FE' and (result is None or result[0][0]>0):":
        "if row['kind']!='system-FE' and row['id'] not in ONE_PAGE and (result is None or result[0][0]>0):",
        "cells=(37 if row['id']=='DK4_MES_B134_R0028' else 36 if row['id'] in ('DK4_MES_B118_R0022','DK4_MES_B127_R0053','DK4_MES_B134_R0028','DK4_MES_B135_R0035','DK4_MES_B136_R0027') else 38) if row['kind']=='system-FE' else 36;":
        "cells=FE_CELLS.get(row['id'],38) if row['kind']=='system-FE' else 36;",
    })
    scoped=preferences['records']
    ordinary={k:{tuple(p) for p in v.get('ordinary_boundaries',[])} for k,v in scoped.items()}
    coherent={k:{tuple(p) for p in v.get('coherent_pairs',[])} for k,v in scoped.items()}
    one_page={k for k,v in scoped.items() if v.get('one_page')}
    fe_cells={'DK4_MES_B118_R0022':36,'DK4_MES_B127_R0053':36,'DK4_MES_B134_R0028':37,'DK4_MES_B135_R0035':36,'DK4_MES_B136_R0027':36}
    fe_cells.update({k:v['FE_planning_cells'] for k,v in scoped.items() if 'FE_planning_cells' in v})
    env={**previous.ENV,'ORDINARY':ordinary,'COHERENT':coherent,'ONE_PAGE':one_page,'FE_CELLS':fe_cells,""",
    "        coherent_pairs=sorted(pairs),":
    """        visual_preferences=str(args.preferences),visual_preferences_sha256=sha(args.preferences.read_bytes()),
        record_scoped_preferences=preferences['records'],
        coherent_pairs=sorted(pairs),""",
    "FE_source_scoped_guard_budget_findings=['DK4_MES_B118_R0022','DK4_MES_B127_R0053','DK4_MES_B134_R0028','DK4_MES_B135_R0035','DK4_MES_B136_R0027']":
    "FE_source_scoped_guard_budget_findings=sorted(fe_cells)",
    "FE_source_scoped_planning_cells={'DK4_MES_B118_R0022':36,'DK4_MES_B127_R0053':36,'DK4_MES_B134_R0028':37,'DK4_MES_B135_R0035':36,'DK4_MES_B136_R0027':36}":
    "FE_source_scoped_planning_cells=fe_cells",
})

env = {**previous.main.__globals__, '__file__': __file__}
filename = __file__ + '::exact-record-visual-preferences'
linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
exec(compile(source, filename, 'exec'), env)
main = env['main']

if __name__ == '__main__':
    main()
