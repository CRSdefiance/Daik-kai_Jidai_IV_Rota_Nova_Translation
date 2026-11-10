"""Reflow only byte-bound visual findings using existing width and guard rules."""
import inspect
import linecache
from scripts import plan_hodram_B151_B170_apology as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "    args=parser.parse_args();assert not args.out.exists()":
        "    parser.add_argument('--preferences',type=Path,required=True)\n    args=parser.parse_args();assert not args.out.exists()\n    preferences=load(args.preferences)",
    "    bound_zero_bodies,source_bindings=qualify_source(doc)":
        """    original={r['id']:r for r in doc['records']}
    assert set(args.ids)==set(preferences['records'])
    for ident,pref in preferences['records'].items():
        assert all(sha(original[ident][k].encode('utf-8'))==v for k,v in pref['bindings'].items())
    bound_zero_bodies,source_bindings=qualify_source(doc)""",
    '    env={**previous.ENV,':
        """    scoped=preferences['records']
    coherent={k:{tuple(p) for p in v.get('coherent_pairs',[])} for k,v in scoped.items()}
    clauses={k:v['page_clause'] for k,v in scoped.items() if 'page_clause' in v}
    one_page={k for k,v in scoped.items() if v.get('one_page')}
    adapter=checked_text(adapter,{
        'or pair in PAIRS));': 'or pair in PAIRS or pair in COHERENT.get(row[\\'id\\'],set())));',
        '    @cache':
            "    clause=PAGE_PHRASES.get(row['id']);target=clause.split() if clause else []\\n    starts=[i for i in range(len(words)-len(target)+1) if words[i:i+len(target)]==target] if target else []\\n    assert not target or len(starts)==1\\n    page_start=starts[0] if starts else None\\n    @cache",
        '            tail=solve(stop,line+1)':
            '            if line==3 and not final and page_start is not None and stop!=page_start:continue\\n            tail=solve(stop,line+1)',
        'if result is None or result[0][0]>0:limit=8;solve.cache_clear();result=solve(0,0)':
            "if row['id'] not in ONE_PAGE and (result is None or result[0][0]>0):limit=8;solve.cache_clear();result=solve(0,0)",
    })
    env={**previous.ENV,'COHERENT':coherent,'PAGE_PHRASES':clauses,'ONE_PAGE':one_page,""",
    "            rows.append(result)":
        "            result['scoped_visual_preference']=scoped[row['id']]\n            rows.append(result)",
    "        coherent_pairs=sorted(pairs),":
        "        visual_preferences=str(args.preferences),visual_preferences_sha256=sha(args.preferences.read_bytes()),\n        coherent_pairs=sorted(pairs),",
})
env={**previous.main.__globals__,'__file__':__file__}
filename=__file__+'::exact-byte-bound-visual-findings'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']
if __name__=='__main__':main()
