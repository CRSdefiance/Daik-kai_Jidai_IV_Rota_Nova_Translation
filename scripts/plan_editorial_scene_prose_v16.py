"""Reserve one FE guard cell for the long boarding tutorial; keep every source word."""
import inspect
import linecache
from scripts import plan_editorial_scene_prose_v15 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(inspect.getsource(previous.main), {
    '    env={**previous.ENV,':
    '''    adapter=checked_text(adapter,{
        "cells=(36 if row['id'] in ":
        "cells=(37 if row['id']=='DK4_MES_B134_R0028' else 36 if row['id'] in ",
    })
    env={**previous.ENV,''',
    'FE_row_budget_36_only_for_source_bound_observed_records=True':
    "FE_guard_reserve_only_for_source_bound_observed_records=True,FE_source_scoped_planning_cells={'DK4_MES_B118_R0022':36,'DK4_MES_B127_R0053':36,'DK4_MES_B134_R0028':37,'DK4_MES_B135_R0035':36,'DK4_MES_B136_R0027':36}",
})
env = {**previous.main.__globals__, '__file__': __file__}
filename = __file__ + '::exact-boarding-panel-guard-reserve'
linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
exec(compile(source, filename, 'exec'), env)
main = env['main']

if __name__ == '__main__':
    main()
