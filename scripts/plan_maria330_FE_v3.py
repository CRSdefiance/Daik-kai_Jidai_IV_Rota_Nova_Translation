"""Retain two exact byte-bound ordinary English boundaries; keep all native guard checks."""
import inspect
import linecache
from scripts import plan_maria330_FE_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.main),{
    "assert row['id']=='DK4_MES_B115_R0035'":"assert row['id'] in {'DK4_MES_B115_R0035','DK4_MES_B115_R0004'}",
})
filename=__file__+'::two-exact-source-prose-bound-grammatical-soft-wrap-retentions'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
scope={**previous.main.__globals__,'__file__':__file__};exec(compile(source,filename,'exec'),scope);main=scope['main']
if __name__=='__main__':main()
