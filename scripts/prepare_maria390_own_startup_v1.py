"""Freeze the qualified candidate-owned31000-frame Maria startup plan."""
from scripts.prepare_maria337_own_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{'scripts.build_registered_maria337_v1':'scripts.build_registered_maria390_v1',
    'Own cumulative Maria337 candidate':'Own cumulative Maria390 B152-B175 candidate'})
exec(compile(source,__file__+'::same-candidate-owned-startup-plan-no-optional-event-claims','exec'),globals())
