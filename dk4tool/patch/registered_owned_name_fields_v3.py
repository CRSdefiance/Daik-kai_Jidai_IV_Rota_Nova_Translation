"""Same fixed-slot guards with an explicitly named full-catalogue coverage policy."""
import inspect
from dk4tool.patch import registered_owned_name_fields_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.plan_release),{
    "'dk4-registered-owned-name-fields-v2'":"'dk4-registered-owned-name-fields-v3'",
    "actual['Samwell_full_catalogue_UI_unvisited']":"actual[policy['unvisited_key']]",
})
env={**previous.plan_release.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-fixed-slot-source-guards-explicit-catalogue-scope','exec'),env)
plan_release=env['plan_release']
