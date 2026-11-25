"""Keep native FE panels within four rows before applying soft phrase preferences."""
import inspect
import linecache

from scripts import plan_editorial_scene_prose_v13 as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(inspect.getsource(previous.main), {
    '    env={**previous.ENV,':
    '''    adapter=checked_text(adapter,{
        'if result is None or result[0][0]>0:limit=8;solve.cache_clear();result=solve(0,0)':
        "if row['kind']!='system-FE' and (result is None or result[0][0]>0):limit=8;solve.cache_clear();result=solve(0,0)",
    })
    env={**previous.ENV,''',
})
env = {**previous.main.__globals__, '__file__': __file__}
filename = __file__ + '::native-FE-four-row-contract-before-soft-preferences'
linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
exec(compile(source, filename, 'exec'), env)
main = env['main']

if __name__ == '__main__':
    main()
