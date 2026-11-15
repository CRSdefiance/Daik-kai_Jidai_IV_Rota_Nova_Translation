"""Use complete caption source references in place of the legacy byte-offset alias."""
import inspect
from dk4tool.patch import maria301_release_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

compound_source = checked_text(inspect.getsource(previous.env['compound_objects']), {
    "else ['source_index','source_byte_offset']": "else ['source_index','source_reference']",
})
compound_env = dict(previous.env['compound_objects'].__globals__)
exec(compile(compound_source,__file__+'::same-compound-guards-complete-caption-source-reference','exec'),compound_env)
env = {**previous.env,'compound_objects':compound_env['compound_objects'],'__file__':__file__}
exec(compile(previous.source,__file__+'::unchanged-complete-source-current-SC3-transaction','exec'),env)
plan_release = env['plan_release']
