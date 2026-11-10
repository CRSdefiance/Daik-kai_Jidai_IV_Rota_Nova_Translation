"""Keep full registered reconstruction scope distinct from fresh incremental loader cases."""
from scripts import check_reviewed_scene_loaders_incremental_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "set(rebuilt['reviewed_blocks'])-changed==set(rebuilt['unchanged_control_only_blocks'])":
        "set(rebuilt['reviewed_blocks'])-set(rebuilt['changed_blocks'])==set(rebuilt['unchanged_control_only_blocks'])",
})
exec(compile(source,__file__+'::same-loader-guards-explicit-registered-andincremental-scopes','exec'),globals())
