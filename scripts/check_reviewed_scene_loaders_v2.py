"""Use actual changed blocks while retaining inventoried unchanged control-only blocks."""
from scripts import check_reviewed_scene_loaders as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    "    assert changed=={g['block'] for g in rebuilt['groups']}":
        "    assert changed==set(rebuilt['changed_blocks'])\n    assert set(rebuilt['reviewed_blocks'])-changed==set(rebuilt['unchanged_control_only_blocks'])",
})
exec(compile(source,__file__+'::reviewed-scope-versus-actual-changed-blocks','exec'),globals())
