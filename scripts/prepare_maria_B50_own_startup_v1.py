"""Reuse the frozen ordinary Maria input plan and minimal candidate-owned startup worker."""
from scripts.prepare_maria270_own_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'scripts.build_registered_maria270_v1':'scripts.build_registered_maria_B50_v1',
    'Own cumulative Maria270 candidate':'Own cumulative Maria B50 candidate',
})
exec(compile(source,__file__+'::same-complete-own-startup-plan-for-exact-B50-candidate','exec'),globals())
