"""Freeze the established31,000-frame own-candidate Maria startup plan."""
from scripts.prepare_maria303_own_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{'scripts.build_registered_maria303_v1':'scripts.build_registered_maria328_v2',
    'Own cumulative Maria303 candidate':'Own cumulative Maria328 candidate'})
exec(compile(source,__file__+'::unchanged-ordinary-startup-andexisting-system-unlock','exec'),globals())
