"""Freeze the unchanged31000-frame own-candidate startup plan."""
from scripts.prepare_maria330_own_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{'scripts.build_registered_maria330_v1':'scripts.build_registered_maria337_v1','Own cumulative Maria330 candidate':'Own cumulative Maria337 candidate'})
exec(compile(source,__file__+'::same-ordinary-own-candidate-startup-plan','exec'),globals())
