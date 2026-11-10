"""Apply the existing FE guard reserve only to three newly observed failing records."""
import inspect
import linecache
from scripts import plan_editorial_scene_prose_v14 as previous
from scripts.source_locked_derivation_v5118 import checked_text

old_ids = "('DK4_MES_B118_R0022','DK4_MES_B127_R0053')"
new_ids = "('DK4_MES_B118_R0022','DK4_MES_B127_R0053','DK4_MES_B134_R0028','DK4_MES_B135_R0035','DK4_MES_B136_R0027')"
source = checked_text(inspect.getsource(previous.main), {
    '    env={**previous.ENV,':
    '    adapter=checked_text(adapter,{' + repr(old_ids) + ':' + repr(new_ids) + '})\n    env={**previous.ENV,',
    "FE_source_scoped_guard_budget_findings=['DK4_MES_B118_R0022','DK4_MES_B127_R0053']":
    "FE_source_scoped_guard_budget_findings=['DK4_MES_B118_R0022','DK4_MES_B127_R0053','DK4_MES_B134_R0028','DK4_MES_B135_R0035','DK4_MES_B136_R0027']",
    'FE_row_budget_36_only_for_two_observed_extra_wraps=True':
    'FE_row_budget_36_only_for_source_bound_observed_records=True',
})
env = {**previous.main.__globals__, '__file__': __file__}
filename = __file__ + '::same-FE-guard-reserve-new-exact-source-records'
linecache.cache[filename] = (len(source), None, source.splitlines(keepends=True), filename)
exec(compile(source, filename, 'exec'), env)
main = env['main']

if __name__ == '__main__':
    main()
