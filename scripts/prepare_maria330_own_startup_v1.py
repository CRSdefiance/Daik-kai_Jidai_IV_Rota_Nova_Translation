"""Freeze the unchanged31,000-frame startup plan for the exact new candidate."""
from scripts.prepare_maria328_own_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{'scripts.build_registered_maria328_v2':'scripts.build_registered_maria330_v1','Own cumulative Maria328 candidate':'Own cumulative Maria330 candidate'})
exec(compile(source,__file__+'::same-ordinary-own-candidate-startup-plan','exec'),globals())
