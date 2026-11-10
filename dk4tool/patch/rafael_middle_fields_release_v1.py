"""Use the registered exclusive-field contract for three unchanged progressive names."""
import inspect
from dk4tool.patch import registered_owned_name_fields_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(inspect.getsource(previous.plan_release),{
    "actual['Samwell_full_catalogue_UI_unvisited']":"actual['all_changed_full_catalogue_UIs_unvisited']",
})
env={**previous.plan_release.__globals__,'__file__':__file__}
exec(compile(source,__file__+'::same-owned-middle-field-consumer-policy','exec'),env)
plan_release=env['plan_release']
