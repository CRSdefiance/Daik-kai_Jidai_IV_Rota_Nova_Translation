"""Prepare the qualified minimal worker for this candidate's own31000-frame startup."""
from scripts.prepare_maria_B50_own_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'scripts.build_registered_maria_B50_v1':'scripts.build_registered_maria310_v1',
    'Own cumulative Maria B50 candidate':'Own cumulative Maria310 candidate',
})
exec(compile(source,__file__+'::same-own-startup-plan-exact-Maria310-candidate','exec'),globals())
