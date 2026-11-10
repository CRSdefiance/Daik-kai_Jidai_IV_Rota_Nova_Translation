"""Bind the new schema explicitly; preserve the v1 pre-transaction rejection."""
from scripts.prepare_maria270_registered_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    "OUT = ROOT/'registered_preparation_v1'":"OUT = ROOT/'registered_preparation_v2'",
    "format='dk4-reviewed-maria301-release-v1'":"format='dk4-reviewed-maria270-release-v1'",
})
exec(compile(source,__file__+'::same-complete-preparation-correct-explicit-schema','exec'),globals())
