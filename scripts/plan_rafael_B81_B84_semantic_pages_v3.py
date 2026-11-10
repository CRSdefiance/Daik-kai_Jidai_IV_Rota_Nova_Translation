"""Keep exact closing clauses together using formatter-owned native page completion."""
import linecache
from scripts import plan_rafael_B81_B84_subset_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "    plan=env['plan']":
        """    semantic_adapter=checked_text(adapter,{
        '        if line==limit:return None':
            '        if line==limit:return None\\n        if page_start==start and 0<line<4:\\n            tail=solve(start,4)\\n            if tail is not None:\\n                cost,breaks=tail\\n                return (cost[0],cost[1]+4-line,cost[2],cost[3]),(*([start]*(4-line)),*breaks)',
        \"assert ' '.join(lines)==body;markup=\":
            \"assert ' '.join(v for v in lines if v)==body;assert all(any(lines[i:i+4]) for i in range(0,len(lines),4));markup=\",
        'for a,b in zip(lines,lines[1:])':
            'for a,b in zip(lines,lines[1:]) if a.strip() and b.strip()',
        'max_total_rows=limit,':
            'formatter_owned_semantic_page_completion_rows=[i for i,v in enumerate(lines) if not v],max_total_rows=limit,',
    })
    adapter=semantic_adapter
    exec(compile(adapter,__file__+'::formatter-owned-native-row-completion-at-source-bound-clause','exec'),env)
    plan=env['plan']""",
    "assert ' '.join(result['lines'])==row['english']":
        "assert ' '.join(v for v in result['lines'] if v)==row['english']",
})
env={**previous.env,'qualify_source':previous.qualify_source,'__file__':__file__}
filename=__file__+'::same-bounds-words-controls-semantic-page-boundary'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env);main=env['main']
if __name__=='__main__':main()
