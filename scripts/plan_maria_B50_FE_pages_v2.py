"""Retain the inherited planner namespace and inspectable source; preserve v1's pre-output failure."""
import linecache
from scripts import plan_maria_B50_FE_pages_v1 as draft

source=draft.previous.source
env={**draft.env,'previous':draft.previous.env['previous'],'__file__':__file__}
filename=__file__+'::unchanged-Maria-planner-exact-current-B50-parent-andchildren'
linecache.cache[filename]=(len(source),None,source.splitlines(keepends=True),filename)
exec(compile(source,filename,'exec'),env)
main=env['main']
if __name__=='__main__':main()
