"""Replan selected records, preserving a source-specific complete apology clause."""
import inspect
import linecache
from scripts import plan_hodram_B151_B170_ordinary as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "    parser.add_argument('--out',type=Path,required=True)":
        "    parser.add_argument('--out',type=Path,required=True)\n    parser.add_argument('--ids',nargs='+',required=True)",
    "    selectors=sorted(":
        "    source_rows=[r for r in source_rows if r['id'] in args.ids]\n    assert {r['id'] for r in source_rows}==set(args.ids)\n    selectors=sorted(",
    '    page_phrases={': '''    adapter=checked_text(adapter,{
        "terminal=words[stop-1].rstrip('\\\\\\\"\\\\\\')').endswith(('.', '!', '?', ';', ':'));":
        "terminal=(words[stop-1].rstrip('\\\\\\\"\\\\\\')').endswith(('.', '!', '?', ';', ':')) or (row['id']=='DK4_MES_B159_R0112' and start==0 and words[stop-1]=='sorry,'));",
    })
    page_phrases={''',
})
env={**previous.main.__globals__,'__file__':__file__}
filename=__file__+'::selected-source-apology-clause'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']
if __name__=='__main__':main()
